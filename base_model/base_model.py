import numpy as np
from typing import Optional, Tuple, List


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
        
        
    
