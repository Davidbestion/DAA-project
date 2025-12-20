import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from base_model.base_model import Model

def crear_grafo_desde_modelo(modelo):
    """Crea un grafo dirigido NetworkX desde el modelo."""
    G = nx.DiGraph()
    
    # Agregar nodos (puertos)
    for puerto in modelo.get_puertos():
        G.add_node(puerto)
    
    # Agregar aristas dirigidas
    for origen in modelo.get_puertos():
        for destino in modelo.get_puertos():
            if modelo.existe_conexion(origen, destino):
                G.add_edge(origen, destino)
    
    return G

def visualizar_grafo(modelo, titulo="Grafo Dirigido de Puertos"):
    """Visualiza el grafo dirigido de puertos."""
    G = crear_grafo_desde_modelo(modelo)
    
    # Configurar la figura
    plt.figure(figsize=(12, 8))
    
    # Crear layout circular para mejor visualización
    pos = nx.circular_layout(G)
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue', 
                          node_size=800,
                          alpha=0.9)
    
    # Dibujar aristas dirigidas
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          arrowstyle='->',
                          width=1.5,
                          alpha=0.7,
                          connectionstyle="arc3,rad=0.1")  # Curvar las aristas para ver mejor la dirección
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos,
                           font_size=16,
                           font_weight='bold')
    
    plt.title(titulo, fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Mostrar información del grafo
    print(f"Número de nodos (puertos): {G.number_of_nodes()}")
    print(f"Número de aristas: {G.number_of_edges()}")
    print("\nConexiones:")
    for edge in G.edges():
        print(f"  {edge[0]} → {edge[1]}")
    
    plt.show()

if __name__ == "__main__":
    # Importar datos del main.py
    from main import modelo
    
    # Visualizar el grafo
    visualizar_grafo(modelo)