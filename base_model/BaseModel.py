import numpy as np
from typing import Optional, Tuple, List
from abc import ABC, abstractmethod


class Model:
    """
    Clase que encapsula el modelo de puertos y mercancías para el problema de optimización de rutas comerciales.
    """
    
    def __init__(self, puertos: List[int], mapa: np.ndarray, mercancias: dict[int, float], matriz_mercancias: np.ndarray):
        """
        Inicializa el modelo.
        
        Args:
            puertos: Lista de IDs de puertos
            mapa: Matriz NxN donde mapa[i,j] = (tiempo, costo) para ir del puerto i al j
            mercancias: Diccionario {id_mercancia: peso}
            matriz_mercancias: Matriz PxM donde [p,m] = (precio_venta, precio_compra, cantidad_disponible)
        """
        self.puertos = puertos
        self.mercancias = mercancias
        self.mapa = mapa
        self.matriz_mercancias = matriz_mercancias
    
    # ===== Métodos de información general =====
    
    def get_num_puertos(self) -> int:
        """Retorna el número total de puertos."""
        return len(self.puertos)
    
    def get_num_mercancias(self) -> int:
        """Retorna el número total de mercancías."""
        return len(self.mercancias)
    
    def get_puertos(self) -> List[int]:
        """Retorna la lista de puertos."""
        return self.puertos
    
    def get_mercancias(self) -> dict[int, float]:
        """Retorna el diccionario de mercancías."""
        return self.mercancias
    
    # ===== Métodos para información de conexiones entre puertos =====
    
    def existe_conexion(self, puerto_origen: int, puerto_destino: int) -> bool:
        """
        Verifica si existe una conexión entre dos puertos.
        
        Args:
            puerto_origen: ID del puerto de origen
            puerto_destino: ID del puerto de destino
            
        Returns:
            True si existe conexión, False en caso contrario
        """
        return self.mapa[puerto_origen, puerto_destino] is not None
    
    def get_tiempo_viaje(self, puerto_origen: int, puerto_destino: int) -> Optional[float]:
        """
        Obtiene el tiempo de viaje entre dos puertos.
        
        Args:
            puerto_origen: ID del puerto de origen
            puerto_destino: ID del puerto de destino
            
        Returns:
            Tiempo de viaje o None si no hay conexión
        """
        conexion = self.mapa[puerto_origen, puerto_destino]
        return conexion[0] if conexion is not None else None
    
    def get_costo_viaje(self, puerto_origen: int, puerto_destino: int) -> Optional[float]:
        """
        Obtiene el costo de viaje entre dos puertos.
        
        Args:
            puerto_origen: ID del puerto de origen
            puerto_destino: ID del puerto de destino
            
        Returns:
            Costo de viaje o None si no hay conexión
        """
        conexion = self.mapa[puerto_origen, puerto_destino]
        return conexion[1] if conexion is not None else None
    
    def get_info_viaje(self, puerto_origen: int, puerto_destino: int) -> Optional[Tuple[float, float]]:
        """
        Obtiene la información completa del viaje (tiempo, costo).
        
        Args:
            puerto_origen: ID del puerto de origen
            puerto_destino: ID del puerto de destino
            
        Returns:
            Tupla (tiempo, costo) o None si no hay conexión
        """
        return self.mapa[puerto_origen, puerto_destino]
    
    def get_vecinos(self, puerto: int) -> List[int]:
        """
        Obtiene los puertos vecinos (conectados) a un puerto dado.
        
        Args:
            puerto: ID del puerto
            
        Returns:
            Lista de IDs de puertos vecinos
        """
        vecinos = []
        for destino in self.puertos:
            if self.existe_conexion(puerto, destino):
                vecinos.append(destino)
        return vecinos
    
    # ===== Métodos para información de mercancías =====
    
    def get_peso_mercancia(self, id_mercancia: int) -> Optional[float]:
        """
        Obtiene el peso de una mercancía.
        
        Args:
            id_mercancia: ID de la mercancía
            
        Returns:
            Peso de la mercancía o None si no existe
        """
        return self.mercancias.get(id_mercancia)
    
    def get_precio_venta(self, puerto: int, id_mercancia: int) -> Optional[float]:
        """
        Obtiene el precio de venta de una mercancía en un puerto.
        
        Args:
            puerto: ID del puerto
            id_mercancia: ID de la mercancía
            
        Returns:
            Precio de venta o None si no existe
        """
        info = self.matriz_mercancias[puerto, id_mercancia]
        return info[0] if info is not None else None
    
    def get_precio_compra(self, puerto: int, id_mercancia: int) -> Optional[float]:
        """
        Obtiene el precio de compra de una mercancía en un puerto.
        
        Args:
            puerto: ID del puerto
            id_mercancia: ID de la mercancía
            
        Returns:
            Precio de compra o None si no existe
        """
        info = self.matriz_mercancias[puerto, id_mercancia]
        return info[1] if info is not None else None
    
    def get_cantidad_disponible(self, puerto: int, id_mercancia: int) -> Optional[int]:
        """
        Obtiene la cantidad disponible de una mercancía en un puerto.
        
        Args:
            puerto: ID del puerto
            id_mercancia: ID de la mercancía
            
        Returns:
            Cantidad disponible o None si no existe
        """
        info = self.matriz_mercancias[puerto, id_mercancia]
        return info[2] if info is not None else None
    
    def get_info_mercancia_en_puerto(self, puerto: int, id_mercancia: int) -> Optional[Tuple[float, float, int]]:
        """
        Obtiene toda la información de una mercancía en un puerto.
        
        Args:
            puerto: ID del puerto
            id_mercancia: ID de la mercancía
            
        Returns:
            Tupla (precio_venta, precio_compra, cantidad_disponible) o None si no existe
        """
        return self.matriz_mercancias[puerto, id_mercancia]
    
    def get_ganancia_potencial(self, puerto_compra: int, puerto_venta: int, id_mercancia: int) -> Optional[float]:
        """
        Calcula la ganancia potencial por unidad al comprar en un puerto y vender en otro.
        
        Args:
            puerto_compra: ID del puerto donde se compra
            puerto_venta: ID del puerto donde se vende
            id_mercancia: ID de la mercancía
            
        Returns:
            Ganancia por unidad (puede ser negativa) o None si no se puede calcular
        """
        precio_compra = self.get_precio_compra(puerto_compra, id_mercancia)
        precio_venta = self.get_precio_venta(puerto_venta, id_mercancia)
        
        if precio_compra is not None and precio_venta is not None:
            return precio_venta - precio_compra
        return None
    
    # ===== Método para visualización =====
    
    def __str__(self) -> str:
        """Representación en string del modelo."""
        return (f"Model(\n"
                f"  Puertos: {self.get_num_puertos()}\n"
                f"  Mercancías: {self.get_num_mercancias()}\n"
                f")")
    
    def __repr__(self) -> str:
        """Representación del modelo."""
        return self.__str__()
        
