# moodle-toolbox

Herramientas para gestionar preguntas de Moodle (GIFT, XML)

## 🎯 Propósito y Alcance

`moodle-toolbox` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/moodle-toolbox
```

## 🚀 Guía de Uso

### Invocación básica

```bash
moodle-toolbox --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: moodle-toolbox [OPTIONS] COMMAND [ARGS]...

  Herramientas para la gestión de preguntas de Moodle.

Options:
  --llm                 Muestra instrucciones generales para un LLM.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --install-completion  Install completion for the current shell.
  --help                Show this message and exit.

Commands:
  ai        Procesamiento de preguntas usando IA (Gemini).
  analyze   Análisis y estadísticas de preguntas.
  config    Configuración global de las herramientas.
  convert   Comandos para convertir entre formatos.
  fix       Comandos para corregir problemas comunes.
  format    Formatea archivos GIFT y ajusta bloques de código.
  split     Divide archivos GIFT con múltiples preguntas en archivos...
  tree      Organiza bancos en árboles de directorios por categoría.
  validate  Valida archivos o directorios de preguntas GIFT.
  xml       Herramientas para archivos XML de Moodle.
```

## ⚙️ Configuración y Opciones

`moodle-toolbox` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `moodle-toolbox`.

## 📖 Documentación y Detalles Técnicos

# Moodle Toolbox (Questions CLI)

Conjunto de herramientas unificadas en Python para gestionar preguntas de Moodle en formatos XML y GIFT. Facilita la conversión, análisis, limpieza, mantenimiento y generación de preguntas mediante IA.

Todas las herramientas anteriores han sido consolidadas en un único comando raíz: `questions`.

## 🚀 Instalación y Uso

Este proyecto utiliza [uv](https://docs.astral.sh/uv/) para la gestión de dependencias y ejecución.

```bash
# Clonar el repositorio
git clone <repository-url>
cd moodle-toolbox

# Ejecutar la ayuda principal
uv run questions --help
```

## 📦 Comandos Disponibles

El CLI `questions` se organiza en subcomandos especializados:

### 1. Validación y Análisis
- `questions validate`: Valida archivos o directorios GIFT, genera informes detallados y detecta duplicados.
- `questions analyze stats`: Genera estadísticas completas sobre un banco de preguntas.
- `questions analyze similar`: Encuentra preguntas similares usando análisis TF-IDF.

### 2. Formateo y Corrección
- `questions format`: Estandariza el formato visual de archivos GIFT y ajusta bloques de código.
- `questions fix code-indent`: Corrige la indentación dentro de bloques de código (```).
- `questions fix code-chars`: Convierte caracteres especiales entre normal y fullwidth.
- `questions fix slugify`: Normaliza nombres de archivos (minúsculas, sin acentos).
- `questions fix name-from-title`: Renombra archivos según el título de la pregunta.
- `questions fix title-from-name`: Actualiza el título interno según el nombre del archivo.

### 3. Conversión
- `questions convert html-to-md`: Convierte etiquetas HTML a Markdown en archivos XML o GIFT.
- `questions convert xml-to-gift`: Convierte Moodle XML a GIFT (soporta categorías, selección múltiple con pesos, V/F, emparejamiento, numérica con tolerancia, ensayo y descripción).
- `questions convert gift-to-xml`: Convierte GIFT a Moodle XML con bloques CDATA correctos. Ambos conversores viajan sobre el modelo unificado de preguntas del parser PEG y son estables en round-trip.

### 4. Árboles de Directorios (absorbe moodle-reorganizer)
- `questions tree export banco.gift|xml -o dir/`: Exporta un banco monolítico a un árbol de carpetas por categoría (1 archivo por pregunta).
- `questions tree collect dir/ -o reconstruido.gift|xml`: Recolecta el árbol nuevamente a un archivo único, restaurando las categorías.

### 5. Editor Web (absorbe moodle-visor / mxviz)
- `questions ui [dir]`: Abre un editor web local para navegar y editar preguntas organizadas en directorios, con soporte nativo de **Moodle XML y GIFT**. Requiere el extra opcional: `uv tool install "questions[ui] @ git+https://github.com/INGCOM-UNRN/moodle-toolbox"`.

### 6. Mantenimiento XML
- `questions xml cdata`: Asegura que los bloques `<text>` usen secciones CDATA.
- `questions xml clean-tags`: Elimina secciones de etiquetas (`<tags>`) redundantes.
- `questions xml rename`: Renombra archivos XML basándose en el nombre interno de la pregunta.

### 7. Inteligencia Artificial (Gemini)
- `questions ai`: Mejora la calidad pedagógica (`improve`) o crea variaciones (`multiply`) de preguntas usando modelos de Google Gemini.

## 📚 Documentación Detallada

Para más información sobre funcionalidades específicas, consulta la carpeta [docs/](https://github.com/INGCOM-UNRN/moodle-toolbox/tree/main/docs):

- **[Guía de Inicio Rápido](https://github.com/INGCOM-UNRN/moodle-toolbox/blob/main/docs/QUICK_START.md)**
- **[Validación y Análisis](https://github.com/INGCOM-UNRN/moodle-toolbox/blob/main/docs/README_validate_questions.md)**
- **[Mantenimiento XML](https://github.com/INGCOM-UNRN/moodle-toolbox/blob/main/docs/README_xml_maintenance.md)**
- **[Referencia de Caracteres Especiales](https://github.com/INGCOM-UNRN/moodle-toolbox/blob/main/docs/caracteres_especiales.md)**

## 📋 Requisitos

- **Python 3.11+**
- **Dependencias**: tatsu, google-genai, click, python-dotenv (gestionadas por `uv`).

## ✍️ Autor

[Especificar autor]

---

**Última actualización:** Mayo 2026 (Refactorización a CLI Unificado)


## 📊 Formatos de Salida

`moodle-toolbox` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
