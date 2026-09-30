# wierzbowski

Auditor de grafos de inclusión de headers, dependencias circulares y Makefiles en C

## 🎯 Propósito y Alcance

`wierzbowski` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/wierzbowski
```

## 🚀 Guía de Uso

### Invocación básica

```bash
wierzbowski --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/wierzbowski#referencia-rápida), generada desde `wierzbowski --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `wierzbowski <comando> -h`.

## ⚙️ Configuración y Opciones

`wierzbowski` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `wierzbowski`.

## 📖 Documentación y Detalles Técnicos

# WIERZBOWSKI — Auditor de Grafos de Inclusión, Ciclos y Makefiles en C

**WIERZBOWSKI** analiza la arquitectura de proyectos multi-archivo en C, construyendo el grafo de dependencias de `#include`, detectando dependencias circulares, verificando guardas de inclusión y auditando Makefiles.

---

## 🚀 Uso Rápido

```bash
# Auditar dependencias en el directorio actual
wierzbowski audit .

# Auditar proyecto específico
wierzbowski audit ./tp_modular/

# Salida estructurada JSON
wierzbowski audit . --json
```

---

## 🔍 Reglas Auditadas

- **Detección de Ciclos**: Grafos de inclusión circulares (`a.h ➔ b.h ➔ a.h`).
- **Guardas de Inclusión**: Falta de `#ifndef / #define` o `#pragma once`.
- **`MKF001`**: Recetas de Makefiles indentadas con espacios en lugar de TAB.
- **`MKF002`**: Reglas sin archivo objetivo sin declaración en `.PHONY`.
- **`MKF003`**: Ausencia de target `clean`.


## 📊 Formatos de Salida

`wierzbowski` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
