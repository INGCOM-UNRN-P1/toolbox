---
name: deckard
description: Use when authoring, cataloging, verifying, or composing balanced practical exercise guides and problem sets in C based on Bloom taxonomy levels and time budgets.
---

# Deckard — Gestor de Bancos de Ejercicios y Composición Pedagógica

## Overview
`deckard` es la herramienta de autoría y curaduría atómica de ejercicios de programación en C. Cada ejercicio se almacena como una unidad versionada con metadata pedagógica (`ejercicio.yaml`: tema, nivel de Bloom 1-5, duración estimada, pistas progresivas), código fuente y solución modelo. Permite inspeccionar enunciados con control granular de secciones, exportar a PDF con plantillas personalizables locales o globales, gestionar guías de trabajos prácticos, verificar con `ripley` y componer guías balanceadas mediante knapsack pedagógico.

## Cuándo Usar
- Para inspeccionar enunciados de ejercicios con selección de secciones (metadatos, solución, pistas, tests) (`deckard show`).
- Para compilar ejercicios individuales o guías completas a documentos PDF estilizados (`deckard export <id> -t pdf`, `deckard guide pdf`).
- Para listar, auditar, crear y gestionar guías de trabajos prácticos (`deckard guide`).
- Para inicializar un nuevo banco de ejercicios de programación o crear nuevos ejercicios estructurados.
- Para verificar soluciones modelo contra el motor de análisis estático y pruebas de Ripley (`deckard verify`).
- Para listar y auditar el estado del banco (cobertura por temas, niveles de Bloom, estado de verificación).
- Para armar guías balanceadas en tiempo y dificultad a partir de especificaciones YAML (`deckard compose`).
- Para endurecer suites de testcases mediante fuzzing con `dredd fuzz-gen` (`deckard fuzz`).

## Comandos CLI

### 1. Inspección y Creación de Ejercicios (`new` / `show`)
```bash
# Crear ejercicio con firmas de funciones requeridas
deckard new invertir-vector --titulo "Invertir Vector" --tema arreglos --bloom 3 -F "void invertir_vector(int* vec, size_t n); int longitud(const int* vec)"

# Ver enunciado formateado en terminal
deckard show invertir-vector

# Ver funciones requeridas, pistas, solución modelo y casos de prueba (I/O y funciones)
deckard show invertir-vector --solucion --pistas --tests

# Ver todas las partes
deckard show invertir-vector --todos

# Emitir texto plano sin formato Rich (para piping)
deckard show invertir-vector --todos --raw
```

### 2. Reorganización del Banco (`organize`)
```bash
# Reorganizar según nivel de Bloom y tipo de ejercicio (funciones vs io) [default]
deckard organize --by bloom/tipo

# Reorganizar solo por nivel de Bloom (b1-recordar/, b2-comprender/, ...)
deckard organize --by bloom

# Reorganizar por tipo y luego nivel de Bloom (funciones/b3-aplicar/, io/b1-recordar/)
deckard organize --by tipo/bloom

# Reorganizar por tema y luego Bloom (punteros/b3-aplicar/)
deckard organize --by tema/bloom

# Aplanar banco (todos en la raíz del banco)
deckard organize --by plano

# Simulación previa sin mover archivos en disco
deckard organize --dry-run

# Copiar a otro directorio en vez de mover
deckard organize --destino banco_organizado --copy
```

### 3. Exportación Multiformato (`export`)
```bash
# Exportar a PDF directamente (por defecto --type=pdf)
deckard export invertir-pares -t pdf -o ejercicio.pdf

# Exportar a múltiples formatos en simultáneo (--type=pdf,md o -t pdf,md,html)
deckard export invertir-pares --type=pdf,md,html -o dist/
deckard export guias/guia_punteros.yaml --type=pdf,md -o dist/

# Exportar a Markdown (.md)
deckard export invertir-pares -t md -o ejercicio.md

# Exportar a HTML autocontenido
deckard export invertir-pares -t html -o ejercicio.html

# Pipeline Markdown -> HTML -> PDF
deckard export invertir-pares -t pdf --pipeline-md -o ejercicio.pdf

# Exportar con solución y pistas incluidas
deckard export invertir-pares -s -p -o solucion.pdf

# Exportar múltiples ejercicios por comodín a una carpeta en múltiples formatos
deckard export "punteros-*" --type=pdf,md -o dist/
```

### 4. Personalización y Gestión de Plantillas (`export templates`)
```bash
# Inicializar y copiar plantillas por defecto (HTML, Markdown y estilos.css) a ./templates/
deckard export templates init
deckard export templates init --global # ~/.config/deckard/templates
deckard export templates init --force  # Sobrescribir

# Listar plantillas y hojas de estilo descubiertas en el entorno
deckard export templates list
```

