"""Instancias robustas para testing: MICRO + generadas con casos extremos.

Combina:
1. MICRO: 4 instancias manuales documentadas (referencia rápida)
2. EXTREME: Instancias generadas con casos extremos (stress test)
"""

import numpy as np
from solver.schemas.dtp import DTPInstance
from generator.random_gen import RandomDTPGenerator


# ============================================================================
# INSTANCIAS MICRO (Existentes - referencia rápida)
# ============================================================================

from instances.micro import (
    INSTANCE_MICRO_1,
    INSTANCE_MICRO_2,
    INSTANCE_MICRO_3,
    INSTANCE_MICRO_4,
)

MICRO_INSTANCES = [
    (INSTANCE_MICRO_1, "MICRO_1 (n=2, m=1)"),
    (INSTANCE_MICRO_2, "MICRO_2 (n=2, m=2)"),
    (INSTANCE_MICRO_3, "MICRO_3 (n=3, m=1)"),
    (INSTANCE_MICRO_4, "MICRO_4 (n=2, m=2)"),
]

# ============================================================================
# INSTANCIAS EXTREMAS (Generadas - casos de stress)
# ============================================================================

"""
Casos extremos para validar robustez de solvers:
- Capital muy limitado: Requiere decisiones inteligentes
- Tiempo muy limitado: Solo pocos puertos alcanzables
- Muchas mercancías: Complica decisión de compra/venta
- Pocos puertos: Espacio pequeño pero complejo
- Oportunidades escasas: Márgenes pequeños entre compra/venta
"""

def _generate_extreme_instances():
    """Genera batch de instancias extremas con reproducibilidad."""
    extreme_cases = []
    
    # CASO 1: Capital muy limitado (debe ser muy selectivo)
    gen = RandomDTPGenerator(seed=100)
    instance = gen.generate(
        n_ports=3,
        n_goods=2,
        time_range=(5.0, 30.0),
        cost_range=(20.0, 100.0),
        buy_price_range=(5.0, 15.0),
        sell_price_range=(7.0, 20.0),
        max_offer_range=(5, 15),
        weight_range=(2.0, 5.0),
        cargo_capacity_range=(20, 40),
        initial_capital_range=(100, 200),  # ← MUY BAJO
        max_time_range=(100.0, 200.0),
        profit_threshold_range=(10.0, 50.0),
        min_capital_range=(10.0, 50.0),
    )
    extreme_cases.append((instance, "EXTREME_1: Capital limitado (n=3, m=2, capital=$100-200)"))
    
    # CASO 2: Tiempo muy limitado (solo algunos puertos alcanzables)
    gen = RandomDTPGenerator(seed=101)
    instance = gen.generate(
        n_ports=4,
        n_goods=2,
        time_range=(30.0, 80.0),  # Tiempos largos
        cost_range=(50.0, 200.0),
        buy_price_range=(10.0, 30.0),
        sell_price_range=(15.0, 40.0),
        max_offer_range=(5, 20),
        weight_range=(1.0, 3.0),
        cargo_capacity_range=(30, 60),
        initial_capital_range=(500, 1000),
        max_time_range=(60.0, 100.0),  # ← MUY POCO TIEMPO
        profit_threshold_range=(100.0, 300.0),
        min_capital_range=(50.0, 150.0),
    )
    extreme_cases.append((instance, "EXTREME_2: Tiempo limitado (n=4, m=2, tiempo=60-100)"))
    
    # CASO 3: Muchas mercancías (espacio de decisión grande)
    gen = RandomDTPGenerator(seed=102)
    instance = gen.generate(
        n_ports=3,
        n_goods=5,  # ← MUCHAS MERCANCÍAS
        time_range=(10.0, 50.0),
        cost_range=(30.0, 150.0),
        buy_price_range=(5.0, 20.0),
        sell_price_range=(8.0, 30.0),
        max_offer_range=(5, 25),
        weight_range=(1.0, 4.0),
        cargo_capacity_range=(40, 100),
        initial_capital_range=(500, 1500),
        max_time_range=(150.0, 300.0),
        profit_threshold_range=(100.0, 400.0),
        min_capital_range=(50.0, 200.0),
    )
    extreme_cases.append((instance, "EXTREME_3: Muchas mercancías (n=3, m=5)"))
    
    # CASO 4: Márgenes pequeños (poco margen de ganancia)
    gen = RandomDTPGenerator(seed=103)
    instance = gen.generate(
        n_ports=3,
        n_goods=2,
        time_range=(10.0, 40.0),
        cost_range=(20.0, 100.0),
        buy_price_range=(100.0, 120.0),  # Precios altos
        sell_price_range=(105.0, 130.0),  # ← MÁRGENES PEQUEÑOS
        max_offer_range=(10, 30),
        weight_range=(2.0, 4.0),
        cargo_capacity_range=(50, 100),
        initial_capital_range=(1000, 2000),
        max_time_range=(150.0, 300.0),
        profit_threshold_range=(100.0, 300.0),
        min_capital_range=(100.0, 300.0),
    )
    extreme_cases.append((instance, "EXTREME_4: Márgenes pequeños (low profit margin)"))
    
    # CASO 5: Oferta muy limitada (no hay mercancía para comprar)
    gen = RandomDTPGenerator(seed=104)
    instance = gen.generate(
        n_ports=4,
        n_goods=3,
        time_range=(10.0, 50.0),
        cost_range=(30.0, 120.0),
        buy_price_range=(10.0, 30.0),
        sell_price_range=(15.0, 40.0),
        max_offer_range=(1, 3),  # ← OFERTA LIMITADA
        weight_range=(1.0, 2.0),
        cargo_capacity_range=(30, 60),
        initial_capital_range=(500, 1000),
        max_time_range=(150.0, 250.0),
        profit_threshold_range=(100.0, 300.0),
        min_capital_range=(50.0, 150.0),
    )
    extreme_cases.append((instance, "EXTREME_5: Oferta limitada (max offer = 1-3)"))
    
    # CASO 6: Bodega pequeña (restricción de capacidad)
    gen = RandomDTPGenerator(seed=105)
    instance = gen.generate(
        n_ports=3,
        n_goods=3,
        time_range=(10.0, 40.0),
        cost_range=(25.0, 100.0),
        buy_price_range=(8.0, 25.0),
        sell_price_range=(12.0, 35.0),
        max_offer_range=(10, 30),
        weight_range=(3.0, 8.0),  # Pesos altos
        cargo_capacity_range=(10, 20),  # ← BODEGA MUY PEQUEÑA
        initial_capital_range=(800, 1500),
        max_time_range=(150.0, 300.0),
        profit_threshold_range=(150.0, 400.0),
        min_capital_range=(100.0, 250.0),
    )
    extreme_cases.append((instance, "EXTREME_6: Bodega pequeña (capacity=10-20)"))
    
    # CASO 7: Rutas largas (muchos puertos, pero tiempo limitado)
    gen = RandomDTPGenerator(seed=106)
    instance = gen.generate(
        n_ports=5,  # Más puertos
        n_goods=2,
        time_range=(50.0, 150.0),  # Tiempos muy largos
        cost_range=(100.0, 300.0),
        buy_price_range=(20.0, 50.0),
        sell_price_range=(30.0, 70.0),
        max_offer_range=(10, 30),
        weight_range=(1.0, 3.0),
        cargo_capacity_range=(50, 100),
        initial_capital_range=(2000, 4000),
        max_time_range=(200.0, 300.0),  # ← POCO TIEMPO PARA MUCHOS PUERTOS
        profit_threshold_range=(300.0, 800.0),
        min_capital_range=(200.0, 500.0),
    )
    extreme_cases.append((instance, "EXTREME_7: Rutas largas (n=5, m=2, limited time)"))
    
    # CASO 8: Caso balanceado (comparativa)
    gen = RandomDTPGenerator(seed=107)
    instance = gen.generate(
        n_ports=4,
        n_goods=3,
        time_range=(15.0, 60.0),
        cost_range=(40.0, 150.0),
        buy_price_range=(10.0, 30.0),
        sell_price_range=(15.0, 45.0),
        max_offer_range=(10, 25),
        weight_range=(1.0, 3.0),
        cargo_capacity_range=(50, 100),
        initial_capital_range=(1000, 2000),
        max_time_range=(200.0, 400.0),
        profit_threshold_range=(200.0, 500.0),
        min_capital_range=(100.0, 300.0),
    )
    extreme_cases.append((instance, "EXTREME_8: Caso balanceado (n=4, m=3)"))
    
    return extreme_cases


