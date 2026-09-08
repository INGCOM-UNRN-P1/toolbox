---
name: myst-tools
description: Use when managing, formatting, fixing anchor collisions, generating indices, or validating cross-references in educational MyST Markdown projects.
---

# MyST Tools — Herramientas para Material Didáctico MyST Markdown

## Overview
`myst-tools` es una suite CLI para automatizar y normalizar material didáctico escrito en formato MyST Markdown. Permite formatear prosa a 80 columnas respetando bloques de código y directivas MyST, insertar anclas de encabezados (`(slug)=`), detectar y corregir referencias o anclas duplicadas (`fix-anchors`), y generar índices temáticos (`gen-apunte`, `gen-guides`, `gen-rules`).

## Cuándo Usar
- Para formatear archivos `.md` de MyST asegurando un ancho de línea estandarizado (80 caracteres) sin romper directivas o código (`myst-tools fmt`).
- Para detectar y resolver colisiones de anclas o referencias duplicadas entre capítulos (`myst-tools fix-anchors`).
- Para autogenerar índices (`indice.md`) de apuntes de clase, guías de trabajos prácticos o compendios de reglas de estilo.
- Para inyectar anclas semánticas a todos los encabezados de una carpeta de documentación.

## Requisito de Ejecución
Debe ejecutarse en la raíz del proyecto MyST (donde resida `myst.yml` o `mystm.yml`), o utilizando la opción global `-f, --force` para omitir dicha comprobación.

## Comandos CLI

### 1. Formateo de Markdown (`fmt`)
```bash
# Formatear archivos o directorios completos a 80 columnas
myst-tools fmt apunte/capitulo1.md

# Formatear todos los archivos markdown del proyecto
myst-tools fmt

# Comprobar si los archivos requieren formateo (retorna código 1 si hay cambios pendientes)
myst-tools fmt --check

# Formatear con ancho de línea personalizado
myst-tools fmt apunte/ --width 100
```

### 2. Detección y Reparación de Anclas Duplicadas (`fix-anchors`)
```bash
# Reportar anclas duplicadas sin realizar modificaciones
myst-tools fix-anchors . --report

# Modo simulación (dry-run)
myst-tools fix-anchors . --dry-run

# Aplicar corrección y renombrado de anclas duplicadas en todos los archivos
myst-tools fix-anchors .
```

### 3. Inserción de Anclas en Encabezados (`add-anchors`)
```bash
# Agregar anclas MyST automáticas (slug)= antes de cada encabezado (#, ##, ###)
myst-tools add-anchors apunte/
```

### 4. Generación de Índices (`gen-apunte`, `gen-guides`, `gen-rules`)
```bash
# Generar índice general del apunte (indice.md)
myst-tools gen-apunte apunte/

# Generar índice de guías de trabajos prácticos (indice.md)
myst-tools gen-guides guias/

# Generar índice de reglas de estilo de código (indice.md)
myst-tools gen-rules reglas/
```

### 5. Opciones Globales
- `-f, --force`: Permite ejecutar cualquier subcomando en directorios sin archivo de configuración `myst.yml`.
