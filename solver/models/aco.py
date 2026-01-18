"""
Ant Colony Optimization (ACO) Solver para el Problema del Comerciante Holandés.

Este solver utiliza optimización de colonias de hormigas para encontrar buenas rutas
entre puertos, y aplica el algoritmo greedy de knapsack para optimizar las decisiones
de compra/venta en cada puerto.
"""

import numpy as np
from typing import Optional
from solver.models.solver import ABCSolver
from solver.schemas.dtp import DTPInstance, DTPSolution


class ACOSolver(ABCSolver):
    """
    Solver basado en Ant Colony Optimization para encontrar rutas óptimas.
    
    El algoritmo funciona en dos fases:
    1. ACO construye rutas entre puertos usando feromonas y heurística
    2. Greedy Knapsack optimiza compra/venta en cada puerto de la ruta
    
    Parámetros:
        n_ants: Número de hormigas por iteración
        n_iterations: Número de iteraciones del algoritmo
        alpha: Peso de las feromonas (default: 1.0)
        beta: Peso de la información heurística (default: 2.0)
        evaporation_rate: Tasa de evaporación de feromonas (default: 0.5)
        q: Constante para depositar feromonas (default: 100.0)
    """
    
    def __init__(
        self,
        n_ants: int = 10,
        n_iterations: int = 50,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation_rate: float = 0.5,
        q: float = 100.0
    ):
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        
    def solve(self, instance: DTPInstance) -> DTPSolution:
        """
        Resuelve la instancia usando ACO + Greedy Knapsack.
        
        Args:
            instance: Instancia del problema DTP
            
        Returns:
            Mejor solución encontrada
            
        Raises:
            ValueError: Si no se encuentra una solución factible.
        """
        n = instance.tiempos.shape[0] - 1  # Número de puertos (sin Ámsterdam)
        
        # Inicializar matriz de feromonas
        pheromones = self._init_pheromones(n)
        
        # Calcular matriz de información heurística (inverso de costo normalizado)
        heuristic = self._compute_heuristic(instance)
        
        # Mejor solución global
        best_solution = None
        best_capital = float('-inf')
        
        for iteration in range(self.n_iterations):
            # Soluciones de esta iteración
            iteration_solutions = []
            
            for ant in range(self.n_ants):
                # Construir ruta con esta hormiga
                route = self._construct_route(instance, pheromones, heuristic)
                
                if route is None:
                    continue
                
                # Evaluar ruta con greedy knapsack
                solution = self._evaluate_route(instance, route)
                
                if solution is not None:
                    iteration_solutions.append((route, solution))
                    
                    # Actualizar mejor solución
                    if solution.beneficio_final > best_capital:
                        best_capital = solution.beneficio_final
                        best_solution = solution
            
            # Actualizar feromonas
            if iteration_solutions:
                self._update_pheromones(pheromones, iteration_solutions)
        
        # Si no se encontró solución, retornar solución trivial
        if best_solution is None:
            raise ValueError("No se encontró una solución factible para la instancia dada.")
        
        return best_solution
    
    def _init_pheromones(self, n: int) -> np.ndarray:
        """Inicializa matriz de feromonas con valor constante."""
        return np.ones((n + 1, n + 1))
    
    def _compute_heuristic(self, instance: DTPInstance) -> np.ndarray:
        """
        Calcula información heurística para cada arista.
        Combina costo y tiempo de viaje (menor es mejor).
        """
        n = instance.tiempos.shape[0]
        heuristic = np.zeros((n, n))
        
        # Normalizar costos y tiempos
        max_cost = np.max(instance.costos[instance.costos < np.inf])
        max_time = np.max(instance.tiempos[instance.tiempos < np.inf])
        
        for i in range(n):
            for j in range(n):
                if i != j and instance.costos[i, j] < np.inf:
                    # Combinar costo y tiempo normalizados
                    normalized_cost = instance.costos[i, j] / max_cost
                    normalized_time = instance.tiempos[i, j] / max_time
                    combined = 0.5 * normalized_cost + 0.5 * normalized_time
                    
                    # Heurística es inverso (menor costo/tiempo = mayor heurística)
                    heuristic[i, j] = 1.0 / (combined + 1e-6)
        
        return heuristic
    
    def _construct_route(
        self,
        instance: DTPInstance,
        pheromones: np.ndarray,
        heuristic: np.ndarray
    ) -> Optional[list[int]]:
        """
        Construye una ruta usando selección probabilística basada en feromonas y heurística.
        """
        n = instance.tiempos.shape[0] - 1
        
        current = 0  # Comenzar en Ámsterdam
        visited = {0}
        route = [0]
        
        time_accumulated = 0.0
        capital = instance.capital_inicial
        
        # Construir ruta visitando todos los puertos
        while len(visited) <= n:
            # # Si ya visitamos todos, regresar a Ámsterdam
            # if len(visited) == n + 1:
            #     route.append(0)
            #     break
            
            # Calcular probabilidades para próximo puerto
            unvisited = [p for p in range(1, n + 1) if p not in visited]
            
            if not unvisited:
                # Todos visitados, regresar a Ámsterdam
                route.append(0)
                break
            
            # Calcular probabilidades
            probabilities = []
            valid_ports = []
            
            for port in unvisited:
                # Verificar factibilidad básica
                travel_time = instance.tiempos[current, port]
                travel_cost = instance.costos[current, port]
                
                if (time_accumulated + travel_time <= instance.tiempo_maximo and
                    capital >= travel_cost):
                    
                    # Probabilidad = (feromona^alpha) * (heurística^beta)
                    pheromone = pheromones[current, port] ** self.alpha
                    heur = heuristic[current, port] ** self.beta
                    prob = pheromone * heur
                    
                    probabilities.append(prob)
                    valid_ports.append(port)
            
            if not valid_ports:
                # No hay puertos factibles, terminar ruta
                route.append(0)
                break
            
            # Normalizar probabilidades
            probabilities = np.array(probabilities)
            probabilities /= probabilities.sum()
            
            # Seleccionar próximo puerto
            next_port = np.random.choice(valid_ports, p=probabilities)
            
            # Actualizar estado
            time_accumulated += instance.tiempos[current, next_port]
            capital -= instance.costos[current, next_port]
            
            route.append(next_port)
            visited.add(next_port)
            current = next_port
        
        # Verificar que la ruta sea válida (termina en Ámsterdam)
        if route[-1] != 0:
            route.append(0)
        
        # Verificar factibilidad de tiempo total
        total_time = sum(instance.tiempos[route[i], route[i+1]] 
                        for i in range(len(route) - 1))
        
        if total_time > instance.tiempo_maximo:
            return None
        
        return route
    
    def _evaluate_route(
        self,
        instance: DTPInstance,
        route: list[int]
    ) -> Optional[DTPSolution]:
        """
        Evalúa una ruta aplicando greedy knapsack en cada puerto.
        """
        m = instance.pesos.shape[0]
        n_stops = len(route)
        
        # Matrices para registrar operaciones
        compras = np.zeros((m, n_stops))
        ventas = np.zeros((m, n_stops))
        
        # Estado inicial
        capital = instance.capital_inicial
        cargo = np.zeros(m)
        time_accumulated = 0.0
        
        for idx in range(n_stops - 1):
            current_port = route[idx]
            next_port = route[idx + 1]
            
            # Vender todo lo que tengamos en el puerto actual
            for k in range(m):
                if cargo[k] > 0:
                    precio_venta = instance.precios_compra[k, current_port]
                    capital += cargo[k] * precio_venta
                    ventas[k, idx] = cargo[k]
                    cargo[k] = 0
            
            # Calcular costo de viaje
            travel_cost = instance.costos[current_port, next_port]
            travel_time = instance.tiempos[current_port, next_port]
            
            # Verificar factibilidad
            if capital < travel_cost:
                return None
            
            time_accumulated += travel_time
            if time_accumulated > instance.tiempo_maximo:
                return None
            
            # Reservar capital para el viaje
            capital_disponible = capital - travel_cost
            
            # Calcular capacidad disponible
            capacidad_disponible = instance.capacidad_bodega - np.sum(cargo * instance.pesos)
            
            # Aplicar greedy knapsack para compras
            if idx < n_stops - 2:  # No comprar en el último puerto antes de Ámsterdam
                purchases = self._knapsack_greedy(
                    instance,
                    current_port,
                    next_port,
                    capital_disponible,
                    capacidad_disponible
                )
                
                # Ejecutar compras
                for k, cantidad in purchases:
                    precio_compra = instance.precios_venta[k, current_port]
                    cargo[k] += cantidad
                    capital -= cantidad * precio_compra
                    compras[k, idx] = cantidad
            
            # Viajar al siguiente puerto (descontar costo de viaje)
            capital -= travel_cost
        
        # El beneficio_final es el capital final (no la ganancia neta)
        beneficio_final = capital
        
        return DTPSolution(
            ruta=tuple(route),
            compras=compras,
            ventas=ventas,
            beneficio_final=beneficio_final
        )
    
    def _knapsack_greedy(
        self,
        instance: DTPInstance,
        current_port: int,
        next_port: int,
        capital: float,
        capacidad: float
    ) -> list[tuple[int, int]]:
        """
        Resuelve el problema de la mochila de forma greedy para maximizar ganancias.
        Retorna lista de (mercancía, cantidad) a comprar.
        """
        m = instance.pesos.shape[0]
        opportunities = []
        
        for k in range(m):
            precio_compra = instance.precios_venta[k, current_port]
            precio_venta = instance.precios_compra[k, next_port]
            profit = precio_venta - precio_compra
            
            if profit <= 0:
                continue
            
            oferta = instance.oferta_max[k, current_port]
            if oferta <= 0:
                continue
            
            peso = instance.pesos[k]
            
            # Calcular cantidad máxima factible
            max_by_offer = oferta
            max_by_capital = capital / precio_compra if precio_compra > 0 else float('inf')
            max_by_capacity = capacidad / peso if peso > 0 else float('inf')
            
            max_units = min(max_by_offer, max_by_capital, max_by_capacity)
            
            if max_units < 1:
                continue
            
            # Ratio de ganancia por peso
            ratio = profit / peso if peso > 0 else float('inf')
            
            opportunities.append((k, ratio, profit, precio_compra, peso, max_units))
        
        # Ordenar por ratio descendente
        opportunities.sort(key=lambda x: x[1], reverse=True)
        
        # Seleccionar mercancías greedily
        purchases = []
        capital_restante = capital
        capacidad_restante = capacidad
        
        for k, ratio, profit, precio, peso, max_units in opportunities:
            # Calcular cuánto podemos comprar
            cantidad = min(
                max_units,
                capital_restante / precio if precio > 0 else float('inf'),
                capacidad_restante / peso if peso > 0 else float('inf')
            )
            
            cantidad = int(cantidad)
            
            if cantidad > 0:
                purchases.append((k, cantidad))
                capital_restante -= cantidad * precio
                capacidad_restante -= cantidad * peso
        
        return purchases
    
    def _update_pheromones(
        self,
        pheromones: np.ndarray,
        solutions: list[tuple[list[int], DTPSolution]]
    ):
        """
        Actualiza matriz de feromonas basándose en las soluciones encontradas.
        """
        # Evaporación
        pheromones *= (1.0 - self.evaporation_rate)
        
        # Depositar feromonas
        for route, solution in solutions:
            # Cantidad de feromona proporcional a la calidad de la solución
            if solution.beneficio_final > 0:
                delta = self.q * solution.beneficio_final / abs(solution.beneficio_final + 1)
            else:
                delta = 0.1  # Depositar algo mínimo para soluciones válidas
            
            # Depositar en cada arista de la ruta
            for i in range(len(route) - 1):
                pheromones[route[i], route[i + 1]] += delta
    
    def _build_trivial_solution(self, instance: DTPInstance) -> DTPSolution:
        """Construye solución trivial: ir y volver de Ámsterdam sin comerciar."""
        m = instance.pesos.shape[0]
        return DTPSolution(
            ruta=(0, 0),
            compras=np.zeros((m, 2)),
            ventas=np.zeros((m, 2)),
            beneficio_final=instance.capital_inicial
        )
    
    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica si una solución es factible (delegado a la clase base si existe)."""
        # Implementación básica de verificación
        ruta = solution.ruta
        
        # Verificar que comience y termine en Ámsterdam
        if ruta[0] != 0 or ruta[-1] != 0:
            return False
        
        # Verificar tiempo total
        tiempo_total = sum(instance.tiempos[ruta[i], ruta[i+1]] 
                          for i in range(len(ruta) - 1))
        if tiempo_total > instance.tiempo_maximo:
            return False
        
        return True
    
    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        """Evalúa la solución y devuelve el beneficio final."""
        return solution.beneficio_final
