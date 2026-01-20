"""Instancias MICRO para demostración teórica de brute-force puro.

Estas instancias son lo suficientemente pequeñas para que el brute-force
exhaustivo termine en segundos, permitiendo demostración formal de:
- Complejidad teórica
- Optimalidad garantizada
- Comparación con heurísticas (greedy, etc.)
"""

import numpy as np
from solver.schemas.dtp import DTPInstance


# MICRO-1: Mínimo viable (2 puertos, 1 bien)
# - Rutas: 2! = 2 permutaciones
# - Por ruta: 3 pasos (Ámsterdam -> Puerto -> Ámsterdam)
# - Por paso: máximo ~5 ventas × 5 compras = 25 nodos
# - Total: 2 × 3 × 25 ≈ 150 nodos DFS
# - Tiempo: < 1ms ✓
INSTANCE_MICRO_1 = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 20.0, 15.0],
            [25.0, 0.0, 10.0],
            [18.0, 12.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 30.0, 25.0],
            [35.0, 0.0, 20.0],
            [28.0, 22.0, 0.0],
        ]
    ),
    precios_compra=np.array(
        [
            [20.0, 25.0, 22.0],  # Mercancía 0
        ]
    ),
    precios_venta=np.array(
        [
            [25.0, 30.0, 27.0],  # Mercancía 0
        ]
    ),
    oferta_max=np.array(
        [
            [3.0, 3.0, 3.0],  # Mercancía 0 (máximo 3 unidades)
        ]
    ),
    pesos=np.array([1.0]),
    capacidad_bodega=10,
    capital_inicial=200,
    tiempo_maximo=100,
    umbral_beneficio=50.0,
    capital_minimo=50.0,
)

# MICRO-2: Dos mercancías pequeñas (2 puertos, 2 bienes)
# - Rutas: 2! = 2 permutaciones
# - Por ruta: 3 pasos
# - Por paso: ~2 ventas × 2 compras = 4 nodos
# - Total: 2 × 3 × 4 ≈ 24 nodos
# - Tiempo: < 5ms ✓
INSTANCE_MICRO_2 = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 20.0, 15.0],
            [25.0, 0.0, 10.0],
            [18.0, 12.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 30.0, 25.0],
            [35.0, 0.0, 20.0],
            [28.0, 22.0, 0.0],
        ]
    ),
    precios_compra=np.array(
        [
            [20.0, 25.0, 22.0],  # Mercancía 0
            [30.0, 35.0, 32.0],  # Mercancía 1
        ]
    ),
    precios_venta=np.array(
        [
            [25.0, 30.0, 27.0],  # Mercancía 0
            [38.0, 45.0, 40.0],  # Mercancía 1
        ]
    ),
    oferta_max=np.array(
        [
            [1.0, 1.0, 1.0],  # Mercancía 0 (máximo 1 unidad)
            [1.0, 1.0, 1.0],  # Mercancía 1 (máximo 1 unidad)
        ]
    ),
    pesos=np.array([1.0, 1.5]),
    capacidad_bodega=5,
    capital_inicial=300,
    tiempo_maximo=100,
    umbral_beneficio=100.0,
    capital_minimo=50.0,
)

# MICRO-3: Tres puertos, 1 bien (demostra crecimiento factorial en rutas)
# - Rutas: 3! = 6 permutaciones
# - Por ruta: 4 pasos
# - Por paso: ~4 ventas × 4 compras = 16 nodos
# - Total: 6 × 4 × 16 ≈ 384 nodos
# - Tiempo: < 10ms ✓
INSTANCE_MICRO_3 = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 20.0, 25.0, 30.0],
            [22.0, 0.0, 15.0, 20.0],
            [28.0, 18.0, 0.0, 12.0],
            [32.0, 22.0, 14.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 50.0, 60.0, 70.0],
            [55.0, 0.0, 40.0, 50.0],
            [65.0, 45.0, 0.0, 35.0],
            [75.0, 55.0, 40.0, 0.0],
        ]
    ),
    precios_compra=np.array(
        [
            [20.0, 22.0, 18.0, 24.0],  # Mercancía 0
        ]
    ),
    precios_venta=np.array(
        [
            [25.0, 28.0, 23.0, 30.0],  # Mercancía 0
        ]
    ),
    oferta_max=np.array(
        [
            [1.0, 1.0, 1.0, 1.0],  # Mercancía 0 (máximo 1 unidad)
        ]
    ),
    pesos=np.array([1.0]),
    capacidad_bodega=10,
    capital_inicial=300,
    tiempo_maximo=150,
    umbral_beneficio=100.0,
    capital_minimo=50.0,
)

# MICRO-4: Dos puertos, dos bienes pequeños (caso de referencia para análisis)
# Este es el que mejor demuestra la complejidad teórica
# - Rutas: 2! = 2
# - Por ruta: 3 pasos
# - Por paso: ~3 ventas × 3 compras = 9 nodos
# - Total: 2 × 3 × 9 ≈ 54 nodos
# - Tiempo: < 1ms ✓
INSTANCE_MICRO_4 = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 20.0, 15.0],
            [25.0, 0.0, 10.0],
            [18.0, 12.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 30.0, 25.0],
            [35.0, 0.0, 20.0],
            [28.0, 22.0, 0.0],
        ]
    ),
    precios_compra=np.array(
        [
            [15.0, 18.0, 16.0],  # Mercancía 0
            [25.0, 28.0, 26.0],  # Mercancía 1
        ]
    ),
    precios_venta=np.array(
        [
            [20.0, 25.0, 22.0],  # Mercancía 0
            [35.0, 40.0, 37.0],  # Mercancía 1
        ]
    ),
    oferta_max=np.array(
        [
            [1.0, 1.0, 1.0],  # Mercancía 0 (máximo 1 unidad)
            [1.0, 1.0, 1.0],  # Mercancía 1 (máximo 1 unidad)
        ]
    ),
    pesos=np.array([0.8, 1.2]),
    capacidad_bodega=4,
    capital_inicial=250,
    tiempo_maximo=100,
    umbral_beneficio=80.0,
    capital_minimo=50.0,
)
