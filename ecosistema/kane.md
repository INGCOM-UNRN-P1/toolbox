# kane

Simulador y depurador visual de I/O de bajo nivel y archivos binarios en C

## 🎯 Propósito y Alcance

`kane` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/kane
```

## 🚀 Guía de Uso

### Invocación básica

```bash
kane --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: kane [OPTIONS] COMMAND [ARGS]...                                        
                                                                                
 Simulador y depurador visual de I/O de bajo nivel y archivos binarios en C     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ inspect  Inspecciona y desglosa el contenido de un archivo binario           │
│          mapeándolo a un struct C.                                           │
│ version  Muestra la versión de KANE.                                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`kane` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `kane`.

## 📖 Documentación y Detalles Técnicos

# KANE — Simulador y Depurador Visual de I/O Binario en C

**KANE** inspecciona archivos binarios generados por programas C (`fread`, `fwrite`), desglosando sus registros en tablas legibles mapeadas a definiciones de `struct` C con offsets hexadecimales y detección de bytes truncados.

---

## 🚀 Uso Rápido

```bash
# Inspección con mapeo a estructura C
kane inspect datos.bin --struct "int id, char nombre[30], double promedio"

# Hex dump rápido
kane inspect datos.bin

# Salida estructurada JSON
kane inspect datos.bin --struct "int id, float nota" --json
```


## 📊 Formatos de Salida

`kane` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