class Barco:
    """
    Clase que representa un barco con capacidad de carga y velocidad.
    """
    
    def __init__(self, capacidad_carga: float, velocidad: float, modelo: Model, capital_inicial: float = 0.0, umbral_compra: float = 0.0, umbral_tiempo: float = 0.0, puerto_inicial: int = 0):
        """
        Inicializa el barco.
        
        Args:
            capacidad_carga: Capacidad máxima de carga del barco
            velocidad: Velocidad del barco
        """
        self.capacidad_carga = capacidad_carga
        self.bodega = {}  # Diccionario {id_mercancia: cantidad}
        self.modelo = modelo
        self.capital_inicial = capital_inicial  # Dinero inicial
        self.capital = capital_inicial  # Dinero disponible
        self.umbral_tiempo = umbral_tiempo  # Umbral máximo de tiempo para considerar una ruta viable
        self.tiempo = 0.0  # Tiempo total de viaje
        self.puerto_actual = puerto_inicial  # Puerto donde se encuentra el barco al inicio
        self.ruta_recorrida = [puerto_inicial]  # Lista de puertos visitados
    
    def validar_estado(self) -> bool:
        """Metodo para validar el estado del barco."""
        if self.capital < 0:
            return False
        carga_total = sum(self.bodega.values())
        if carga_total > self.capacidad_carga:
            return False
        if self.tiempo < 0 or self.tiempo > self.umbral_tiempo:
            return False
        return True
    
    def comprar_mercancia(self, puerto: int, id_mercancia: int, cantidad: int) -> bool:
        """
        Compra una cantidad de mercancía en un puerto.
        
        Args:
            puerto: ID del puerto donde se compra
            id_mercancia: ID de la mercancía
            cantidad: Cantidad a comprar
            
        Returns:
            True si se compró exitosamente, False si no hay suficiente dinero o cantidad disponible
        """
        precio_compra = self.modelo.get_precio_compra(puerto, id_mercancia)
        cantidad_disponible = self.modelo.get_cantidad_disponible(puerto, id_mercancia)
        
        if precio_compra is None or cantidad_disponible is None:
            return False
        
        costo_total = precio_compra * cantidad
        
        if (self.capital >= costo_total and 
            cantidad <= cantidad_disponible and 
            self.cargar_mercancia(id_mercancia, cantidad)):
                self.capital -= costo_total
                # Actualizar la cantidad disponible en el modelo
                nueva_cantidad = cantidad_disponible - cantidad
                self.modelo.matriz_mercancias[puerto, id_mercancia] = (
                    precio_compra,
                    self.modelo.get_precio_venta(puerto, id_mercancia),
                    nueva_cantidad
                )
                return True
        return False
    
    def vender_mercancia(self, puerto: int, id_mercancia: int, cantidad: int) -> bool:
        """
        Vende una cantidad de mercancía en un puerto.
        
        Args:
            puerto: ID del puerto donde se vende
            id_mercancia: ID de la mercancía
            cantidad: Cantidad a vender
            
        Returns:
            True si se vendió exitosamente, False si no hay suficiente mercancía en la bodega
        """
        precio_venta = self.modelo.get_precio_venta(puerto, id_mercancia)
        
        if precio_venta is None:
            return False
        
        if self.descargar_mercancia(id_mercancia, cantidad):
            ingreso_total = precio_venta * cantidad
            self.capital += ingreso_total
            # Actualizar la cantidad disponible en el modelo
            cantidad_disponible = self.modelo.get_cantidad_disponible(puerto, id_mercancia)
            nueva_cantidad = cantidad_disponible + cantidad if cantidad_disponible is not None else cantidad
            self.modelo.matriz_mercancias[puerto, id_mercancia] = (
                precio_venta,
                self.modelo.get_precio_compra(puerto, id_mercancia),
                nueva_cantidad
            )
            return True
        return False
    
    def viajar_a_puerto(self, puerto_destino: int) -> Optional[Tuple[float, float]]:
        """
        Viaja al puerto destino si hay conexión.
        
        Args:
            puerto_destino: ID del puerto destino
            
        Returns:
            Tupla (tiempo_viaje, costo_viaje) si el viaje es exitoso, None si no hay conexión
        """
        if self.modelo.existe_conexion(self.puerto_actual, puerto_destino):
            info = self.modelo.get_info_viaje(self.puerto_actual, puerto_destino)
            if info is None:
                return None
            tiempo_viaje, costo_viaje = info
            self.puerto_actual = puerto_destino
            self.tiempo += tiempo_viaje
            self.capital -= costo_viaje
            self.ruta_recorrida.append(puerto_destino)
            return (tiempo_viaje, costo_viaje)
        return None
    
    def cargar_mercancia(self, id_mercancia: int, cantidad: int) -> bool:
        """
        Carga una cantidad de mercancía en el barco.
        
        Args:
            id_mercancia: ID de la mercancía
            cantidad: Cantidad a cargar
            
        Returns:
            True si se cargó exitosamente, False si excede la capacidad
        """
        peso_total = sum(cantidad * peso for id_m, cantidad in self.bodega.items() for peso in [self.modelo.get_peso_mercancia(id_m)])
        # peso_nueva = self.modelo.get_peso_mercancia(id_mercancia) * cantidad
        peso = self.modelo.get_peso_mercancia(id_mercancia)
        if peso is None:
            return False
        peso_nuevo = peso * cantidad
        
        if peso_total + peso_nuevo <= self.capacidad_carga:
            if id_mercancia in self.bodega:
                self.bodega[id_mercancia] += cantidad
            else:
                self.bodega[id_mercancia] = cantidad
            return True
        return False
    
    def descargar_mercancia(self, id_mercancia: int, cantidad: int) -> bool:
        """
        Descarga una cantidad de mercancía del barco.
        
        Args:
            id_mercancia: ID de la mercancía
            cantidad: Cantidad a descargar
            
        Returns:
            True si se descargó exitosamente, False si no hay suficiente cantidad
        """
        if id_mercancia in self.bodega and self.bodega[id_mercancia] >= cantidad:
            self.bodega[id_mercancia] -= cantidad
            if self.bodega[id_mercancia] == 0:
                del self.bodega[id_mercancia]
            return True
        return False
    
    def get_carga_actual(self) -> float:
        """
        Obtiene el peso total de la carga actual en el barco.
        
        Returns:
            Peso total de la carga
        """
        return sum(cantidad * self.modelo.get_peso_mercancia(id_m) for id_m, cantidad in self.bodega.items())
    
    def get_dinero(self) -> float:
        """
        Obtiene la cantidad de dinero disponible en el barco.
        
        Returns:
            Cantidad de dinero
        """
        return self.capital
    
    def agregar_dinero(self, cantidad: float):
        """
        Agrega una cantidad de dinero al barco.
        
        Args:
            cantidad: Cantidad a agregar
        """
        self.capital += cantidad
        
    def restar_dinero(self, cantidad: float) -> bool:
        """
        Resta una cantidad de dinero del barco si hay suficiente.
        
        Args:
            cantidad: Cantidad a restar
        Returns:
            True si se restó exitosamente, False si no hay suficiente dinero
        """        
        if self.capital >= cantidad:
            self.capital -= cantidad
            return True
        return False
    
    def __str__(self) -> str:
        """Representación en string del barco."""
        return (f"Barco(\n"
                f"  Capacidad de carga: {self.capacidad_carga}\n"
                f"  Carga actual: {self.get_carga_actual()}\n"
                f"  Bodega: {self.bodega}\n"
                f")")
    
