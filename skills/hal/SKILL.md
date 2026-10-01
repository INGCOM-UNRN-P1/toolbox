---
name: hal
description: Use when diagnosing segfaults, core dumps, memory violations, or fatal signals (SIGSEGV, SIGABRT, SIGFPE) in C programs with pedagogical plain Spanish feedback.
---

# HAL — Asistente Forense de Core Dumps y Segfaults en C

HAL diagnostica fallos en tiempo de ejecución en programas C, traduciendo volcados y backtraces de GDB a explicaciones pedagógicas directas con ubicación exacta de la falla y acciones correctivas sugeridas.

## Cuándo usar HAL
- Alumnos con errores de `Segmentation fault (core dumped)`, `Aborted (core dumped)` o `Floating point exception`.
- Diagnosticar desreferencia de puntero `NULL` (`SEGV_MAPERR`), violaciones de acceso (`SEGV_ACCERR`), desbordamiento de pila por recursión infinita (`Stack Overflow`), divisiones por cero (`SIGFPE`) o `double free` (`SIGABRT`).

## Comandos Principales

```bash
# 1. Compilar, ejecutar y diagnosticar un archivo fuente C
hal run programa_fallido.c

# 2. Diagnosticar con salida estructurada JSON para pipelines CI
hal run programa_fallido.c --json

# 3. Pasar argumentos y datos por stdin
hal run programa.c arg1 arg2 --stdin "10\n20\n"

# 4. Inspeccionar un binario precompilado
hal inspect ./binario_compilado

# 5. Comprobar salud del entorno (GCC, GDB, Valgrind)
hal doctor

# 6. Modo pista para evaluaciones (o P1_PISTA=1): la falla y la función, sin la línea ni la corrección
hal check programa_fallido.c --pista
```
