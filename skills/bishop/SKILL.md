---
name: bishop
description: Use when tracing, inspecting, or visualizing C memory (Stack Frames, local variables, pointer relationships, and dynamic Heap allocations with malloc/free) in ASCII terminal tables or Mermaid diagrams.
---

# BISHOP — Visualizador Pedagógico de Memoria C

BISHOP inspecciona y visualiza el estado vivo de la memoria (Stack Frames, variables locales, direcciones y bloques asignados en el Heap) en programas C, renderizando diagramas ASCII interactivos y diagramas Mermaid.

## Cuándo usar BISHOP
- Ayudar a los alumnos a visualizar el Stack de ejecución y la memoria dinámica (Heap).
- Mostrar diagramas de punteros simples, dobles o punteros a estructuras.
- Auditar bloques asignados con `malloc`/`calloc` y detectar punteros huérfanos o fugas de memoria (leaks).

## Comandos Principales

```bash
# 1. Trazar ejecución e inspeccionar memoria en breakpoint
bishop trace main.c --break invertir_vector

# 2. Emitir diagrama de punteros en sintaxis Mermaid
bishop trace main.c --mermaid

# 3. Tomar una foto del estado de memoria en una línea específica
bishop snapshot main.c --line 25

# 4. Auditar bloques activos en Heap y detectar punteros huérfanos
bishop heap main.c

# 5. Salida estructurada JSON
bishop trace main.c --json
```
