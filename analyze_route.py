"""Analizar ruta 0->2->1->0."""

from instances.predefined import INSTANCE_TINY
import numpy as np

instance = INSTANCE_TINY

print("="*60)
print("ANÁLISIS: Ruta 0 -> 2 -> 1 -> 0")
print("="*60)

capital = float(instance.capital_inicial)
cargo = np.zeros(2)
print(f"\nInicio: Capital={capital}")

# Viajar 0 -> 2
print(f"\n--- Viaje 0->2 ---")
print(f"Costo: {instance.costos[0,2]}, Tiempo: {instance.tiempos[0,2]}")
capital -= instance.costos[0,2]
print(f"Capital: {capital}")

# En puerto 2
print(f"\n--- Puerto 2 ---")
capital_para_compras = capital - instance.costos[2,1]
print(f"Capital disponible (reservando viaje 2->1): {capital_para_compras}")

for k in range(2):
    precio_compra = instance.precios_venta[k, 2]
    precio_venta = instance.precios_compra[k, 1]
    profit = precio_venta - precio_compra
    peso = instance.pesos[k]
    oferta = instance.oferta_max[k, 2]
    max_units = min(oferta, capital_para_compras / precio_compra, 40 / peso)
    print(f"Merc {k}: comprar a {precio_compra}, vender en 1 a {precio_venta}, "
          f"profit={profit}, max_units={max_units:.1f}")

# Comprar lo mejor (mercancía 0)
k = 0
precio_compra = instance.precios_venta[k, 2]
cantidad = min(6, capital_para_compras / precio_compra)
cantidad = int(cantidad)
capital -= cantidad * precio_compra
cargo[k] = cantidad
print(f"\nComprar {cantidad} unidades de merc 0 a {precio_compra} cada una")
print(f"Capital: {capital}, Cargo: {cargo}")

# Viajar 2 -> 1
print(f"\n--- Viaje 2->1 ---")
print(f"Costo: {instance.costos[2,1]}, Tiempo: {instance.tiempos[2,1]}")
capital -= instance.costos[2,1]
print(f"Capital: {capital}")

# En puerto 1 - VENDER
print(f"\n--- Puerto 1 ---")
precio_venta = instance.precios_compra[0, 1]
capital += cargo[0] * precio_venta
print(f"Vender {cargo[0]} unidades de merc 0 a {precio_venta} cada una")
print(f"Capital: {capital}")
cargo[0] = 0

# No comprar nada en puerto 1 (último puerto)

# Viajar 1 -> 0
print(f"\n--- Viaje 1->0 ---")
print(f"Costo: {instance.costos[1,0]}, Tiempo: {instance.tiempos[1,0]}")
capital -= instance.costos[1,0]
print(f"Capital: {capital}")

print(f"\n{'='*60}")
print(f"BENEFICIO FINAL: {capital - instance.capital_inicial}")
print(f"{'='*60}")
