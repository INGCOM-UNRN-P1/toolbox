---
name: parker
description: Use when auditing the ABI and symbol visibility of C shared libraries, object files and headers.
---

# parker — Auditor de estabilidad de ABIs, visibilidad de símbolos y compatibilidad binaria en C

**PARKER** es un linter y evaluador de interfaces binarias (ABI) en C. Audita bibliotecas compartidas (`.so`), archivos objeto (`.o`) y cabeceras (`.h`) para detectar fugas de símbolos privados, símbolos faltantes y malas prácticas en interfaces públicas.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/parker
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `parker check`, `parker audit` | Audita la cabecera (o todas las de un directorio) y contrasta los símbolos exportados por los binarios. |
| `parker report` | Genera directamente la sección de reporte Markdown de PARKER para Dredd. |
| `parker doctor` | Verifica el estado del entorno de auditoría ABI PARKER (Python, nm, GCC). |

Ayuda de cada comando: `parker <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `parker doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
