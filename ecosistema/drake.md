# drake

Fuzzer pedagógico guiado por límites y analizador de cobertura dinámica en C

## 🎯 Propósito y Alcance

`drake` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/drake
```

## 🚀 Guía de Uso

### Invocación básica

```bash
drake --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: drake [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 ⚡ DRAKE — Fuzzer pedagógico guiado por límites y analizador de robustez en C. 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de DRAKE.                 │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ fuzz  Ejecuta fuzzing enviando payloads extremos y mutados a la entrada      │
│       estándar.                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`drake` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `drake`.

## 📖 Documentación y Detalles Técnicos

# ⚡ DRAKE — Fuzzer Pedagógico y Analizador de Límites en C

DRAKE es una herramienta de fuzzing liviana que genera entradas con valores límite (`INT_MAX`, `INT_MIN`, cadenas largas, carácteres nulos y mutaciones aleatorias) para poner a prueba la robustez de programas C y detectar segfaults antes de las entregas.

## Uso Rápido

```bash
# 1. Correr 50 iteraciones de fuzzing contra un programa C
drake fuzz main.c --runs 50

# 2. Salida estructurada JSON
drake fuzz main.c --runs 20 --json
```


## 📊 Formatos de Salida

`drake` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
