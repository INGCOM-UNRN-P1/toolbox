# corbel

Generador liviano de documentación de APIs, TDAs y man pages (man 3) en C

## 🎯 Propósito y Alcance

`corbel` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/corbel
```

## 🚀 Guía de Uso

### Invocación básica

```bash
corbel --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: corbel [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 Generador liviano de documentación de APIs, TDAs, man pages (man 3) y          
 scaffolding de comentarios en C                                                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ doc       Genera documentación a partir de comentarios estructurados o       │
│           inyecta placeholders en cabeceras C.                               │
│ stub      Agrega placeholders estructurados de documentación (@brief,        │
│           @param, @return, @pre, @post)                                      │
│           a todas las funciones, estructuras, uniones, enumeraciones y tipos │
│           indocumentados.                                                    │
│ scaffold  Agrega placeholders estructurados de documentación (@brief,        │
│           @param, @return, @pre, @post)                                      │
│           a todas las funciones, estructuras, uniones, enumeraciones y tipos │
│           indocumentados.                                                    │
│ lint      Audita e informa todos los elementos C que carecen de comentarios  │
│           Doxygen.                                                           │
│ check     Audita e informa todos los elementos C que carecen de comentarios  │
│           Doxygen.                                                           │
│ version   Muestra la versión de CORBEL.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`corbel` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `corbel`.

## 📖 Documentación y Detalles Técnicos

# CORBEL — Generador Liviano de Documentación y man pages (man 3) en C

**CORBEL** extrae comentarios estructurados Doxygen (`@brief`, `@param`, `@return`, `@pre`, `@post`) desde cabeceras C (`.h`) y genera páginas estáticas en Markdown o páginas de manual para terminal (`man 3 <modulo>`).

---

## 🚀 Uso Rápido

```bash
# Visualizar documentación en terminal
corbel doc tda_lista.h

# Exportar a Markdown
corbel doc tda_lista.h --format markdown -o LISTA_API.md

# Generar página man 3 para UNIX
corbel doc tda_lista.h --format man -o /usr/local/man/man3/tda_lista.3
```


## 📊 Formatos de Salida

`corbel` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
