# motoko

Verificador de encapsulamiento estricto y opacidad de Tipos Abstractos de Datos (TDAs) en C

## 🎯 Propósito y Alcance

`motoko` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/motoko
```

## 🚀 Guía de Uso

### Invocación básica

```bash
motoko --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: motoko [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 Verificador de encapsulamiento estricto y opacidad de TDAs en C                
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ verify   Verifica que los TDAs sean opacos y no sufran accesos directos a    │
│          sus campos internos.                                                │
│ version  Muestra la versión de MOTOKO.                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`motoko` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `motoko`.

## 📖 Documentación y Detalles Técnicos

# MOTOKO — Verificador de Encapsulamiento y Opacidad de TDAs en C

**MOTOKO** analiza archivos de cabecera e implementaciones en C para asegurar el ocultamiento de información y encapsulamiento estricto de Tipos Abstractos de Datos (TDAs), detectando accesos directos a campos internos desde código cliente.

---

## 🚀 Uso Rápido

```bash
# Verificar encapsulamiento de cabeceras en el directorio
motoko verify tda_pila.h

# Especificar archivo cliente e implementación
motoko verify tda_pila.h --client main.c --impl tda_pila.c

# Salida estructurada JSON
motoko verify tda_pila.h --json
```

---

## 🔍 Reglas Auditadas

- **`MOT001`**: TDAs que exponen sus campos dentro del `.h` público (debe usarse declaración incompleta).
- **`MOT002`**: Código cliente que desreferencia directamente campos del TDA (`tda->campo`) en lugar de invocar primitivas públicas.


## 📊 Formatos de Salida

`motoko` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
