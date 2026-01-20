"""Extensiones del Greedy Solver para reducir margen de error.

Implementa:
1. MultiGreedySolver: Ejecuta múltiples estrategias y elige la mejor
2. GreedyWithLocalSearch: Greedy + 2-OPT improvement
"""

from solver.schemas.dtp import DTPInstance, DTPSolution
from .greedy import GreedySolver
from .solver import ABCSolver

import numpy as np


class MultiGreedySolver(ABCSolver):
    """Heurística multi-estrategia: ejecuta varios greedy y selecciona el mejor.

    Combina diferentes estrategias de selección de puertos y compras para
    obtener una solución más robusta que un único greedy.

    Complejidad: O(k × n²) donde k = número de estrategias (típicamente 3-4)
    Error esperado: 1-2% en problemas medianos (mejora respecto a 1.94% simple)
    """

    def __init__(self, num_strategies: int = 3):
        """Inicializa con varias estrategias.

        Args:
            num_strategies: Número de estrategias greedy diferentes a probar
        """
        self.num_strategies = num_strategies

    def solve(self, instance: DTPInstance) -> DTPSolution:
        """Ejecuta múltiples estrategias y retorna la mejor solución."""
        strategies = [
            GreedySolver(port_selection="min_cost", buy_criterion="profit_per_weight"),
            GreedySolver(port_selection="min_time", buy_criterion="profit_per_weight"),
            GreedySolver(port_selection="combined", buy_criterion="profit_margin"),
        ]

        if self.num_strategies > 3:
            strategies.append(
                GreedySolver(port_selection="min_cost", buy_criterion="profit_margin")
            )

        # Resolver con cada estrategia
        solutions = [s.solve(instance) for s in strategies]

        # Retornar la mejor
        return max(solutions, key=lambda x: x.beneficio_final)

    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica si la solución es factible."""
        greedy = GreedySolver()
        return greedy.is_feasible(instance, solution)

    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        """Evalúa la solución."""
        return solution.beneficio_final


class GreedyWithLocalSearch(ABCSolver):
    """Greedy + búsqueda local (2-OPT) para mejorar soluciones.

    Estrategia:
    1. Obtener solución greedy inicial
    2. Aplicar mejoras locales: invertir segmentos de ruta
    3. Aceptar mejoras que aumenten el beneficio
    4. Iterar hasta convergencia

    Complejidad: O(n³) - dos bucles anidados + evaluación
    Error esperado: 0.5-1.5% en problemas medianos
    Mejora sobre greedy: 2-5% típicamente
    """

    def __init__(self, max_iterations: int = 100, verbose: bool = False):
        """Inicializa el solver con búsqueda local.

        Args:
            max_iterations: Máximo número de iteraciones de mejora
            verbose: Si mostrar progreso
        """
        self.max_iterations = max_iterations
        self.verbose = verbose

    def solve(self, instance: DTPInstance) -> DTPSolution:
        """Resuelve usando greedy + local search."""
        # Paso 1: Obtener solución greedy inicial
        greedy = GreedySolver(port_selection="combined")
        solution = greedy.solve(instance)

        if self.verbose:
            print(f"Solución inicial (greedy): ${solution.beneficio_final:.2f}")

        # Paso 2: Mejorar con búsqueda local
        improved_solution = self._local_search(solution, instance, greedy)

        if self.verbose:
            print(
                f"Solución final (con 2-OPT): ${improved_solution.beneficio_final:.2f}"
            )
            improvement = (
                (improved_solution.beneficio_final - solution.beneficio_final)
                / solution.beneficio_final
                * 100
            )
            print(f"Mejora: {improvement:.2f}%")

        return improved_solution

    def _local_search(
        self, initial_solution: DTPSolution, instance: DTPInstance, greedy: GreedySolver
    ) -> DTPSolution:
        """Aplica 2-OPT iterativo para mejorar la ruta.

        La mejora se enfoca en reordenar puertos visitados,
        re-evaluando decisiones de compra/venta con la nueva ruta.
        """
        current_solution = initial_solution
        current_benefit = current_solution.beneficio_final

        improved = True
        iteration = 0

        while improved and iteration < self.max_iterations:
            improved = False
            iteration += 1

            route = list(current_solution.ruta)

            # Intentar invertir cada segmento de ruta (2-OPT)
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route) - 1):
                    # Invertir segmento entre i y j
                    new_route = (
                        tuple(route[:i])
                        + tuple(reversed(route[i : j + 1]))
                        + tuple(route[j + 1 :])
                    )

                    # Evaluar nueva ruta
                    new_solution = self._evaluate_route(new_route, instance, greedy)

                    if new_solution and new_solution.beneficio_final > current_benefit:
                        current_solution = new_solution
                        current_benefit = new_solution.beneficio_final
                        improved = True

                        if self.verbose:
                            print(
                                f"  Mejora en iter {iteration}: ${current_benefit:.2f}"
                            )
                        break

                if improved:
                    break

        return current_solution

    def _evaluate_route(
        self, route: tuple, instance: DTPInstance, greedy: GreedySolver
    ) -> DTPSolution | None:
        """Evalúa beneficio de una ruta específica usando greedy para compras.

        Recalcula compras/ventas para la ruta dada manteniendo la estrategia greedy.
        """
        try:
            # Simular ejecución con esta ruta específica
            m = instance.m

            capital = float(instance.capital_inicial)
            cargo = np.zeros(m, dtype=float)
            time_spent = 0.0

            compras_list = []
            ventas_list = []

            # Iterar por la ruta
            for idx in range(len(route)):
                current_port = route[idx]

                # Calcular costo de viaje al llegar a este puerto (excepto el primero)
                if idx > 0:
                    prev_port = route[idx - 1]
                    travel_cost = instance.costos[prev_port, current_port]
                    travel_time = instance.tiempos[prev_port, current_port]

                    capital -= travel_cost
                    time_spent += travel_time

                    # Restricciones
                    if capital < 0 or time_spent > instance.tiempo_maximo:
                        return None

                # Determinar próximo puerto para lookahead en compras
                if idx < len(route) - 1:
                    next_port = route[idx + 1]
                else:
                    next_port = None

                # Operaciones en puerto
                ventas, compras, capital, cargo = greedy._trade_at_port(
                    instance, current_port, capital, cargo, next_port
                )
                compras_list.append(compras)
                ventas_list.append(ventas)

            # Construir matriz
            steps = len(route)
            compras_matrix = np.zeros((m, steps), dtype=float)
            ventas_matrix = np.zeros((m, steps), dtype=float)

            for idx in range(min(steps, len(compras_list))):
                compras_matrix[:, idx] = compras_list[idx]
                ventas_matrix[:, idx] = ventas_list[idx]

            return DTPSolution(
                ruta=tuple(route),
                compras=compras_matrix,
                ventas=ventas_matrix,
                beneficio_final=capital,
            )

        except Exception:
            return None

    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica si la solución es factible."""
        greedy = GreedySolver()
        return greedy.is_feasible(instance, solution)

    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        """Evalúa la solución."""
        return solution.beneficio_final
