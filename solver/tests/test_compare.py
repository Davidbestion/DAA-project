"""Test de comparación: Todos los solvers disponibles."""

from .test_models import (
    run_brute_tests,
    run_greedy_tests,
    run_multigreedy_tests,
    run_local_search_tests,
    run_aco_tests,
    run_ga_beam_tests,
)


def test_compare():
    """Ejecuta todos los solvers y retorna resultados para comparación."""
    brute_results = run_brute_tests()
    greedy_results = run_greedy_tests()
    multigreedy_results = run_multigreedy_tests()
    local_search_results = run_local_search_tests()
    aco_results = run_aco_tests()
    ga_beam_results = run_ga_beam_tests()

    return (
        brute_results,
        greedy_results,
        multigreedy_results,
        local_search_results,
        aco_results,
        ga_beam_results,
    )


def display_comparison():
    """Ejecuta todos los solvers y muestra comparativa detallada."""
    print("=" * 180)
    print("COMPARATIVA: TODOS LOS SOLVERS")
    print("=" * 180)
    print()

    # Ejecutar tests
    (
        brute_results,
        greedy_results,
        multigreedy_results,
        local_search_results,
        aco_results,
        ga_beam_results,
    ) = test_compare()

    # Mostrar resultados detallados por instancia
    print(
        f"{'Instancia':<18} {'Brute-Force':<18} {'Greedy':<18} "
        f"{'MultiGreedy':<18} {'Greedy+2OPT':<18} {'ACO':<18} {'GA+Beam':<18}"
    )
    print("-" * 180)

    for bf, gr, mg, ls, aco, ga_b in zip(
        brute_results,
        greedy_results,
        multigreedy_results,
        local_search_results,
        aco_results,
        ga_beam_results,
    ):
        nombre = bf["nombre"]

        bf_benefit = bf["beneficio"]
        bf_time = bf["tiempo_ms"]

        gr_benefit = gr["beneficio"]
        gr_time = gr["tiempo_ms"]

        mg_benefit = mg["beneficio"]
        mg_time = mg["tiempo_ms"]

        ls_benefit = ls["beneficio"]
        ls_time = ls["tiempo_ms"]

        aco_benefit = aco["beneficio"]
        aco_time = aco["tiempo_ms"]

        ga_b_benefit = ga_b["beneficio"]
        ga_b_time = ga_b["tiempo_ms"]

        print(f"{nombre:<18}", end="")
        print(
            f"${bf_benefit:6.1f}({bf_time:6.1f}ms) "
            f"${gr_benefit:6.1f}({gr_time:6.1f}ms) "
            f"${mg_benefit:6.1f}({mg_time:6.1f}ms) "
            f"${ls_benefit:6.1f}({ls_time:6.1f}ms) "
            f"${aco_benefit:6.1f}({aco_time:6.1f}ms) "
            f"${ga_b_benefit:6.1f}({ga_b_time:6.1f}ms)"
        )

    print()
    print("=" * 180)
    print("MÉTRICAS CONSOLIDADAS")
    print("=" * 180)
    print()

    # Calcular totales y promedios
    bf_total_time = sum(r["tiempo_ms"] for r in brute_results)
    gr_total_time = sum(r["tiempo_ms"] for r in greedy_results)
    mg_total_time = sum(r["tiempo_ms"] for r in multigreedy_results)
    ls_total_time = sum(r["tiempo_ms"] for r in local_search_results)
    aco_total_time = sum(r["tiempo_ms"] for r in aco_results)
    ga_b_total_time = sum(r["tiempo_ms"] for r in ga_beam_results)

    bf_avg_benefit = sum(r["beneficio"] for r in brute_results) / len(brute_results)
    gr_avg_benefit = sum(r["beneficio"] for r in greedy_results) / len(greedy_results)
    mg_avg_benefit = (
        sum(r["beneficio"] for r in multigreedy_results) / len(multigreedy_results)
    )
    ls_avg_benefit = (
        sum(r["beneficio"] for r in local_search_results) / len(local_search_results)
    )
    aco_avg_benefit = sum(r["beneficio"] for r in aco_results) / len(aco_results)
    ga_b_avg_benefit = (
        sum(r["beneficio"] for r in ga_beam_results) / len(ga_beam_results)
    )

    print("TIEMPO DE EJECUCIÓN:")
    print(f"  Brute-Force:       {bf_total_time:8.2f}ms")
    print(
        f"  Greedy:            {gr_total_time:8.2f}ms (speedup: {bf_total_time / gr_total_time:8.1f}x)"
    )
    print(
        f"  MultiGreedy:       {mg_total_time:8.2f}ms (speedup: {bf_total_time / mg_total_time:8.1f}x)"
    )
    print(
        f"  Greedy+2OPT:       {ls_total_time:8.2f}ms (speedup: {bf_total_time / ls_total_time:8.1f}x)"
    )
    print(f"  ACO:               {aco_total_time:8.2f}ms (speedup: {bf_total_time / aco_total_time:8.1f}x)")
    print(f"  GA+Beam:           {ga_b_total_time:8.2f}ms (speedup: {bf_total_time / ga_b_total_time:8.1f}x)")
    print()

    print("BENEFICIO PROMEDIO:")
    print(f"  Brute-Force:       ${bf_avg_benefit:8.2f}")
    print(
        f"  Greedy:            ${gr_avg_benefit:8.2f} (error: {(1 - gr_avg_benefit / bf_avg_benefit) * 100:5.2f}%)"
    )
    print(
        f"  MultiGreedy:       ${mg_avg_benefit:8.2f} (error: {(1 - mg_avg_benefit / bf_avg_benefit) * 100:5.2f}%)"
    )
    print(
        f"  Greedy+2OPT:       ${ls_avg_benefit:8.2f} (error: {(1 - ls_avg_benefit / bf_avg_benefit) * 100:5.2f}%)"
    )
    print(f"  ACO:               ${aco_avg_benefit:8.2f} (error: {(1 - aco_avg_benefit / bf_avg_benefit) * 100:5.2f}%)")
    print(f"  GA+Beam:           ${ga_b_avg_benefit:8.2f} (error: {(1 - ga_b_avg_benefit / bf_avg_benefit) * 100:5.2f}%)")
    print()

    # Análisis de mejora respecto a greedy
    print("MEJORA RESPECTO A GREEDY:")
    mg_improvement = (mg_avg_benefit - gr_avg_benefit) / gr_avg_benefit * 100
    ls_improvement = (ls_avg_benefit - gr_avg_benefit) / gr_avg_benefit * 100
    aco_improvement = (aco_avg_benefit - gr_avg_benefit) / gr_avg_benefit * 100
    ga_b_improvement = (ga_b_avg_benefit - gr_avg_benefit) / gr_avg_benefit * 100
    print(f"  MultiGreedy:       +{mg_improvement:5.2f}%")
    print(f"  Greedy+2OPT:       +{ls_improvement:5.2f}%")
    print(f"  ACO:               +{aco_improvement:5.2f}%")
    print(f"  GA+Beam:           +{ga_b_improvement:5.2f}%")
    print()


if __name__ == "__main__":
    display_comparison()
