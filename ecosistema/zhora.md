# zhora

Linter y auditor de seguridad en macros del preprocesador C (#define)

## 🎯 Propósito y Alcance

`zhora` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/zhora
```

## 🚀 Guía de Uso

### Invocación básica

```bash
zhora --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/zhora#referencia-rápida), generada desde `zhora --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `zhora <comando> -h`.

## ⚙️ Configuración y Opciones

`zhora` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `zhora`.

## 📖 Documentación y Detalles Técnicos

# ZHORA — Linter y Auditor de Seguridad en Macros C (#define)

**ZHORA** audita macros del preprocesador C para detectar efectos de lado en evaluación múltiple de parámetros, falta de paréntesis defensivos en argumentos y cuerpos, y puntos y coma espurios.

---

## 🚀 Uso Rápido

```bash
# Auditar macros en archivos y carpetas
zhora audit src/

# Salida estructurada JSON
zhora audit src/ --json
```

---

## 🔍 Reglas Auditadas

- **`ZH001`**: Macros que finalizan con punto y coma (`;`), rompiendo sentencias `if/else`.
- **`ZH002`**: Parámetros evaluados más de una vez (riesgo de side effects con `x++`).
- **`ZH003`**: Parámetros de macro no envueltos individualmente en paréntesis `(x)`.
- **`ZH004`**: Cuerpo de expresión matemática no protegido con paréntesis externos.


## 📊 Formatos de Salida

`zhora` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
