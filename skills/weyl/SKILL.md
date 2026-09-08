---
name: weyl
description: Use when performing semantic diffing, AST structural comparison, or identifying missing/added/modified C functions between student submissions and canonical solutions.
---

# WEYL — Diffing Semántico y Comparación AST en C

WEYL compara semánticamente dos archivos de código C función por función, abstrayendo diferencias de espaciado para identificar qué funciones fueron agregadas, eliminadas o modificadas.

## Comandos Principales

```bash
# Comparar entrega contra solución modelo
weyl diff estudiante.c modelo.c

# Salida estructurada JSON
weyl diff estudiante.c modelo.c --json
```
