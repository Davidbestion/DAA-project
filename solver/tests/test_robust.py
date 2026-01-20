"""Test robustos: validar solvers con casos extremos."""

from .test_models import (
    run_brute_tests,
    run_greedy_tests,
    run_multigreedy_tests,
    run_local_search_tests,
    run_aco_tests,
    run_ga_beam_tests,
)
from .test_common import run_robust_tests
from solver.models import BruteForceSolver, GreedySolver
from solver.models.heuristics import MultiGreedySolver, GreedyWithLocalSearch
from solver.models.aco import ACOSolver
from solver.models.ga_beam import GABeamSolver


def test_robust_micro():
    """Ejecuta todos los solvers en instancias MICRO (rápido, 4 casos)."""
    print("\n" + "=" * 100)
    print("ROBUST TEST: MICRO INSTANCES (4 casos rápidos)")
    print("=" * 100 + "\n")
    
    solvers = {
        "BruteForceSolver": BruteForceSolver(),
        "GreedySolver": GreedySolver(),
        "MultiGreedySolver": MultiGreedySolver(),
        "GreedyWithLocalSearch": GreedyWithLocalSearch(verbose=False),
        "ACOSolver": ACOSolver(n_ants=10, n_iterations=50),
        "GABeamSolver": GABeamSolver(population_size=50, n_generations=100),
    }
    
    results = {}
    for solver_name, solver in solvers.items():
        results[solver_name] = run_robust_tests(solver, batch_type="micro")
        print(f"✓ {solver_name} completado")
    
    return results


def test_robust_extreme():
    """Ejecuta todos los solvers en instancias EXTREME (exhaustivo, 8 casos extremos)."""
    print("\n" + "=" * 100)
    print("ROBUST TEST: EXTREME INSTANCES (8 casos de stress)")
    print("=" * 100 + "\n")
    
    solvers = {
        "BruteForceSolver": BruteForceSolver(),
        "GreedySolver": GreedySolver(),
        "MultiGreedySolver": MultiGreedySolver(),
        "GreedyWithLocalSearch": GreedyWithLocalSearch(verbose=False),
        "ACOSolver": ACOSolver(n_ants=10, n_iterations=50),
        "GABeamSolver": GABeamSolver(population_size=50, n_generations=100),
    }
    
    results = {}
    for solver_name, solver in solvers.items():
        print(f"Testing {solver_name}...")
        results[solver_name] = run_robust_tests(solver, batch_type="extreme")
        print(f"✓ {solver_name} completado\n")
    
    return results


def test_robust_all():
    """Ejecuta todos los solvers en todas las instancias (12 casos totales)."""
    print("\n" + "=" * 100)
    print("ROBUST TEST: ALL INSTANCES (12 casos: 4 MICRO + 8 EXTREME)")
    print("=" * 100 + "\n")
    
    solvers = {
        "BruteForceSolver": BruteForceSolver(),
        "GreedySolver": GreedySolver(),
        "MultiGreedySolver": MultiGreedySolver(),
        "GreedyWithLocalSearch": GreedyWithLocalSearch(verbose=False),
        "ACOSolver": ACOSolver(n_ants=10, n_iterations=50),
        "GABeamSolver": GABeamSolver(population_size=50, n_generations=100),
    }
    
    results = {}
    for solver_name, solver in solvers.items():
        print(f"Testing {solver_name}...")
        results[solver_name] = run_robust_tests(solver, batch_type="all")
        print(f"✓ {solver_name} completado\n")
    
    return results


def display_robust_results(results, title: str = "ROBUST TEST RESULTS"):
    """Muestra resultados de un test robusto."""
    print("\n" + "=" * 120)
    print(title)
    print("=" * 120 + "\n")
    
    # Tabla de resultados
    print(f"{'Instancia':<40} {'BruteForceSolver':<18} {'GreedySolver':<18} {'Greedy+2OPT':<18} {'ACOSolver':<18} {'GABeamSolver':<18}")
    print("-" * 120)
    
    # Obtener nombre de instancias del primer solver
    first_solver = list(results.keys())[0]
    instance_names = [r["nombre"] for r in results[first_solver]]
    
    for i, instance_name in enumerate(instance_names):
        print(f"{instance_name:<40}", end="")
        for solver_name in ["BruteForceSolver", "GreedySolver", "GreedyWithLocalSearch", "ACOSolver", "GABeamSolver"]:
            if solver_name in results:
                if i < len(results[solver_name]):
                    result = results[solver_name][i]
                    benefit = result["beneficio"]
                    time_ms = result["tiempo_ms"]
                    viable = "✓" if result["viable"] else "✗"
                    print(f"${benefit:6.1f}({time_ms:6.1f}ms){viable}  ", end="")
                else:
                    print(f"{'N/A':<18}", end="")
        print()
    
    print("\n" + "=" * 120)


if __name__ == "__main__":
    # Opción 1: Test MICRO (rápido)
    # results = test_robust_micro()
    # display_robust_results(results, "ROBUST TEST: MICRO INSTANCES")
    
    # Opción 2: Test EXTREME (exhaustivo)
    # results = test_robust_extreme()
    # display_robust_results(results, "ROBUST TEST: EXTREME INSTANCES")
    
    # Opción 3: Test ALL (completo)
    results = test_robust_all()
    display_robust_results(results, "ROBUST TEST: ALL INSTANCES (MICRO + EXTREME)")
