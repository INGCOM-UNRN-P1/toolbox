---
name: tyrell
description: Use when generating deterministic .in/.out test cases with constraints for C programs (nostromo test format).
---

# tyrell — Generador sintético y determinista de datasets y casos de prueba (.in/.out) con restricciones

**TYRELL** genera colecciones deterministas de casos de prueba (`.in` y `.out`) con restricciones configurables (enteros, flotantes, cadenas, arreglos y valores extremos) en el formato que lee `nostromo test <binario> <directorio>` (un `caso.in` y su `caso.out` por caso; hay un test de extremo a extremo que lo verifica). No hay integración automática con `deckard` ni con el resto de los orquestadores: los archivos se copian a mano al ejercicio o al banco que corresponda.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/tyrell
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `tyrell generate` | Genera casos de prueba .in (y .out con binario de referencia) deterministas. |
| `tyrell version` | Muestra la versión de TYRELL. |
| `tyrell doctor` | Verifica el estado del entorno de TYRELL (Python, GCC opcional). |

Ayuda de cada comando: `tyrell <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `tyrell doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
