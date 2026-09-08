# spunkmeyer

Detector de antipatrones de programación y vicios de diseño en código C

## 🎯 Propósito y Alcance

`spunkmeyer` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/spunkmeyer
```

## 🚀 Guía de Uso

### Invocación básica

```bash
spunkmeyer --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: spunkmeyer [OPTIONS] COMMAND [ARGS]...                                  
                                                                                
 💡 SPUNKMEYER — Detector de antipatrones de programación y vicios didácticos   
 en código C.                                                                   
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de SPUNKMEYER.            │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ detect   Detecta antipatrones y malas prácticas en el código C.              │
│ catalog  Muestra el catálogo completo de antipatrones detectados.            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

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
