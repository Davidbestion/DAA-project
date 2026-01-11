"""Generador aleatorio de instancias del Problema del Comerciante Holandés (DTP)."""

import numpy as np
from solver.schemas.dtp import DTPInstance
# from .solver.schemas.dtp import DTPInstance


class RandomDTPGenerator:
    """Genera instancias aleatorias del DTP con parámetros configurables."""

    def __init__(self, seed: int | None = None):
        """Inicializa el generador.

        Args:
            seed: Semilla para reproducibilidad. Si es None, usa una semilla aleatoria.
        """
        self.rng = np.random.default_rng(seed)

    def generate(
        self,
        n_ports: int = 5,
        n_goods: int = 3,
        time_range: tuple[float, float] = (10.0, 100.0),
        cost_range: tuple[float, float] = (50.0, 500.0),
        buy_price_range: tuple[float, float] = (10.0, 100.0),
        sell_price_range: tuple[float, float] = (15.0, 150.0),
        max_offer_range: tuple[int, int] = (10, 50),
        weight_range: tuple[float, float] = (1.0, 10.0),
        cargo_capacity_range: tuple[int, int] = (50, 200),
        initial_capital_range: tuple[int, int] = (1000, 5000),
        max_time_range: tuple[float, float] = (200.0, 500.0),
        profit_threshold_range: tuple[float, float] = (500.0, 2000.0),
        min_capital_range: tuple[float, float] = (0.0, 500.0),
    ) -> DTPInstance:
        """Genera una instancia aleatoria del DTP.

        Args:
            n_ports: Número de puertos además de Ámsterdam (puerto 0).
            n_goods: Número de mercancías diferentes.
            time_range: Rango (min, max) para tiempos de viaje entre puertos.
            cost_range: Rango (min, max) para costos de viaje entre puertos.
            buy_price_range: Rango (min, max) para precios de compra de mercancías.
            sell_price_range: Rango (min, max) para precios de venta de mercancías.
            max_offer_range: Rango (min, max) para oferta máxima de mercancías.
            weight_range: Rango (min, max) para pesos de mercancías.
            warehouse_capacity_range: Rango (min, max) para capacidad de bodega.
            initial_capital_range: Rango (min, max) para capital inicial.
            max_time_range: Rango (min, max) para tiempo máximo del viaje.
            profit_threshold_range: Rango (min, max) para umbral de beneficio.
            min_capital_range: Rango (min, max) para capital mínimo requerido.

        Returns:
            Una instancia aleatoria del DTP.
        """
        total_ports = n_ports + 1  # +1 para incluir Ámsterdam (puerto 0)

        # Generar matrices de tiempo y costo (asimétricas, con diagonal 0)
        tiempos = self._generate_matrix(
            total_ports, time_range[0], time_range[1]
        )
        costos = self._generate_matrix(
            total_ports, cost_range[0], cost_range[1]
        )

        # Generar matrices de precios de compra y venta (mercancías x puertos)
        # IMPORTANTE: Desde el punto de vista del PUERTO:
        # - precios_compra: precio al que el puerto COMPRA del comerciante
        # - precios_venta: precio al que el puerto VENDE al comerciante
        # Para que haya oportunidades de negocio: precios_compra < precios_venta
        
        # Generar precios de compra del puerto (lo que paga al comerciante)
        precios_compra = self.rng.uniform(
            buy_price_range[0], buy_price_range[1], size=(n_goods, total_ports)
        )
        
        # Precios de venta del puerto deben ser mayores (lo que cobra al comerciante)
        # Agregar un margen positivo para asegurar precios_venta > precios_compra
        margen = self.rng.uniform(
            (sell_price_range[0] - buy_price_range[0]) * 0.5,
            sell_price_range[1] - buy_price_range[1],
            size=(n_goods, total_ports),
        )
        precios_venta = precios_compra + np.abs(margen)
        # Asegurar al menos 10% más para que siempre haya margen
        precios_venta = np.maximum(precios_venta, precios_compra * 1.1)

        # Generar oferta máxima por mercancía y puerto
        oferta_max = self.rng.integers(
            max_offer_range[0], max_offer_range[1] + 1, size=(n_goods, total_ports)
        ).astype(float)

        # Generar pesos de mercancías
        # TODO: Revisar si es mejor entero o float
        pesos = self.rng.uniform(weight_range[0], weight_range[1], size=n_goods)
        # entero
        # pesos = self.rng.integers(int(weight_range[0]), int(weight_range[1]) + 1, size=n_goods)

        # Generar parámetros escalares
        capacidad_bodega = int(self.rng.integers(
            cargo_capacity_range[0], cargo_capacity_range[1] + 1
        ))
        capital_inicial = int(self.rng.integers(
            initial_capital_range[0], initial_capital_range[1] + 1
        ))
        tiempo_maximo = int(self.rng.uniform(max_time_range[0], max_time_range[1]))
        umbral_beneficio = self.rng.uniform(
            profit_threshold_range[0], profit_threshold_range[1]
        )
        capital_minimo = self.rng.uniform(
            min_capital_range[0], min_capital_range[1]
        )

        return DTPInstance(
            tiempos=tiempos,
            costos=costos,
            precios_compra=precios_compra,
            precios_venta=precios_venta,
            oferta_max=oferta_max,
            pesos=pesos,
            capacidad_bodega=capacidad_bodega,
            capital_inicial=capital_inicial,
            tiempo_maximo=tiempo_maximo,
            umbral_beneficio=umbral_beneficio,
            capital_minimo=capital_minimo,
        ) 

    def _generate_matrix(
        self, size: int, min_val: float, max_val: float
    ) -> np.ndarray:
        """Genera una matriz con diagonal cero.

        Se asume que A -> B puede tener un valor diferente a B -> A,
        reflejando que el viaje en una dirección puede ser diferente
        del viaje en la dirección opuesta (corrientes, vientos, etc.).

        Args:
            size: Tamaño de la matriz (size x size).
            min_val: Valor mínimo para elementos fuera de la diagonal.
            max_val: Valor máximo para elementos fuera de la diagonal.

        Returns:
            Matriz asimétrica con diagonal cero.
        """
        matrix = self.rng.uniform(min_val, max_val, size=(size, size))
        # Poner la diagonal en cero (no hay costo/tiempo de un puerto a sí mismo)
        np.fill_diagonal(matrix, 0.0)
        
        return matrix

    def generate_batch(self, n_instances: int, **kwargs) -> list[DTPInstance]:
        """Genera un lote de instancias aleatorias.

        Args:
            n_instances: Número de instancias a generar.
            **kwargs: Parámetros para pasar a generate().

        Returns:
            Lista de instancias DTP.
        """
        return [self.generate(**kwargs) for _ in range(n_instances)]


