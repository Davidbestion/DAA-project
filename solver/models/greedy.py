"""Solver Greedy para el Problema del Comerciante Holandés (DTP).

Implementa estrategias golosas para encontrar soluciones rápidas,
seleccionando en cada paso las opciones localmente óptimas.
"""

from solver.schemas.dtp import DTPInstance, DTPSolution
from .solver import ABCSolver

import numpy as np
from typing import Literal


class GreedySolver(ABCSolver):
    """Solver greedy que toma decisiones localmente óptimas.
    
    Estrategia:
    - Selección de puerto: escoge el puerto no visitado con menor costo de viaje
    - En cada puerto: vende las mercancías más rentables y compra las mejores oportunidades
    - Llena la bodega maximizando ganancia por unidad de peso
    """

    def __init__(
        self,
        port_selection: Literal["min_cost", "min_time", "combined"] = "min_cost",
        buy_criterion: Literal["profit_margin", "profit_per_weight", "cheapest"] = "profit_per_weight",
    ):
        """Inicializa el solver greedy.
        
        Args:
            port_selection: Criterio para seleccionar el próximo puerto
                - "min_cost": minimiza costo de viaje
                - "min_time": minimiza tiempo de viaje
                - "combined": minimiza suma normalizada de costo y tiempo
            buy_criterion: Criterio para seleccionar qué comprar
                - "profit_margin": maximiza diferencia entre precio compra y venta
                - "profit_per_weight": maximiza ganancia por unidad de peso
                - "cheapest": compra lo más barato primero
        """
        self.port_selection = port_selection
        self.buy_criterion = buy_criterion

    def solve(self, instance: DTPInstance) -> DTPSolution:
        """Resuelve la instancia usando estrategia greedy."""
        n_ports = instance.n
        m = instance.m
        
        # Estado inicial
        current_port = 0
        capital = float(instance.capital_inicial)
        cargo = np.zeros(m, dtype=float)
        time_spent = 0.0
        visited = {0}
        route = [0]
        
        # Matrices para registrar operaciones
        max_steps = n_ports + 2  # Peor caso: visitar todos + ida y vuelta
        compras_list = []
        ventas_list = []
        
        # Realizar operaciones en el puerto inicial (Ámsterdam)
        # Determinar el primer puerto de destino para optimizar compras
        first_port = self._select_next_port(
            instance, current_port, visited, capital, 0.0
        )
        ventas, compras, capital, cargo = self._trade_at_port(
            instance, current_port, capital, cargo, first_port
        )
        compras_list.append(compras)
        ventas_list.append(ventas)
        
        # Iterar hasta visitar todos los puertos o no poder continuar
        while len(visited) <= n_ports:
            # Seleccionar próximo puerto no visitado
            next_port = self._select_next_port(
                instance, current_port, visited, capital, time_spent
            )
            
            if next_port is None:
                break  # No hay más puertos viables
            
            # Viajar al siguiente puerto
            travel_cost = instance.costos[current_port, next_port]
            travel_time = instance.tiempos[current_port, next_port]
            
            capital -= travel_cost
            time_spent += travel_time
            
            # Verificar restricciones
            if capital < 0 or time_spent > instance.tiempo_maximo:
                break
            
            current_port = next_port
            visited.add(next_port)
            route.append(next_port)
            
            # Realizar operaciones en el puerto (ahora conocemos el próximo destino)
            lookahead_port = self._select_next_port(
                instance, current_port, visited, capital, time_spent
            )
            ventas, compras, capital, cargo = self._trade_at_port(
                instance, current_port, capital, cargo, lookahead_port
            )
            
            compras_list.append(compras)
            ventas_list.append(ventas)
        
        # Regresar a Ámsterdam si no estamos allí
        if current_port != 0:
            travel_cost = instance.costos[current_port, 0]
            travel_time = instance.tiempos[current_port, 0]
            
            if capital >= travel_cost and time_spent + travel_time <= instance.tiempo_maximo:
                capital -= travel_cost
                time_spent += travel_time
                current_port = 0
                route.append(0)
                
                # Vender todo el cargo restante en Ámsterdam
                ventas = np.copy(cargo)
                for k in range(m):
                    if cargo[k] > 0:
                        capital += cargo[k] * instance.precios_compra[k, 0]
                cargo = np.zeros(m, dtype=float)
                
                compras_list.append(np.zeros(m, dtype=float))
                ventas_list.append(ventas)
        
        # Construir matrices de compras y ventas
        steps = len(route)
        compras_matrix = np.zeros((m, steps), dtype=float)
        ventas_matrix = np.zeros((m, steps), dtype=float)
        
        for i in range(min(steps, len(compras_list))):
            compras_matrix[:, i] = compras_list[i]
            ventas_matrix[:, i] = ventas_list[i]
        
        return DTPSolution(
            ruta=tuple(route),
            compras=compras_matrix,
            ventas=ventas_matrix,
            beneficio_final=capital,
        )

    def _select_next_port(
        self,
        instance: DTPInstance,
        current_port: int,
        visited: set[int],
        capital: float,
        time_spent: float,
    ) -> int | None:
        """Selecciona el próximo puerto a visitar usando criterio greedy.
        
        No considera el puerto 0 (Ámsterdam) hasta que sea el retorno final.
        """
        n_ports = instance.n
        best_port = None
        best_score = float('inf')
        
        for port in range(1, n_ports + 1):  # Solo considerar puertos 1..n (no 0)
            if port in visited:
                continue
            
            cost = instance.costos[current_port, port]
            time = instance.tiempos[current_port, port]
            
            # Verificar viabilidad
            if capital < cost or time_spent + time > instance.tiempo_maximo:
                continue
            
            # Calcular score según criterio
            if self.port_selection == "min_cost":
                score = cost
            elif self.port_selection == "min_time":
                score = time
            else:  # combined
                # Normalizar y combinar
                max_cost = np.max(instance.costos)
                max_time = np.max(instance.tiempos)
                score = (cost / max_cost + time / max_time) / 2
            
            if score < best_score:
                best_score = score
                best_port = port
        
        return best_port

    def _trade_at_port(
        self,
        instance: DTPInstance,
        port: int,
        capital: float,
        cargo: np.ndarray,
        next_port: int | None,
    ) -> tuple[np.ndarray, np.ndarray, float, np.ndarray]:
        """Realiza operaciones de compra/venta en un puerto usando greedy para optimizar compras.
        
        Args:
            next_port: Puerto de destino donde se venderá (None si es el último, vender en Amsterdam)
        
        Returns:
            (ventas, compras, nuevo_capital, nuevo_cargo)
        """
        m = instance.m
        ventas = np.zeros(m, dtype=float)
        
        # 1. VENDER: vender todo (siempre óptimo localmente)
        for k in range(m):
            if cargo[k] > 0:
                precio_venta = instance.precios_compra[k, port]
                ventas[k] = cargo[k]
                capital += cargo[k] * precio_venta
                cargo[k] = 0
        
        # 2. COMPRAR: resolver knapsack con greedy
        if next_port is None:
            # No hay siguiente puerto, no comprar nada
            compras = np.zeros(m, dtype=float)
        else:
            # Calcular cuánto capital podemos usar (reservar costo de viaje)
            travel_cost = instance.costos[port, next_port]
            capital_disponible = capital - travel_cost
            
            if capital_disponible > 0:
                # Usar greedy para encontrar la mejor combinación de compras
                compras = self._knapsack_greedy(
                    instance, port, next_port, capital_disponible, instance.capacidad_bodega
                )
            else:
                compras = np.zeros(m, dtype=float)
            
            # Actualizar capital y cargo
            for k in range(m):
                if compras[k] > 0:
                    precio_compra = instance.precios_venta[k, port]
                    capital -= compras[k] * precio_compra
                    cargo[k] = compras[k]
        
        return ventas, compras, capital, cargo

    def _knapsack_greedy(
        self,
        instance: DTPInstance,
        current_port: int,
        next_port: int,
        capital: float,
        capacidad: float,
    ) -> np.ndarray:
        """Resuelve el problema de knapsack usando greedy (fractional knapsack).
        
        Encuentra la combinación óptima de mercancías a comprar en current_port
        para maximizar la ganancia al venderlas en next_port.
        
        Args:
            current_port: Puerto actual donde compramos
            next_port: Puerto donde venderemos
            capital: Capital disponible
            capacidad: Capacidad de bodega disponible
        
        Returns:
            Array con cantidades a comprar de cada mercancía
        """
        m = instance.m
        
        # Calcular oportunidades por mercancía
        opportunities = []
        for k in range(m):
            precio_compra = instance.precios_venta[k, current_port]
            precio_venta = instance.precios_compra[k, next_port]
            ganancia_unitaria = precio_venta - precio_compra
            peso = instance.pesos[k]
            oferta = instance.oferta_max[k, current_port]
            
            # Solo considerar si hay ganancia positiva
            if ganancia_unitaria > 0 and oferta > 0 and peso > 0 and precio_compra > 0:
                # Calcular cantidad máxima que puedo comprar de esta mercancía
                max_por_oferta = oferta
                max_por_capital = capital / precio_compra
                max_por_peso = capacidad / peso
                max_units = min(max_por_oferta, max_por_capital, max_por_peso)
                
                if max_units > 0:
                    ratio = ganancia_unitaria / peso
                    opportunities.append({
                        'good': k,
                        'ratio': ratio,
                        'profit': ganancia_unitaria,
                        'cost': precio_compra,
                        'weight': peso,
                        'max_units': max_units
                    })
        
        if not opportunities:
            return np.zeros(m, dtype=float)
        
        # Ordenar por ratio ganancia/peso (mejor primero)
        opportunities.sort(key=lambda x: x['ratio'], reverse=True)
        
        # Comprar greedily respetando restricciones
        compras = np.zeros(m, dtype=float)
        capital_restante = capital
        peso_restante = capacidad
        
        for opp in opportunities:
            k = opp['good']
            precio_compra = opp['cost']
            peso = opp['weight']
            
            # Calcular cuánto puedo comprar ahora con los recursos restantes
            max_por_capital = capital_restante / precio_compra
            max_por_peso = peso_restante / peso
            cantidad = min(opp['max_units'], max_por_capital, max_por_peso)
            cantidad = int(cantidad)  # Cantidades enteras
            
            if cantidad > 0:
                compras[k] = cantidad
                capital_restante -= cantidad * precio_compra
                peso_restante -= cantidad * peso
        
        return compras

    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica si la solución es factible."""
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
        """Evalúa la solución y retorna el beneficio final."""
        return solution.beneficio_final
