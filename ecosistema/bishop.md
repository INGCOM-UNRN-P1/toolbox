# bishop

Visualizador pedagógico de memoria C (Stack, Heap y punteros) en terminal y diagramas

## 🎯 Propósito y Alcance

`bishop` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "bishop[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/bishop"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
bishop --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/bishop#referencia-rápida), generada desde `bishop --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `bishop <comando> -h`.

## ⚙️ Configuración y Opciones

`bishop` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `bishop`.

## 📖 Documentación y Detalles Técnicos

# 🧠 BISHOP — Visualizador Pedagógico de Memoria C

BISHOP es una herramienta standalone diseñada para inspeccionar y visualizar el estado vivo de la memoria (Stack Frames, variables locales, direcciones y bloques asignados en el Heap) en programas C, renderizando diagramas ASCII interactivos en terminal y diagramas Mermaid.

## Uso Rápido

```bash
# 1. Trazar ejecución e inspeccionar memoria en breakpoint
bishop trace main.c --break invertir_vector

# 2. Emitir diagrama de punteros en sintaxis Mermaid
bishop trace main.c --mermaid

# 3. Tomar una foto del estado de memoria en una línea específica
bishop snapshot main.c --line 25

# 4. Auditar bloques activos en Heap y detectar punteros huérfanos
bishop heap main.c

# 5. Salida estructurada JSON
bishop trace main.c --json
```


## 📊 Formatos de Salida

`bishop` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
