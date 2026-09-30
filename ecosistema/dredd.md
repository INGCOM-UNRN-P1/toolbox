# dredd

Multi-channel batch autograder and submission manager for C programming courses (GitHub Classroom & Moodle)

## 🎯 Propósito y Alcance

`dredd` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install "dredd[ecosistema,guias] @ git+https://github.com/INGCOM-UNRN-P1/dredd"
```

## 🚀 Guía de Uso

### Invocación básica

```bash
dredd --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: dredd [OPTIONS] COMMAND [ARGS]...                                       
                                                                                
 Orquestador docente de evaluación masiva y gestión de entregas (GitHub         
 Classroom + Moodle).                                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ init           Inicializa un espacio de trabajo de Dredd con carpetas        │
│                estructuradas y mapeo declarativo en dredd.yaml.              │
│ eval           Clona/actualiza el repositorio o evalúa entregas locales,     │
│                ejecuta el análisis con Ripley y genera el informe Markdown.  │
│ comment        Envía el informe Markdown generado como comentario en el Pull │
│                Request de GitHub.                                            │
│ plagiarism     Calcula la matriz de similitud Winnowing entre todas las      │
│                entregas descargadas.                                         │
│ pr-fix         Reconstruye o crea el Pull Request de corrección para un      │
│                estudiante (reemplaza prfix.sh).                              │
│ map            Mapeo interactivo y heurístico entre archivos C de            │
│                estudiantes y especificaciones de la guía.                    │
│ export         Exporta calificaciones CSV, paquete ZIP de retroalimentación  │
│                y dashboard consolidado de cohorte.                           │
│ export-report  Convierte un informe Markdown a HTML autocontenido            │
│                enriquecido o PDF (zero-dependencies).                        │
│ fuzz-gen       fuzz-gen: endurece el banco generando casos límite contra la  │
│                solución modelo.                                              │
│ oral-guide     oral-exam-companion: genera una guía de preguntas para        │
│                coloquio/defensa.                                             │
│ multiplex      tp-multiplexer: Genera variantes combinatorias y asignación   │
│                determinista por alumno.                                      │
│ moodle         Gestión de canales Moodle (ingesta ZIP y planillas).          │
│ config         Gestión de configuración, entregas, guías y políticas de      │
│                chequeo.                                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`dredd` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `dredd`.

## 📖 Documentación y Detalles Técnicos

# Dredd: Juez de Trabajos Prácticos y Orquestador Docente

Orquestador docente de evaluación masiva, autograding multicanal y gestión de entregas en C (compatible con **GitHub Classroom** y **Moodle**).

---

## 🚀 Instalación y Entorno

Dredd está desarrollado en Python 3.11+ con `typer` y `rich`.

```bash
# Instalación en modo desarrollo
cd dredd
uv sync --extra dev

# Ver catálogo de comandos
uv run dredd --help
```

---

## 🛠️ Flujos de Trabajo y Comandos

### 1. Flujo GitHub Classroom

#### Evaluación de Entregas (`dredd eval`)
Clona o actualiza el repositorio en `<actividad>-submissions/<estudiante>/`, ejecuta el análisis con el motor Ripley (o fallback nativo con reglas P1 de cátedra) y ensambla `${estudiante}.md`:

```bash
# Evaluar un estudiante puntual
dredd eval tp01 alvarez_juan

# Evaluar toda la cohorte presente en el workspace
dredd eval tp01 --all
```

#### Publicación de Feedback en GitHub (`dredd github comment`)
Envía automáticamente el informe `${estudiante}.md` como comentario en el Pull Request abierto del estudiante utilizando GitHub CLI (`gh`):

```bash
dredd github comment tp01 alvarez_juan --open
```

#### Creación / Reparación de Pull Requests (`dredd github pr-fix`)
Reconstruye o abre el Pull Request de corrección en caso de que el estudiante no lo haya generado o haya alterado las ramas base:

```bash
dredd github pr-fix tp01 alvarez_juan https://github.com/INGCOM-UNRN-P1/tp01-alvarez_juan
```

---

### 2. Flujo Moodle

#### Ingesta Masiva y Versionado (`dredd moodle ingest`)
Descomprime el ZIP masivo de Moodle, normaliza la codificación a UTF-8 (soportando CP1252, ISO-8859-1 y UTF-8-sig), aplana las carpetas y genera versiones deterministas (`r1`, `r2`, ...) mediante hash SHA-256 en `.metadata.db`:

```bash
dredd moodle ingest entregas_tp01.zip
```

#### Mapeo Interactivo de Archivos (`dredd map`)
Vincula heurísticamente o mediante interfaz interactiva los archivos fuente `.c` de los estudiantes con los testcases correspondientes, guardando las reglas en `mappings.json`:

```bash
dredd map tp01_1228009 -e ejercicio1 -e ejercicio2 --auto
```

#### Exportación de Calificaciones y Dashboard (`dredd export` / `dredd moodle export`)
Genera el archivo CSV compatible con el Libro de Calificaciones de Moodle, el ZIP de retroalimentación masiva para subir al aula virtual y el reporte `dashboard.md` con estadísticas de la cohorte:

```bash
# Exportación completa (CSV + ZIP + Dashboard)
dredd export tp01_1228009

# Exportación puntual de planilla CSV
dredd moodle export -e tp01 -o calificaciones.csv
```

---

### 3. Herramientas de Auditoría y Reportes

#### Detección de Plagio con Winnowing (`dredd plagiarism`)
Calcula la matriz de similitud de código fuente normalizado en todas las entregas descargadas utilizando el algoritmo Winnowing:

```bash
dredd plagiarism tp01_1228009 --threshold 0.70
```

#### Conversión de Informes a HTML / PDF (`dredd export-report`)
Convierte informes Markdown a HTML enriquecido autocontenido (con CSS embebido) o PDF con formato de imprenta (generación pura en Python sin dependencias externas pesadas):

```bash
# Exportar a HTML
dredd export-report tp01_1228009/alvarez_juan/alvarez_juan.md --format html

# Exportar a PDF
dredd export-report tp01_1228009/alvarez_juan/alvarez_juan.md --format pdf
```

---

## 🧱 Arquitectura del Paquete

```
src/dredd/
├── cli.py               # Punto de entrada Typer y comandos CLI
└── core/
    ├── ast_checker.py   # Linter nativo de reglas P1 (0xXXXXh) y AST
    ├── db.py            # Capa SQLite de persistencia (.metadata.db)
    ├── exporter.py      # Generador de CSV Moodle, ZIP feedback y dashboard
    ├── git_ops.py       # Gestión de caché local de repositorios de estudiantes
    ├── github_api.py    # Integración con gh CLI (PRs y comentarios)
    ├── ingest.py        # Ingesta masiva de ZIPs Moodle, encodings y SHA-256
    ├── makefile_eval.py # Soporte para proyectos modulares con Makefiles
    ├── mapping.py       # Mapeo heurístico e interactivo (mappings.json)
    ├── moodle.py        # Adaptadores y utilitarios para Moodle
    ├── plagiarism.py    # Detector de similitud por huellas Winnowing
    ├── report_export.py # Conversor Markdown a HTML y PDF (zero-dependencies)
    ├── reporter.py      # Ensamblador de informes Markdown modulares
    └── ripley_client.py # Cliente de integración con el motor stateless Ripley
```


## 📊 Formatos de Salida

`dredd` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
