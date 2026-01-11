"""Script para verificar que todas las instancias tienen precios correctos."""

import numpy as np
from instances import INSTANCE_TINY, INSTANCE_SMALL, INSTANCE_MEDIUM, INSTANCE_LARGE

def verificar_precios(instance, nombre):
    print(f"\n{'='*60}")
    print(f"Verificando {nombre}")
    print(f"{'='*60}")
    
    precios_compra = instance.precios_compra
    precios_venta = instance.precios_venta
    
    diferencia = precios_venta - precios_compra
    
    print(f"Forma de precios_compra: {precios_compra.shape}")
    print(f"Forma de precios_venta: {precios_venta.shape}")
    
    # Verificar que todos los precios de venta sean mayores
    if np.all(diferencia > 0):
        print("✅ CORRECTO: Todos los precios_venta > precios_compra")
        print(f"   Margen mínimo: {np.min(diferencia):.2f}")
        print(f"   Margen máximo: {np.max(diferencia):.2f}")
        print(f"   Margen promedio: {np.mean(diferencia):.2f}")
    else:
        print("❌ ERROR: Algunos precios están invertidos")
        malos = np.where(diferencia <= 0)
        for i, j in zip(malos[0], malos[1]):
            print(f"   Mercancía {i}, Puerto {j}: compra={precios_compra[i,j]:.2f}, venta={precios_venta[i,j]:.2f}")
    
    return np.all(diferencia > 0)

# Verificar todas las instancias
instancias = [
    (INSTANCE_TINY, "INSTANCE_TINY"),
    (INSTANCE_SMALL, "INSTANCE_SMALL"),
    (INSTANCE_MEDIUM, "INSTANCE_MEDIUM"),
    (INSTANCE_LARGE, "INSTANCE_LARGE"),
]

todas_correctas = True
for instance, nombre in instancias:
    if not verificar_precios(instance, nombre):
        todas_correctas = False

print(f"\n{'='*60}")
if todas_correctas:
    print("✅ TODAS LAS INSTANCIAS SON CORRECTAS")
else:
    print("❌ HAY INSTANCIAS CON ERRORES")
print(f"{'='*60}")

# Ahora probar el solver con INSTANCE_TINY
print("\n\nProbando BruteForceSolver con INSTANCE_TINY...")
from solver.models.brute import BruteForceSolver

solver = BruteForceSolver()
solution = solver.solve(INSTANCE_TINY)

print("\nSolución encontrada:")
print(solution.summary())
print(f"\nCapital inicial: {INSTANCE_TINY.capital_inicial}")
print(f"Capital final: {solution.beneficio_final:.2f}")
print(f"Ganancia neta: {solution.beneficio_final - INSTANCE_TINY.capital_inicial:.2f}")
