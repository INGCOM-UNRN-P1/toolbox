---
name: wierzbowski
description: Use when auditing the #include graph, circular dependencies, include guards and Makefiles of a multi-file C project.
---

# wierzbowski — Auditor de grafos de inclusión de headers, dependencias circulares y Makefiles en C

**WIERZBOWSKI** analiza la arquitectura de proyectos multi-archivo en C, construyendo el grafo de dependencias de `#include`, detectando dependencias circulares, verificando guardas de inclusión y auditando Makefiles.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/wierzbowski
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `wierzbowski check`, `wierzbowski audit` | Audita dependencias entre cabeceras, ciclos de inclusión y Makefiles. |
| `wierzbowski report` | Genera directamente la sección de reporte Markdown de WIERZBOWSKI para Dredd. |
| `wierzbowski doctor` | Verifica el estado del entorno de auditoría de dependencias WIERZBOWSKI (Python, Make, GCC). |

Ayuda de cada comando: `wierzbowski <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `wierzbowski doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