def generate_small_instance(seed: int | None = None) -> DTPInstance:
    """Genera una instancia pequeña para pruebas rápidas.

    Args:
        seed: Semilla para reproducibilidad.

    Returns:
        Instancia pequeña del DTP (3 puertos, 2 mercancías).
    """
    generator = RandomDTPGenerator(seed)
    return generator.generate(
        n_ports=3,
        n_goods=2,
        cargo_capacity_range=(30, 50),
        initial_capital_range=(500, 1000),
        max_time_range=(150.0, 250.0),
    )


def generate_medium_instance(seed: int | None = None) -> DTPInstance:
    """Genera una instancia mediana.

    Args:
        seed: Semilla para reproducibilidad.

    Returns:
        Instancia mediana del DTP (5 puertos, 3 mercancías).
    """
    generator = RandomDTPGenerator(seed)
    return generator.generate(
        n_ports=5,
        n_goods=3,
        cargo_capacity_range=(80, 150),
        initial_capital_range=(2000, 4000),
        max_time_range=(300.0, 500.0),
    )


def generate_large_instance(seed: int | None = None) -> DTPInstance:
    """Genera una instancia grande (advertencia: costosa computacionalmente).

    Args:
        seed: Semilla para reproducibilidad.

    Returns:
        Instancia grande del DTP (8 puertos, 5 mercancías).
    """
    generator = RandomDTPGenerator(seed)
    return generator.generate(
        n_ports=8,
        n_goods=5,
        cargo_capacity_range=(150, 300),
        initial_capital_range=(5000, 10000),
        max_time_range=(500.0, 800.0),
    )
    
##################### TESTS #####################################

# if __name__ == "__main__":
#     # Generar y mostrar una instancia pequeña
#     small_instance = generate_small_instance(seed=42)
#     print("Instancia Pequeña:")
#     print(small_instance)

#     # Generar y mostrar una instancia mediana
#     medium_instance = generate_medium_instance(seed=42)
#     print("\nInstancia Mediana:")
#     print(medium_instance)

#     # Generar y mostrar una instancia grande
#     large_instance = generate_large_instance(seed=42)
#     print("\nInstancia Grande:")
#     print(large_instance)