from solver.models.brute import BruteForceSolver
from instances.predefined import INSTANCE_TINY


def test_bruteforce_progress_callback():
    events = []

    def cb(ev: dict):
        # Simple collector for progress events
        events.append(ev)

    # progress_interval=1 to get frequent events on the tiny instance
    bf = BruteForceSolver(progress_callback=cb, progress_interval=1)

    sol = bf.solve(INSTANCE_TINY)

    # Basic sanity checks
    assert sol is not None
    assert bf.is_feasible(INSTANCE_TINY, sol)

    # We should have seen at least one route_progress and one dfs_progress
    has_route = any(e.get("event") == "route_progress" for e in events)
    has_dfs = any(e.get("event") == "dfs_progress" for e in events)

    assert has_route, "No route_progress events were emitted"
    assert has_dfs, "No dfs_progress events were emitted"

    # The best_benefit reported during progress should not exceed final benefit
    route_benefits = [
        e.get("best_benefit")
        for e in events
        if e.get("event") == "route_progress" and e.get("best_benefit") is not None
    ]
    if route_benefits:
        max_reported = max(route_benefits)
        # final benefit must be at least the best reported so far
        assert sol.beneficio_final + 1e-9 >= max_reported

    # visited nodes should be positive in dfs progress
    dfs_nodes = [
        e.get("visited_nodes")
        for e in events
        if e.get("event") == "dfs_progress" and e.get("visited_nodes") is not None
    ]
    if dfs_nodes:
        assert max(dfs_nodes) > 0
