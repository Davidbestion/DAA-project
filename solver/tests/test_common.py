"""Test base/complejo que funciona con cualquier solucionador."""

import time

from instances.micro import (
    INSTANCE_MICRO_1,
    INSTANCE_MICRO_2,
    INSTANCE_MICRO_3,
    INSTANCE_MICRO_4,
)
from instances.robust import get_all_instances, get_micro_instances, get_extreme_instances


def test_solver(solver, instance, instance_name=""):
    """
    Ejecuta un solucionador en una instancia y retorna métricas.

    Args:
        solver: Instancia de solver (BruteForceSolver o GreedySolver)
        instance: DTPInstance a resolver
        instance_name: Nombre descriptivo de la instancia

    Returns:
        dict con: nombre, tiempo_ms, beneficio, viable, ruta
    """
    start = time.perf_counter()
    solution = solver.solve(instance)
    elapsed = time.perf_counter() - start

    is_feasible = solver.is_feasible(instance, solution) if solution else False
    benefit = solution.beneficio_final if solution else 0
    route = solution.ruta if solution else None

    return {
        "nombre": instance_name,
        "tiempo_ms": elapsed * 1000,
        "beneficio": benefit,
        "viable": is_feasible,
        "ruta": route,
    }


def run_solver_tests(solver):
    """
    Ejecuta un solucionador en todas las instancias MICRO.

    Args:
        solver: Instancia de solver (BruteForceSolver o GreedySolver)

    Returns:
        list de dicts con resultados
    """
    instances = [
        (INSTANCE_MICRO_1, "MICRO_1 (n=2, m=1)"),
        (INSTANCE_MICRO_2, "MICRO_2 (n=2, m=2)"),
        (INSTANCE_MICRO_3, "MICRO_3 (n=3, m=1)"),
        (INSTANCE_MICRO_4, "MICRO_4 (n=2, m=2)"),
    ]

    results = []
    for instance, name in instances:
        result = test_solver(solver, instance, name)
        results.append(result)

    return results


def run_robust_tests(solver, batch_type: str = "micro"):
    """
    Ejecuta un solucionador en un batch de instancias (MICRO o EXTREME).

    Args:
        solver: Instancia de solver
        batch_type: "micro" (4 instancias), "extreme" (8 casos extremos), "all" (12 total)

    Returns:
        list de dicts con resultados
    """
    if batch_type == "micro":
        instances = get_micro_instances()
    elif batch_type == "extreme":
        instances = get_extreme_instances()
    else:  # "all"
        instances = get_all_instances()

    results = []
    for instance, name in instances:
        result = test_solver(solver, instance, name)
        results.append(result)

    return results
