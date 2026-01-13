"""Instancias predefinidas del DTP para pruebas y benchmarking.

IMPORTANTE: Precios desde el punto de vista del PUERTO:
- precios_compra: precio al que el puerto COMPRA del comerciante (el comerciante VENDE)
- precios_venta: precio al que el puerto VENDE al comerciante (el comerciante COMPRA)
- Siempre: precios_compra < precios_venta (el puerto compra barato, vende caro)
"""

import numpy as np
from solver.schemas.dtp import DTPInstance


# Instancia muy pequeña (2 puertos, 2 mercancías) - Para pruebas rápidas
INSTANCE_TINY = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 20.0, 30.0],
            [25.0, 0.0, 15.0],
            [35.0, 18.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 30.0, 50.0],
            [35.0, 0.0, 25.0],
            [45.0, 28.0, 0.0],
        ]
    ),
    precios_compra=np.array(  # Lo que el puerto PAGA al comerciante
        [
            [25.0, 30.0, 20.0],  # Mercancía 0
            [35.0, 30.0, 40.0],  # Mercancía 1
        ]
    ),
    precios_venta=np.array(  # Lo que el puerto COBRA al comerciante
        [
            [30.0, 55.0, 25.0],  # Mercancía 0 (mayor variación entre puertos)
            [45.0, 65.0, 50.0],  # Mercancía 1 (mayor variación entre puertos)
        ]
    ),
    oferta_max=np.array(
        [
            [5.0, 4.0, 6.0],  # Mercancía 0
            [4.0, 5.0, 4.0],  # Mercancía 1
        ]
    ),
    pesos=np.array([2.0, 3.0]),
    capacidad_bodega=40,
    capital_inicial=500,
    tiempo_maximo=100,
    umbral_beneficio=200.0,
    capital_minimo=100.0,
)


# Instancia pequeña (4 puertos, 2 mercancías)
INSTANCE_SMALL = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 25.0, 40.0, 35.0],
            [30.0, 0.0, 20.0, 25.0],
            [45.0, 22.0, 0.0, 18.0],
            [38.0, 28.0, 20.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 150.0, 220.0, 200.0],
            [160.0, 0.0, 120.0, 140.0],
            [230.0, 130.0, 0.0, 100.0],
            [210.0, 150.0, 110.0, 0.0],
        ]
    ),
    precios_compra=np.array(  # Lo que el puerto PAGA al comerciante
        [
            [20.0, 22.0, 18.0, 24.0],  # Mercancía 0
            [45.0, 40.0, 42.0, 43.0],  # Mercancía 1
        ]
    ),
    precios_venta=np.array(  # Lo que el puerto COBRA al comerciante
        [
            [30.0, 35.0, 28.0, 32.0],  # Mercancía 0 (siempre > precios_compra)
            [60.0, 55.0, 58.0, 62.0],  # Mercancía 1 (siempre > precios_compra)
        ]
    ),
    oferta_max=np.array(
        [
            [30.0, 25.0, 35.0, 28.0],  # Mercancía 0
            [20.0, 25.0, 22.0, 30.0],  # Mercancía 1
        ]
    ),
    pesos=np.array([2.5, 4.0]),
    capacidad_bodega=60,
    capital_inicial=1000,
    tiempo_maximo=180,
    umbral_beneficio=500.0,
    capital_minimo=200.0,
)


