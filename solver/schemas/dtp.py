from dataclasses import dataclass

from typing import Sequence, TypeAlias
from numpy.typing import NDArray

import numpy as np

MatrixFloat: TypeAlias = NDArray[np.floating]
VectorFloat: TypeAlias = NDArray[np.floating]


@dataclass(slots=True)
class DTPInstance:
    """Instancia de entrada del Comerciante Holandés."""

    tiempos: MatrixFloat
    costos: MatrixFloat
    precios_compra: MatrixFloat
    precios_venta: MatrixFloat
    oferta_max: MatrixFloat

    pesos: VectorFloat

    capacidad_bodega: int
    capital_inicial: int
    tiempo_maximo: int

    umbral_beneficio: float
    capital_minimo: float

    @property
    def n(self) -> int:
        """Número de puertos distintos de Ámsterdam."""
        return self.tiempos.shape[0] - 1

    @property
    def m(self) -> int:
        """Número de mercancías."""
        return self.pesos.shape[0]


@dataclass(slots=True)
class DTPSolution:
    """Solución candidata al problema de decisión u optimización."""

    ruta: Sequence[int]
    compras: MatrixFloat
    ventas: MatrixFloat
    beneficio_final: float
