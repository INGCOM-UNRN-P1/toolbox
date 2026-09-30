# giger

Generador de grafos de flujo de control (CFG) y mapas de llamadas (Call Graphs) en C

## 🎯 Propósito y Alcance

`giger` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/giger
```

## 🚀 Guía de Uso

### Invocación básica

```bash
giger --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/giger#referencia-rápida), generada desde `giger --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `giger <comando> -h`.

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
