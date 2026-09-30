---
name: vassili
description: Use when measuring the quality of a C test suite with mutation testing (mutation score).
---

# vassili — Motor de Mutation Testing en C para evaluación de calidad y robustez de suites de tests

**VASSILI** evalúa la calidad y exhaustividad real de las suites de prueba de los estudiantes mediante la inyección procedural de mutantes sintéticos en el código fuente C (operadores aritméticos, relacionales y lógicos) y calcula el **Mutation Score** (% de mutantes detectados).

## Instalación

```bash
uv tool install "vassili[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/vassili"
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `vassili check`, `vassili mutate` | Genera mutantes sintéticos del código C y evalúa qué porcentaje es detectado por los tests. |
| `vassili report` | Genera directamente la sección de reporte Markdown de VASSILI para Dredd. |
| `vassili version` | Muestra la versión de VASSILI. |
| `vassili doctor` | Verifica el estado del entorno de VASSILI (Python, GCC). |

Ayuda de cada comando: `vassili <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `vassili doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
