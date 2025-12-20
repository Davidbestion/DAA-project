from solver.schemas.dtp import DTPInstance, DTPSolution
from abc import ABC, abstractmethod
from typing import Iterable, Sequence

import itertools
import numpy as np


class ABCSolver(ABC):
    """Interface base para cualquier solver del Comerciante Holandés."""

    @abstractmethod
    def solve(self, instance: DTPInstance) -> DTPSolution:
        """Resuelve la instancia y devuelve una solución candidata."""
        raise NotImplementedError

    @abstractmethod
    def is_feasible(self, instance: DTPInstance, solution: DTPSolution) -> bool:
        """Verifica si la solución es factible para la instancia dada."""
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, instance: DTPInstance, solution: DTPSolution) -> float:
        """Evalúa la solución para la instancia dada y devuelve el beneficio final."""
        raise NotImplementedError

    # -------- Helpers --------
    def _port_permutations(self, n_ports: int) -> Iterable[tuple[int, ...]]:
        ports = list(range(1, n_ports + 1))
        return itertools.permutations(ports)

    def _route_time(self, instance: DTPInstance, route: Sequence[int]) -> float:
        if len(route) < 2:
            return 0.0
        arr = np.array(route, dtype=int)
        return float(np.sum(instance.tiempos[arr[:-1], arr[1:]]))
