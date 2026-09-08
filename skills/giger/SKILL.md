---
name: giger
description: Use when analyzing or visualizing C Call Graphs, Control Flow Graphs (CFG), recursion cycles, or detecting uncalled dead functions.
---

# GIGER — Generador de Mapas de Llamadas y Grafos de Control en C

GIGER construye el mapa estático de llamadas entre funciones (Call Graph), detecta ciclos recursivos, funciones no invocadas (*dead code*) y exporta diagramas Mermaid.

## Comandos Principales

```bash
# Analizar mapa de llamadas
giger callgraph main.c

# Exportar diagrama Mermaid
giger callgraph main.c --mermaid

# Salida estructurada JSON
giger callgraph main.c --json
```
