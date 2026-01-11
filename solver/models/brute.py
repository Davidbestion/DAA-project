from solver.schemas.dtp import DTPInstance, DTPSolution
from typing import Sequence

from .solver import ABCSolver

import itertools
import numpy as np


class BruteForceSolver(ABCSolver):
    """Solver por fuerza bruta completo: rutas + comercio discreto.

    Explora todas las rutas 0→perm(1..n)→0 y, para cada ruta, todas las
    combinaciones de ventas/compras enteras en cada puerto, respetando:
    tiempo máximo, capital disponible, capacidad de bodega y oferta.
    (Escala factorial x exponencial); solo viable para instancias pequeñas.
    """

    def solve(self, instance: DTPInstance) -> DTPSolution:
        n_ports = instance.n
        best_benefit = -np.inf

        best = DTPSolution(
            ruta=(0, 0),
            compras=np.zeros((instance.m, 2), dtype=float),
            ventas=np.zeros((instance.m, 2), dtype=float),
            beneficio_final=instance.capital_inicial,
        )

        for perm in self._port_permutations(n_ports):
            route = (0, *perm, 0)

            # Poda rápida por tiempo fijo de la ruta (sin comercio)
            if self._route_time(instance, route) > instance.tiempo_maximo:
                continue

            candidate = self._search_trades(instance, route)
            if (
                candidate
                and candidate.beneficio_final > best_benefit
                and self.is_feasible(instance, candidate)
            ):
                best = candidate
                best_benefit = candidate.beneficio_final

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

    # -------- Búsqueda de comercio --------
    def _search_trades(
        self, instance: DTPInstance, route: Sequence[int]
    ) -> DTPSolution | None:
        m = instance.m
        steps = len(route)
        pesos = instance.pesos
        # Desde el punto de vista del comerciante:
        # - Compra del puerto a precios_venta (lo que el puerto vende)
        # - Vende al puerto a precios_compra (lo que el puerto compra)
        precios_compra_comerciante = instance.precios_venta  # Compra del puerto
        precios_venta_comerciante = instance.precios_compra  # Vende al puerto
        oferta = instance.oferta_max

        best_capital = -np.inf
        best_compras: np.ndarray | None = None
        best_ventas: np.ndarray | None = None

        compras = np.zeros((m, steps), dtype=float)
        ventas = np.zeros((m, steps), dtype=float)

        def dfs(idx: int, capital: float, cargo: np.ndarray, time_spent: float) -> None:
            nonlocal best_capital, best_compras, best_ventas

            # Llegada al puerto idx (aplicar costo/tiempo desde el anterior)
            if idx > 0:
                prev_port = route[idx - 1]
                curr_port = route[idx]
                capital -= instance.costos[prev_port, curr_port]
                time_spent += instance.tiempos[prev_port, curr_port]
                if capital < 0 or time_spent > instance.tiempo_maximo:
                    return

            current_port = route[idx]

            # Enumerar ventas posibles (0..cargo[k])
            sell_ranges = [range(int(cargo[k]) + 1) for k in range(m)]

            for sells in itertools.product(*sell_ranges):
                sells_arr = np.array(sells, dtype=float)
                cargo_after_sell = cargo - sells_arr
                # Cuando el comerciante VENDE al puerto, usa precios_compra (lo que el puerto compra)
                capital_after_sell = capital + float(
                    np.dot(sells_arr, precios_venta_comerciante[:, current_port])
                )

                current_weight = float(np.dot(cargo_after_sell, pesos))
                if current_weight > instance.capacidad_bodega + 1e-9:
                    continue

                # Límite máximo de compra por commodity
                # Cuando el comerciante COMPRA del puerto, usa precios_venta (lo que el puerto vende)
                buy_max = []
                for k in range(m):
                    price = precios_compra_comerciante[k, current_port]
                    if price <= 0:
                        max_by_capital = oferta[k, current_port]
                    else:
                        max_by_capital = capital_after_sell / price
                    max_by_offer = oferta[k, current_port]
                    max_by_weight = (
                        (instance.capacidad_bodega - current_weight) / pesos[k]
                        if pesos[k] > 0
                        else max_by_offer
                    )
                    buy_max.append(
                        int(max(0.0, min(max_by_offer, max_by_capital, max_by_weight)))
                    )

                buy_ranges = [range(bm + 1) for bm in buy_max]

                for buys in itertools.product(*buy_ranges):
                    buys_arr = np.array(buys, dtype=float)
                    cargo_after_buy = cargo_after_sell + buys_arr
                    new_weight = float(np.dot(cargo_after_buy, pesos))
                    if new_weight > instance.capacidad_bodega + 1e-9:
                        continue

                    cost_buys = float(np.dot(buys_arr, precios_compra_comerciante[:, current_port]))
                    capital_after_buy = capital_after_sell - cost_buys
                    if capital_after_buy < 0:
                        continue

                    compras[:, idx] = buys_arr
                    ventas[:, idx] = sells_arr

                    if idx == steps - 1:
                        # Último puerto de la ruta
                        if capital_after_buy > best_capital:
                            best_capital = capital_after_buy
                            best_compras = compras.copy()
                            best_ventas = ventas.copy()
                    else:
                        dfs(idx + 1, capital_after_buy, cargo_after_buy, time_spent)

            # limpiar decisiones del paso para otras ramas
            compras[:, idx] = 0
            ventas[:, idx] = 0

        initial_cargo = np.zeros(m, dtype=float)
        dfs(0, instance.capital_inicial, initial_cargo, 0.0)

        if best_capital == -np.inf:
            return None

        return DTPSolution(
            ruta=tuple(route),
            compras=best_compras,
            ventas=best_ventas,
            beneficio_final=best_capital,
        )