# Generar instancias extremas (una sola vez)
EXTREME_INSTANCES = _generate_extreme_instances()

# ============================================================================
# CONJUNTOS TOTALES
# ============================================================================

ALL_INSTANCES = MICRO_INSTANCES + EXTREME_INSTANCES

# Alias para conveniencia
ROBUST_TEST_SUITE = {
    "micro": MICRO_INSTANCES,        # Rápido, 4 casos
    "extreme": EXTREME_INSTANCES,    # Exhaustivo, 8 casos extremos
    "all": ALL_INSTANCES,            # Todos, 12 casos totales
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def get_micro_instances():
    """Retorna solo las instancias MICRO (referencia rápida)."""
    return MICRO_INSTANCES


def get_extreme_instances():
    """Retorna solo las instancias extremas (stress test)."""
    return EXTREME_INSTANCES


def get_all_instances():
    """Retorna todas las instancias (MICRO + EXTREME)."""
    return ALL_INSTANCES


def get_instance_batch(batch_type: str = "micro"):
    """
    Retorna un batch de instancias.
    
    Args:
        batch_type: "micro", "extreme", "all"
    
    Returns:
        Lista de tuplas (instance, name)
    """
    return ROBUST_TEST_SUITE.get(batch_type, ALL_INSTANCES)


if __name__ == "__main__":
    # Demostración de uso
    print("=" * 80)
    print("INSTANCIAS DISPONIBLES PARA TESTING")
    print("=" * 80)
    print()
    
    print(f"📦 MICRO instances: {len(MICRO_INSTANCES)}")
    for instance, name in MICRO_INSTANCES:
        print(f"   └─ {name}")
    print()
    
    print(f"⚡ EXTREME instances: {len(EXTREME_INSTANCES)}")
    for instance, name in EXTREME_INSTANCES:
        print(f"   └─ {name}")
    print()
    
    print(f"🎯 TOTAL: {len(ALL_INSTANCES)} instancias")
    print()
    print("Uso en tests:")
    print("  from instances.robust import get_all_instances")
    print("  instances = get_all_instances()")
    print("  for instance, name in instances:")
    print("      result = solver.solve(instance)")
