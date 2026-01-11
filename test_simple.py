"""Test con una instancia muy simple y controlada."""

import numpy as np
from solver.schemas.dtp import DTPInstance
from solver.models.brute import BruteForceSolver

# Crear una instancia super simple y claramente rentable
instance = DTPInstance(
    tiempos=np.array([
        [0.0, 10.0],
        [10.0, 0.0],
    ]),
    costos=np.array([
        [0.0, 10.0],  # Viaje barato
        [10.0, 0.0],
    ]),
    precios_compra=np.array([  # Lo que el PUERTO paga
        [10.0, 50.0],  # M0: Puerto 0 paga 10, Puerto 1 paga 50
    ]),
    precios_venta=np.array([  # Lo que el PUERTO cobra
        [20.0, 60.0],  # M0: Puerto 0 cobra 20, Puerto 1 cobra 60
    ]),
    oferta_max=np.array([
        [10.0, 10.0],
    ]),
    pesos=np.array([1.0]),
    capacidad_bodega=10,
    capital_inicial=200,
    tiempo_maximo=100,
    umbral_beneficio=0.0,
    capital_minimo=0.0,
)

print("INSTANCIA DE PRUEBA SIMPLE:")
print("="*60)
print("Estrategia óptima esperada:")
print("1. En Puerto 0: Comprar M0 a 20 (puerto vende)")
print("2. Viajar a Puerto 1 (costo: 10)")
print("3. En Puerto 1: Vender M0 a 50 (puerto compra)")
print("4. Regresar a Puerto 0 (costo: 10)")
print()
print("Cálculo esperado:")
print("- Capital inicial: 200")
print("- Comprar 9 unidades de M0 a 20 = -180")
print("- Capital después: 20")
print("- Viajar 0→1: -10, Capital: 10")
print("- Vender 9 unidades a 50 = +450")
print("- Capital después: 460")
print("- Viajar 1→0: -10")
print("- Capital final esperado: 450")
print("- Ganancia esperada: 250")
print("="*60)

instance.display()

solver = BruteForceSolver()
print("\nResolviendo...")
solution = solver.solve(instance)

print("\nSOLUCIÓN:")
solution.display()

print(f"\n{'='*60}")
print(f"Capital inicial: {instance.capital_inicial}")
print(f"Capital final: {solution.beneficio_final:.2f}")
print(f"Ganancia/Pérdida: {solution.beneficio_final - instance.capital_inicial:.2f}")
