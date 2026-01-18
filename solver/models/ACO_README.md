# ACO Solver - Ant Colony Optimization para DTP

## Descripción

El **ACOSolver** implementa el algoritmo de Optimización por Colonias de Hormigas (Ant Colony Optimization) para resolver el Problema del Comerciante Holandés (DTP).

### Características

- **Fase 1 - Construcción de Rutas (ACO):**
  - Las "hormigas" construyen rutas probabilísticamente
  - Usa matriz de feromonas e información heurística
  - Balance entre exploración (nuevas rutas) y explotación (mejores rutas)

- **Fase 2 - Optimización de Trading (Greedy Knapsack):**
  - En cada puerto de la ruta, aplica knapsack greedy
  - Maximiza ganancia por peso
  - Respeta restricciones de capital y capacidad

### Parámetros Configurables

```python
ACOSolver(
    n_ants=10,              # Número de hormigas por iteración
    n_iterations=50,        # Número de iteraciones del algoritmo
    alpha=1.0,              # Peso de las feromonas
    beta=2.0,               # Peso de la heurística
    evaporation_rate=0.5,   # Tasa de evaporación de feromonas
    q=100.0                 # Constante para depositar feromonas
)
```

### Algoritmo

1. **Inicialización:**
   - Matriz de feromonas con valores constantes
   - Heurística: `h[i,j] = 1 / (costo_normalizado + tiempo_normalizado)`

2. **Iteraciones:**
   - Cada hormiga construye una ruta:
     - Selección probabilística: `P[i,j] ∝ τ[i,j]^α × η[i,j]^β`
     - Verifica factibilidad (capital y tiempo)
   - Evalúa cada ruta con greedy knapsack
   - Actualiza feromonas:
     - Evaporación: `τ[i,j] ← (1-ρ) × τ[i,j]`
     - Depósito: `τ[i,j] ← τ[i,j] + Δτ`
     - `Δτ` proporcional a la calidad de la solución

3. **Retorno:**
   - Mejor solución encontrada en todas las iteraciones

### Complejidad

- **Temporal:** `O(ants × iterations × (n² + nm log m))`
  - `n²`: construcción de rutas
  - `nm log m`: knapsack greedy por cada parada

- **Espacial:** `O(n² + mn)`
  - Matrices de feromonas y heurística

### Comparación con otros Solvers

| Solver      | Complejidad    | Calidad        | Uso Recomendado                    |
|-------------|----------------|----------------|------------------------------------|
| Brute Force | `O(n! × 2^mn)` | Óptima         | Instancias muy pequeñas (n ≤ 8)    |
| Greedy      | `O(n² + nm log m)` | Buena      | Solución rápida inicial            |
| **ACO**     | `O(k×n² + knm log m)` | Muy buena | Balance calidad-tiempo (n ≤ 20)   |

donde `k = ants × iterations`

### Uso

```python
from solver.models.aco import ACOSolver
from instances.predefined import INSTANCE_MEDIUM

# Configuración básica
aco = ACOSolver(n_ants=15, n_iterations=30)
solution = aco.solve(INSTANCE_MEDIUM)
print(f"Capital final: {solution.beneficio_final}")
print(f"Ruta: {solution.ruta}")

# Configuración agresiva (más exploración)
aco_exploratory = ACOSolver(
    n_ants=20,
    n_iterations=50,
    alpha=0.8,          # Menos peso a feromonas
    beta=3.0,           # Más peso a heurística
    evaporation_rate=0.6  # Mayor evaporación
)
solution = aco_exploratory.solve(INSTANCE_MEDIUM)

# Configuración conservadora (más explotación)
aco_conservative = ACOSolver(
    n_ants=10,
    n_iterations=30,
    alpha=1.5,          # Más peso a feromonas
    beta=1.5,           # Menos peso a heurística
    evaporation_rate=0.3  # Menor evaporación
)
solution = aco_conservative.solve(INSTANCE_MEDIUM)
```

### Resultados Experimentales

Pruebas en instancias predefinidas (15 hormigas, 30 iteraciones):

| Instancia | Greedy | ACO    | Mejora | Tiempo ACO |
|-----------|--------|--------|--------|------------|
| TINY      | 400    | 417    | +4.25% | 0.026s     |
| SMALL     | 420    | 420    | 0%     | 0.022s     |
| MEDIUM    | 1900   | 1950   | +2.63% | 0.034s     |

### Ventajas

✅ Mejor calidad que Greedy en instancias complejas  
✅ Escalable a instancias medianas  
✅ Configurable (exploración vs explotación)  
✅ Robusto (explora múltiples soluciones)  

### Limitaciones

❌ Más lento que Greedy (factor 200-700x)  
❌ No garantiza óptimo (metaheurística)  
❌ Requiere ajuste de parámetros  
❌ Puede converger prematuramente

### Mejoras Futuras

1. **Paralelización:** Evaluar hormigas en paralelo
2. **ACO-MMAS:** Max-Min Ant System para mejor convergencia
3. **Hiperparámetros adaptativos:** Ajustar α, β, ρ dinámicamente
4. **Búsqueda local:** 2-opt o 3-opt post-ACO en la ruta

### Referencias

- Dorigo, M., & Stützle, T. (2004). *Ant Colony Optimization*. MIT Press.
- Stützle, T., & Hoos, H. H. (2000). MAX–MIN ant system. *Future Generation Computer Systems*, 16(8), 889-914.
