from solver.schemas.dtp import DTPInstance, DTPSolution
from typing import Sequence
from .solver import ABCSolver

import itertools
import numpy as np


class BruteForceSolver(ABCSolver):
    """VERDADERO BRUTE-FORCE EXHAUSTIVO - Baseline teórico formal para DAA.

    DESCRIPCIÓN FORMAL:
    ===================
    Implementa un algoritmo de fuerza bruta PURO sin optimizaciones:

    1. ENUMERACIÓN DE RUTAS: O(n!)
       - Prueba TODAS las permutaciones posibles de puertos
       - No hay poda en rutas

    2. ENUMERACIÓN DE TRANSACCIONES: O(max_cargo^(n*m))
       - Para cada ruta, prueba TODAS las combinaciones de compra/venta
       - En cada puerto: enumera [0..cargo[k]] para cada mercancía
       - Recursión DFS exhaustiva: sin memoización, sin heurísticas

    COMPLEJIDAD TEÓRICA TOTAL:
    - Mejor caso: O(n!) si todas las rutas se podan rápido
    - Caso general: O(n! × max_cargo^(n×m))

    EJEMPLO INSTANCE_TINY (n=3, m=2, oferta_max≈6):
    - Rutas: 3! = 6 permutaciones
    - DFS nodos por ruta: ~17 millones
    - Tiempo estimado: 50-200 horas en CPU moderna (infeasible)

    USO:
    - Baseline teórico para demostración formal en proyecto DAA
    - Solo viable para: n ≤ 2 (segundos), n=3 con paciencia (horas)
    - NO usar en instancias grandes

    GARANTÍA:
    - Si termina, encuentra la solución ÓPTIMA
    - Exploración exhaustiva completa del espacio de soluciones
    - Sin aproximaciones ni heurísticas
    """

    def solve(self, instance: DTPInstance) -> DTPSolution:
        n_ports = instance.n
        best_benefit = -np.inf
        best = None

        # Enumerate all routes exhaustively
        for perm in self._port_permutations(n_ports):
            route = (0, *perm, 0)

            # For this route, exhaustively enumerate all trade combinations
            candidate = self._search_trades_exhaustive(instance, route)
            if (
                candidate
                and candidate.beneficio_final > best_benefit
                and self.is_feasible(instance, candidate)
            ):
                best = candidate
                best_benefit = candidate.beneficio_final

        # If no valid solution, return trivial
        if best is None:
            best = DTPSolution(
                ruta=(0, 0),
                compras=np.zeros((instance.m, 2), dtype=float),
                ventas=np.zeros((instance.m, 2), dtype=float),
                beneficio_final=instance.capital_inicial,
            )

        return best

    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        route = solution.ruta
        if not route or route[0] != 0 or route[-1] != 0:
            return False

        if self._route_time(instance, route) > instance.tiempo_maximo:
            return False

        if solution.beneficio_final < instance.capital_minimo:
            return False

        if np.any(solution.compras < 0) or np.any(solution.ventas < 0):
            return False

        return True

    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        return solution.beneficio_final

    # -------- BÚSQUEDA EXHAUSTIVA DE TRANSACCIONES (SIN OPTIMIZACIONES) --------
    def _search_trades_exhaustive(
        self, instance: DTPInstance, route: Sequence[int]
    ) -> DTPSolution | None:
        """
        ENUMERA EXHAUSTIVAMENTE TODAS LAS COMBINACIONES DE COMPRA/VENTA.

        Este es un algoritmo de FUERZA BRUTA PURO:
        - Para cada paso en la ruta
        - Enumera TODAS las cantidades a vender: [0..cargo[k]] para cada k
        - Enumera TODAS las cantidades a comprar: [0..max[k]] para cada k
        - Recursión DFS sin poda

        NO hay:
        - Memoización
        - Poda por optimalidad
        - Heurísticas greedy
        - Límites de tiempo

        Complejidad: O(max_cargo^(n*m)) - exponencial puro

        ADVERTENCIA: Para instancias grandes (n>3), puede tardar DÍAS u HORAS.
        """
        m = instance.m
        steps = len(route)
        pesos = instance.pesos
        precios_compra_comerciante = instance.precios_venta
        precios_venta_comerciante = instance.precios_compra
        oferta = instance.oferta_max

        best_capital = -np.inf
        best_compras = None
        best_ventas = None

        compras = np.zeros((m, steps), dtype=float)
        ventas = np.zeros((m, steps), dtype=float)

        def dfs(idx: int, capital: float, cargo: np.ndarray, time_spent: float) -> None:
            """
            DFS EXHAUSTIVO: Explora TODOS los caminos posibles.

            Sin poda, sin memoización, sin límites de tiempo.
            Esto es fuerza bruta pura.
            """
            nonlocal best_capital, best_compras, best_ventas

            # Aplicar costo/tiempo del viaje anterior
            if idx > 0:
                prev_port = route[idx - 1]
                curr_port = route[idx]
                capital -= instance.costos[prev_port, curr_port]
                time_spent += instance.tiempos[prev_port, curr_port]
                # Poda mínima: restricciones de viabilidad
                if capital < 0 or time_spent > instance.tiempo_maximo:
                    return

            current_port = route[idx]

            # ENUMERAR TODAS LAS VENTAS POSIBLES
            # [0..cargo[0]] × [0..cargo[1]] × ... × [0..cargo[m-1]]
            sell_ranges = [range(int(cargo[k]) + 1) for k in range(m)]

            for sells in itertools.product(*sell_ranges):
                sells_arr = np.array(sells, dtype=float)
                cargo_after_sell = cargo - sells_arr
                capital_after_sell = capital + float(
                    np.dot(sells_arr, precios_venta_comerciante[:, current_port])
                )

                # Verificar restricción de bodega
                current_weight = float(np.dot(cargo_after_sell, pesos))
                if current_weight > instance.capacidad_bodega + 1e-9:
                    continue

                # ENUMERAR TODAS LAS COMPRAS POSIBLES
                # Para cada commodity: [0..max_posible[k]]
                buy_max = []
                for k in range(m):
                    price = precios_compra_comerciante[k, current_port]
                    # Máximo por capital disponible
                    if price <= 0:
                        max_by_capital = oferta[k, current_port]
                    else:
                        max_by_capital = capital_after_sell / price
                    # Máximo por oferta disponible
                    max_by_offer = oferta[k, current_port]
                    # Máximo por capacidad de bodega
                    max_by_weight = (
                        (instance.capacidad_bodega - current_weight) / pesos[k]
                        if pesos[k] > 0
                        else max_by_offer
                    )
                    buy_max.append(
                        int(max(0.0, min(max_by_offer, max_by_capital, max_by_weight)))
                    )

                # Enumerar TODAS las combinaciones de compra
                buy_ranges = [range(bm + 1) for bm in buy_max]

                for buys in itertools.product(*buy_ranges):
                    buys_arr = np.array(buys, dtype=float)
                    cargo_after_buy = cargo_after_sell + buys_arr
                    new_weight = float(np.dot(cargo_after_buy, pesos))

                    # Verificar restricción de bodega después de compra
                    if new_weight > instance.capacidad_bodega + 1e-9:
                        continue

                    cost_buys = float(
                        np.dot(buys_arr, precios_compra_comerciante[:, current_port])
                    )
                    capital_after_buy = capital_after_sell - cost_buys

                    # Verificar restricción de capital
                    if capital_after_buy < 0:
                        continue

                    # Registrar esta decisión (estado actual del DFS)
                    compras[:, idx] = buys_arr
                    ventas[:, idx] = sells_arr

                    # RECURSIÓN: ir al siguiente puerto
                    if idx == steps - 1:
                        # Terminal: último puerto de la ruta
                        if capital_after_buy > best_capital:
                            best_capital = capital_after_buy
                            best_compras = compras.copy()
                            best_ventas = ventas.copy()
                    else:
                        # Continuar DFS al siguiente paso
                        dfs(idx + 1, capital_after_buy, cargo_after_buy, time_spent)

            # Limpiar estado para backtrack
            compras[:, idx] = 0
            ventas[:, idx] = 0

        # Iniciar búsqueda desde el puerto 0
        initial_cargo = np.zeros(m, dtype=float)
        dfs(0, instance.capital_inicial, initial_cargo, 0.0)

        # Retornar la mejor solución encontrada (o None si ninguna es válida)
        if best_capital == -np.inf:
            return None

        return DTPSolution(
            ruta=tuple(route),
            compras=best_compras,
            ventas=best_ventas,
            beneficio_final=best_capital,
        )
