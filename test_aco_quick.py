"""Script rápido de prueba del ACO Solver."""

from instances.predefined import INSTANCE_TINY
from solver.models.greedy import GreedySolver
from solver.models.aco import ACOSolver
import time

print("="*60)
print("PRUEBA RÁPIDA: ACO Solver")
print("="*60)

instance = INSTANCE_TINY
print(f"\nInstancia TINY:")
print(f"  Puertos: {instance.tiempos.shape[0] - 1}")
print(f"  Mercancías: {instance.pesos.shape[0]}")

# Greedy
print("\n" + "-"*60)
print("Greedy Solver")
print("-"*60)
greedy = GreedySolver(port_selection='min_cost')
start = time.time()
sol_greedy = greedy.solve(instance)
time_greedy = time.time() - start
print(f"Tiempo: {time_greedy:.4f}s")
print(f"Beneficio: {sol_greedy.beneficio_final:.2f}")
print(f"Ruta: {' -> '.join(map(str, sol_greedy.ruta))}")

# ACO
print("\n" + "-"*60)
print("ACO Solver (5 hormigas, 20 iteraciones)")
print("-"*60)
aco = ACOSolver(n_ants=5, n_iterations=20)
start = time.time()
sol_aco = aco.solve(instance)
time_aco = time.time() - start
print(f"Tiempo: {time_aco:.4f}s")
print(f"Beneficio: {sol_aco.beneficio_final:.2f}")
print(f"Ruta: {' -> '.join(map(str, sol_aco.ruta))}")

print("\n" + "="*60)
print(f"Mejora ACO vs Greedy: {sol_aco.beneficio_final - sol_greedy.beneficio_final:.2f}")
print("="*60)
