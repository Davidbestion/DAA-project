"""Script de debug del ACO para entender qué está pasando."""

from instances.predefined import INSTANCE_TINY
from solver.models.aco import ACOSolver
import numpy as np

print("="*60)
print("DEBUG: ACO Solver en INSTANCE_TINY")
print("="*60)

instance = INSTANCE_TINY

print("\nInfo de la instancia:")
print(f"Capital inicial: {instance.capital_inicial}")
print(f"Capacidad bodega: {instance.capacidad_bodega}")
print(f"Tiempo máximo: {instance.tiempo_maximo}")

print("\nPrecios compra (lo que el puerto paga al comerciante):")
print(instance.precios_compra)

print("\nPrecios venta (lo que el puerto cobra al comerciante):")
print(instance.precios_venta)

print("\nCostos de viaje:")
print(instance.costos)

print("\nTiempos de viaje:")
print(instance.tiempos)

# Simular ruta 0 -> 1 -> 2 -> 0 manualmente
print("\n" + "="*60)
print("SIMULACIÓN MANUAL: Ruta 0 -> 1 -> 2 -> 0")
print("="*60)

capital = float(instance.capital_inicial)
cargo = np.zeros(2)
print(f"\nInicio: Capital={capital}, Cargo={cargo}")

# En puerto 0 (Amsterdam), no hay compras iniciales
print("\n--- Puerto 0 (Amsterdam) ---")
print("No se comercia en el puerto inicial")

# Viajar a puerto 1
print(f"\nViajando 0->1: Costo={instance.costos[0,1]}, Tiempo={instance.tiempos[0,1]}")
capital -= instance.costos[0,1]
print(f"Capital después de viajar: {capital}")

# En puerto 1
print("\n--- Puerto 1 ---")
print("Vender cargo (ninguno por ahora)")
print(f"Capital disponible para compras: {capital - instance.costos[1,2]}")

# Comprar para vender en puerto 2
for k in range(2):
    precio_compra = instance.precios_venta[k, 1]
    precio_venta = instance.precios_compra[k, 2]
    profit = precio_venta - precio_compra
    print(f"Mercancía {k}: comprar a {precio_compra}, vender en 2 a {precio_venta}, profit={profit}")

# Viajar a puerto 2
print(f"\nViajando 1->2: Costo={instance.costos[1,2]}, Tiempo={instance.tiempos[1,2]}")
capital -= instance.costos[1,2]
print(f"Capital después de viajar: {capital}")

# En puerto 2
print("\n--- Puerto 2 ---")
print("Vender cargo...")

# Viajar de vuelta a 0
print(f"\nViajando 2->0: Costo={instance.costos[2,0]}, Tiempo={instance.tiempos[2,0]}")
capital -= instance.costos[2,0]
print(f"Capital después de viajar: {capital}")

print(f"\nBeneficio final estimado: {capital - instance.capital_inicial}")

# Ahora probar con ACO
print("\n" + "="*60)
print("RESULTADO ACO")
print("="*60)
aco = ACOSolver(n_ants=5, n_iterations=20)
solution = aco.solve(instance)
print(f"Ruta: {' -> '.join(map(str, solution.ruta))}")
print(f"Beneficio: {solution.beneficio_final}")
print(f"Compras:\n{solution.compras}")
print(f"Ventas:\n{solution.ventas}")
