# Toolbox — Ecosistema de herramientas pedagógicas de C
## Programación 1 — UNRN Andina

Bienvenido al repositorio central de documentación, gestión global y manuales operativos del ecosistema de herramientas pedagógicas de **Programación 1**.

Este repositorio contiene:
* La documentación técnica y funcional de todas las herramientas creadas por la cátedra ([`./ecosistema/`](ecosistema/index.md)).
* Los scripts de automatización para clonación, instalación y auditoría de salud del toolbox ([`./scripts/`](scripts/)).
* Las definiciones de skills pedagógicas para agentes de inteligencia artificial ([`./skills/`](skills/)).
* Las directivas y estándares arquitectónicos obligatorios para la incorporación de nuevas herramientas ([`LINEAMIENTOS.md`](LINEAMIENTOS.md)).
* El manual de uso para estudiantes ([`MANUAL_ESTUDIANTE.md`](MANUAL_ESTUDIANTE.md)).
* El manual para el equipo docente ([`MANUAL_DOCENTE.md`](MANUAL_DOCENTE.md)).

---

## 🚀 Inicio Rápido (Quickstart)

Podés poner a punto toda la estación de trabajo y el ecosistema completo en cuatro pasos ejecutados desde la raíz de este repositorio:

### 1. Clonar o sincronizar todos los repositorios de herramientas
```bash
./scripts/clone_repos.sh
```
*Clona los repositorios listados en [`ecosistema.toml`](ecosistema.toml) (herramientas, plantillas, librerías y documentación) o los actualiza con fast-forward si ya existen.*

### 2. Instalar las herramientas CLI en tu sistema
```bash
./scripts/install_tools.sh
```
*Instala cada herramienta en modo editable mediante `uv tool install --editable` y registra el autocompletado en tu shell (bash/zsh).*

### 3. Instalar las skills pedagógicas para agentes de IA
```bash
./scripts/install_skills.sh
```
*Despliega las skills pedagógicas de [`skills/`](skills/) en las rutas estándar de Gemini (`~/.gemini/config/skills/`), Claude y agentes locales.*

### 4. Auditar la salud del entorno
```bash
./scripts/health_check.sh
```
*Ejecuta el subcomando `doctor` en todas las herramientas para comprobar compiladores (`gcc`), depuradores (`gdb`), memoria (`valgrind`), linters (`clang-format`) y tipografía (`typst`).*

---

## 📚 Documentación y Manuales

| Documento | Audiencia | Propósito |
| :--- | :--- | :--- |
| [**`MANUAL_ESTUDIANTE.md`**](MANUAL_ESTUDIANTE.md) | **Estudiantes** | Flujo diario de resolución, linter de estilo con `gaff`, detección de antipatrones con `spunkmeyer`, traducción de errores con `daedalus`, trazado de memoria con `bishop`, diagnóstico de segfaults con `hal` y chequeo final con `ripley`. |
| [**`MANUAL_DOCENTE.md`**](MANUAL_DOCENTE.md) | **Docentes** | Planificación didáctica con `deckard`, generación procedural de exámenes con `idkfa`, maquetación en Typst con `alucarD`, ingesta de entregas Moodle/GitHub, evaluación masiva con `dredd`, detección de plagio Winnowing y publicación de notas. |
| [**`LINEAMIENTOS.md`**](LINEAMIENTOS.md) | **Desarrolladores** | Convenciones de arquitectura, Typer + Rich, subcomando `doctor`, banderas estándar (`--json`, `--version`), pruebas de fallo deliberado, Conventional Commits y estándares de código en español rioplatense. |
| [**`ecosistema/index.md`**](ecosistema/index.md) | **General** | Catálogo taxonómico exhaustivo con la ficha detallada de cada una de las 38 herramientas de la cátedra. |

---

## 🛠️ Catálogo Resumido de Herramientas

### Linters, Estilo y Calidad de Código
* [**`gaff`**](ecosistema/gaff.md): Linter de estilo y convenciones arquitectónicas (indentación x4, un solo return, snake_case, nombres sin sufijos numéricos).
* [**`spunkmeyer`**](ecosistema/spunkmeyer.md): Detector de antipatrones didácticos C (`while(!feof())`, malloc casts, punteros colgantes).
* [**`ripley`**](ecosistema/ripley.md): Motor pedagógico central y validador de reglas `0xXXXXh` de cátedra.
* [**`corbel`**](ecosistema/corbel.md): Normalizador de preprocesador y formato estandarizado de código.
* [**`dietrich`**](ecosistema/dietrich.md): Linter de inclusión mínima de encabezados (`#include`).
* [**`parker`**](ecosistema/parker.md): Auditor de macros y constantes `#define`.

