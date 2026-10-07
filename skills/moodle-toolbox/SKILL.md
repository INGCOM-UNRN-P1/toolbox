---
name: moodle-toolbox
description: Use when validating, converting (GIFT <-> XML), formatting, reorganizing category directory trees, or performing maintenance on Moodle question banks.
---

# voight (repositorio moodle-toolbox) — Gestión Integral de Preguntas Moodle (GIFT & XML)

## Overview
`moodle-toolbox` (comando `voight`; los nombres anteriores `questions` y `moodle-toolbox` son alias deprecados) es el conjunto unificado de herramientas CLI en Python para gestionar bancos de preguntas de Moodle en formatos XML y GIFT. Proporciona validación sintáctica basada en gramática PEG (TatSu), conversión bidireccional estable entre XML y GIFT, normalización de estilos/indentación de bloques de código, análisis de similitud TF-IDF, descomposición y reconstrucción de árboles de directorios por categorías, y operaciones de mantenimiento y enriquecimiento pedagógico con IA.

## Cuándo Usar
- Para validar la sintaxis de archivos o directorios GIFT y detectar duplicados (`voight validate`).
- Para convertir bancos de preguntas entre Moodle XML y GIFT de forma bidireccional (`voight convert xml-to-gift` / `voight convert gift-to-xml`).
- Para desarmar un archivo monolítico GIFT/XML en un árbol de directorios por categoría (un archivo por pregunta) o recolectarlo nuevamente (`voight tree export` / `voight tree collect`).
- Para corregir y formatear indentación de código, caracteres especiales (fullwidth a normal) y nombres/títulos (`voight fix`).
- Para analizar estadísticas de categorías y preguntas similares (`voight analyze stats` / `voight analyze similar`).
- Para mantenimiento y sanitización de etiquetas XML (`voight xml cdata` / `voight xml clean-tags` / `voight xml rename`).

## Comandos CLI

### 1. Validación y Análisis (`validate` / `analyze`)
```bash
# Validar archivo o directorio GIFT (reporte detallado y detección de duplicados)
voight validate banco.gift
voight validate preguntas/ --report informe.md

# Estadísticas del banco (tipos de pregunta, categorías, distribución)
voight analyze stats banco.gift

# Detección de preguntas duplicadas o similares usando TF-IDF
voight analyze similar banco.gift --threshold 0.85
```

### 2. Conversión Bidireccional (`convert`)
```bash
# Convertir Moodle XML a GIFT
voight convert xml-to-gift cuestionario.xml -o banco.gift

# Convertir GIFT a Moodle XML (con bloques CDATA correctos)
voight convert gift-to-xml banco.gift -o cuestionario.xml

# Convertir etiquetas HTML a Markdown dentro de archivos XML o GIFT
voight convert html-to-md banco.gift -o banco_md.gift
```

### 3. Reorganización en Árbol de Categorías (`tree`)
```bash
# Descomponer archivo monolítico (GIFT o XML) en un árbol de carpetas por categoría (1 archivo por pregunta)
voight tree export banco.gift -o arbol_preguntas/
voight tree export cuestionario.xml -o arbol_preguntas/

# Reconstruir un árbol de carpetas nuevamente a un archivo único (GIFT o XML) restaurando categorías
voight tree collect arbol_preguntas/ -o banco_reconstruido.gift
voight tree collect arbol_preguntas/ -o cuestionario_reconstruido.xml
```

### 4. Formateo y Correcciones (`format` / `fix`)
```bash
# Estandarizar formato visual de archivos GIFT
voight format banco.gift

# Corregir indentación dentro de bloques de código (```)
voight fix code-indent banco.gift

# Convertir caracteres especiales/invisibles entre normal y fullwidth
voight fix code-chars banco.gift

# Normalizar nombres de archivo (slugify: minúsculas, sin acentos)
voight fix slugify arbol_preguntas/

# Sincronizar nombres de archivo según el título de la pregunta
voight fix name-from-title arbol_preguntas/

# Sincronizar título interno según el nombre del archivo
voight fix title-from-name arbol_preguntas/
```

### 5. Mantenimiento de Moodle XML (`xml`)
```bash
# Envolver bloques de texto con secciones CDATA
voight xml cdata cuestionario.xml -o cuestionario_cdata.xml

# Eliminar secciones de etiquetas (<tags>) redundantes
voight xml clean-tags cuestionario.xml

# Renombrar archivos XML según el nombre interno de la pregunta
voight xml rename preguntas_xml/
```

### 6. IA y Variaciones con Gemini (`ai`)
```bash
# Mejorar calidad didáctica y enunciados con IA
voight ai improve pregunta.gift -o pregunta_mejorada.gift

# Generar múltiples variantes pedagógicas de una pregunta
voight ai multiply pregunta.gift -n 3 -o variantes/
```
