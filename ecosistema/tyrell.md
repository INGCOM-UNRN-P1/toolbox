# tyrell

Generador sintético y determinista de datasets y casos de prueba (.in/.out) con restricciones

## 🎯 Propósito y Alcance

`tyrell` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/tyrell
```

## 🚀 Guía de Uso

### Invocación básica

```bash
tyrell --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: tyrell [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 Generador sintético y determinista de datasets y casos de prueba (.in/.out)    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ generate  Genera casos de prueba .in (y .out con binario de referencia)      │
│           deterministas.                                                     │
│ version   Muestra la versión de TYRELL.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`tyrell` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `tyrell`.

## 📖 Documentación y Detalles Técnicos

# TYRELL — Generador Sintético de Datasets y Casos de Prueba (.in/.out)

**TYRELL** genera colecciones deterministas de casos de prueba (`.in` y `.out`) con restricciones configurables (enteros, flotantes, cadenas, arreglos y valores extremos) para alimentar el banco de testcases de `deckard` y `nostromo`.

---

## 🚀 Uso Rápido

```bash
# Generar 20 casos de enteros deterministas
tyrell generate -n 20 --min 1 --max 1000 -o tests/

# Generar casos y contrastar contra binario de referencia para crear los .out
tyrell generate -n 10 -o tests/ --reference ./solucion_canon

# Generar a partir de especificación YAML
tyrell generate spec.yaml -o tests/
```


## 📊 Formatos de Salida

`tyrell` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
