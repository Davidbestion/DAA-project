"""Script para verificar los cálculos de la solución."""

from instances import INSTANCE_TINY
from solver.models.brute import BruteForceSolver

print("Verificación de la solución:\n")

instance = INSTANCE_TINY

# Mostrar precios relevantes
print("PRECIOS DE COMPRA Y VENTA:")
print(f"Mercancía 0 en Puerto 0: Compra={instance.precios_compra[0, 0]:.2f}, Venta={instance.precios_venta[0, 0]:.2f}")
print(f"Mercancía 0 en Puerto 1: Compra={instance.precios_compra[0, 1]:.2f}, Venta={instance.precios_venta[0, 1]:.2f}")
print(f"Mercancía 0 en Puerto 2: Compra={instance.precios_compra[0, 2]:.2f}, Venta={instance.precios_venta[0, 2]:.2f}")
print()
print(f"Mercancía 1 en Puerto 0: Compra={instance.precios_compra[1, 0]:.2f}, Venta={instance.precios_venta[1, 0]:.2f}")
print(f"Mercancía 1 en Puerto 1: Compra={instance.precios_compra[1, 1]:.2f}, Venta={instance.precios_venta[1, 1]:.2f}")
print(f"Mercancía 1 en Puerto 2: Compra={instance.precios_compra[1, 2]:.2f}, Venta={instance.precios_venta[1, 2]:.2f}")

print("\n" + "="*60)
print("SIMULACIÓN MANUAL DE LA RUTA 0 → 1 → 2 → 0:")
print("="*60)

capital = instance.capital_inicial
print(f"\n📍 Puerto 0 (Ámsterdam) - Capital inicial: {capital:.2f}")

# Comprar 13 unidades de mercancía 0 en puerto 0
compra_m0_p0 = 13 * instance.precios_compra[0, 0]
capital -= compra_m0_p0
print(f"  Comprar 13 unidades de mercancía 0 a {instance.precios_compra[0, 0]:.2f} c/u")
print(f"  Costo: {compra_m0_p0:.2f}")
print(f"  Capital después: {capital:.2f}")

# Viajar a puerto 1
costo_viaje_0_1 = instance.costos[0, 1]
capital -= costo_viaje_0_1
print(f"\n🚢 Viaje 0→1 - Costo: {costo_viaje_0_1:.2f}")
print(f"  Capital después: {capital:.2f}")

print(f"\n📍 Puerto 1 - Capital: {capital:.2f}")

# Vender 13 unidades de mercancía 0 en puerto 1
venta_m0_p1 = 13 * instance.precios_venta[0, 1]
capital += venta_m0_p1
print(f"  Vender 13 unidades de mercancía 0 a {instance.precios_venta[0, 1]:.2f} c/u")
print(f"  Ingreso: {venta_m0_p1:.2f}")
print(f"  Capital después: {capital:.2f}")

# Comprar 10 unidades de mercancía 1 en puerto 1
compra_m1_p1 = 10 * instance.precios_compra[1, 1]
capital -= compra_m1_p1
print(f"  Comprar 10 unidades de mercancía 1 a {instance.precios_compra[1, 1]:.2f} c/u")
print(f"  Costo: {compra_m1_p1:.2f}")
print(f"  Capital después: {capital:.2f}")

# Viajar a puerto 2
costo_viaje_1_2 = instance.costos[1, 2]
capital -= costo_viaje_1_2
print(f"\n🚢 Viaje 1→2 - Costo: {costo_viaje_1_2:.2f}")
print(f"  Capital después: {capital:.2f}")

print(f"\n📍 Puerto 2 - Capital: {capital:.2f}")

# Vender 10 unidades de mercancía 1 en puerto 2
venta_m1_p2 = 10 * instance.precios_venta[1, 2]
capital += venta_m1_p2
print(f"  Vender 10 unidades de mercancía 1 a {instance.precios_venta[1, 2]:.2f} c/u")
print(f"  Ingreso: {venta_m1_p2:.2f}")
print(f"  Capital después: {capital:.2f}")

# Comprar 10 unidades de mercancía 1 en puerto 2
compra_m1_p2 = 10 * instance.precios_compra[1, 2]
capital -= compra_m1_p2
print(f"  Comprar 10 unidades de mercancía 1 a {instance.precios_compra[1, 2]:.2f} c/u")
print(f"  Costo: {compra_m1_p2:.2f}")
print(f"  Capital después: {capital:.2f}")

# Viajar de vuelta a puerto 0
costo_viaje_2_0 = instance.costos[2, 0]
capital -= costo_viaje_2_0
print(f"\n🚢 Viaje 2→0 - Costo: {costo_viaje_2_0:.2f}")
print(f"  Capital después: {capital:.2f}")

print(f"\n📍 Puerto 0 (Ámsterdam) - Capital final: {capital:.2f}")

# Vender las 10 unidades restantes de mercancía 1
venta_m1_p0 = 10 * instance.precios_venta[1, 0]
capital += venta_m1_p0
print(f"  Vender 10 unidades de mercancía 1 a {instance.precios_venta[1, 0]:.2f} c/u")
print(f"  Ingreso: {venta_m1_p0:.2f}")
print(f"  Capital después: {capital:.2f}")

print(f"\n💰 CAPITAL FINAL: {capital:.2f}")
print(f"💰 BENEFICIO: {capital - instance.capital_inicial:.2f}")

print("\n" + "="*60)
print("Ahora ejecutemos el solver:")
print("="*60)
solver = BruteForceSolver()
solution = solver.solve(instance)
print(solution)
