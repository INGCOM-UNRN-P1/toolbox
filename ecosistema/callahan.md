# callahan

Verificador formal de contratos ACSL y especificaciones deductivas con Frama-C

## 🎯 Propósito y Alcance

`callahan` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/callahan
```

## 🚀 Guía de Uso

### Invocación básica

```bash
callahan --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: callahan [OPTIONS] COMMAND [ARGS]...                                    
                                                                                
 📜 CALLAHAN — Verificador formal de contratos ACSL (pre/post condiciones) y    
 Frama-C WP.                                                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de CALLAHAN.              │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ verify   Verifica deductivamente las precondiciones, postcondiciones e       │
│          invariantes del archivo C.                                          │
│ extract  Extrae e imprime las cláusulas de contratos ACSL encontradas en el  │
│          código.                                                             │
│ doctor   Comprueba si el entorno cuenta con Frama-C y provers SMT (Alt-Ergo, │
│          Z3).                                                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`callahan` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `callahan`.

## 📖 Documentación y Detalles Técnicos

# 📜 CALLAHAN — Verificador Formal de Contratos ACSL en C

CALLAHAN realiza análisis y verificación deductiva de contratos formales de software en C escritos en lenguaje de especificación ACSL (`/*@ requires ... ensures ... */`) integrándose con Frama-C (WP).

## Uso Rápido

```bash
# 1. Extraer e inspeccionar contratos ACSL de un archivo
callahan extract algoritmo.c

# 2. Probar formalmente contratos con Frama-C
callahan verify algoritmo.c

# 3. Salida estructurada JSON
callahan extract algoritmo.c --json

# 4. Comprobar provers SMT disponibles (Z3, Alt-Ergo)
callahan doctor
```


## 📊 Formatos de Salida

`callahan` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
