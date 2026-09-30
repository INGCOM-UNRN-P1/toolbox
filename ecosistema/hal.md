# hal

Asistente forense de core dumps y análisis pedagógico post-mortem de segfaults en C

## 🎯 Propósito y Alcance

`hal` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "hal[ecosistema] @ git+https://github.com/INGCOM-UNRN-P1/hal"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
hal --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/hal#referencia-rápida), generada desde `hal --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `hal <comando> -h`.

## ⚙️ Configuración y Opciones

`hal` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `hal`.

## 📖 Documentación y Detalles Técnicos

# 🤖 HAL — Asistente Forense de Core Dumps y Segfaults en C

HAL es una herramienta standalone diseñada para diagnosticar fallos en tiempo de ejecución (`SIGSEGV`, `SIGABRT`, `SIGFPE`, `SIGILL`) en programas C estudiantiles, traduciendo volcados crudos y backtraces de GDB a explicaciones pedagógicas claras en español rioplatense con ubicación exacta de la falla y acciones correctivas concretas.

## Instalación

```bash
uv tool install --editable .
```

## Uso Rápido

```bash
# 1. Compilar, ejecutar y diagnosticar un archivo fuente C
hal run programa_con_fallo.c

# 2. Diagnosticar con salida estructurada JSON para bots y CI
hal run programa_con_fallo.c --json

# 3. Pasar argumentos y datos por stdin
hal run programa.c arg1 arg2 --stdin "10\n20\n"

# 4. Inspeccionar un binario precompilado
hal inspect ./binario_compilado

# 5. Comprobar salud del entorno (GCC, GDB, Valgrind)
hal doctor
```


## 📊 Formatos de Salida

`hal` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
