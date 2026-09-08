# tetsuo

Traductor y explicador pedagógico en español de sanitizers (ASan, UBSan, MSan)

## 🎯 Propósito y Alcance

`tetsuo` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/tetsuo
```

## 🚀 Guía de Uso

### Invocación básica

```bash
tetsuo --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: tetsuo [OPTIONS] COMMAND [ARGS]...                                      
                                                                                
 Traductor y explicador pedagógico de sanitizers (ASan, UBSan, MSan) en español 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ run      Compila y ejecuta con AddressSanitizer/UBSan traduciendo cualquier  │
│          violación a español didáctico.                                      │
│ version  Muestra la versión de TETSUO.                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`tetsuo` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `tetsuo`.

## 📖 Documentación y Detalles Técnicos

# TETSUO — Traductor y Explicador Pedagógico de Sanitizers (ASan / UBSan)

**TETSUO** compila y ejecuta programas C bajo AddressSanitizer y UndefinedBehaviorSanitizer, interceptando sus salidas complejas en inglés y traduciéndolas a diagnósticos formativos en español con sugerencias concretas de corrección.

---

## 🚀 Uso Rápido

```bash
# Compilar y ejecutar con sanitizers explicando cualquier fallo
tetsuo run main.c

# Pasar entrada estándar
tetsuo run main.c --input "10\n"

# Salida estructurada JSON
tetsuo run main.c --json
```

---

## 🔬 Errores Diagnosticados

- **`heap-buffer-overflow`**: Desbordamiento en bloques de memoria dinámica (`malloc`).
- **`stack-buffer-overflow`**: Desbordamiento en arrays locales de la pila.
- **`heap-use-after-free`**: Lectura/escritura en punteros ya liberados.
- **`double-free`**: Múltiples llamadas a `free()` sobre la misma dirección.
- **`undefined-behavior`**: Overflows con signo, desreferencia de nulos o shifts inválidos.


## 📊 Formatos de Salida

`tetsuo` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
