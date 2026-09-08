---
name: drake
description: Use when running boundary-guided fuzzing or testing robustness against extreme payloads (INT_MAX, INT_MIN, buffer overruns) in C programs.
---

# DRAKE — Fuzzer Pedagógico y Analizador de Límites en C

DRAKE somete programas C a entradas límite extremas y mutaciones aleatorias para detectar segfaults y vulnerabilidades en tiempo de ejecución.

## Comandos Principales

```bash
# Correr fuzzing contra un programa
drake fuzz main.c --runs 50

# Salida estructurada JSON
drake fuzz main.c --runs 20 --json
```
