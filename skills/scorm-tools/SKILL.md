---
name: scorm-tools
description: Use when creating, packaging or validating SCORM 1.2/2004 content for Moodle.
---

# scorm-tools — Herramientas para crear, empaquetar y validar contenido SCORM (1.2 / 2004) para Moodle

Herramientas de línea de comandos, gestionadas con [`uv`](https://docs.astral.sh/uv/), para crear, gestionar y validar contenido compatible con el estándar **SCORM** (1.2 y 2004 3ra/4ta edición), listo para integrarse en plataformas LMS como **Moodle**.

## Instalación

```bash
uv tool install "scorm-tools[ecosistema] @ git+https://github.com/INGCOM-UNRN/scorm-tools"
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `scorm-tools doctor` | Verificá el estado del entorno, dependencias y esquemas XSD de scorm-tools. |
| `scorm-tools init` | Creá un curso SCORM de ejemplo listo para editar. |
| `scorm-tools build` | Generá imsmanifest.xml y empaquetá el curso en un .zip para Moodle. |
| `scorm-tools validate` | Validá un paquete SCORM contra el esquema XSD y reglas de Moodle (`--a11y`: también la accesibilidad de sus páginas HTML). |
| `scorm-tools info` | Mostrá un resumen de la estructura del curso definida en scorm.yaml. |
| `scorm-tools check-sequencing` | Verificá el grafo de secuenciamiento IMSSS y detectá ciclos o actividades huérfanas. |
| `scorm-tools check-size` | Audita el peso del paquete y su desglose por tipo de contenido para Moodle. |
| `scorm-tools moodle-config` | Generá la configuración recomendada de actividad Moodle (moodle_settings.json). |
| `scorm-tools from-deckard` | Convertí una guía de ejercicios de Deckard a un curso SCORM interactivo. |
| `scorm-tools from-gift` | Convertí un banco de preguntas GIFT (Moodle) en un módulo SCORM interactivo autoevaluable. |
| `scorm-tools audit-c` | Auditá fragmentos de código C embebidos en el contenido SCORM contra reglas Ripley. |
| `scorm-tools dredd-sync` | Procesá registros de tracking de Moodle SCORM para integrarlos al calificador docente Dredd. |
| `scorm-tools diagram-memory` | Generá un diagrama Mermaid de memoria Stack y Heap (Bishop/Sebastian) para lecciones SCORM. |
| `scorm-tools from-idkfa` | Convertí una plantilla de tracing C de IDKFA a una lección interactiva SCORM autoevaluable. |
| `scorm-tools playground` | Generá un módulo SCORM interactivo con compilador C WebAssembly en el navegador. |

Ayuda de cada comando: `scorm-tools <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `scorm-tools doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
