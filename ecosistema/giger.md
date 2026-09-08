# giger

Generador de grafos de flujo de control (CFG) y mapas de llamadas (Call Graphs) en C

## 🎯 Propósito y Alcance

`giger` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/giger
```

## 🚀 Guía de Uso

### Invocación básica

```bash
giger --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: giger [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 🕸️ GIGER — Generador de grafos de flujo de control (CFG) y mapas de llamadas   
 (Call Graphs) en C.                                                            
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de GIGER.                 │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ callgraph  Construye el mapa de llamadas entre funciones y detecta recursión │
│            y código muerto.                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`giger` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `giger`.

## 📖 Documentación y Detalles Técnicos

# 🕸️ GIGER — Generador de Mapas de Llamadas y Grafos de Control en C

GIGER analiza el código fuente en C para construir el mapa estático de llamadas entre funciones (Call Graph), detectar ciclos recursivos, funciones no invocadas (*dead code*) y exportar diagramas en sintaxis Mermaid.

## Uso Rápido

```bash
# 1. Analizar e imprimir mapa de llamadas
giger callgraph main.c

# 2. Exportar diagrama en sintaxis Mermaid
giger callgraph main.c --mermaid

# 3. Salida estructurada JSON
giger callgraph main.c --json
```


## 📊 Formatos de Salida

`giger` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