# Instancia mediana (6 puertos, 3 mercancías)
INSTANCE_MEDIUM = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 30.0, 45.0, 50.0, 40.0, 55.0],
            [35.0, 0.0, 25.0, 30.0, 28.0, 38.0],
            [48.0, 28.0, 0.0, 20.0, 35.0, 42.0],
            [52.0, 32.0, 22.0, 0.0, 25.0, 30.0],
            [42.0, 30.0, 38.0, 28.0, 0.0, 20.0],
            [58.0, 40.0, 45.0, 32.0, 22.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 200.0, 280.0, 320.0, 250.0, 350.0],
            [220.0, 0.0, 150.0, 180.0, 170.0, 240.0],
            [300.0, 160.0, 0.0, 120.0, 210.0, 270.0],
            [330.0, 190.0, 130.0, 0.0, 150.0, 190.0],
            [260.0, 180.0, 220.0, 160.0, 0.0, 120.0],
            [360.0, 250.0, 280.0, 200.0, 130.0, 0.0],
        ]
    ),
    precios_compra=np.array(  # Lo que el puerto PAGA al comerciante
        [
            [25.0, 28.0, 22.0, 27.0, 30.0, 20.0],  # Mercancía 0
            [50.0, 48.0, 52.0, 49.0, 47.0, 53.0],  # Mercancía 1
            [70.0, 72.0, 68.0, 71.0, 69.0, 74.0],  # Mercancía 2
        ]
    ),
    precios_venta=np.array(  # Lo que el puerto COBRA al comerciante
        [
            [35.0, 40.0, 32.0, 38.0, 42.0, 30.0],  # Mercancía 0 (siempre > precios_compra)
            [65.0, 62.0, 68.0, 64.0, 60.0, 70.0],  # Mercancía 1 (siempre > precios_compra)
            [85.0, 88.0, 82.0, 86.0, 84.0, 92.0],  # Mercancía 2 (siempre > precios_compra)
        ]
    ),
    oferta_max=np.array(
        [
            [40.0, 35.0, 45.0, 38.0, 42.0, 50.0],  # Mercancía 0
            [30.0, 35.0, 28.0, 32.0, 38.0, 30.0],  # Mercancía 1
            [25.0, 30.0, 22.0, 28.0, 25.0, 35.0],  # Mercancía 2
        ]
    ),
    pesos=np.array([2.0, 3.5, 5.0]),
    capacidad_bodega=120,
    capital_inicial=3000,
    tiempo_maximo=300,
    umbral_beneficio=1000.0,
    capital_minimo=500.0,
)


# Instancia grande (8 puertos, 4 mercancías)
INSTANCE_LARGE = DTPInstance(
    tiempos=np.array(
        [
            [0.0, 35.0, 50.0, 45.0, 60.0, 55.0, 65.0, 70.0],
            [40.0, 0.0, 28.0, 32.0, 42.0, 38.0, 48.0, 52.0],
            [55.0, 30.0, 0.0, 25.0, 35.0, 40.0, 45.0, 50.0],
            [48.0, 35.0, 28.0, 0.0, 30.0, 35.0, 40.0, 45.0],
            [62.0, 45.0, 38.0, 32.0, 0.0, 25.0, 30.0, 35.0],
            [58.0, 40.0, 42.0, 38.0, 28.0, 0.0, 22.0, 28.0],
            [68.0, 50.0, 48.0, 42.0, 32.0, 25.0, 0.0, 20.0],
            [72.0, 55.0, 52.0, 48.0, 38.0, 30.0, 22.0, 0.0],
        ]
    ),
    costos=np.array(
        [
            [0.0, 250.0, 350.0, 320.0, 420.0, 380.0, 450.0, 480.0],
            [270.0, 0.0, 200.0, 230.0, 300.0, 270.0, 340.0, 370.0],
            [380.0, 220.0, 0.0, 180.0, 250.0, 290.0, 320.0, 360.0],
            [340.0, 250.0, 190.0, 0.0, 220.0, 260.0, 290.0, 330.0],
            [440.0, 320.0, 270.0, 240.0, 0.0, 180.0, 210.0, 250.0],
            [400.0, 290.0, 300.0, 270.0, 200.0, 0.0, 160.0, 200.0],
            [470.0, 360.0, 340.0, 310.0, 230.0, 180.0, 0.0, 150.0],
            [500.0, 390.0, 370.0, 350.0, 270.0, 220.0, 170.0, 0.0],
        ]
    ),
    precios_compra=np.array(  # Lo que el puerto PAGA al comerciante
        [
            [30.0, 32.0, 28.0, 33.0, 35.0, 26.0, 38.0, 31.0],  # Mercancía 0
            [55.0, 52.0, 58.0, 54.0, 50.0, 60.0, 48.0, 56.0],  # Mercancía 1
            [80.0, 82.0, 78.0, 83.0, 81.0, 85.0, 76.0, 84.0],  # Mercancía 2
            [105.0, 102.0, 108.0, 104.0, 106.0, 100.0, 110.0, 103.0],  # Mercancía 3
        ]
    ),
    precios_venta=np.array(  # Lo que el puerto COBRA al comerciante
        [
            [42.0, 45.0, 38.0, 46.0, 48.0, 36.0, 52.0, 43.0],  # Mercancía 0 (siempre > precios_compra)
            [70.0, 68.0, 75.0, 71.0, 65.0, 78.0, 62.0, 72.0],  # Mercancía 1 (siempre > precios_compra)
            [95.0, 98.0, 92.0, 99.0, 96.0, 102.0, 90.0, 100.0],  # Mercancía 2 (siempre > precios_compra)
            [125.0, 122.0, 130.0, 126.0, 128.0, 118.0, 135.0, 124.0],  # Mercancía 3 (siempre > precios_compra)
        ]
    ),
    oferta_max=np.array(
        [
            [50.0, 45.0, 55.0, 48.0, 52.0, 60.0, 42.0, 58.0],  # Mercancía 0
            [35.0, 40.0, 32.0, 38.0, 42.0, 35.0, 45.0, 38.0],  # Mercancía 1
            [30.0, 35.0, 28.0, 32.0, 30.0, 40.0, 28.0, 35.0],  # Mercancía 2
            [25.0, 30.0, 22.0, 28.0, 26.0, 35.0, 24.0, 30.0],  # Mercancía 3
        ]
    ),
    pesos=np.array([2.0, 3.0, 4.5, 6.0]),
    capacidad_bodega=180,
    capital_inicial=5000,
    tiempo_maximo=450,
    umbral_beneficio=1500.0,
    capital_minimo=800.0,
)


