---
name: motoko
description: Use when checking encapsulation of C abstract data types (opaque types, client code touching internal fields).
---

# motoko — Verificador de encapsulamiento estricto y opacidad de Tipos Abstractos de Datos (TDAs) en C

**MOTOKO** analiza archivos de cabecera e implementaciones en C para asegurar el ocultamiento de información y encapsulamiento estricto de Tipos Abstractos de Datos (TDAs), detectando accesos directos a campos internos desde código cliente.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/motoko
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `motoko audit-all`, `motoko check`, `motoko verify` | Verifica que los TDAs sean opacos y no sufran accesos directos a sus campos internos. |
| `motoko report` | Genera directamente la sección de reporte Markdown de MOTOKO para Dredd. |
| `motoko doctor` | Verifica el estado del entorno de auditoría de TDAs MOTOKO (Tree-Sitter C, Python, GCC). |

Ayuda de cada comando: `motoko <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `motoko doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
