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

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/kaneda#referencia-rápida), generada desde `kaneda --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `kaneda <comando> -h`.

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
