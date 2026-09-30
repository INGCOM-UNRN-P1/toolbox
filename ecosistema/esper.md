# esper

> **Retirado.** Lo reemplaza [`daedalus`](daedalus.md), que compila con las banderas de la
> cátedra y explica los diagnósticos de GCC en español. ripley y dredd ya no lo usan y el
> manifiesto no lo clona ni lo instala (estado `retirado`). Esta página queda como referencia.

Explicador pedagógico y formateador interactivo de salidas y errores de GCC/Clang

## 🎯 Propósito y Alcance

`esper` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/esper
```

## 🚀 Guía de Uso

### Invocación básica

```bash
esper --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: esper [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 Explicador pedagógico y formateador interactivo de salidas y errores de        
 GCC/Clang                                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ compile  Envuelve la ejecución de GCC y traduce todos los errores y          │
│          advertencias.                                                       │
│ explain  Explica un mensaje de error puntual o texto copiado de GCC.         │
│ pipe     Lee mensajes de GCC desde stdin (tubería: `gcc ... 2>&1 | esper     │
│          pipe`).                                                             │
│ version  Muestra la versión de ESPER.                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`esper` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `esper`.

## 📖 Documentación y Detalles Técnicos

# ESPER — Explicador Pedagógico y Formateador de Diagnósticos GCC/Clang

**ESPER** envuelve la invocación del compilador GCC/Clang e intercepta errores, advertencias (`-Wall -Wextra -pedantic`) y notas del linker, traduciéndolas en paneles interactivos con diagnósticos pedagógicos en español rioplatense, causas raíz típicas y acciones correctivas sugeridas.

---

## 🚀 Uso Rápido

```bash
# Compilar archivo traduciendo advertencias y errores automáticamente
esper compile main.c -o app -Wall -Wextra

# Explicar un mensaje de error puntual copiado de la terminal
esper explain "main.c:12:5: warning: format '%d' expects argument of type 'int *' [-Wformat=]"

# Piping directo desde GCC
gcc -Wall main.c -o app 2>&1 | esper pipe

# Salida estructurada JSON
esper compile main.c -o app --json
```


## 📊 Formatos de Salida

`esper` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
