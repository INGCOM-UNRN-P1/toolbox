# voight (antes moodle-toolbox)

Herramientas para gestionar preguntas de Moodle (GIFT, XML)

## 🎯 Propósito y Alcance

`voight` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "voight[ai,ui,languagetool] @ git+https://github.com/INGCOM-UNRN/voight"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
voight --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN/voight#referencia-rápida), generada desde `voight --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `voight <comando> -h`.

## ⚙️ Configuración y Opciones

`voight` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `voight`.

## 📖 Documentación y Detalles Técnicos

# Moodle Toolbox (Questions CLI)

Conjunto de herramientas unificadas en Python para gestionar preguntas de Moodle en formatos XML y GIFT. Facilita la conversión, análisis, limpieza, mantenimiento y generación de preguntas mediante IA.

Todas las herramientas anteriores han sido consolidadas en un único comando raíz: `voight` (antes `questions`).

## 🚀 Instalación y Uso

Este proyecto utiliza [uv](https://docs.astral.sh/uv/) para la gestión de dependencias y ejecución.

```bash
# Clonar el repositorio
git clone <repository-url>
cd voight

# Ejecutar la ayuda principal
uv run voight --help
```

## 📦 Comandos Disponibles

El CLI `voight` se organiza en subcomandos especializados:

### 1. Validación y Análisis
- `voight validate`: Valida archivos o directorios GIFT, genera informes detallados y detecta duplicados.
- `voight analyze stats`: Genera estadísticas completas sobre un banco de preguntas.
- `voight analyze similar`: Encuentra preguntas similares usando análisis TF-IDF.

### 2. Formateo y Corrección
- `voight format`: Estandariza el formato visual de archivos GIFT y ajusta bloques de código.
- `voight fix code-indent`: Corrige la indentación dentro de bloques de código (```).
- `voight fix code-chars`: Convierte caracteres especiales entre normal y fullwidth.
- `voight fix slugify`: Normaliza nombres de archivos (minúsculas, sin acentos).
- `voight fix name-from-title`: Renombra archivos según el título de la pregunta.
- `voight fix title-from-name`: Actualiza el título interno según el nombre del archivo.

### 3. Conversión
- `voight convert html-to-md`: Convierte etiquetas HTML a Markdown en archivos XML o GIFT.
- `voight convert xml-to-gift`: Convierte Moodle XML a GIFT (soporta categorías, selección múltiple con pesos, V/F, emparejamiento, numérica con tolerancia, ensayo y descripción).
- `voight convert gift-to-xml`: Convierte GIFT a Moodle XML con bloques CDATA correctos. Ambos conversores viajan sobre el modelo unificado de preguntas del parser PEG y son estables en round-trip.

### 4. Árboles de Directorios (absorbe moodle-reorganizer)
- `voight tree export banco.gift|xml -o dir/`: Exporta un banco monolítico a un árbol de carpetas por categoría (1 archivo por pregunta).
- `voight tree collect dir/ -o reconstruido.gift|xml`: Recolecta el árbol nuevamente a un archivo único, restaurando las categorías.

### 5. Editor Web (absorbe moodle-visor / mxviz)
- `voight ui [dir]`: Abre un editor web local para navegar y editar preguntas organizadas en directorios, con soporte nativo de **Moodle XML y GIFT**. Requiere el extra opcional: `uv tool install "voight[ui] @ git+https://github.com/INGCOM-UNRN/voight"`.

### 6. Mantenimiento XML
- `voight xml cdata`: Asegura que los bloques `<text>` usen secciones CDATA.
- `voight xml clean-tags`: Elimina secciones de etiquetas (`<tags>`) redundantes.
- `voight xml rename`: Renombra archivos XML basándose en el nombre interno de la pregunta.

### 7. Inteligencia Artificial (Gemini)
- `voight ai`: Mejora la calidad pedagógica (`improve`) o crea variaciones (`multiply`) de preguntas usando modelos de Google Gemini.

## 📚 Documentación Detallada

Para más información sobre funcionalidades específicas, consulta la carpeta [docs/](https://github.com/INGCOM-UNRN/voight/tree/main/docs):

- **[Guía de Inicio Rápido](https://github.com/INGCOM-UNRN/voight/blob/main/docs/QUICK_START.md)**
- **[Validación y Análisis](https://github.com/INGCOM-UNRN/voight/blob/main/docs/README_validate_questions.md)**
- **[Mantenimiento XML](https://github.com/INGCOM-UNRN/voight/blob/main/docs/README_xml_maintenance.md)**
- **[Referencia de Caracteres Especiales](https://github.com/INGCOM-UNRN/voight/blob/main/docs/caracteres_especiales.md)**

## 📋 Requisitos

- **Python 3.11+**
- **Dependencias**: tatsu, google-genai, click, python-dotenv (gestionadas por `uv`).

## ✍️ Autor

[Especificar autor]

---

**Última actualización:** Mayo 2026 (Refactorización a CLI Unificado)


## 📊 Formatos de Salida

`voight` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
