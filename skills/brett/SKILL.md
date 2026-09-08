---
name: brett
description: Use when auditing struct memory layout, calculating wasted padding bytes, or generating optimized field reordering in C structs.
---

# BRETT — Auditor de Padding y Alineación de Structs en C

BRETT analiza la disposición en memoria (`Memory Layout`) de tipos `typedef struct`, calcula los bytes de padding desperdiciados y genera sugerencias de reordenamiento de campos para minimizar el consumo de memoria.

## Comandos Principales

```bash
# Auditar padding en archivos C/H
brett audit src/ main.h

# Optimizar struct
brett optimize tipos.h

# Salida estructurada JSON
brett audit src/ --json
```
