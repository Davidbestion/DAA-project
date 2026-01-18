"""Verificar TODAS las rutas posibles en TINY."""

from instances.predefined import INSTANCE_TINY
import numpy as np
from itertools import permutations

instance = INSTANCE_TINY

def evaluate_route_simple(route):
    """Evaluación simple: solo costos de viaje, sin comercio."""
    capital = float(instance.capital_inicial)
    for i in range(len(route) - 1):
        capital -= instance.costos[route[i], route[i+1]]
    return capital - instance.capital_inicial

print("="*60)
print("TODAS LAS RUTAS POSIBLES (sin comercio)")
print("="*60)

# Todas las permutaciones de {1, 2}
ports = [1, 2]
for perm in permutations(ports):
    route = [0] + list(perm) + [0]
    benefit = evaluate_route_simple(route)
    print(f"Ruta {' -> '.join(map(str, route))}: Beneficio = {benefit:.2f}")

print("\n" + "="*60)
print("MEJOR ESTRATEGIA: No comerciar, tomar la ruta más barata")
print("="*60)
