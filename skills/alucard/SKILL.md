---
name: alucard
description: Use when generating academic exams from YAML definitions and GIFT/Moodle XML question banks, optimizing paper layouts, synthesizing C code-tracing questions with GCC verification (daedalus), or linting GIFT files.
---

# alucarD — Generador de Exámenes y Síntesis de Preguntas

## Overview
`alucarD` (`generador-examenes` / `alucard`) es una herramienta de composición y renderizado de exámenes impresos o digitales a partir de bancos de preguntas (GIFT / Moodle XML) y archivos de configuración YAML. Incluye el sintetizador `daedalus` para generar preguntas paramétricas de C verificadas con GCC y `gift-linter` para validación sintáctica de bancos.

## Cuándo Usar
- Para generar variantes de exámenes impresos o en PDF/HTML con control tipográfico y ahorro de papel.
- Para sintetizar bancos de preguntas de análisis de trazas de C (punteros, recursión, operadores) sin errores en la clave de respuesta.
- Para auditar y validar la sintaxis de bancos de preguntas GIFT antes de usarlos.
- Para inspeccionar la jerarquía de categorías de un banco GIFT o XML.

## Comandos CLI

### 1. Inicialización y Exploración
```bash
# Inicializar estructura de proyecto (templates/, i18n/, bancos/, output/)
generador-examenes --init

# Inspeccionar árbol de categorías de un banco y generar reporte HTML
generador-examenes --category-tree bancos/preguntas.gift
```

### 2. Generación de Exámenes
```bash
# Generar 3 variantes de examen basadas en YAML
generador-examenes -d examen.yaml -i bancos/preguntas.gift -n 3 -o output/

# Asistente interactivo para crear o editar la configuración YAML
generador-examenes --wizard examen.yaml
```

### 3. Síntesis de Preguntas C (`daedalus`)
```bash
# Listar generadores disponibles (punteros, recursión, operadores, etc.)
generador-examenes --listar-sintetizadores

# Sintetizar 8 preguntas de traza de punteros con semilla determinista
generador-examenes --sintetizar traza-punteros -n 8 -s 42 -o output/ --formato-banco gift

# Sintetizar en formato Moodle XML
generador-examenes --sintetizar recursion -n 5 --formato-banco xml -o output/
```

### 4. Validación de Bancos GIFT
```bash
gift-linter bancos/mi_banco.gift
```

## Configuración YAML (`examen.yaml`)

```yaml
titulo: "Primer Parcial - Programación 1"
materia: "Programación 1"
institucion: "Universidad Nacional de Río Negro"
fecha: "2026-05-15"
duracion: "90 minutos"
instrucciones:
  - "Responda en la grilla de respuestas."
  - "No se permite el uso de material de consulta."

layout:
  tipo: "compact-2col"  # Opciones: default, compact-2col, compact-3col, compact-4col
  modo_bn: true         # Optimización para fotocopias / ahorro de tinta

secciones:
  - nombre: "Teoría y Conceptos"
    categoria: "Teoria/**"
    cantidad: 5
    puntos_por_pregunta: 1.0

  - nombre: "Análisis de Código"
    categoria: "Codigo/Punteros"
    cantidad: 3
    puntos_por_pregunta: 2.0
```

## Reglas y Buenas Prácticas
- **Layouts**: Usar `compact-2col` o `compact-3col` para exámenes extensos; reducen entre 30% y 60% el consumo de papel.
- **Determinismo**: Pasar `--semilla <int>` o fijar la semilla en la configuración para reproducciones exactas de variantes.
- **Verificación**: Correr siempre `gift-linter` antes de generar exámenes masivos para atrapar caracteres de escape no balanceados en GIFT.
