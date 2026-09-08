---
name: kaneda
description: Use when auditing C code for security vulnerabilities, buffer overflows (gets, strcpy, sprintf, scanf format), format strings, or restricted syscalls.
---

# KANEDA — Auditor de Seguridad y Funciones Inseguras en C

KANEDA audita código C detectando tempranamente funciones inseguras (`gets`, `strcpy`, `sprintf`), vulnerabilidades de Format String y llamadas a sistema no autorizadas.

## Comandos Principales

```bash
# Auditar seguridad en archivos C
kaneda audit src/ main.c

# Salida estructurada JSON
kaneda audit src/ --json

# Ver catálogo de reglas
kaneda rules
```
