---
name: holden
description: Use when generating C function mocks or injecting memory allocation / file errors (malloc returning NULL, fopen failing, deterministic rand seeds).
---

# HOLDEN — Generador de Mocks e Inyección de Fallos en C

HOLDEN genera envoltorios de enlace (`-Wl,--wrap=symbol`) para simular fallos de memoria (`malloc() == NULL`), errores de archivo y secuencias deterministas en tests C.

## Comandos Principales

```bash
# Generar mock de malloc que falla en la llamada N
holden generate malloc --fail-at 2 -o mock_malloc.c

# Salida estructurada JSON
holden generate malloc --json

# Listar funciones soportadas
holden list
```
