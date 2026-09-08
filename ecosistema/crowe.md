# crowe

Linter de portabilidad multi-arquitectura (x86_64, ARM, RISC-V, endianness) en C

## 🎯 Propósito y Alcance

`crowe` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/crowe
```

## 🚀 Guía de Uso

### Invocación básica

```bash
crowe --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: crowe [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 Linter de portabilidad multi-arquitectura y compatibilidad C                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ lint     Analiza archivos C buscando asunciones no portables de hardware y   │
│          endianness.                                                         │
│ version  Muestra la versión de CROWE.                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`crowe` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `crowe`.

## 📖 Documentación y Detalles Técnicos

# CROWE — Linter de Portabilidad Multi-Arquitectura en C

**CROWE** analiza código C para detectar asunciones no portables de hardware (endianness, tamaños fijos de punteros, signo de `char`, VLAs y tamaños de `long`) y opcionalmente valida compilación cruzada para `x86_64`, `aarch64` y `riscv64`.

---

## 🚀 Uso Rápido

```bash
# Auditar portabilidad en archivos C
crowe lint src/

# Probar compilación multi-arquitectura
crowe lint src/ --cross-compile

# Salida estructurada en JSON
crowe lint src/ --json
```

---

## 🔍 Reglas Auditadas

- **`CRW001`**: Casteo de puntero a `int` (provoca truncamiento en arquitecturas de 64 bits).
- **`CRW002`**: Uso de `char` esperando valores negativos (en ARM es `unsigned char` por defecto).
- **`CRW003`**: Asunciones fijas de orden de bytes (Endianness).
- **`CRW004`**: Suposición del tamaño de `long` (`sizeof(long) == 4` vs `8`).
- **`CRW005`**: Uso de Variable-Length Arrays (VLAs) con riesgo de desbordamiento de pila.


## 📊 Formatos de Salida

`crowe` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
