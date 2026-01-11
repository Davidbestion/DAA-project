"""Verificación manual detallada de la solución."""

from instances import INSTANCE_TINY
from solver.models.brute import BruteForceSolver

print("="*60)
print("INSTANCIA TINY")
print("="*60)
instance = INSTANCE_TINY
instance.display()

print("\n" + "="*60)
print("RESOLVIENDO CON BRUTE FORCE")
print("="*60)

solver = BruteForceSolver()
solution = solver.solve(instance)

print("\nSOLUCIÓN ENCONTRADA:")
solution.display()

print("\n" + "="*60)
print("VERIFICACIÓN MANUAL DE LA SOLUCIÓN")
print("="*60)

ruta = solution.ruta
compras = solution.compras
ventas = solution.ventas

capital = instance.capital_inicial
cargo = {0: 0.0, 1: 0.0}  # Mercancías en bodega

print(f"\nCapital inicial: {capital:.2f}")
print(f"Ruta: {' → '.join(map(str, ruta))}")

for step in range(len(ruta)):
    puerto = ruta[step]
    print(f"\n{'='*50}")
    print(f"PASO {step}: Puerto {puerto}")
    print(f"{'='*50}")
    
    # Costo de viaje (si no es el primer paso)
    if step > 0:
        puerto_anterior = ruta[step - 1]
        costo_viaje = instance.costos[puerto_anterior, puerto]
        capital -= costo_viaje
        print(f"🚢 Viaje {puerto_anterior}→{puerto}: -{costo_viaje:.2f}")
        print(f"   Capital después del viaje: {capital:.2f}")
    
    print(f"   Cargo actual: M0={cargo[0]:.0f}, M1={cargo[1]:.0f}")
    
    # Ventas en este puerto
    for merc in range(instance.m):
        if ventas[merc, step] > 0:
            cantidad = ventas[merc, step]
            precio = instance.precios_compra[merc, puerto]  # El puerto COMPRA
            ingreso = cantidad * precio
            capital += ingreso
            cargo[merc] -= cantidad
            print(f"💲 Vende {cantidad:.0f} unidades de M{merc} al puerto a {precio:.2f} c/u = +{ingreso:.2f}")
            print(f"   Capital después de venta: {capital:.2f}")
            print(f"   Cargo después: M0={cargo[0]:.0f}, M1={cargo[1]:.0f}")
    
    # Compras en este puerto
    for merc in range(instance.m):
        if compras[merc, step] > 0:
            cantidad = compras[merc, step]
            precio = instance.precios_venta[merc, puerto]  # El puerto VENDE
            costo = cantidad * precio
            capital -= costo
            cargo[merc] += cantidad
            print(f"🛒 Compra {cantidad:.0f} unidades de M{merc} del puerto a {precio:.2f} c/u = -{costo:.2f}")
            print(f"   Capital después de compra: {capital:.2f}")
            print(f"   Cargo después: M0={cargo[0]:.0f}, M1={cargo[1]:.0f}")

print(f"\n{'='*60}")
print(f"RESUMEN FINAL")
print(f"{'='*60}")
print(f"Capital inicial: {instance.capital_inicial:.2f}")
print(f"Capital final: {capital:.2f}")
print(f"Ganancia/Pérdida: {capital - instance.capital_inicial:.2f}")
print(f"Cargo final: M0={cargo[0]:.0f}, M1={cargo[1]:.0f}")

if abs(capital - solution.beneficio_final) < 0.01:
    print("\n✅ La verificación manual coincide con la solución")
else:
    print(f"\n❌ ERROR: Discrepancia entre manual ({capital:.2f}) y solución ({solution.beneficio_final:.2f})")
