---
name: sebastian
description: Use when analyzing recursive functions in C, profiling stack frame memory consumption, detecting stack overflow risks, or rendering call trees in ASCII or Mermaid diagrams.
---

# SEBASTIAN — Analizador de Recursión y Stack Frame en C

SEBASTIAN analiza algoritmos recursivos en C, mide el consumo de memoria en la pila de ejecución (Stack), detecta riesgos de `Stack Overflow` y renderiza árboles de ejecución interactivos.

## Cuándo usar SEBASTIAN
- Analizar funciones recursivas para detectar tipo de recursión (lineal, de cola / tail, múltiple / árbol).
- Comprobar la presencia y correctitud del caso base.
- Calcular la profundidad máxima de llamadas y el consumo pico de Stack en bytes.
- Generar diagramas Mermaid o árboles visuales del flujo de ejecución recursiva.

## Comandos Principales

```bash
# 1. Trazar ejecución recursiva y renderizar árbol en terminal
sebastian trace factorial.c --function factorial

# 2. Emitir diagrama en sintaxis Mermaid
sebastian trace fibonacci.c --mermaid

# 3. Analizar estáticamente todas las funciones de un archivo
sebastian analyze algoritmo.c

# 4. Salida estructurada JSON para pipelines CI
sebastian trace factorial.c --json
```
