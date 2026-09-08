# ferro

Perfilador de rendimiento algorítmico y hardware counters en C

## 🎯 Propósito y Alcance

`ferro` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/ferro
```

## 🚀 Guía de Uso

### Invocación básica

```bash
ferro --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: ferro [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 Perfilador de rendimiento algorítmico y hardware counters en C                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ profile  Mide tiempo de ejecución, ciclos estimados y evalúa complejidad     │
│          empírica vs teórica.                                                │
│ version  Muestra la versión de FERRO.                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`ferro` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `ferro`.

## 📖 Documentación y Detalles Técnicos

# FERRO — Perfilador de Rendimiento Algorítmico y Hardware Counters en C

**FERRO** ejecuta programas C a través de múltiples tamaños de entrada ($N$), midiendo tiempos de alta resolución, ciclos de CPU estimados, throughput e infiriendo la complejidad temporal empírica ($O(N)$, $O(N \log N)$, $O(N^2)$).

---

## 🚀 Uso Rápido

```bash
# Perfilar algoritmo con diferentes tamaños de entrada
ferro profile ordenamiento.c --inputs "1000,10000,50000"

# Salida estructurada JSON
ferro profile ordenamiento.c --json
```


## 📊 Formatos de Salida

`ferro` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
