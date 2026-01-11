from dataclasses import dataclass

from typing import Sequence, TypeAlias
from numpy.typing import NDArray

import numpy as np

MatrixFloat: TypeAlias = NDArray[np.floating]
VectorFloat: TypeAlias = NDArray[np.floating]


@dataclass(slots=True)
class DTPInstance:
    """Instancia de entrada del Comerciante Holandés.
    
    Nota importante sobre precios (perspectiva del PUERTO):
    - precios_compra: precio al que el puerto COMPRA (el comerciante VENDE al puerto)
    - precios_venta: precio al que el puerto VENDE (el comerciante COMPRA del puerto)
    
    Por lo tanto: precios_compra < precios_venta (el puerto compra barato y vende caro)
    El comerciante hace lo opuesto: compra del puerto (a precios_venta) y vende al puerto (a precios_compra)
    """

    tiempos: MatrixFloat
    costos: MatrixFloat
    precios_compra: MatrixFloat  # Precio al que el PUERTO compra (comerciante vende)
    precios_venta: MatrixFloat   # Precio al que el PUERTO vende (comerciante compra)
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

    def __str__(self) -> str:
        """Representación en string legible de la instancia."""
        lines = [
            "=" * 60,
            "INSTANCIA DEL PROBLEMA DEL COMERCIANTE HOLANDÉS (DTP)",
            "=" * 60,
            f"\n📊 DIMENSIONES:",
            f"   • Puertos (además de Ámsterdam): {self.n}",
            f"   • Mercancías: {self.m}",
            f"\n💰 RECURSOS:",
            f"   • Capital inicial: {self.capital_inicial}",
            f"   • Capital mínimo requerido: {self.capital_minimo}",
            f"   • Capacidad de bodega: {self.capacidad_bodega}",
            f"   • Tiempo máximo: {self.tiempo_maximo}",
            f"   • Umbral de beneficio: {self.umbral_beneficio}",
            f"\n📦 MERCANCÍAS (pesos):",
        ]
        
        for i, peso in enumerate(self.pesos):
            lines.append(f"   • Mercancía {i}: {peso:.2f} unidades de peso")
        
        lines.extend([
            f"\n🗺️  MATRIZ DE TIEMPOS (puertos × puertos):",
            self._format_matrix(self.tiempos, "tiempo"),
            f"\n💵 MATRIZ DE COSTOS (puertos × puertos):",
            self._format_matrix(self.costos, "costo"),
            f"\n🛒 PRECIOS DE COMPRA (mercancías × puertos):",
            self._format_matrix(self.precios_compra, "precio"),
            f"\n💲 PRECIOS DE VENTA (mercancías × puertos):",
            self._format_matrix(self.precios_venta, "precio"),
            f"\n📊 OFERTA MÁXIMA (mercancías × puertos):",
            self._format_matrix(self.oferta_max, "unidades"),
            "=" * 60,
        ])
        
        return "\n".join(lines)

    def _format_matrix(self, matrix: MatrixFloat, unit: str = "") -> str:
        """Formatea una matriz para visualización en consola."""
        rows, cols = matrix.shape
        
        # Determinar ancho de columna necesario
        max_val = np.max(np.abs(matrix))
        col_width = max(8, len(f"{max_val:.2f}"))
        
        lines = []
        
        # Encabezado con números de columna
        header = "      " + "".join(f"{j:>{col_width}}" for j in range(cols))
        lines.append(header)
        lines.append("      " + "-" * (col_width * cols))
        
        # Filas con datos
        for i in range(rows):
            row_label = f"  {i:2d} |"
            row_data = "".join(f"{matrix[i, j]:>{col_width}.2f}" for j in range(cols))
            lines.append(row_label + row_data)
        
        return "\n".join(lines)

    def display(self) -> None:
        """Imprime la instancia en consola."""
        print(self)

    def summary(self) -> str:
        """Retorna un resumen breve de la instancia."""
        return (
            f"DTPInstance({self.n} puertos, {self.m} mercancías, "
            f"capital={self.capital_inicial}, tiempo_max={self.tiempo_maximo})"
        )


@dataclass(slots=True)
class DTPSolution:
    """Solución candidata al problema de decisión u optimización."""

    ruta: Sequence[int]
    compras: MatrixFloat
    ventas: MatrixFloat
    beneficio_final: float

    def __str__(self) -> str:
        """Representación en string legible de la solución."""
        lines = [
            "=" * 60,
            "SOLUCIÓN DEL PROBLEMA DEL COMERCIANTE HOLANDÉS",
            "=" * 60,
            f"\n🗺️  RUTA:",
            f"   {' → '.join(map(str, self.ruta))}",
            f"\n💰 BENEFICIO FINAL: {self.beneficio_final:.2f}",
            f"\n🛒 COMPRAS (mercancías × pasos en ruta):",
            self._format_matrix(self.compras),
            f"\n💲 VENTAS (mercancías × pasos en ruta):",
            self._format_matrix(self.ventas),
            "=" * 60,
        ]
        return "\n".join(lines)

    def _format_matrix(self, matrix: MatrixFloat) -> str:
        """Formatea una matriz para visualización en consola."""
        rows, cols = matrix.shape
        
        max_val = np.max(np.abs(matrix))
        col_width = max(8, len(f"{max_val:.2f}"))
        
        lines = []
        
        # Encabezado
        header = "      " + "".join(f"{j:>{col_width}}" for j in range(cols))
        lines.append(header)
        lines.append("      " + "-" * (col_width * cols))
        
        # Filas
        for i in range(rows):
            row_label = f"  {i:2d} |"
            row_data = "".join(f"{matrix[i, j]:>{col_width}.2f}" for j in range(cols))
            lines.append(row_label + row_data)
        
        return "\n".join(lines)

    def display(self) -> None:
        """Imprime la solución en consola."""
        print(self)

    def summary(self) -> str:
        """Retorna un resumen breve de la solución."""
        ruta_str = " → ".join(map(str, self.ruta))
        return f"DTPSolution(ruta={ruta_str}, beneficio={self.beneficio_final:.2f})"
