"""
Genetic Algorithm (GA) + Beam Search Solver para el Problema del Comerciante Holandés.

Este solver utiliza:
- Algoritmo Genético para evolucionar buenas rutas entre puertos
- Beam Search para optimizar decisiones de compra/venta en cada ruta
"""

import numpy as np
from typing import Optional, List, Tuple
from solver.models.solver import ABCSolver
from solver.schemas.dtp import DTPInstance, DTPSolution
import random


class GABeamSolver(ABCSolver):
    """
    Solver híbrido GA + Beam Search.

    - GA evoluciona la población de rutas usando crossover y mutación
    - Beam Search mantiene los k mejores estados de trading en cada puerto

    Parámetros:
        population_size: Tamaño de la población de rutas
        n_generations: Número de generaciones a evolucionar
        beam_width: Número de estados a mantener en beam search
        crossover_rate: Probabilidad de crossover (default: 0.8)
        mutation_rate: Probabilidad de mutación (default: 0.2)
        tournament_size: Tamaño del torneo para selección (default: 3)
        elitism: Mantener mejores individuos sin modificar (default: 2)
    """

    def __init__(
        self,
        population_size: int = 50,
        n_generations: int = 100,
        beam_width: int = 5,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.2,
        tournament_size: int = 3,
        elitism: int = 2,
    ):
        self.population_size = population_size
        self.n_generations = n_generations
        self.beam_width = beam_width
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def solve(self, instance: DTPInstance) -> DTPSolution:
        """
        Resuelve la instancia usando Genetic Algorithm (GA) para routing y Beam Search para trading.
        """
        n = instance.tiempos.shape[0] - 1  # Número de puertos (sin Ámsterdam)

        # Inicializar población de rutas
        population = self._initialize_population(n)

        # Evaluar población inicial
        fitness_scores = [self._evaluate_route(instance, route) for route in population]

        # Mejor solución global
        best_idx = np.argmax(
            [f[1] if f is not None else float("-inf") for f in fitness_scores]
        )
        best_solution = (
            fitness_scores[best_idx][0]
            if fitness_scores[best_idx] is not None
            else None
        )
        best_fitness = (
            fitness_scores[best_idx][1]
            if fitness_scores[best_idx] is not None
            else float("-inf")
        )

        # Evolución
        for generation in range(self.n_generations):
            # Nueva población
            new_population = []
            new_fitness = []

            # Elitismo: mantener los mejores individuos
            if self.elitism > 0:
                # Ordenar por fitness
                sorted_indices = sorted(
                    range(len(fitness_scores)),
                    key=lambda i: fitness_scores[i][1]
                    if fitness_scores[i] is not None
                    else float("-inf"),
                    reverse=True,
                )

                for i in range(min(self.elitism, len(sorted_indices))):
                    idx = sorted_indices[i]
                    if fitness_scores[idx] is not None:
                        new_population.append(population[idx][:])
                        new_fitness.append(fitness_scores[idx])

            # Generar resto de la población
            while len(new_population) < self.population_size:
                # Selección
                parent1 = self._tournament_selection(population, fitness_scores)
                parent2 = self._tournament_selection(population, fitness_scores)

                # Crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self._ordered_crossover(parent1, parent2)
                else:
                    child1, child2 = parent1[:], parent2[:]

                # Mutación
                if random.random() < self.mutation_rate:
                    child1 = self._swap_mutation(child1)
                if random.random() < self.mutation_rate:
                    child2 = self._swap_mutation(child2)

                # Evaluar hijos
                result1 = self._evaluate_route(instance, child1)
                if result1 is not None:
                    new_population.append(child1)
                    new_fitness.append(result1)

                    # Actualizar mejor solución
                    if result1[1] > best_fitness:
                        best_solution = result1[0]
                        best_fitness = result1[1]

                if len(new_population) < self.population_size:
                    result2 = self._evaluate_route(instance, child2)
                    if result2 is not None:
                        new_population.append(child2)
                        new_fitness.append(result2)

                        # Actualizar mejor solución
                        if result2[1] > best_fitness:
                            best_solution = result2[0]
                            best_fitness = result2[1]

            # Actualizar población
            population = new_population[: self.population_size]
            fitness_scores = new_fitness[: self.population_size]

        # Si no se encontró solución, retornar trivial
        if best_solution is None:
            return self._build_trivial_solution(instance)

        return best_solution

    def _initialize_population(self, n: int) -> List[List[int]]:
        """Genera población inicial de rutas aleatorias."""
        population = []
        ports = list(range(1, n + 1))

        for _ in range(self.population_size):
            route = ports[:]
            random.shuffle(route)
            population.append(route)

        return population

    def _evaluate_route(
        self, instance: DTPInstance, route_ports: List[int]
    ) -> Optional[Tuple[DTPSolution, float]]:
        """
        Evalúa una ruta usando Beam Search para optimizar trading.

        Returns:
            (DTPSolution, fitness) o None si la ruta no es factible
        """
        # Construir ruta completa: 0 -> ports -> 0
        route = [0] + route_ports + [0]

        # Verificar factibilidad de tiempo
        total_time = sum(
            instance.tiempos[route[i], route[i + 1]] for i in range(len(route) - 1)
        )
        if total_time > instance.tiempo_maximo:
            return None

        # Aplicar Beam Search para encontrar mejor estrategia de trading
        solution = self._beam_search_trading(instance, route)

        if solution is None:
            return None

        return (solution, solution.beneficio_final)

    def _beam_search_trading(
        self, instance: DTPInstance, route: List[int]
    ) -> Optional[DTPSolution]:
        """
        Beam Search para optimizar trading en una ruta dada.

        Mantiene los k mejores estados (capital, cargo) en cada puerto.
        """
        m = instance.pesos.shape[0]
        n_stops = len(route)

        # Estado: (capital, cargo, compras_historia, ventas_historia)
        # Inicializar beam con estado inicial
        initial_state = (
            float(instance.capital_inicial),
            np.zeros(m),
            [np.zeros(m) for _ in range(n_stops)],
            [np.zeros(m) for _ in range(n_stops)],
        )
        beam = [initial_state]

        # Procesar cada transición en la ruta
        for idx in range(n_stops - 1):
            current_port = route[idx]
            next_port = route[idx + 1]

            # Generar nuevos estados desde cada estado en el beam
            new_states = []

            for capital, cargo, compras_hist, ventas_hist in beam:
                # Generar estados sucesor
                successors = self._generate_successors(
                    instance,
                    current_port,
                    next_port,
                    capital,
                    cargo,
                    compras_hist,
                    ventas_hist,
                    idx,
                )
                new_states.extend(successors)

            if not new_states:
                return None

            # Ordenar por capital y mantener los mejores k
            new_states.sort(key=lambda s: s[0], reverse=True)
            beam = new_states[: self.beam_width]

        # Mejor estado final
        if not beam:
            return None

        best_capital, final_cargo, compras_hist, ventas_hist = beam[0]

        # Construir matrices de operaciones
        compras_matrix = np.zeros((m, n_stops))
        ventas_matrix = np.zeros((m, n_stops))

        for i in range(n_stops):
            compras_matrix[:, i] = compras_hist[i]
            ventas_matrix[:, i] = ventas_hist[i]

        return DTPSolution(
            ruta=tuple(route),
            compras=compras_matrix,
            ventas=ventas_matrix,
            beneficio_final=best_capital,
        )

    def _generate_successors(
        self,
        instance: DTPInstance,
        current_port: int,
        next_port: int,
        capital: float,
        cargo: np.ndarray,
        compras_hist: List[np.ndarray],
        ventas_hist: List[np.ndarray],
        idx: int,
    ) -> List[Tuple[float, np.ndarray, List[np.ndarray], List[np.ndarray]]]:
        """
        Genera estados sucesores explorando diferentes combinaciones de venta/compra.
        """

        m = instance.pesos.shape[0]
        successors = []

        # 1. VENDER todo lo que tengamos
        new_capital = capital
        ventas = np.zeros(m)

        for k in range(m):
            if cargo[k] > 0:
                precio_venta = instance.precios_compra[k, current_port]
                new_capital += cargo[k] * precio_venta
                ventas[k] = cargo[k]

        new_cargo = np.zeros(m)

        # 2. Calcular costo de viaje
        travel_cost = instance.costos[current_port, next_port]

        if new_capital < travel_cost:
            return []  # No factible

        # 3. COMPRAR: explorar diferentes combinaciones
        capital_disponible = new_capital - travel_cost
        capacidad_disponible = instance.capacidad_bodega

        # No comprar nada (opción base)
        new_compras_hist = [c.copy() for c in compras_hist]
        new_ventas_hist = [v.copy() for v in ventas_hist]
        new_ventas_hist[idx] = ventas

        final_capital = new_capital - travel_cost

        successors.append(
            (final_capital, new_cargo.copy(), new_compras_hist, new_ventas_hist)
        )

        # Si no es el último puerto antes de volver, considerar compras
        if idx < len(compras_hist) - 2:
            # Generar combinaciones de compra (greedy top-k)
            opportunities = []

            for k in range(m):
                precio_compra = instance.precios_venta[k, current_port]
                precio_venta = instance.precios_compra[k, next_port]
                profit = precio_venta - precio_compra

                if profit > 0 and instance.oferta_max[k, current_port] > 0:
                    peso = instance.pesos[k]
                    ratio = profit / peso if peso > 0 else float("inf")
                    opportunities.append((k, ratio, profit, precio_compra, peso))

            # Ordenar por ratio
            opportunities.sort(key=lambda x: x[1], reverse=True)

            # Generar algunas combinaciones de compra (top mercancías)
            for num_items in range(min(3, len(opportunities) + 1)):
                if num_items == 0:
                    continue

                compras = np.zeros(m)
                cap_temp = capital_disponible
                cap_temp_disponible = capacidad_disponible
                cargo_temp = new_cargo.copy()

                for i in range(num_items):
                    k, ratio, profit, precio_compra, peso = opportunities[i]

                    # Calcular cuánto comprar
                    max_by_offer = instance.oferta_max[k, current_port]
                    max_by_capital = (
                        cap_temp / precio_compra if precio_compra > 0 else float("inf")
                    )
                    max_by_capacity = (
                        cap_temp_disponible / peso if peso > 0 else float("inf")
                    )

                    cantidad = min(max_by_offer, max_by_capital, max_by_capacity)
                    cantidad = int(cantidad)

                    if cantidad > 0:
                        compras[k] = cantidad
                        cargo_temp[k] = cantidad
                        cap_temp -= cantidad * precio_compra
                        cap_temp_disponible -= cantidad * peso

                # Crear estado sucesor
                new_compras_hist2 = [c.copy() for c in compras_hist]
                new_ventas_hist2 = [v.copy() for v in ventas_hist]
                new_compras_hist2[idx] = compras
                new_ventas_hist2[idx] = ventas

                final_capital2 = (
                    new_capital
                    - compras.dot(instance.precios_venta[:, current_port])
                    - travel_cost
                )

                if final_capital2 >= 0:
                    successors.append(
                        (
                            final_capital2,
                            cargo_temp.copy(),
                            new_compras_hist2,
                            new_ventas_hist2,
                        )
                    )

        return successors

    def _tournament_selection(
        self,
        population: List[List[int]],
        fitness_scores: List[Optional[Tuple[DTPSolution, float]]],
    ) -> List[int]:
        """Selección por torneo."""
        tournament = random.sample(range(len(population)), self.tournament_size)
        best_idx = max(
            tournament,
            key=lambda i: fitness_scores[i][1]
            if fitness_scores[i] is not None
            else float("-inf"),
        )
        return population[best_idx][:]

    def _ordered_crossover(
        self, parent1: List[int], parent2: List[int]
    ) -> Tuple[List[int], List[int]]:
        """
        Order Crossover (OX) - mantiene el orden relativo de los elementos.
        """
        size = len(parent1)

        # Seleccionar dos puntos de corte
        start, end = sorted(random.sample(range(size), 2))

        # Crear hijos
        child1 = [None] * size
        child2 = [None] * size

        # Copiar segmento del padre
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        # Llenar resto con elementos del otro padre en orden
        def fill_child(child, parent):
            pos = end
            for gene in parent[end:] + parent[:end]:
                if gene not in child:
                    if pos >= size:
                        pos = 0
                    child[pos] = gene
                    pos += 1

        fill_child(child1, parent2)
        fill_child(child2, parent1)

        return child1, child2

    def _swap_mutation(self, route: List[int]) -> List[int]:
        """Mutación por intercambio de dos posiciones."""
        if len(route) < 2:
            return route

        mutated = route[:]
        i, j = random.sample(range(len(route)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated

    def _build_trivial_solution(self, instance: DTPInstance) -> DTPSolution:
        """Construye solución trivial."""
        m = instance.pesos.shape[0]
        return DTPSolution(
            ruta=(0, 0),
            compras=np.zeros((m, 2)),
            ventas=np.zeros((m, 2)),
            beneficio_final=instance.capital_inicial,
        )

    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica factibilidad de la solución."""
        ruta = solution.ruta

        if ruta[0] != 0 or ruta[-1] != 0:
            return False

        tiempo_total = sum(
            instance.tiempos[ruta[i], ruta[i + 1]] for i in range(len(ruta) - 1)
        )

        return tiempo_total <= instance.tiempo_maximo

    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        """Evalúa la solución."""
        return solution.beneficio_final
