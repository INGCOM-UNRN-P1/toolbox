---
name: corbel
description: Use when generating API/ADT documentation (Markdown or man 3 pages) from Doxygen comments in C headers.
---

# corbel — Generador liviano de documentación de APIs, TDAs y man pages (man 3) en C

**CORBEL** extrae comentarios estructurados Doxygen (`@brief`, `@param`, `@return`, `@pre`, `@post`) desde cabeceras C (`.h`) y genera páginas estáticas en Markdown o páginas de manual para terminal (`man 3 <modulo>`).

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/corbel
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `corbel doc` | Genera documentación a partir de comentarios estructurados o inyecta placeholders en cabeceras C. |
| `corbel stub`, `corbel scaffold` | Agrega placeholders estructurados de documentación (@brief, @param, @return, @pre, @post) a todas las funciones, estructuras, uniones, enumeraciones y tipos indocumentados. |
| `corbel lint`, `corbel check` | Audita e informa todos los elementos C que carecen de comentarios Doxygen. |
| `corbel report` | Genera directamente la sección de reporte Markdown de CORBEL para Dredd. |
| `corbel doctor` | Verifica el estado del entorno de documentación CORBEL (Python, man). |
| `corbel version` | Muestra la versión de CORBEL. |

Ayuda de cada comando: `corbel <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `corbel doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
