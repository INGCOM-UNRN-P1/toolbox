---
name: daedalus
description: Use when compiling C code under strict cátedra flags or translating compiler errors from GCC, Clang, or ld into pedagogical plain Spanish explanations.
---

# DAEDALUS — Compilador Pedagógico y Traductor GCC/Clang

DAEDALUS compila programas C bajo flags estrictos (`-std=c11 -Wall -Wextra -pedantic -Wconversion`) y traduce los mensajes crudos de error a explicaciones didácticas en español rioplatense.

## Comandos Principales

```bash
# Compilar código y traducir diagnósticos
daedalus compile main.c -o ./programa

# Salida estructurada JSON
daedalus compile main.c --json

# Traducir archivo de log crudo de compilador
daedalus translate stderr.log

# Modo pista para evaluaciones (o P1_PISTA=1): el tipo de error y la función, sin la línea ni la corrección
daedalus compile main.c --pista

# Comprobar toolchain
daedalus doctor
```
