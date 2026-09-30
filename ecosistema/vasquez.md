# vasquez

Motor de inyección de fallos de entorno y hardware (Fault Injection Engine) en C vía LD_PRELOAD

## 🎯 Propósito y Alcance

`vasquez` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/vasquez
```

## 🚀 Guía de Uso

### Invocación básica

```bash
vasquez --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: vasquez [OPTIONS] COMMAND [ARGS]...                                     
                                                                                
 Motor de inyección de fallos de entorno y hardware en C vía LD_PRELOAD         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ inject   Inyecta fallos controlados (malloc NULL, fopen EACCES) evaluando si │
│          el código C maneja el error sin crashear.                           │
│ version  Muestra la versión de VASQUEZ.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`vasquez` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `vasquez`.

## 📖 Documentación y Detalles Técnicos

# VASQUEZ — Motor de Inyección de Fallos de Entorno en C (Fault Injection Engine)

**VASQUEZ** intercepta llamadas estándar a `malloc`, `calloc` y `fopen` mediante `LD_PRELOAD` para inyectar fallos deterministas en tiempo de ejecución (retornos `NULL` simulando falta de memoria o accesos denegados a disco), verificando si el estudiante implementó manejo defensivo de errores o si el programa sufre un `SIGSEGV`.

---

## 🚀 Uso Rápido

```bash
# Inyectar fallos por defecto (malloc y fopen) sobre código fuente o binario
vasquez inject solucion_alumno.c

# Especificar fallos exactos (fallar en el 2do malloc y 1er fopen)
vasquez inject app --faults "malloc:2,fopen:1"

# Salida estructurada JSON
vasquez inject solucion_alumno.c --json
```


## 📊 Formatos de Salida

`vasquez` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
