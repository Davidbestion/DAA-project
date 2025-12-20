from base_model.base_model import Model
import numpy as np

puertos = list(range(6))  # Puertos del 0 al 5
total_puertos = len(puertos)

# Mercancias
mercancias = {  # {int: float} ID de mercancia : peso
    0: 50.0,
    1: 75.0,
    2: 100.0,
    }

#Mapa de aristas entre puertos
mapa = np.empty((total_puertos, total_puertos), dtype=object)
mapa.fill(None)
# Rellenar el mapa con tuplas de (tiempo, costo) - GRAFO DIRIGIDO NO SIMÉTRICO
#            tiempo, costo
# Desde puerto 0
mapa[0, 1] = (2.0, 100.0)   # 0 -> 1
mapa[0, 2] = (3.5, 150.0)   # 0 -> 2
mapa[0, 3] = (4.2, 180.0)   # 0 -> 3 (nueva ruta directa)

# Desde puerto 1
mapa[1, 0] = (2.5, 120.0)   # 1 -> 0 (asimétrico: diferente tiempo/costo que 0->1)
mapa[1, 2] = (2.5, 120.0)   # 1 -> 2
mapa[1, 3] = (4.0, 180.0)   # 1 -> 3
mapa[1, 5] = (6.0, 220.0)   # 1 -> 5

# Desde puerto 2
mapa[2, 1] = (3.0, 140.0)   # 2 -> 1 (asimétrico)
mapa[2, 3] = (3.0, 130.0)   # 2 -> 3
mapa[2, 4] = (4.5, 170.0)   # 2 -> 4
mapa[2, 5] = (5.8, 195.0)   # 2 -> 5 (nueva ruta)

# Desde puerto 3
mapa[3, 2] = (2.8, 125.0)   # 3 -> 2 (asimétrico)
mapa[3, 4] = (2.0, 110.0)   # 3 -> 4
mapa[3, 5] = (5.5, 210.0)   # 3 -> 5
# NO hay ruta de vuelta 3 -> 1 (solo existe 1 -> 3)

# Desde puerto 4
mapa[4, 0] = (6.0, 250.0)   # 4 -> 0 
mapa[4, 2] = (4.8, 180.0)   # 4 -> 2 (asimétrico)
mapa[4, 3] = (1.8, 105.0)   # 4 -> 3 (asimétrico)
mapa[4, 5] = (3.5, 160.0)   # 4 -> 5

# Desde puerto 5
mapa[5, 1] = (6.5, 240.0)   # 5 -> 1 (asimétrico)
mapa[5, 3] = (5.2, 200.0)   # 5 -> 3 (asimétrico)
mapa[5, 4] = (3.8, 170.0)   # 5 -> 4 (asimétrico)
# NO hay rutas 5 -> 0 ni 5 -> 2 directas 

# Matriz de mercancias por puertos
matriz_mercancias = np.empty((total_puertos, len(mercancias)), dtype=object)
# Rellenar la matriz_mercancias con tuplas de (precio venta, precio compra, cantidad total en ese puerto)
matriz_mercancias[0, 0] = (10.0, 20.0, 400)# en puerto 0 el producto 0 se vende a 10.0, se compra a 20.0 y hay 400 unidades
matriz_mercancias[0, 1] = (15.0, 30.0, 300)
matriz_mercancias[0, 2] = (47.0, 25.0, 250)
matriz_mercancias[1, 0] = (12.0, 15.0, 150)
matriz_mercancias[1, 1] = (80.0, 20.0, 200)
matriz_mercancias[1, 2] = (22.0, 30.0, 300)
matriz_mercancias[2, 0] = (11.0, 25.0, 250)
matriz_mercancias[2, 1] = (16.0, 35.0, 350)
matriz_mercancias[2, 2] = (21.0, 20.0, 200)
matriz_mercancias[3, 0] = (50.0, 60.0, 300)
matriz_mercancias[3, 1] = (19.0, 25.0, 250)
matriz_mercancias[3, 2] = (23.0, 15.0, 150)
matriz_mercancias[4, 0] = (14.0, 10.0, 100)
matriz_mercancias[4, 1] = (17.0, 40.0, 400)
matriz_mercancias[4, 2] = (24.0, 35.0, 350)
matriz_mercancias[5, 0] = (15.0, 20.0, 200)
matriz_mercancias[5, 1] = (20.0, 30.0, 300)
matriz_mercancias[5, 2] = (30.0, 40.0, 421)

# Crear el modelo
modelo = Model(puertos, mapa, mercancias, matriz_mercancias)

# Ejemplos de uso
print("="*50)
print(modelo)
print("="*50)

# Información general
print(f"\nNúmero de puertos: {modelo.get_num_puertos()}")
print(f"Número de mercancías: {modelo.get_num_mercancias()}")

# Información de conexiones
print(f"\n¿Existe conexión 0->1? {modelo.existe_conexion(0, 1)}")
print(f"Tiempo de viaje 0->1: {modelo.get_tiempo_viaje(0, 1)}")
print(f"Costo de viaje 0->1: {modelo.get_costo_viaje(0, 1)}")
print(f"Info completa 0->1: {modelo.get_info_viaje(0, 1)}")
print(f"Vecinos del puerto 0: {modelo.get_vecinos(0)}")

# Información de mercancías
print(f"\nPeso de mercancía 1: {modelo.get_peso_mercancia(1)}")
print(f"Precio venta mercancía 0 en puerto 0: {modelo.get_precio_venta(0, 0)}")
print(f"Precio compra mercancía 0 en puerto 0: {modelo.get_precio_compra(0, 0)}")
print(f"Cantidad disponible mercancía 0 en puerto 0: {modelo.get_cantidad_disponible(0, 0)}")
print(f"Info completa mercancía 0 en puerto 0: {modelo.get_info_mercancia_en_puerto(0, 0)}")

# Ganancia potencial
print(f"\nGanancia potencial comprando mercancía 0 en puerto 4 y vendiendo en puerto 0:")
print(f"  {modelo.get_ganancia_potencial(4, 1, 0)}")
