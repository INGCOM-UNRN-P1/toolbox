---
name: rachel
description: Use when disassembling, analyzing, or visualizing control flow structures (switch vs if-else chains, jump tables) in C, or comparing computational complexity and branch prediction costs.
---

# RACHEL — Desensamblador y Visualizador de Jump Tables en C

RACHEL analiza sentencias `switch` y cadenas de `if-else` en C, desensamblando las tablas de salto (`Jump Tables`) generadas por el compilador y renderizando diagramas de flujo interactivos.

## Cuándo usar RACHEL
- Analizar cómo compila GCC una sentencia `switch` (Jump Table $O(1)$, Árbol Binario $O(\log N)$ o Comparación Secuencial $O(N)$).
- Comparar el rendimiento y coste de memoria entre `switch` y cadenas de `if-else`.
- Generar diagramas de flujo Mermaid de bifurcaciones complejas.

## Comandos Principales

```bash
# 1. Analizar e inspeccionar switches en un archivo C
rachel switch parser.c

# 2. Emitir diagrama de flujo en sintaxis Mermaid
rachel switch parser.c --mermaid

# 3. Comparar costo temporal y de memoria entre switch e if-else
rachel compare parser.c

# 4. Salida estructurada JSON
rachel switch parser.c --json
```