# Diccionario de todas las instancias
_INSTANCES = {
    "tiny": INSTANCE_TINY,
    "small": INSTANCE_SMALL,
    "medium": INSTANCE_MEDIUM,
    "large": INSTANCE_LARGE,
}


# ============================================================
# INSTANCIAS ESPECIALES PARA CASOS EXTREMOS
# ============================================================

# Instancia tipo KNAPSACK (2 puertos, muchos productos)
# El problema se reduce a decidir qué productos comprar/transportar
# dadas las restricciones de peso y capital
INSTANCE_KNAPSACK = DTPInstance(
    tiempos=np.array([
        [0.0, 15.0],
        [15.0, 0.0],
    ]),
    costos=np.array([
        [0.0, 20.0],
        [20.0, 0.0],
    ]),
    # 8 mercancías con diferentes pesos y márgenes de ganancia
    precios_compra=np.array([  # Lo que el puerto PAGA al comerciante
        [15.0, 45.0],  # Mercancía 0: buen margen
        [25.0, 60.0],  # Mercancía 1: buen margen
        [10.0, 35.0],  # Mercancía 2: buen margen
        [30.0, 70.0],  # Mercancía 3: buen margen
        [20.0, 50.0],  # Mercancía 4: buen margen
        [12.0, 38.0],  # Mercancía 5: buen margen
        [18.0, 55.0],  # Mercancía 6: muy buen margen
        [22.0, 48.0],  # Mercancía 7: buen margen
    ]),
    precios_venta=np.array([  # Lo que el puerto COBRA al comerciante
        [20.0, 50.0],   # Mercancía 0
        [30.0, 65.0],   # Mercancía 1
        [15.0, 40.0],   # Mercancía 2
        [35.0, 75.0],   # Mercancía 3
        [25.0, 55.0],   # Mercancía 4
        [17.0, 43.0],   # Mercancía 5
        [23.0, 60.0],   # Mercancía 6
        [27.0, 53.0],   # Mercancía 7
    ]),
    oferta_max=np.array([
        [20.0, 20.0],  # Mercancía 0
        [15.0, 15.0],  # Mercancía 1
        [25.0, 25.0],  # Mercancía 2
        [12.0, 12.0],  # Mercancía 3
        [18.0, 18.0],  # Mercancía 4
        [22.0, 22.0],  # Mercancía 5
        [16.0, 16.0],  # Mercancía 6
        [20.0, 20.0],  # Mercancía 7
    ]),
    pesos=np.array([2.0, 3.5, 1.5, 5.0, 2.5, 1.8, 4.0, 3.0]),  # Pesos variados
    capacidad_bodega=50,  # Capacidad limitada - clave del problema tipo knapsack
    capital_inicial=10000,
    tiempo_maximo=100,
    umbral_beneficio=100.0,
    capital_minimo=0.0,
)


