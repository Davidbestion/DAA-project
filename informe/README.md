# Informe: El Problema del Comerciante Holandés

Este directorio contiene el informe formal en formato LaTeX sobre el Problema del Comerciante Holandés (DTP).

## Contenido

- `main.tex`: Documento principal del informe
- `Makefile`: Automatización de compilación
- `README.md`: Esta guía

## Estructura del Informe

El documento incluye:

1. **Introducción y Motivación**
2. **Definición Formal del Problema**
3. **Análisis de Complejidad**
   - Demostración de NP-completitud
   - Demostración de NP-dureza
   - Reducciones desde TSP y Knapsack
4. **Modelado Computacional**
   - Arquitectura del sistema
   - Estructuras de datos
   - Interfaz abstracta de solvers
5. **Algoritmo de Fuerza Bruta**
   - Descripción detallada
   - Pseudocódigo
   - Análisis de complejidad
6. **Algoritmo Greedy con Optimización Local**
   - Estrategia de dos niveles
   - Knapsack greedy para optimizar compras
   - Análisis de complejidad
7. **Resultados Experimentales**
8. **Conclusiones y Trabajo Futuro**

## Requisitos

Para compilar el documento necesitas:

- `pdflatex` (incluido en TeX Live, MiKTeX, etc.)
- Paquetes LaTeX:
  - `IEEEtran` (formato de conferencia IEEE)
  - `amsmath`, `amssymb`, `amsthm` (matemáticas)
  - `algorithm`, `algpseudocode` (pseudocódigo)
  - `listings` (código fuente)
  - `hyperref` (referencias cruzadas)

### Instalación en Ubuntu/Debian

```bash
sudo apt-get install texlive-full
```

### Instalación en Fedora/RHEL

```bash
sudo dnf install texlive-scheme-full
```

## Compilación

### Usando Make (recomendado)

```bash
# Compilar el documento
make

# Ver el PDF generado
make view

# Limpiar archivos auxiliares
make clean

# Limpiar todo (incluido el PDF)
make cleanall

# Recompilar desde cero
make rebuild

# Ver ayuda
make help
```

### Compilación manual

```bash
# Primera pasada
pdflatex main.tex

# Segunda pasada (para referencias)
pdflatex main.tex
```

Esto generará `main.pdf`.

## Notas sobre el Formato

- **Estilo:** IEEE Conference Paper
- **Idioma:** Español
- **Longitud:** ~12-15 páginas
- **Formato:** Dos columnas (estándar IEEE)

## Referencias

El informe incluye referencias a textos clásicos de teoría de complejidad y optimización combinatoria:

- Garey & Johnson: "Computers and Intractability"
- Cormen et al.: "Introduction to Algorithms"
- Applegate et al.: "The Traveling Salesman Problem"
- Kellerer et al.: "Knapsack Problems"

## Modificaciones

Si deseas modificar el informe:

1. Edita `main.tex`
2. Recompila con `make`
3. El PDF se actualizará automáticamente

## Contenido Técnico

### Demostraciones Incluidas

- **NP-completitud:** Reducción polinomial desde TSP
- **NP-dureza del problema de optimización:** Mediante reducción del problema de decisión
- **Reducción desde Knapsack:** Mostrando que DTP contiene Knapsack como subproblema

### Algoritmos Documentados

1. **BruteForceSolver**
   - Exploración exhaustiva con DFS
   - Complejidad: O(n! · exp(m·n))
   - Garantiza optimalidad

2. **GreedySolver**
   - Selección greedy de puertos
   - Knapsack greedy para compras
   - Complejidad: O(n² + nm log m)
   - Soluciones de calidad aproximada

## Autor

Trabajo desarrollado para el curso de Diseño y Análisis de Algoritmos, Universidad de La Habana, 2025-2026.
