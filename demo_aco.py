"""
Script de ejemplo y prueba del ACOSolver.

Compara el rendimiento del ACO contra los otros solvers.
"""

from instances.predefined import INSTANCE_TINY, INSTANCE_SMALL, INSTANCE_MEDIUM
from solver.models.brute import BruteForceSolver
from solver.models.greedy import GreedySolver
from solver.models.aco import ACOSolver
import time


def test_solver(solver, instance, name):
    """Prueba un solver y mide el tiempo de ejecución."""
    print(f"\n{'='*60}")
    print(f"Probando: {name}")
    print('='*60)
    
    start = time.time()
    solution = solver.solve(instance)
    elapsed = time.time() - start
    
    print(f"Tiempo de ejecución: {elapsed:.4f}s")
    print(f"Beneficio final: {solution.beneficio_final:.2f}")
    print(f"Ruta: {' -> '.join(map(str, solution.ruta))}")
    print(f"Factible: {solver.is_feasible(instance, solution)}")
    
    return solution, elapsed


def compare_solvers():
    """Compara todos los solvers en diferentes instancias."""
    
    instances = [
        ("TINY", INSTANCE_TINY),
        ("SMALL", INSTANCE_SMALL),
        ("MEDIUM", INSTANCE_MEDIUM),
    ]
    
    for instance_name, instance in instances:
        print(f"\n\n{'#'*70}")
        print(f"# INSTANCIA: {instance_name}")
        print(f"# Puertos: {instance.tiempos.shape[0] - 1}, "
              f"Mercancías: {instance.pesos.shape[0]}")
        print('#'*70)
        
        results = []
        
        # Greedy Solver (rápido)
        greedy = GreedySolver(port_selection='min_cost')
        sol_greedy, time_greedy = test_solver(greedy, instance, "Greedy (min_cost)")
        results.append(("Greedy", sol_greedy.beneficio_final, time_greedy))
        
        # ACO Solver con diferentes configuraciones
        aco_configs = [
            ("ACO (10 hormigas, 50 iter)", ACOSolver(n_ants=10, n_iterations=50)),
            ("ACO (20 hormigas, 30 iter)", ACOSolver(n_ants=20, n_iterations=30)),
            ("ACO (5 hormigas, 100 iter)", ACOSolver(n_ants=5, n_iterations=100)),
        ]
        
        for config_name, aco in aco_configs:
            sol_aco, time_aco = test_solver(aco, instance, config_name)
            results.append((config_name, sol_aco.beneficio_final, time_aco))
        
        # Brute Force solo para TINY (muy lento)
        if instance_name == "TINY":
            brute = BruteForceSolver()
            sol_brute, time_brute = test_solver(brute, instance, "Brute Force (óptimo)")
            results.append(("Brute Force", sol_brute.beneficio_final, time_brute))
        
        # Resumen comparativo
        print(f"\n{'='*70}")
        print("RESUMEN COMPARATIVO")
        print('='*70)
        print(f"{'Algoritmo':<35} {'Beneficio':>15} {'Tiempo (s)':>15}")
        print('-'*70)
        
        for name, benefit, time_taken in results:
            print(f"{name:<35} {benefit:>15.2f} {time_taken:>15.4f}")
        
        # Mejor solución
        best = max(results, key=lambda x: x[1])
        print('-'*70)
        print(f"Mejor solución: {best[0]} con beneficio {best[1]:.2f}")


def test_aco_detailed():
    """Prueba detallada del ACO con INSTANCE_SMALL."""
    print("\n\n" + "="*70)
    print("PRUEBA DETALLADA: ACO en INSTANCE_SMALL")
    print("="*70)
    
    instance = INSTANCE_SMALL
    
    print(f"\nCaracterísticas de la instancia:")
    print(f"  - Puertos: {instance.tiempos.shape[0] - 1}")
    print(f"  - Mercancías: {instance.pesos.shape[0]}")
    print(f"  - Capital inicial: {instance.capital_inicial}")
    print(f"  - Capacidad bodega: {instance.capacidad_bodega}")
    print(f"  - Tiempo máximo: {instance.tiempo_maximo}")
    
    # Probar con diferentes parámetros
    configs = [
        {"n_ants": 10, "n_iterations": 50, "alpha": 1.0, "beta": 2.0, "evaporation_rate": 0.5},
        {"n_ants": 15, "n_iterations": 40, "alpha": 1.5, "beta": 2.5, "evaporation_rate": 0.3},
        {"n_ants": 20, "n_iterations": 30, "alpha": 0.8, "beta": 3.0, "evaporation_rate": 0.6},
    ]
    
    for i, config in enumerate(configs, 1):
        print(f"\n{'-'*70}")
        print(f"Configuración {i}:")
        print(f"  α={config['alpha']}, β={config['beta']}, "
              f"hormigas={config['n_ants']}, iter={config['n_iterations']}, "
              f"evap={config['evaporation_rate']}")
        
        aco = ACOSolver(**config)
        start = time.time()
        solution = aco.solve(instance)
        elapsed = time.time() - start
        
        print(f"\nResultado:")
        print(f"  - Beneficio: {solution.beneficio_final:.2f}")
        print(f"  - Tiempo: {elapsed:.4f}s")
        print(f"  - Ruta: {' -> '.join(map(str, solution.ruta))}")
        
        # Mostrar algunas operaciones de compra/venta
        print(f"\nOperaciones destacadas:")
        for idx, port in enumerate(solution.ruta[:-1]):
            compras_puerto = solution.compras[:, idx]
            ventas_puerto = solution.ventas[:, idx]
            
            if compras_puerto.sum() > 0 or ventas_puerto.sum() > 0:
                print(f"  Puerto {port}:")
                if ventas_puerto.sum() > 0:
                    print(f"    Ventas: {ventas_puerto[ventas_puerto > 0]}")
                if compras_puerto.sum() > 0:
                    print(f"    Compras: {compras_puerto[compras_puerto > 0]}")


if __name__ == "__main__":
    print("="*70)
    print("DEMO: Ant Colony Optimization (ACO) Solver para DTP")
    print("="*70)
    
    # Comparación general
    compare_solvers()
    
    # Prueba detallada
    test_aco_detailed()
    
    print("\n\n" + "="*70)
    print("DEMO COMPLETADO")
    print("="*70)