### Compilación y Diagnóstico Pedagógico
* [**`daedalus`**](ecosistema/daedalus.md): Compilador estricto C11 (`-Wall -Wextra -Werror -pedantic`) con traducción de diagnósticos a español rioplatense.
* [**`hal`**](ecosistema/hal.md): Diagnóstico pedagógico de segfaults (`SIGSEGV`), abortos (`SIGABRT`) y core dumps.
* [**`esper`**](ecosistema/esper.md): Wrapper de compilación con perfiles pedagógicos preconfigurados.

### Memoria, Structs y Bajo Nivel
* [**`bishop`**](ecosistema/bishop.md): Trazador e inspector visual de Stack Frames, Heap y relaciones de punteros en tablas ASCII y Mermaid.
* [**`brett`**](ecosistema/brett.md): Auditor de padding y alineación de structs C con cálculo de reordenamiento óptimo de memoria.
* [**`sebastian`**](ecosistema/sebastian.md): Analizador de funciones recursivas, profundidad de pila y riesgo de desborde de stack.
* [**`zhora`**](ecosistema/zhora.md): Auditor de fugas de descriptores de archivos (`fclose`).
* [**`rachel`**](ecosistema/rachel.md): Desensamblador y comparador de costo computacional (`switch` vs `if-else`).
* [**`giger`**](ecosistema/giger.md): Analizador de Call Graphs (árbol de llamadas) y grafos de flujo de control (CFG).

### Seguridad y Ejecución en Sandbox
* [**`kaneda`**](ecosistema/kaneda.md): Auditor de seguridad estática (bloqueo de `gets`, `strcpy`, `sprintf`, `scanf` sin límite de ancho).
* [**`nostromo`**](ecosistema/nostromo.md): Sandbox aislado de ejecución mediante Bubblewrap y `setrlimit`.
* [**`callahan`**](ecosistema/callahan.md): Verificación formal de contratos ACSL con Frama-C WP.

### Testing y Fuzzing
* [**`drake`**](ecosistema/drake.md): Fuzzer guiado por valores de frontera (`INT_MAX`, `INT_MIN`, desbordes).
* [**`holden`**](ecosistema/holden.md): Generador de mocks e inyector determinista de fallos de memoria e I/O.
* [**`vassili`**](ecosistema/vassili.md): Analizador de cobertura de código para suites de pruebas.

### Evaluación Masiva y Autograding Docente
* [**`dredd`**](ecosistema/dredd.md): Orquestador masivo de corrección para Moodle y GitHub Classroom, sin `git pull` destructivo, con carpetas `i_<shorthash>/` y detección de plagio por huellas de Winnowing.
* [**`weyl`**](ecosistema/weyl.md): Comparador estructural y semántico de AST contra la solución canónica.

### Autoría de Guías y Exámenes
* [**`deckard`**](ecosistema/deckard.md): Autoría y calibración horaria de guías de trabajos prácticos bajo Taxonomía de Bloom.
* [**`idkfa`**](ecosistema/idkfa.md): Generador procedural de exámenes de tracing en C con GCC embebido para Moodle XML.
* [**`alucarD`**](ecosistema/alucarD.md): Sintetizador tipográfico de exámenes impresos en Typst con hojas de respuesta OMR.
* [**`moodle-toolbox`**](ecosistema/moodle-toolbox.md): Conversión bidireccional GIFT ↔ Moodle XML y mantenimiento de bancos de preguntas.
* [**`myst-tools`**](ecosistema/myst-tools.md): Gestión y compilación de libros didácticos en MyST Markdown.

---

## Integración de Nuevas Herramientas

Para agregar una nueva herramienta al ecosistema, consultá la guía paso a paso en [**`LINEAMIENTOS.md`**](LINEAMIENTOS.md).
El procedimiento incluye la creación del paquete con `typer` + `rich`, la implementación obligatoria de `<herramienta> doctor`, la redacción del manual en `ecosistema/<herramienta>.md`, la creación de la skill en `skills/<herramienta>/SKILL.md` y su registro en [`ecosistema.toml`](ecosistema.toml) (de ahí lo toman los scripts de clonado, instalación y salud, y el CI; `python3 scripts/ecosistema.py verificar` controla que el manifiesto coincida con los repos).

Y por otro lado, ¡se aceptan contribuciones!
