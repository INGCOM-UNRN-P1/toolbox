# rachel

Desensamblador y visualizador pedagógico de estructuras de control y jump tables en C

## 🎯 Propósito y Alcance

`rachel` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/rachel
```

## 🚀 Guía de Uso

### Invocación básica

```bash
rachel --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/rachel#referencia-rápida), generada desde `rachel --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `rachel <comando> -h`.

## ⚙️ Configuración y Opciones

`rachel` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `rachel`.

## 📖 Documentación y Detalles Técnicos

# ⚡ RACHEL — Desensamblador y Visualizador de Jump Tables en C

RACHEL es una herramienta pedagógica diseñada para analizar sentencias `switch` y cadenas de `if-else` en C, desensamblando las tablas de salto (`Jump Tables`) generadas por el compilador y renderizando diagramas de flujo interactivos.

## Uso Rápido

```bash
# 1. Analizar e inspeccionar switches en un archivo C
rachel switch parser.c

# 2. Emitir diagrama de flujo en sintaxis Mermaid
rachel switch parser.c --mermaid

# 3. Comparar costo temporal y de memoria entre switch e if-else
rachel compare parser.c

# 4. Salida estructurada JSON
rachel switch parser.c --json
```


## 📊 Formatos de Salida

`rachel` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
