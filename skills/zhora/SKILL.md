---
name: zhora
description: Use when auditing C preprocessor macros (#define) for multiple evaluation, missing parentheses and stray semicolons.
---

# zhora — Linter y auditor de seguridad en macros del preprocesador C (#define)

**ZHORA** audita macros del preprocesador C para detectar efectos de lado en evaluación múltiple de parámetros, falta de paréntesis defensivos en argumentos y cuerpos, y puntos y coma espurios.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/zhora
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `zhora check`, `zhora audit` | Audita macros #define en busca de efectos de lado, falta de paréntesis o puntos y coma. |
| `zhora report` | Genera directamente la sección de reporte Markdown de ZHORA para Dredd. |
| `zhora catalog`, `zhora rules` | Muestra el catálogo oficial de reglas de macros de ZHORA y su mapeo al namespace de cátedra. |
| `zhora doctor` | Verifica el estado del entorno de auditoría de macros ZHORA (Tree-Sitter C, Python). |

Ayuda de cada comando: `zhora <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `zhora doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
