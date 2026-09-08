# Lineamientos de Integración y Desarrollo del Ecosistema P1
## Cátedra de Programación 1 — Universidad Nacional de Río Negro

Este documento establece las directivas arquitectónicas, técnicas, pedagógicas y de control de versiones obligatorias para desarrollar, auditar e incorporar nuevas herramientas a la suite de la cátedra.

---

## 1. Commits Semánticos Obligatorios (Conventional Commits)

Todo aporte al ecosistema debe registrarse mediante **commits semánticos estructurados** siguiendo la especificación [Conventional Commits v1.0.0](https://www.conventionalcommits.org/).

### 1.1 Formato General
```text
<tipo>(<alcance>): <descripción directa en minúsculas y sin punto final>

[cuerpo opcional detallando el motivo del cambio, alternativa descartada y verificación]

[pie opcional con referencias a tickets o breaking changes]
```

### 1.2 Tipos Permitidos
* **`feat`**: Nueva funcionalidad, comando CLI, subcomando, regla pedagógica o exportador.
* **`fix`**: Corrección de bugs, regresiones, fallos de parsing o excepciones no controladas.
* **`docs`**: Modificaciones exclusivas en documentación (`README.md`, manuales, `ecosistema/*.md`).
* **`style`**: Ajustes de formato, espaciado o limpieza que no alteran la lógica de ejecución.
* **`refactor`**: Reestructuración interna del código sin modificar la API pública ni agregar features.
* **`perf`**: Optimizaciones algorítmicas, reducción de consumo de memoria o tiempo de ejecución.
* **`test`**: Nuevos tests unitarios, fixtures de prueba o casos de prueba para el smoke test.
* **`build`**: Cambios en empaquetado (`pyproject.toml`), dependencias externas o scripts de construcción.
* **`ci`**: Ajustes en workflows automatizados o integración continua.
* **`chore`**: Tareas de mantenimiento, sincronización de repositorios o actualización de `.gitignore`.

### 1.3 Alcances (`scope`)
El alcance debe identificar con precisión el componente modificado:
* Nombre del paquete: `(deckard)`, `(dredd)`, `(ripley)`, `(gaff)`, `(daedalus)`, `(bishop)`, etc.
* Módulos transversales: `(doctor)`, `(cli)`, `(smoke-test)`, `(ast)`, `(reporter)`.

### 1.4 Ejemplos Válidos
```bash
git commit -m "feat(gaff): verificar indentacion estricta en multiplos de 4 espacios"
git commit -m "fix(dredd): suprimir git pull durante evaluacion en repositorios locales"
git commit -m "docs(p1-tools): actualizar manual de integracion para nuevas herramientas"
git commit -m "feat(bishop): incorporar visualizador ascii de bloques dinamicos de heap"
```

---

## 2. Arquitectura Estándar de una Herramienta

Toda herramienta debe implementarse como un paquete Python modular e independiente, empaquetado con estándares modernos (`pyproject.toml`).

### 2.1 Estructura de Directorios Mandatoria
```text
<nombre_herramienta>/
├── pyproject.toml               # Configuración declarativa (hatchling / flit / uv)
├── README.md                    # Manual conciso de instalación, flags y ejemplos de uso
├── src/
│   └── <nombre_herramienta>/
│       ├── __init__.py          # Define __version__
│       ├── cli.py               # Punto de entrada CLI con Typer y Rich
│       └── core/                # Lógica pura desacoplada de la terminal
│           ├── doctor.py        # Diagnóstico del entorno y dependencias del sistema
│           └── ...              # Módulos específicos de dominio
└── tests/
    ├── test_cli.py              # Tests de integración de la interfaz de comandos
    ├── test_doctor.py           # Pruebas del subcomando doctor
    └── test_domain.py           # Pruebas unitarias de las funciones centrales
```

### 2.2 Requisitos de `pyproject.toml`
* Soporte para Python 3.10 o superior.
* Declaración explícita del punto de entrada en `[project.scripts]`:
  ```toml
  [project.scripts]
  nombre_herramienta = "nombre_herramienta.cli:app"
  ```
* Dependencias mínimas y controladas (preferir `typer`, `rich`, bibliotecas de la biblioteca estándar de Python y herramientas nativas del sistema operativo).

---

## 3. Convenciones de Interfaz de Línea de Comandos (CLI)

### 3.1 Framework y Experiencia de Usuario
* **Typer + Rich**: La interfaz se implementa con `typer` y los mensajes visuales se formatean mediante `rich` (tablas, paneles, colores sobrios).
* **Autocompletado**: Los comandos deben admitir autocompletado en el shell (`--install-completion` / `--show-completion`).

### 3.2 Banderas Universales Obligatorias
1. `--version` / `-v`: Imprime la versión actual del paquete con `is_eager=True` y finaliza con código 0.
2. `--help` / `-h`: Ofrece ayuda detallada con ejemplos concisos.
3. `--json`: Emite el resultado estructurado en formato JSON estándar a `stdout`. Esto permite la composición por tuberías (`pipes`) y la ingesta desde `dredd`.
4. `--output-md` / `-o` (opcional según el caso): Genera un fragmento Markdown estructurado apto para ser incrustado en el informe de evaluación docente de `dredd`.

### 3.3 Subcomando `doctor` Mandatorio
Toda herramienta que dependa de binarios del sistema (`gcc`, `gdb`, `valgrind`, `clang-format`, `typst`, `bubblewrap`, `git`, etc.) **debe implementar un subcomando `doctor`**:
* Inspecciona la presencia y versión de los binarios requeridos en el `PATH`.
* Verifica permisos de ejecución o capacidades del kernel (como soporte de namespaces para Bubblewrap).
* Retorna código de salida `0` si todos los requisitos se cumplen o código no cero si falta algún componente crítico, indicando con precisión cómo instalarlo en Ubuntu/Debian y Fedora.

Ejemplo de uso:
```bash
daedalus doctor
gaff doctor
dredd doctor
```

---

## 4. Estándares de Código y Pedagogía

### 4.1 Tipado Estático y Robustez
* **Type Annotations**: Obligatorias en todas las funciones y métodos públicos.
* **Encabezado Moderno**: Incluir `from __future__ import annotations` en todos los archivos `.py`.
* **Manejo de Errores**: Prohibido usar bloques `except:` vacíos o genéricos sin registrar la causa. Degradar graciosamente ante herramientas opcionales faltantes.
* **Desacoplamiento**: La lógica central (`core/`) no debe depender de `typer` ni escribir directamente a `sys.stdout`. Debe retornar estructuras de datos o aceptar un objeto de consola opcional.

### 4.2 Idioma y Tono Pedagógico
* **Español Rioplatense con Voseo**: Todos los mensajes por terminal, descripciones de ayuda, diagnósticos de error y documentación deben redactarse en español rioplatense directo con voseo (`revisá`, `ejecutá`, `hacé`, `verificá`, `configurá`).
* **Terminología**: Los bucles se denominan formalmente **lazos** (lazo `for`, lazo `while`).
* **Explicación Causal**: Cada diagnóstico pedagógico debe explicar la **causa raíz conceptual** del error y guiar al estudiante hacia la solución autónoma, evitando volcados técnicos incomprensibles.

---

## 5. Pruebas y Cobertura (100% Passing)

1. **Suite `pytest` Completa**: Todo el código debe tener pruebas automatizadas en el subdirectorio `tests/`.
2. **Aislamiento**: Las pruebas de manipulación de archivos deben usar fixtures aisladas (`tmp_path`).
3. **Negative Testing (Pruebas de Fallo Deliberado)**: Cada regla, linter o analizador debe incluir pruebas con fragmentos de código en C que contengan el fallo deliberado, comprobando que la herramienta lo detecte, emita el código de regla correspondiente y retorne un estado de fallo.
4. **Validación del Smoke Test**: Antes de dar por integrada una herramienta, debe incluirse en la batería `scripts/health_check.sh` y verificarse contra el `student-smoke-test`.

---

## 6. Procedimiento Paso a Paso para Agregar una Nueva Herramienta

Para incorporar una nueva herramienta (`mi-herramienta`) al ecosistema P1:

1. **Crear el repositorio**:
   Inicializar el repositorio Git bajo la organización `INGCOM-UNRN-P1` con la estructura estándar descripta en la sección 2.
2. **Implementar el CLI y subcomando `doctor`**:
   Garantizar las banderas `--help`, `--version`, `--json` y el comando `mi-herramienta doctor`.
3. **Escribir la documentación de la herramienta**:
   Crear el archivo `ecosistema/mi-herramienta.md` detallando:
   - Propósito didáctico.
   - Requisitos y dependencias.
   - Comandos principales y flags.
   - Ejemplos de uso con entradas y salidas reales.
4. **Crear la Skill Pedagógica**:
   Crear la carpeta `skills/mi-herramienta/SKILL.md` con las instrucciones específicas para que los agentes de IA (Gemini, Antigravity, Claude) sepan cuándo y cómo invocarla.
5. **Registrar en los scripts de gestión global**:
   - Agregar el repositorio a la lista `REPOSITORIOS` en `scripts/clone_repos.sh`.
   - Agregar el binario a la lista de auditoría en `scripts/health_check.sh`.
6. **Actualizar el Catálogo**:
   Incorporar la herramienta al índice temático en `ecosistema/index.md` y en la tabla general de `README.md`.
