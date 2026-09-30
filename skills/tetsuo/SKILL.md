---
name: tetsuo
description: Use when running C programs under AddressSanitizer/UBSan and explaining the sanitizer reports in Spanish.
---

# tetsuo — Traductor y explicador pedagógico en español de sanitizers (ASan, UBSan, LSan)

**TETSUO** compila y ejecuta programas C bajo AddressSanitizer y UndefinedBehaviorSanitizer, interceptando sus salidas complejas en inglés y traduciéndolas a diagnósticos formativos en español con sugerencias concretas de corrección.

## Instalación

```bash
uv tool install "tetsuo[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/tetsuo"
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `tetsuo check`, `tetsuo run` | Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier violación a español didáctico. |
| `tetsuo report` | Genera directamente la sección de reporte Markdown de TETSUO para Dredd. |
| `tetsuo doctor` | Verifica el estado del entorno de sanitizers TETSUO (GCC, Clang, soporte libasan/libubsan). |
| `tetsuo version` | Muestra la versión de TETSUO. |

Ayuda de cada comando: `tetsuo <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `tetsuo doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
