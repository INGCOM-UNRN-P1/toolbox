# vassili

Motor de Mutation Testing en C para evaluación de calidad y robustez de suites de tests

## 🎯 Propósito y Alcance

`vassili` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "vassili[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/vassili"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
vassili --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: vassili [OPTIONS] COMMAND [ARGS]...                                     
                                                                                
 Motor de Mutation Testing en C para evaluar la efectividad de los tests        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ mutate   Genera mutantes sintéticos del código C y evalúa qué porcentaje es  │
│          detectado por los tests.                                            │
│ version  Muestra la versión de VASSILI.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`vassili` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `vassili`.

## 📖 Documentación y Detalles Técnicos

# VASSILI — Motor de Mutation Testing en C

**VASSILI** evalúa la calidad y exhaustividad real de las suites de prueba de los estudiantes mediante la inyección procedural de mutantes sintéticos en el código fuente C (operadores aritméticos, relacionales y lógicos) y calcula el **Mutation Score** (% de mutantes detectados).

---

## 🚀 Uso Rápido

```bash
# Ejecutar análisis de mutación sobre un archivo C con testcases
vassili mutate solucion_alumno.c --tests-dir tests/

# Exigir un Mutation Score mínimo del 80%
vassili mutate solucion_alumno.c --tests-dir tests/ --min-score 80

# Salida estructurada JSON
vassili mutate solucion_alumno.c --tests-dir tests/ --json
```

---

## 🔬 Operadores de Mutación

- **`AOR`** (Arithmetic Operator Replacement): `+` ➔ `-`, `*` ➔ `/`.
- **`ROR`** (Relational Operator Replacement): `==` ➔ `!=`, `<` ➔ `<=`, `>` ➔ `>=`.
- **`LCR`** (Logical Connector Replacement): `&&` ➔ `||`.


## 📊 Formatos de Salida

`vassili` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
