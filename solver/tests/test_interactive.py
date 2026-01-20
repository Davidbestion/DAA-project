"""Script de comparación simple entre solvers."""

from solver.tests.test_models import (
    run_brute_tests,
    run_greedy_tests,
    run_multigreedy_tests,
    run_local_search_tests,
)


def compare_two(name1: str, results1, name2: str, results2):
    """Compara dos solvers en formato tabular."""
    print(f"\n{'═'*90}")
    print(f"COMPARATIVA: {name1} vs {name2}")
    print(f"{'═'*90}\n")

    print(
        f"{'Instancia':<18} {name1:<35} {name2:<35} {'Mejor':<10}"
    )
    print("-" * 90)

    for r1, r2 in zip(results1, results2):
        nombre = r1["nombre"]
        b1 = r1["beneficio"]
        t1 = r1["tiempo_ms"]
        v1 = "✓" if r1["viable"] else "✗"

        b2 = r2["beneficio"]
        t2 = r2["tiempo_ms"]
        v2 = "✓" if r2["viable"] else "✗"

        mejor = name1 if b1 >= b2 else name2
        if b1 == b2:
            mejor = "EMPATE"

        print(f"{nombre:<18}", end="")
        print(f"${b1:6.1f}({t1:6.1f}ms){v1} ", end="")
        print(f"${b2:6.1f}({t2:6.1f}ms){v2} ", end="")
        print(f"{mejor:<10}")

    # Totales
    print()
    t1_total = sum(r["tiempo_ms"] for r in results1)
    t2_total = sum(r["tiempo_ms"] for r in results2)
    b1_avg = sum(r["beneficio"] for r in results1) / len(results1)
    b2_avg = sum(r["beneficio"] for r in results2) / len(results2)

    print(f"Tiempo total:        {t1_total:8.2f}ms          {t2_total:8.2f}ms")
    print(f"Beneficio promedio:  ${b1_avg:8.2f}          ${b2_avg:8.2f}")

    if t1_total > 0 and t2_total > 0:
        speedup = t1_total / t2_total
        print(
            f"Speedup:             {speedup:8.1f}x (name2 es {speedup:.1f}x más rápido)"
        )

    if b1_avg > 0:
        error = abs(b1_avg - b2_avg) / b1_avg * 100
        print(f"Error relativo:      {error:8.2f}%")

    print()


if __name__ == "__main__":
    print("\n" + "="*90)
    print("COMPARADOR DE SOLVERS - Elige qué comparar:")
    print("="*90)

    print("\nCargando solvers...")
    bf = run_brute_tests()
    gr = run_greedy_tests()
    mg = run_multigreedy_tests()
    ls = run_local_search_tests()

    print(
        """
1. Brute-Force vs Greedy
2. Greedy vs MultiGreedy
3. Greedy vs Greedy+2OPT
4. MultiGreedy vs Greedy+2OPT
5. Brute-Force vs Greedy+2OPT (mejor)
6. Ver todas (4 comparativas)

Presiona Ctrl+C para salir.
    """
    )

    while True:
        try:
            opcion = input("\nElige opción (1-6): ").strip()

            if opcion == "1":
                compare_two("Brute-Force", bf, "Greedy", gr)
            elif opcion == "2":
                compare_two("Greedy", gr, "MultiGreedy", mg)
            elif opcion == "3":
                compare_two("Greedy", gr, "Greedy+2OPT", ls)
            elif opcion == "4":
                compare_two("MultiGreedy", mg, "Greedy+2OPT", ls)
            elif opcion == "5":
                compare_two("Brute-Force", bf, "Greedy+2OPT", ls)
            elif opcion == "6":
                compare_two("Brute-Force", bf, "Greedy", gr)
                compare_two("Greedy", gr, "MultiGreedy", mg)
                compare_two("Greedy", gr, "Greedy+2OPT", ls)
                compare_two("MultiGreedy", mg, "Greedy+2OPT", ls)
            else:
                print("Opción no válida.")

        except KeyboardInterrupt:
            print("\n\nSaliendo...")
            break
        except Exception as e:
            print(f"Error: {e}")
