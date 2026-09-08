# brett

Auditor de alineación y padding de estructuras C y optimizador de reordenamiento de campos

## 🎯 Propósito y Alcance

`brett` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/brett
```

## 🚀 Guía de Uso

### Invocación básica

```bash
brett --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: brett [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 📏 BRETT — Auditor de alineación y padding de estructuras C y optimizador de   
 reordenamiento de campos.                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de BRETT.                 │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ audit     Audita estructuras en busca de bytes de memoria desperdiciados por │
│           desalineación y padding.                                           │
│ optimize  Genera el código C optimizado reordenando los campos de menor a    │
│           mayor alineación.                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`brett` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `brett`.

## 📖 Documentación y Detalles Técnicos

# 📏 BRETT — Auditor de Padding y Alineación de Estructuras C

BRETT analiza la disposición en memoria (`Memory Layout`) de tipos de datos compuestos (`typedef struct`) en C, calcula los bytes de relleno (`padding`) desperdiciados por desalineación de campos y genera sugerencias automáticas de reordenamiento para minimizar el tamaño de las estructuras.

## Uso Rápido

```bash
# 1. Auditar estructuras en archivos C o cabeceras H
brett audit src/ main.h

# 2. Generar sugerencias de layout optimizado
brett optimize tipos.h

# 3. Salida estructurada JSON
brett audit src/ --json
```


## 📊 Formatos de Salida

`brett` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
