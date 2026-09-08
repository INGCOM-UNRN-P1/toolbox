# weyl

Herramienta de diffing semántico y comparación estructural AST entre códigos C

## 🎯 Propósito y Alcance

`weyl` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/weyl
```

## 🚀 Guía de Uso

### Invocación básica

```bash
weyl --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: weyl [OPTIONS] COMMAND [ARGS]...                                        
                                                                                
 ⚖️ WEYL — Herramienta de diffing semántico y comparación estructural AST entre 
 códigos C.                                                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de WEYL.                  │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ diff  Compara semánticamente ambos códigos función por función.              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`weyl` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `weyl`.

## 📖 Documentación y Detalles Técnicos

# ⚖️ WEYL — Diffing Semántico y Comparación AST en C

WEYL compara semánticamente dos archivos de código fuente C función por función, abstrayendo diferencias de espaciado para identificar qué funciones fueron agregadas, eliminadas o modificadas respecto a la solución modelo.

## Uso Rápido

```bash
# 1. Comparar entrega de estudiante contra solución modelo
weyl diff estudiante.c modelo.c

# 2. Salida estructurada JSON
weyl diff estudiante.c modelo.c --json
```


## 📊 Formatos de Salida

`weyl` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
