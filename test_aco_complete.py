"""Prueba completa del ACO en múltiples instancias."""

from instances.predefined import INSTANCE_TINY, INSTANCE_SMALL, INSTANCE_MEDIUM
from solver.models.greedy import GreedySolver  
from solver.models.aco import ACOSolver
import time

def test_instance(name, instance, show_details=False):
    """Prueba una instancia con Greedy y ACO."""
    print(f"\n{'='*70}")
    print(f"INSTANCIA: {name}")
    print(f"Puertos: {instance.tiempos.shape[0] - 1}, Mercancías: {instance.pesos.shape[0]}")
    print('='*70)
    
    results = []
    
    # Greedy
    print("\n[1/2] Greedy Solver...")
    greedy = GreedySolver(port_selection='min_cost')
    start = time.time()
    sol_greedy = greedy.solve(instance)
    time_greedy = time.time() - start
    print(f"  ✓ Capital final: {sol_greedy.beneficio_final:.2f}")
    print(f"  ✓ Tiempo: {time_greedy:.4f}s")
    print(f"  ✓ Ruta: {' -> '.join(map(str, sol_greedy.ruta))}")
    results.append(("Greedy", sol_greedy.beneficio_final, time_greedy))
    
    # ACO
    print("\n[2/2] ACO Solver...")
    aco = ACOSolver(n_ants=15, n_iterations=30, alpha=1.0, beta=2.5, evaporation_rate=0.4)
    start = time.time()
    sol_aco = aco.solve(instance)
    time_aco = time.time() - start
    print(f"  ✓ Capital final: {sol_aco.beneficio_final:.2f}")
    print(f"  ✓ Tiempo: {time_aco:.4f}s")
    print(f"  ✓ Ruta: {' -> '.join(map(str, sol_aco.ruta))}")
    results.append(("ACO", sol_aco.beneficio_final, time_aco))
    
    # Comparación
    mejora = sol_aco.beneficio_final - sol_greedy.beneficio_final
    mejora_pct = (mejora / sol_greedy.beneficio_final * 100) if sol_greedy.beneficio_final > 0 else 0
    
    print(f"\n{'─'*70}")
    print(f"RESUMEN:")
    print(f"  • Mejora ACO: {mejora:+.2f} ({mejora_pct:+.2f}%)")
    print(f"  • Factor tiempo: {time_aco/time_greedy:.1f}x más lento que Greedy")
    print('─'*70)
    
    if show_details:
        print("\nOperaciones ACO:")
        for idx, port in enumerate(sol_aco.ruta[:-1]):
            compras = sol_aco.compras[:, idx]
            ventas = sol_aco.ventas[:, idx]
            if compras.sum() > 0 or ventas.sum() > 0:
                print(f"  Puerto {port}:")
                if ventas.sum() > 0:
                    print(f"    Ventas: {ventas[ventas > 0]}")
                if compras.sum() > 0:
                    print(f"    Compras: {compras[compras > 0]}")
    
    return results

print("="*70)
print("EVALUACIÓN COMPLETA: ACO vs Greedy")
print("="*70)

# TINY
test_instance("TINY", INSTANCE_TINY, show_details=True)

# SMALL
test_instance("SMALL", INSTANCE_SMALL, show_details=True)

# MEDIUM
test_instance("MEDIUM", INSTANCE_MEDIUM, show_details=False)

print(f"\n{'='*70}")
print("EVALUACIÓN COMPLETADA")
print('='*70)
