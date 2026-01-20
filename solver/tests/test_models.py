"""Pruebas unitarias para los modelos de solver."""

from solver.models import BruteForceSolver, GreedySolver
from solver.models.heuristics import MultiGreedySolver, GreedyWithLocalSearch
from solver.models.aco import ACOSolver
from solver.models.ga_beam import GABeamSolver
from .test_common import run_solver_tests


def run_brute_tests():
    """Ejecuta BruteForceSolver en todas las instancias MICRO."""
    solver = BruteForceSolver()
    return run_solver_tests(solver)


def run_greedy_tests():
    """Ejecuta GreedySolver en todas las instancias MICRO."""
    solver = GreedySolver()
    return run_solver_tests(solver)


def run_multigreedy_tests():
    """Ejecuta MultiGreedySolver en todas las instancias MICRO."""
    solver = MultiGreedySolver()
    return run_solver_tests(solver)


def run_local_search_tests():
    """Ejecuta GreedyWithLocalSearch en todas las instancias MICRO."""
    solver = GreedyWithLocalSearch(verbose=False)
    return run_solver_tests(solver)


def run_aco_tests():
    """Ejecuta ACOSolver en todas las instancias MICRO."""
    solver = ACOSolver(n_ants=10, n_iterations=50)
    return run_solver_tests(solver)


def run_ga_beam_tests():
    """Ejecuta GABeamSolver en todas las instancias MICRO."""
    solver = GABeamSolver(population_size=50, n_generations=100, beam_width=5)
    return run_solver_tests(solver)
