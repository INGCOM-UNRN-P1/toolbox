---
name: crowe
description: Use when checking C code for non-portable hardware assumptions (endianness, pointer and long sizes, char signedness) or cross-compiling for x86_64, aarch64 and riscv64.
---

# crowe — Linter de portabilidad multi-arquitectura (x86_64, ARM, RISC-V, endianness) en C

**CROWE** analiza código C para detectar asunciones no portables de hardware (endianness, tamaños fijos de punteros, signo de `char`, VLAs y tamaños de `long`) y opcionalmente valida compilación cruzada para `x86_64`, `aarch64` y `riscv64`.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/crowe
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `crowe lint` | Analiza archivos C buscando asunciones no portables de hardware y endianness. |
| `crowe check` | Gate de portabilidad: lint + verificación multi-arquitectura (lo que invoca ripley). |
| `crowe report` | Genera directamente la sección de reporte Markdown de CROWE para Dredd. |
| `crowe doctor` | Verifica el estado del entorno de auditoría de portabilidad CROWE (Python, GCC nativo y cross-compiladores). |

Ayuda de cada comando: `crowe <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `crowe doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
