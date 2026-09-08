# holden

Generador de mocks e inyección controlada de fallos en funciones C

## 🎯 Propósito y Alcance

`holden` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/holden
```

## 🚀 Guía de Uso

### Invocación básica

```bash
holden --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: holden [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 💉 HOLDEN — Generador de mocks e inyección controlada de fallos en funciones C 
 (malloc, fopen, etc.).                                                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de HOLDEN.                │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ generate  Genera un archivo C con la implementación del mock y wrapper de la │
│           función.                                                           │
│ list      Lista las funciones con soporte de mocks preconfigurados.          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`holden` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `holden`.

## 📖 Documentación y Detalles Técnicos

# 💉 HOLDEN — Generador de Mocks e Inyección de Fallos en C

HOLDEN permite generar mocks y envoltorios de enlace (`-Wl,--wrap=symbol`) para simular condiciones adversas de ejecución en pruebas de software C (fallos de `malloc()`, errores de apertura en `fopen()`, generación pseudoaleatoria determinista).

## Uso Rápido

```bash
# 1. Generar mock de malloc que falla en la 2da llamada
holden generate malloc --fail-at 2 -o mock_malloc.c

# 2. Salida estructurada JSON
holden generate malloc --json

# 3. Listar funciones mockeables soportadas
holden list
```


## 📊 Formatos de Salida

`holden` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
