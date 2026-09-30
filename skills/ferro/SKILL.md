---
name: ferro
description: Use when profiling the running time of a C program over growing input sizes and estimating its empirical complexity.
---

# ferro — Perfilador de rendimiento algorítmico y hardware counters en C

**FERRO** ejecuta programas C a través de múltiples tamaños de entrada ($N$), midiendo el tiempo y las instrucciones ejecutadas (con Cachegrind) e infiriendo la complejidad temporal empírica ($O(N)$, $O(N \log N)$, $O(N^2)$).

## Instalación

```bash
uv tool install "ferro[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/ferro"
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `ferro check`, `ferro profile` | Mide tiempo de ejecución e instrucciones ejecutadas, y evalúa la complejidad empírica. |
| `ferro report` | Genera directamente la sección de reporte Markdown de FERRO para Dredd. |
| `ferro doctor` | Verifica el estado del entorno de perfilado de rendimiento FERRO (Python, GCC, perf/time). |
| `ferro version` | Muestra la versión de FERRO. |

Ayuda de cada comando: `ferro <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `ferro doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
