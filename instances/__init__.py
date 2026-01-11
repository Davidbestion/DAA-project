"""Paquete de instancias predefinidas del DTP.

Este paquete contiene instancias del Problema del Comerciante Holandés
que pueden ser importadas y utilizadas para pruebas, benchmarking, etc.
"""

from .predefined import (
    INSTANCE_TINY,
    INSTANCE_SMALL,
    INSTANCE_MEDIUM,
    INSTANCE_LARGE,
    INSTANCE_KNAPSACK,
    INSTANCE_TSP,
    get_all_instances,
    get_instance_by_name,
)

__all__ = [
    "INSTANCE_TINY",
    "INSTANCE_SMALL",
    "INSTANCE_MEDIUM",
    "INSTANCE_LARGE",
    "INSTANCE_KNAPSACK",
    "INSTANCE_TSP",
    "get_all_instances",
    "get_instance_by_name",
]
