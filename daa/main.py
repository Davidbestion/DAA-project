"""Comparación de solvers del DTP."""

import time
from typing import Dict, Optional

from instances.predefined import INSTANCE_TINY, INSTANCE_SMALL, INSTANCE_MEDIUM
from solver.models.brute import BruteForceSolver
from solver.models.greedy import GreedySolver
from solver.models.aco import ACOSolver
from solver.models.ga_beam import GABeamSolver


def format_time(seconds: float) -> str:
    """Formatea tiempo en segundos a string legible."""
    if seconds < 0.001:
        return f"{seconds*1000000:.1f}μs"
    elif seconds < 1:
        return f"{seconds*1000:.1f}ms"
    else:
        return f"{seconds:.2f}s"


def compare_solvers(instance_name: str, instance, use_brute: bool = False):
    """Compara todos los solvers en una instancia."""
    print(f"\n{'='*70}")
    print(f"INSTANCIA: {instance_name}")
    print(f"{'='*70}")
    print(f"Puertos: {instance.tiempos.shape[0]-1}")
    print(f"Mercancías: {instance.pesos.shape[0]}")
    print(f"Capital inicial: {instance.capital_inicial}")
    print(f"Tiempo máximo: {instance.tiempo_maximo}")
    print(f"{'-'*70}")
    
    results = {}
    
    # Greedy Solver
    print("🔄 Ejecutando Greedy Solver...")
    greedy = GreedySolver()
    start = time.time()
    greedy_sol = greedy.solve(instance)
    greedy_time = time.time() - start
    results['Greedy'] = {
        'beneficio': greedy_sol.beneficio_final,
        'tiempo': greedy_time,
        'ruta': greedy_sol.ruta
    }
    
    # ACO Solver
    print("🔄 Ejecutando ACO Solver...")
    aco = ACOSolver(n_ants=10, n_iterations=20)
    start = time.time()
    aco_sol = aco.solve(instance)
    aco_time = time.time() - start
    results['ACO'] = {
        'beneficio': aco_sol.beneficio_final,
        'tiempo': aco_time,
        'ruta': aco_sol.ruta
    }
    
    # GA+Beam Solver
    print("🔄 Ejecutando GA+Beam Solver...")
    ga_beam = GABeamSolver(population_size=30, n_generations=50, beam_width=3)
    start = time.time()
    ga_beam_sol = ga_beam.solve(instance)
    ga_beam_time = time.time() - start
    results['GA+Beam'] = {
        'beneficio': ga_beam_sol.beneficio_final,
        'tiempo': ga_beam_time,
        'ruta': ga_beam_sol.ruta
    }
    
    # Brute Force (solo para TINY)
    if use_brute:
        print("🔄 Ejecutando Brute Force Solver...")
        brute = BruteForceSolver()
        start = time.time()
        brute_sol = brute.solve(instance)
        brute_time = time.time() - start
        results['Brute Force'] = {
            'beneficio': brute_sol.beneficio_final,
            'tiempo': brute_time,
            'ruta': brute_sol.ruta
        }
    
    # Encontrar mejor resultado
    best_beneficio = max(r['beneficio'] for r in results.values())
    
    # Mostrar resultados
    print(f"\n{'RESULTADOS':^70}")
    print(f"{'-'*70}")
    print(f"{'Solver':<15} {'Beneficio':>12} {'Tiempo':>12} {'vs Mejor':>12} {'Ruta'}")
    print(f"{'-'*70}")
    
    # Ordenar por beneficio (descendente)
    sorted_results = sorted(results.items(), key=lambda x: x[1]['beneficio'], reverse=True)
    
    for solver_name, data in sorted_results:
        beneficio = data['beneficio']
        tiempo = data['tiempo']
        ruta_str = ' → '.join(map(str, data['ruta'][:5])) + ('...' if len(data['ruta']) > 5 else '')
        
        # Calcular diferencia porcentual
        if beneficio == best_beneficio:
            diff_str = "🏆 MEJOR"
        else:
            diff_pct = ((beneficio - best_beneficio) / best_beneficio) * 100
            diff_str = f"{diff_pct:+.2f}%"
        
        print(f"{solver_name:<15} {beneficio:>12.2f} {format_time(tiempo):>12} {diff_str:>12} {ruta_str}")
    
    print(f"{'-'*70}")
    
    # Estadísticas adicionales
    greedy_beneficio = results['Greedy']['beneficio']
    print(f"\n📊 Análisis:")
    for solver_name, data in results.items():
        if solver_name != 'Greedy':
            mejora = ((data['beneficio'] - greedy_beneficio) / greedy_beneficio) * 100
            speedup = results['Greedy']['tiempo'] / data['tiempo']
            print(f"  • {solver_name}: {mejora:+.2f}% vs Greedy, {speedup:.1f}x más lento")


def main():
    """Ejecuta comparación de todos los solvers."""
    print("\n" + "="*70)
    print("COMPARACIÓN DE SOLVERS PARA EL DYNAMIC TRADING PROBLEM")
    print("="*70)
    
    # TINY - con Brute Force
    compare_solvers("TINY", INSTANCE_TINY, use_brute=True)
    
    # SMALL - sin Brute Force
    compare_solvers("SMALL", INSTANCE_SMALL, use_brute=False)
    
    # MEDIUM - sin Brute Force
    compare_solvers("MEDIUM", INSTANCE_MEDIUM, use_brute=False)
    
    print("\n" + "="*70)
    print("✅ Comparación completada")
    print("="*70 + "\n")
