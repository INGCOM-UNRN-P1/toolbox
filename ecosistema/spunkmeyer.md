# spunkmeyer

Detector de antipatrones de programación y vicios de diseño en código C

## 🎯 Propósito y Alcance

`spunkmeyer` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/spunkmeyer
```

## 🚀 Guía de Uso

### Invocación básica

```bash
spunkmeyer --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/spunkmeyer#referencia-rápida), generada desde `spunkmeyer --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `spunkmeyer <comando> -h`.

## ⚙️ Configuración y Opciones

`spunkmeyer` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `spunkmeyer`.

## 📖 Documentación y Detalles Técnicos

# 💡 SPUNKMEYER — Detector de Antipatrones Didácticos en C

SPUNKMEYER es una herramienta pedagógica diseñada para identificar vicios de diseño y antipatrones comunes en estudiantes de C (`malloc()` con casting innecesario, `while(!feof())`, retorno de punteros a variables locales en Stack, etc.).

## Uso Rápido

```bash
# 1. Detectar antipatrones en archivos o carpetas
spunkmeyer detect src/ main.c

# 2. Salida estructurada JSON
spunkmeyer detect src/ --json

# 3. Ver catálogo completo de antipatrones
spunkmeyer catalog
```


## 📊 Formatos de Salida

`spunkmeyer` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
