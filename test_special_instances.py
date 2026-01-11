"""Test de las instancias especiales KNAPSACK y TSP."""

from instances import INSTANCE_KNAPSACK, INSTANCE_TSP

print("="*70)
print("INSTANCIA TIPO KNAPSACK")
print("="*70)
print("\nCaracterísticas:")
print(f"- Puertos: {INSTANCE_KNAPSACK.n + 1} (incluyendo Ámsterdam)")
print(f"- Mercancías: {INSTANCE_KNAPSACK.m}")
print(f"- Capacidad de bodega: {INSTANCE_KNAPSACK.capacidad_bodega}")
print(f"- Capital inicial: {INSTANCE_KNAPSACK.capital_inicial}")
print("\nEste problema se reduce a un KNAPSACK:")
print("- Solo hay 2 puertos (ida y vuelta simple)")
print("- El desafío es elegir qué mercancías llevar")
print("- Restricciones: peso máximo y capital disponible")
print("- Objetivo: maximizar ganancia con la selección óptima")

INSTANCE_KNAPSACK.display()

print("\n\n" + "="*70)
print("INSTANCIA TIPO VIAJANTE (TSP)")
print("="*70)
print("\nCaracterísticas:")
print(f"- Puertos: {INSTANCE_TSP.n + 1} (incluyendo Ámsterdam)")
print(f"- Mercancías: {INSTANCE_TSP.m}")
print(f"- Oferta por puerto: 1 unidad")
print(f"- Capital inicial: {INSTANCE_TSP.capital_inicial}")
print("\nEste problema se reduce a TSP (Viajante):")
print("- Solo 1 mercancía con cantidad limitada a 1 por puerto")
print("- Los precios solo son buenos en el puerto 0 (Ámsterdam)")
print("- El desafío principal es encontrar la ruta más eficiente")
print("- Objetivo: minimizar costos de viaje visitando todos los puertos")

INSTANCE_TSP.display()

# Verificar que los precios son correctos
print("\n" + "="*70)
print("VERIFICACIÓN DE PRECIOS")
print("="*70)

import numpy as np

def verificar(instance, nombre):
    diff = instance.precios_venta - instance.precios_compra
    if np.all(diff > 0):
        print(f"✅ {nombre}: Todos los precios son válidos")
    else:
        print(f"❌ {nombre}: Hay precios inválidos")

verificar(INSTANCE_KNAPSACK, "KNAPSACK")
verificar(INSTANCE_TSP, "TSP")
