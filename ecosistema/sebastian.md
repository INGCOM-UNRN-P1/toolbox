# sebastian

Analizador de llamadas recursivas, consumo de stack frame y riesgos de stack overflow en C

## 🎯 Propósito y Alcance

`sebastian` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/sebastian
```

## 🚀 Guía de Uso

### Invocación básica

```bash
sebastian --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: sebastian [OPTIONS] COMMAND [ARGS]...                                   
                                                                                
 🌀 SEBASTIAN — Analizador de llamadas recursivas, consumo de stack frame y     
 riesgos de stack overflow en C.                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de SEBASTIAN.             │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ trace    Ejecuta el código instrumentado, traza las llamadas recursivas y    │
│          visualiza el árbol de ejecución.                                    │
│ analyze  Analiza estáticamente todas las funciones del archivo en busca de   │
│          recursión y riesgos de desbordamiento.                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`sebastian` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `sebastian`.

## 📖 Documentación y Detalles Técnicos

# 🌀 SEBASTIAN — Analizador de Recursión y Stack Frame en C

SEBASTIAN es una herramienta pedagógica diseñada para analizar algoritmos recursivos en C, medir el consumo de memoria en la pila de ejecución (Stack), detectar riesgos de `Stack Overflow` y renderizar árboles de ejecución interactivos en terminal y diagramas Mermaid.

## Uso Rápido

```bash
# 1. Trazar ejecución recursiva y renderizar árbol en terminal
sebastian trace factorial.c --function factorial

# 2. Emitir diagrama en sintaxis Mermaid
sebastian trace fibonacci.c --mermaid

# 3. Analizar estáticamente todas las funciones de un archivo
sebastian analyze algoritmo.c

# 4. Salida estructurada JSON para pipelines CI
sebastian trace factorial.c --json
```


## 📊 Formatos de Salida

`sebastian` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
