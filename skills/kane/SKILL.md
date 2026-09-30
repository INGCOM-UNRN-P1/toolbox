---
name: kane
description: Use when inspecting binary files written by C programs (fread/fwrite) mapped to struct layouts.
---

# kane — Simulador y depurador visual de I/O de bajo nivel y archivos binarios en C

**KANE** inspecciona archivos binarios generados por programas C (`fread`, `fwrite`), desglosando sus registros en tablas legibles mapeadas a definiciones de `struct` C con offsets hexadecimales y detección de bytes truncados.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/kane
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `kane check`, `kane inspect` | Inspecciona y desglosa el contenido de un archivo binario mapeándolo a un struct C. |
| `kane report` | Genera directamente la sección de reporte Markdown de KANE para Dredd. |
| `kane doctor` | Verifica el estado del entorno de inspección binaria KANE (Python, xxd/hexdump, GCC). |

Ayuda de cada comando: `kane <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `kane doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
