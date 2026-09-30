# kaneda

Auditor pedagógico de seguridad C, buffer overflows y llamadas a sistema restringidas

## 🎯 Propósito y Alcance

`kaneda` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/kaneda
```

## 🚀 Guía de Uso

### Invocación básica

```bash
kaneda --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: kaneda [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 🔒 KANEDA — Auditor pedagógico de seguridad C, buffer overflows y llamadas a   
 sistema restringidas.                                                          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de KANEDA.                │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ audit  Audita código C en busca de funciones vulnerables a buffer overflow y │
│        llamadas restringidas.                                                │
│ rules  Lista las reglas de seguridad auditadas por KANEDA.                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`kaneda` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `kaneda`.

## 📖 Documentación y Detalles Técnicos

# 🔒 KANEDA — Auditor de Seguridad y Funciones Inseguras en C

KANEDA es una herramienta pedagógica para la detección temprana de funciones C prohibidas o inseguras (`gets`, `strcpy`, `sprintf`, `scanf("%s")`, `system`), vulnerabilidades de tipo `Format String` y llamadas a sistema no autorizadas.

## Uso Rápido

```bash
# 1. Auditar archivos C o carpetas de código
kaneda audit src/ main.c

# 2. Salida estructurada JSON
kaneda audit src/ --json

# 3. Listar catálogo de reglas
kaneda rules
```


## 📊 Formatos de Salida

`kaneda` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
