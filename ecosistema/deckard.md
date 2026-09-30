# deckard

Gestor de bancos de ejercicios prácticos, guías y graduación para cátedras de C.

## 🎯 Propósito y Alcance

`deckard` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "deckard[ecosistema,languagetool] @ git+https://github.com/INGCOM-UNRN/deckard"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
deckard --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN/deckard#referencia-rápida), generada desde `deckard --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `deckard <comando> -h`.

## ⚙️ Configuración y Opciones

`deckard` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `deckard`.

## 📖 Documentación y Detalles Técnicos

# Deckard — Gestor de Bancos de Ejercicios, Guías y Graduación

> *"Se ha reportado que algunos replicantes escapan..."* — Rick Deckard administra
> las pruebas: qué ejercicio va a cada guía, con qué dificultad taxonómica y cuánto tiempo insume.

`deckard` es la herramienta docente del ecosistema P1 para la **autoría atómica, curaduría pedagógica, verificación técnica y exportación multiformato** de ejercicios prácticos de C.

Cada ejercicio vive en una carpeta aislada con metadata YAML (`tema`, nivel de **Bloom 1-5**, minutos estimados, pistas progresivas), su solución modelo en C (`solucion.c`), su enunciado en Markdown y su suite de tests.

---

## ⚡ Instalación

```bash
# Instalación global editable con uv
uv tool install . --editable --force

# O en entorno virtual local
uv sync
uv run deckard --help
```

---

## 🚀 Inicio Rápido

```bash
# 1. Inicializar la estructura del banco y guías
deckard init

# 2. Crear un nuevo ejercicio
deckard new invertir-pares --titulo "Invertir pares" --tema arreglos --bloom 3 --minutos 25

# 3. Inspeccionar el banco y enunciados
deckard bank list
deckard show invertir-pares -s -p

# 4. Verificar la solución modelo con Ripley
deckard verify invertir-pares

# 5. Crear una especificación y componer una guía balanceada
deckard spec new parcial1.yaml --duracion 90 --margen 0.8 --temas "arreglos,punteros" --bloom-min 2 --bloom-max 4
deckard spec compose parcial1.yaml

# 6. Exportar la guía a PDF y Markdown
deckard export guias/parcial1.yaml --type=pdf,md -o dist/
```

---

## 🧭 Mapa de Comandos de Deckard

### 1. Banco y Enunciados
* `deckard init`: Inicializa la estructura `banco/`, `guias/` y un ejercicio de ejemplo.
* `deckard new <id>`: Crea un nuevo ejercicio con esqueleto completo (`ejercicio.yaml`, `solucion.c`, `enunciado.md`, `tests/`).
* `deckard bank list`: Catálogo tabular del banco con filtros por tema, nivel de Bloom y estado de verificación.
* `deckard show <id>`: Inspección en consola de enunciados, soluciones, pistas progresivas, tests y metadata (`-s`, `-p`, `--tests`, `--todos`, `--raw`).

### 2. Especificaciones Pedagógicas (`deckard spec`)
* `deckard spec new <archivo>`: Crea especificaciones de diseño curricular (`GuiaSpec`).
* `deckard spec list`: Lista specs con duración nominal, carga útil calculada, temas y rango Bloom.
* `deckard spec show <archivo>`: Detalle del spec y candidatos elegibles en el banco.
* `deckard spec validate <archivo>`: Diagnóstico de satisfactibilidad temática y temporal contra el banco actual.
* `deckard spec edit <archivo>`: Modificación de parámetros de la especificación por CLI.
* `deckard spec compose <archivo>`: Composición directa de la guía a partir del spec.

### 3. Guías de Trabajos Prácticos (`deckard guide`)
* `deckard guide list`: Lista guías compuestas en `guias/` con desglose de ejercicios y verificación.
* `deckard guide show <guia>`: Muestra ejercicios, carga horaria, temas y enunciados.
* `deckard guide compose <spec>`: Algoritmo knapsack de balanceo pedagógico.
* `deckard guide add <guia> <ejercicio>`: Incorpora un ejercicio y recalcula métricas.
* `deckard guide remove <guia> <ejercicio>`: Remueve un ejercicio y actualiza la guía.
* `deckard guide verify <guia>`: Verifica todas las soluciones modelo de la guía con Ripley.
* `deckard guide export <guia>`: Exporta la guía completa a PDF, Markdown o HTML.

### 4. Exportación Multiformato (`deckard export`)
* `deckard export <objetivo>`: Exporta ejercicios o guías a **PDF**, **Markdown** o **HTML** (`--type=pdf,md,html`).
* `deckard export templates init`: Copia plantillas por defecto (HTML, Markdown y `estilos.css`) a `./templates/` o global (`--global`).
* `deckard export templates list`: Lista plantillas descubiertas (locales, globales y built-in).

### 5. Verificación, Fuzzing y Arnés (`deckard verify`)
* `deckard verify [id]`: Verificación de reglas pedagógicas y compilación con `ripley check`. Admite comodines, `--all`, barra de progreso interactiva y generación de reporte de fallos (`--log-fallos`).
  > Los ejercicios que fallan se marcan automáticamente como no-verificados (`verificado: false`).
* `deckard verify fuzz [id]`: Fuzzing y endurecimiento de testcases con `dredd fuzz-gen` y libFuzzer.
* `deckard verify test-harness <id> <spec>`: Arnés de pruebas con inyección de fallos de malloc vía `vasquez inject`.

### 6. Empaquetado y Distribución
* `deckard pack <objetivo>`: Empaqueta ejercicios/guías en archivos firmados `.ripkg` y genera starter repos para GitHub Classroom.
* `deckard multiplex <spec>`: Generador de variantes combinatorias de TPs con asignación determinista por padrón/legajo.

---

## 📖 Documentación Detallada

Para una guía paso a paso con todos los flujos pedagógicos, modelos de datos, personalización de plantillas CSS y ejemplos de integración con Ripley y Dredd, consultá el [**Manual Integral de Uso (`MANUAL.md`)**](https://github.com/INGCOM-UNRN/deckard/blob/main/MANUAL.md).

---

## 🏗️ Integración en el Ecosistema

| Herramienta | Rol en el ecosistema |
| :--- | :--- |
| **deckard** | Banco de ejercicios, balanceo pedagógico (Bloom) y exportación multiformato. |
| **ripley** | Verificación estática/dinámica de soluciones modelo y sandbox docente. |
| **dredd** | Corrección masiva de entregas de alumnos, feedback y fuzzing de testcases. |
| **alucard** | Síntesis de exámenes, question banks (GIFT/Moodle) y tracing C con GCC. |
| **idkfa** | Generador de cuestionarios Moodle XML aleatorizados y anti-trampas. |
| **myst-tools** | Validador y gestor de enlaces/anclas para documentación MyST Markdown. |


## 📊 Formatos de Salida

`deckard` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
