# daedalus

Compilador C pedagógico y traductor de diagnósticos de GCC/Clang/ld a español rioplatense

## 🎯 Propósito y Alcance

`daedalus` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/daedalus
```

## 🚀 Guía de Uso

### Invocación básica

```bash
daedalus --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: daedalus [OPTIONS] COMMAND [ARGS]...                                    
                                                                                
 🛠️ DAEDALUS — Compilador C pedagógico y traductor de diagnósticos GCC/Clang/ld 
 a español rioplatense.                                                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de DAEDALUS.              │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ compile    Compila código C con banderas estrictas de cátedra y traduce      │
│            errores a español didáctico.                                      │
│ translate  Traduce un bloque de texto o log de compilador a diagnósticos     │
│            didácticos.                                                       │
│ doctor     Verifica disponibilidad de herramientas del toolchain (GCC,       │
│            Clang, Make, ld).                                                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`daedalus` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `daedalus`.

## 📖 Documentación y Detalles Técnicos

# 🛠️ DAEDALUS — Compilador Pedagógico y Traductor GCC/Clang

DAEDALUS compila programas C bajo los estándares rigurosos de la cátedra (C11, `-Wall -Wextra -pedantic -Wconversion`) y traduce los mensajes crudos de error del compilador a explicaciones amigables en español rioplatense con sugerencias concretas.

## Uso Rápido

```bash
# 1. Compilar código C con banderas pedagógicas y traducción de errores
daedalus compile main.c -o ./programa

# 2. Salida estructurada JSON
daedalus compile main.c --json

# 3. Traducir un archivo de log de compilador
daedalus translate stderr.log

# 4. Comprobar salud del toolchain (gcc, clang, ld, gdb)
daedalus doctor
```


## 📊 Formatos de Salida

`daedalus` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