### 5. Gestión y Validación de Especificaciones (`spec`)
```bash
# Listar todas las especificaciones de guías disponibles
deckard spec list

# Crear una nueva especificación de diseño pedagógico
deckard spec new parcial1.yaml --titulo "Primer Parcial" --duracion 90 --margen 0.8 --temas "punteros,arreglos" --bloom-min 2 --bloom-max 4

# Inspeccionar una spec y ver los ejercicios candidatos en el banco
deckard spec show parcial1.yaml

# Validar si el banco actual satisface el presupuesto y temas del spec
deckard spec validate parcial1.yaml

# Modificar parámetros de un spec existente
deckard spec edit parcial1.yaml --duracion 120 --margen 0.75

# Componer la guía directamente a partir del spec
deckard spec compose parcial1.yaml
```

### 6. Gestión de Guías de Trabajos Prácticos (`guide`) y Empaquetado (`pack`)
Las guías de trabajos prácticos residen en carpetas dedicadas dentro de `guias/`, donde la definición `guia.yaml` convive con los paquetes empaquetados `.ripkg`:

```text
guias/
└── guia_punteros/
    ├── guia.yaml
    ├── invertir-vector.ripkg
    └── contar-pares.ripkg
```

```bash
# Listar todas las guías en guias/ (descubre carpetas con guia.yaml y archivos .yaml)
deckard guide list

# Inspeccionar el detalle de una guía y sus ejercicios (acepta carpeta o archivo)
deckard guide show guia_punteros
deckard guide show guias/guia_punteros/guia.yaml --enunciados --soluciones

# Agregar o remover ejercicios de una guía compuesta
deckard guide add guia_punteros nuevo-ejercicio
deckard guide remove guia_punteros viejo-ejercicio

# Verificar todas las soluciones de una guía con Ripley
deckard guide verify guia_punteros

# Empaquetar todos los .ripkg de la guía dentro de su carpeta junto a guia.yaml
deckard pack guias/guia_punteros/guia.yaml
deckard pack guia_punteros --starter

# Exportar guía a PDF, Markdown o HTML
deckard guide export guia_punteros -t pdf -o parcial1.pdf
```

### 7. Auditoría de Salud del Banco y Enunciados (`audit` / `verify audit`)
Analiza la calidad de redacción y la completitud de componentes de cada ejercicio (longitud en caracteres y palabras, presencia de `enunciado.md`, `solucion.c`, `pistas`, `testcases` y `tags`):

```bash
# Auditar todo el banco
deckard audit
deckard verify audit

# Filtrar únicamente ejercicios con redacción pobre o incompleta (< 100 caracteres)
deckard audit --pobres
deckard audit --min-chars 150

# Filtrar ejercicios con componentes faltantes (sin tests, sin pistas, sin solución)
deckard audit --incompletos
deckard audit --sin-tests
deckard audit --sin-solucion
deckard audit --sin-pistas

# Salida estructurada JSON para pipelines CI
deckard audit --json
```

### 8. Gestión de Etiquetas / Tags (`tag`)
Permite clasificar, consultar y reetiquetar ejercicios de forma granular:

```bash
# Listar todas las etiquetas del banco con recuento de ejercicios
deckard tag list

# Agregar etiquetas a uno o más ejercicios por ID o comodín
deckard tag add invertir-vector punteros,memoria,algoritmos
deckard tag add "punteros-*" examen,parcial1

# Remover etiquetas
deckard tag remove invertir-vector facil

# Filtrar listados y auditorías por tag
deckard bank list --tag punteros
deckard audit --tag examen
```

### 9. Verificación Pedagógica, Fuzzing y Arnés de Pruebas (`verify`)
```bash
# 1. Verificación pedagógica con ripley check (con barra de progreso en batch y log de fallos)
deckard verify invertir-pares
deckard verify "punteros-*"
deckard verify --all --pendientes
deckard verify --all --log-fallos dist/verify_fallos.md

# Si un ejercicio falla en la verificación, queda automáticamente marcado como 'no-verificado' (verificado: false)

# 2. Fuzzing y endurecimiento de testcases con dredd (verify fuzz)
deckard verify fuzz invertir-pares -n 8
deckard verify fuzz "arreglos/*" --segundos 15
deckard verify fuzz --all --log-fallos dist/fuzz_fallos.md

# 3. Arnés de pruebas con inyección de fallos de malloc vía vasquez inject (verify test-harness)
deckard verify test-harness invertir-pares spec.yaml
```

### 10. Composición Automática de Guías (`compose`)
```bash
# Componer una guía balanceada según la especificación YAML
deckard compose guias/guia_punteros/guia.yaml
```

## Jerarquía de Plantillas para PDF y Markdown
1. **Locales al proyecto:** `./templates/<nombre>` o `<banco>/templates/<nombre>`
2. **Globales de usuario:** `~/.config/deckard/templates/<nombre>` o `~/.gemini/config/deckard/templates/<nombre>`
3. **Built-in de la herramienta:** `ejercicio.html`, `guia.html`, `ejercicio.md`, `guia.md`, `estilos.css`.
