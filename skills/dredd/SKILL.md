---
name: dredd
description: Use when orchestrating batch evaluations, automated grading, plagiarism detection (Winnowing), or feedback distribution for C student submissions from Moodle or GitHub Classroom.
---

# Dredd — Juez de Trabajos Prácticos y Orquestador Docente

## Overview
`dredd` es el orquestador docente para evaluación masiva, autograding multicanal y gestión de entregas en C. Soporta tanto el flujo de **Moodle** (ingesta de ZIP masivo, normalización de encodings, versionado SHA-256 en SQLite, mapeo de fuentes a tests y exportación de CSV de calificaciones) como el flujo de **GitHub Classroom** (clonación de repositorios, ejecución de análisis vía Ripley, apertura de PRs y publicación automatizada de feedback). Incluye auditoría de plagio mediante el algoritmo Winnowing.

## Cuándo Usar
- Para procesar paquetes ZIP masivos descargados de Moodle, normalizando archivos y rastreando re-entregas (`dredd moodle ingest`).
- Para mapear archivos de estudiantes a casos de prueba automáticamente o de forma interactiva (`dredd map`).
- Para ejecutar evaluaciones masivas o individuales sobre entregas de GitHub Classroom (`dredd eval`).
- Para comentar informes de evaluación en Pull Requests de GitHub (`dredd comment`).
- Para detectar código duplicado o copias masivas mediante análisis de huellas Winnowing (`dredd plagiarism`).
- Para exportar planillas de notas CSV de Moodle y reportes de feedback HTML/PDF (`dredd export`, `dredd export-report`).

## Comandos CLI

### 1. Flujo Moodle (ZIP / Entregas de Campus)
```bash
# Ingesta masiva de archivo ZIP de entregas de Moodle
dredd moodle ingest entregas_tp01.zip

# Mapear archivos de código a ejercicios
dredd map tp01_1228009 -e ejercicio1 -e ejercicio2 --auto

# Detección de plagio entre entregas (umbral de similitud 0.0 - 1.0)
dredd plagiarism tp01_1228009 --threshold 0.70

# Exportar calificaciones CSV para Moodle + ZIP de devoluciones + Dashboard
dredd export tp01_1228009
```

### 2. Flujo GitHub Classroom
```bash
# Evaluar una entrega específica
dredd eval tp01 alvarez_juan

# Evaluar toda la cohorte presente en el workspace
dredd eval tp01 --all

# Publicar el reporte Markdown generado como comentario en el PR del estudiante
dredd comment tp01 alvarez_juan --open

# Reparar o abrir PR de corrección si el estudiante no lo hizo
dredd pr-fix tp01 alvarez_juan
```

### 3. Conversión de Reportes
```bash
# Convertir informe Markdown a HTML autocontenido
dredd export-report entregas/alvarez_juan/alvarez_juan.md --format html

# Convertir informe a PDF para archivo o impresión
dredd export-report entregas/alvarez_juan/alvarez_juan.md --format pdf
```

## Estructura y Archivos de Trabajo
- `.metadata.db`: Base de datos SQLite que registra versiones (`r1`, `r2`), hashes SHA-256 y timestamps de cada entrega.
- `mappings.json`: Definición de relaciones entre archivos subidos por el estudiante y los suites de prueba de la cátedra.
- `<estudiante>.md`: Informe consolidado de corrección generado por el motor de análisis.
- `dashboard.md`: Resumen estadístico de la cohorte (aprobados, desaprobados, errores comunes).