# Instancia tipo VIAJANTE (TSP) - (6 puertos, 1 mercancía)
# Solo hay 1 mercancía disponible en cantidad 1 en cada puerto
# Los precios de venta son muy bajos excepto en el puerto 0
# Esto obliga al problema a enfocarse en encontrar la ruta óptima (minimizar costos)
INSTANCE_TSP = DTPInstance(
    tiempos=np.array([
        [0.0, 25.0, 45.0, 35.0, 50.0, 40.0],
        [30.0, 0.0, 20.0, 28.0, 35.0, 32.0],
        [48.0, 22.0, 0.0, 18.0, 30.0, 25.0],
        [38.0, 30.0, 20.0, 0.0, 22.0, 28.0],
        [52.0, 38.0, 32.0, 25.0, 0.0, 18.0],
        [42.0, 35.0, 28.0, 30.0, 20.0, 0.0],
    ]),
    costos=np.array([
        [0.0, 180.0, 280.0, 220.0, 320.0, 260.0],
        [200.0, 0.0, 140.0, 180.0, 240.0, 210.0],
        [300.0, 150.0, 0.0, 120.0, 200.0, 170.0],
        [240.0, 190.0, 130.0, 0.0, 150.0, 180.0],
        [340.0, 250.0, 210.0, 160.0, 0.0, 120.0],
        [280.0, 220.0, 180.0, 190.0, 130.0, 0.0],
    ]),
    # Solo 1 mercancía
    precios_compra=np.array([  # Lo que el puerto PAGA al comerciante
        [80.0, 5.0, 5.0, 5.0, 5.0, 5.0],  # Solo en puerto 0 paga bien
    ]),
    precios_venta=np.array([  # Lo que el puerto COBRA al comerciante
        [100.0, 10.0, 10.0, 10.0, 10.0, 10.0],  # Solo en puerto 0 vale la pena vender
    ]),
    oferta_max=np.array([
        [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],  # Solo 1 unidad disponible en cada puerto
    ]),
    pesos=np.array([1.0]),  # Peso mínimo
    capacidad_bodega=5,  # Puede llevar todas las mercancías disponibles
    capital_inicial=2000,  # Capital alto para no ser restricción
    tiempo_maximo=300,
    umbral_beneficio=0.0,
    capital_minimo=0.0,
)


# Diccionario de todas las instancias
_INSTANCES = {
    "tiny": INSTANCE_TINY,
    "small": INSTANCE_SMALL,
    "medium": INSTANCE_MEDIUM,
    "large": INSTANCE_LARGE,
    "knapsack": INSTANCE_KNAPSACK,
    "tsp": INSTANCE_TSP,
}


def get_all_instances() -> dict[str, DTPInstance]:
    """Retorna un diccionario con todas las instancias predefinidas.

    Returns:
        Diccionario con nombre -> instancia.
    """
    return _INSTANCES.copy()


def get_instance_by_name(name: str) -> DTPInstance:
    """Obtiene una instancia por su nombre.

    Args:
        name: Nombre de la instancia ('tiny', 'small', 'medium', 'large', 'knapsack', 'tsp').

    Returns:
        La instancia solicitada.

    Raises:
        KeyError: Si el nombre no corresponde a ninguna instancia.
    """
    if name not in _INSTANCES:
        available = ", ".join(_INSTANCES.keys())
        raise KeyError(
            f"Instancia '{name}' no encontrada. Disponibles: {available}"
        )
    return _INSTANCES[name]


