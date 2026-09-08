---
name: spunkmeyer
description: Use when detecting educational C antipatterns (malloc casts, while(!feof()), dangling stack pointers, redundant NULL checks before free, redundant boolean comparisons).
---

# SPUNKMEYER — Detector de Antipatrones Didácticos en C

SPUNKMEYER identifica vicios comunes en estudiantes de C (`(int*)malloc()`, `while(!feof())`, retorno de punteros a variables locales en Stack, chequeos innecesarios antes de `free()`).

## Comandos Principales

```bash
# Detectar antipatrones
spunkmeyer detect src/ main.c

# Salida estructurada JSON
spunkmeyer detect src/ --json

# Ver catálogo completo
spunkmeyer catalog
```
