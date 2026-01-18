"""Verificar qué hace exactamente el Greedy."""

from instances.predefined import INSTANCE_TINY
from solver.models.greedy import GreedySolver

instance = INSTANCE_TINY

greedy = GreedySolver(port_selection='min_cost')
solution = greedy.solve(instance)

print("="*60)
print("SOLUCIÓN GREEDY")
print("="*60)
print(f"Ruta: {' -> '.join(map(str, solution.ruta))}")
print(f"Beneficio: {solution.beneficio_final}")

print("\nCompras por puerto:")
for idx, port in enumerate(solution.ruta[:-1]):
    compras = solution.compras[:, idx]
    if compras.sum() > 0:
        print(f"  Puerto {port}: {compras}")

print("\nVentas por puerto:")
for idx, port in enumerate(solution.ruta[:-1]):
    ventas = solution.ventas[:, idx]
    if ventas.sum() > 0:
        print(f"  Puerto {port}: {ventas}")
