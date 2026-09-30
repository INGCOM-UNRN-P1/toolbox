# nostromo

Sandbox de ejecución aislada con Bubblewrap y evaluador de casos de prueba .in/.out

## 🎯 Propósito y Alcance

`nostromo` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/nostromo
```

## 🚀 Guía de Uso

### Invocación básica

```bash
nostromo --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: nostromo [OPTIONS] COMMAND [ARGS]...                                    
                                                                                
 📦 NOSTROMO — Sandbox de ejecución aislada con Bubblewrap y evaluador de casos 
 de prueba .in/.out.                                                            
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de NOSTROMO.              │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ run     Ejecuta un binario dentro del sandbox con límites estrictos de CPU y │
│         memoria.                                                             │
│ test    Ejecuta una suite completa de casos de prueba .in/.out y genera el   │
│         reporte de evaluación.                                               │
│ doctor  Verifica disponibilidad del motor de sandbox (Bubblewrap /           │
│         namespaces del kernel).                                              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`nostromo` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `nostromo`.

## 📖 Documentación y Detalles Técnicos

# 📦 NOSTROMO — Sandbox de Ejecución y Test Runner en C

NOSTROMO es un entorno aislado de ejecución (sandbox basado en `Bubblewrap` / `setrlimit`) y evaluador automático de casos de prueba (`.in` / `.out`) con control estricto de timeouts, límites de memoria y reporte de diffs unificados.

## Uso Rápido

```bash
# 1. Ejecutar binario dentro del sandbox con límites
nostromo run ./programa --timeout 1.5 --memory 64

# 2. Evaluar suite de casos .in / .out
nostromo test ./programa ./testcases/

# 3. Salida estructurada JSON para evaluación desatendida
nostromo test ./programa ./testcases/ --json

# 4. Comprobar salud del sandbox (bwrap, límites)
nostromo doctor
```


## 📊 Formatos de Salida

`nostromo` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
