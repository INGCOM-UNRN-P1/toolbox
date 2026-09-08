---
name: nostromo
description: Use when executing C binaries in an isolated sandbox (Bubblewrap / setrlimit) with CPU/memory limits or evaluating suites of .in/.out testcases.
---

# NOSTROMO — Sandbox de Ejecución Aislada y Test Runner

NOSTROMO provee ejecución aislada segura en sandbox con límites estrictos de CPU y memoria, y evalúa automáticamente casos de prueba `.in` / `.out` con reporte de diffs unificados.

## Comandos Principales

```bash
# Correr binario en sandbox con límites
nostromo run ./programa --timeout 1.5 --memory 64

# Evaluar suite de casos de prueba
nostromo test ./programa ./testcases/

# Salida estructurada JSON
nostromo test ./programa ./testcases/ --json
```
