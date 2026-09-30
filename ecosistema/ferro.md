# ferro

Perfilador de rendimiento algorítmico y hardware counters en C

## 🎯 Propósito y Alcance

`ferro` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "ferro[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/ferro"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
ferro --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/ferro#referencia-rápida), generada desde `ferro --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `ferro <comando> -h`.

## ⚙️ Configuración y Opciones

`ferro` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `ferro`.

## 📖 Documentación y Detalles Técnicos

# FERRO — Perfilador de Rendimiento Algorítmico y Hardware Counters en C

**FERRO** ejecuta programas C a través de múltiples tamaños de entrada ($N$), midiendo tiempos de alta resolución, ciclos de CPU estimados, throughput e infiriendo la complejidad temporal empírica ($O(N)$, $O(N \log N)$, $O(N^2)$).

---

## 🚀 Uso Rápido

```bash
# Perfilar algoritmo con diferentes tamaños de entrada
ferro profile ordenamiento.c --inputs "1000,10000,50000"

# Salida estructurada JSON
ferro profile ordenamiento.c --json
```


## 📊 Formatos de Salida

`ferro` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
