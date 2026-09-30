---
name: dietrich
description: Use when analyzing compound boolean decisions in C for MC/DC coverage and deriving the minimal test vectors.
---

# dietrich — Validador de cobertura lógica avanzada MC/DC (Modified Condition/Decision Coverage) en C

**DIETRICH** analiza las decisiones booleanas compuestas (`if (A && (B || C))`) en código fuente C, desglosa las condiciones atómicas y genera la tabla de verdad y los vectores de prueba mínimos ($k + 1$) requeridos para garantizar **Modified Condition/Decision Coverage (MC/DC)** al 100%.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/dietrich
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `dietrich check`, `dietrich analyze` | Analiza condiciones booleanas compuestas (&&, \|\|) y calcula los vectores de prueba requeridos para MC/DC. |
| `dietrich report` | Genera directamente la sección de reporte Markdown de DIETRICH para Dredd. |
| `dietrich doctor` | Verifica el estado del entorno de análisis MC/DC de DIETRICH. |
| `dietrich version` | Muestra la versión de DIETRICH. |

Ayuda de cada comando: `dietrich <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `dietrich doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
