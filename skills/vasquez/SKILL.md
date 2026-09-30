---
name: vasquez
description: Use when testing how a C program handles failing malloc/calloc/realloc/fopen/fwrite (fault injection).
---

# vasquez — Motor de inyección de fallos de entorno y hardware (Fault Injection Engine) en C vía LD_PRELOAD

**VASQUEZ** intercepta llamadas estándar a la biblioteca de C (`malloc`, `calloc`, `realloc`, `strdup`, `fopen`, `fwrite`, `fread`, `fclose`) mediante `LD_PRELOAD` para inyectar fallos deterministas en tiempo de ejecución (retornos `NULL` o códigos de error simulando falta de memoria o accesos denegados a disco), verificando si el estudiante implementó manejo defensivo de errores o si el programa sufre un `SIGSEGV`.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/vasquez
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `vasquez check`, `vasquez inject` | Inyecta fallos controlados (malloc/calloc/realloc NULL, cascada, memoria basura) evaluando la resiliencia del código C. |
| `vasquez stress` | Ejecuta una prueba de estrés repetitiva con fallos probabilísticos de asignación. |
| `vasquez doctor` | Audita el entorno y verifica la disponibilidad del compilador y la librería de inyección. |
| `vasquez report` | Genera directamente la sección de reporte Markdown de VASQUEZ para Dredd. |
| `vasquez version` | Muestra la versión de VASQUEZ. |

Ayuda de cada comando: `vasquez <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `vasquez doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
