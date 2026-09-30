# brett

Auditor de alineación y padding de estructuras C y optimizador de reordenamiento de campos

## 🎯 Propósito y Alcance

`brett` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/brett
```

## 🚀 Guía de Uso

### Invocación básica

```bash
brett --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/brett#referencia-rápida), generada desde `brett --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `brett <comando> -h`.

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
