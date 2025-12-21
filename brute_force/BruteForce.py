from base_model import Model
import numpy as np

class BruteForceSolver:
    """
    Clase que implementa un solucionador por fuerza bruta para el problema de optimización de rutas comerciales.
    """
    
    def __init__(self, model: Model):
        """
        Inicializa el solucionador con un modelo dado.
        
        Args:
            model: Instancia de la clase Model
        """
        self.model = model
    
    def solve(self):
        """
        Método placeholder para resolver el problema utilizando fuerza bruta.
        Implementación pendiente.
        """
        return self._recursive_explore(current_port=0, visited=set(), current_path=[])
    
    def _recursive_explore(self, current_port: int, visited: set, current_path: list):
        """Explora todos los caminos posibles de manera recursiva."""
        for puerto in self.model.get_puertos():
            print(f"Estoy en puerto: {puerto}")
            for destino in self.model.get_vecinos(puerto):
                tiempo = self.model.get_tiempo_viaje(puerto, destino)
                costo = self.model.get_costo_viaje(puerto, destino)
                print(f"  Puedo ir al puerto {destino} en {tiempo} horas con un costo de {costo}.")