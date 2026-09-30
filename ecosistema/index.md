# Ecosistema de Herramientas Pedagógicas de C
## Cátedra de Programación 1 — Universidad Nacional de Río Negro

Este catálogo documenta integralmente las 41 herramientas pedagógicas, linters, visualizadores de bajo nivel y motores de evaluación desarrollados para la formación en **C11 / GNU C** bajo estándares rigurosos de compilación (`-Wall -Wextra -Werror -pedantic`).

---

## 🗺️ Mapa Taxonómico del Ecosistema

### 0. Instalación y Diagnóstico del Ecosistema
* [**`mother`**](mother.md): Instala, actualiza y diagnostica las herramientas por perfil (estudiante, análisis, docente, contenido, aula), siempre desde git y leyendo `ecosistema.toml`; también como `mother.pyz`.

### 1. Estilo, Buenas Prácticas y Antipatrones
* [**`gaff`**](gaff.md): Linter de estilo y convenciones arquitectónicas de cátedra. Audita indentación en múltiplos de 4 espacios, naming sin sufijos/prefijos numéricos redundantes (`num_1`, `a_n`), máximo un único return por función, `snake_case` estricto y guardas de encabezado.
* [**`spunkmeyer`**](spunkmeyer.md): Detector de antipatrones didácticos en C. Marca patrones viciosos como `while(!feof())`, casteo innecesario de `malloc()`, verificación redundante de `NULL` antes de `free()`, retornos de punteros a variables de stack y comparaciones booleanas redundantes (`if (cond == true)`).
* [**`ripley`**](ripley.md): Linter pedagógico central y motor de reglas de cátedra (`0xXXXXh`). Audita reglas de estilo, funciones extensas, uso de globales y arquitectura de entregas.
* [**`zhora`**](zhora.md): Linter y auditor de seguridad de macros del preprocesador (`#define`): efectos de lado por evaluación múltiple de parámetros, falta de paréntesis defensivos y puntos y coma espurios.

### 2. Compilación, Diagnóstico y Manejo de Errores
* [**`daedalus`**](daedalus.md): Compilador pedagógico que ejecuta GCC/Clang bajo las banderas estrictas de cátedra y traduce diagnósticos crudos a explicaciones claras en español rioplatense.
* [**`hal`**](hal.md): Diagnóstico pedagógico de fallos fatales (`SIGSEGV`, `SIGABRT`, `SIGFPE`, doble liberación) con decodificación de core dumps e indicación de la línea exacta del fallo.
* [**`tetsuo`**](tetsuo.md): Compila y ejecuta programas bajo AddressSanitizer y UndefinedBehaviorSanitizer y traduce sus diagnósticos a explicaciones en español con sugerencias de corrección.
* [**`esper`**](esper.md): **retirado**; lo reemplaza `daedalus`, que explica los diagnósticos de GCC.

### 3. Inspección de Memoria y Arquitectura Interna
* [**`bishop`**](bishop.md): Trazador visual de memoria C. Genera diagramas ASCII y Mermaid de Stack Frames, variables locales, relaciones entre punteros y bloques del Heap (`malloc`/`free`).
* [**`brett`**](brett.md): Auditor de alineación de memoria y padding en structs de C. Calcula bytes desperdiciados y propone el reordenamiento óptimo de campos.
* [**`sebastian`**](sebastian.md): Analizador de funciones recursivas, cálculo de tamaño de stack frame y prevención de Stack Overflow.
* [**`kane`**](kane.md): Inspector de archivos binarios generados con `fread`/`fwrite`: muestra cada registro mapeado a la definición del `struct`, con offsets en hexadecimal y detección de bytes truncados.

### 4. Seguridad y Ejecución en Sandbox
* [**`kaneda`**](kaneda.md): Auditor de seguridad estática. Bloquea llamadas peligrosas (`gets`, `strcpy`, `sprintf`, `scanf` sin límite de ancho, `system`, `popen`, fork bombs).
* [**`nostromo`**](nostromo.md): Sandbox aislado de ejecución mediante Bubblewrap y `setrlimit` con cuotas estrictas de CPU y memoria RAM.
* [**`callahan`**](callahan.md): Verificación formal de contratos ACSL (precondiciones, postcondiciones, invariantes de lazo) con Frama-C WP.

### 5. Fuzzing, Mocks y Testing
* [**`drake`**](drake.md): Fuzzer guiado por límites de frontera (`INT_MAX`, `INT_MIN`, buffers límite, saltos de línea extremos).
* [**`holden`**](holden.md): Generador de mocks e inyector determinista de fallos de memoria (`malloc` retornando `NULL`) o E/S (`fopen` fallando).
* [**`vasquez`**](vasquez.md): Motor de inyección de fallos de entorno: hace fallar `malloc`/`calloc`/`realloc`/`strdup` (NULL) y `fopen`/`fwrite`/`fread`/`fclose` para verificar que el programa maneje los errores en lugar de terminar con `SIGSEGV`.
* [**`vassili`**](vassili.md): Mutation testing: inyecta mutantes en el código (operadores aritméticos, relacionales y lógicos) y calcula qué porcentaje detecta la suite de pruebas del estudiante.
* [**`dietrich`**](dietrich.md): Cobertura lógica MC/DC: desglosa las decisiones compuestas (`if (A && (B || C))`) en condiciones atómicas y propone la tabla de verdad y los vectores de prueba mínimos.
* [**`tyrell`**](tyrell.md): Generador determinista de casos de prueba (`.in`/`.out`) con restricciones configurables (enteros, cadenas, arreglos, valores extremos), en el formato que lee `nostromo test`.
* [**`student-smoke-test`**](student-smoke-test.md): Batería de verificación integral de extremo a extremo que valida todas las herramientas del entorno.

### 6. Análisis de Control de Flujo, Rendimiento y Bajo Nivel
* [**`rachel`**](rachel.md): Desensamblador comparativo de estructuras de control (`switch` vs cadenas `if-else`, tablas de salto, predicción de saltos).
* [**`giger`**](giger.md): Visualizador de Call Graphs (árboles de llamadas) y grafos de flujo de control (CFG), con detección de funciones muertas.
* [**`ferro`**](ferro.md): Perfilador de rendimiento: mide tiempo e instrucciones (Cachegrind) para varios tamaños de entrada e infiere la complejidad empírica ($O(N)$, $O(N \log N)$, $O(N^2)$).
* [**`parker`**](parker.md): Auditor de ABI y visibilidad de símbolos en bibliotecas compartidas y objetos ELF (`.so`, `.o`) y sus cabeceras: símbolos privados expuestos o faltantes.
* [**`crowe`**](crowe.md): Linter de portabilidad multi-arquitectura: detecta asunciones no portables (endianness, tamaño de punteros y de `long`, signo de `char`, VLAs) y puede validar la compilación cruzada para x86_64, aarch64 y riscv64.

### 7. Diseño Modular, TDAs y Documentación
* [**`motoko`**](motoko.md): Verificador de encapsulamiento de TDAs: detecta accesos directos a campos internos desde el código cliente y controla el uso de tipos opacos.
* [**`wierzbowski`**](wierzbowski.md): Auditor de la arquitectura de proyectos de varios archivos: grafo de `#include`, dependencias circulares, guardas de inclusión y Makefiles.
* [**`corbel`**](corbel.md): Generador de documentación de APIs y TDAs: extrae los comentarios Doxygen de las cabeceras (`@brief`, `@param`, `@pre`, `@post`) y genera Markdown o páginas `man 3`.

### 8. Evaluación Masiva, Autograding y Detección de Plagio
* [**`dredd`**](dredd.md): Orquestador docente central. Soporta:
  - Ingesta masiva desde Moodle (`dredd moodle ingest`) con normalización UTF-8, versionado SHA-256 en SQLite y creación de esqueleto ante prácticas desconocidas.
  - Gestión con GitHub Classroom (`dredd github clone`, `dredd github comment`, `dredd github pr-fix`).
  - Evaluación local segura (`dredd eval`) sin alteraciones destructivas de Git.
  - Carpetas modulares de reporte intermedio `i_<shorthash>/` e informes consolidados `<estudiante>_<shorthash>.md`.
  - Detección de código duplicado mediante el algoritmo Winnowing (`dredd plagiarism`).
  - Exportación de calificaciones a CSV compatible con Moodle (`dredd export`).
* [**`weyl`**](weyl.md): Comparador semántico de AST entre entregas de estudiantes y la solución canónica de cátedra.

### 9. Autoría de Materiales Didácticos y Exámenes
* [**`deckard`**](deckard.md): Autoría, composición y balance taxonómico (Bloom) de guías de trabajos prácticos. Calibra la carga horaria semanal (`deckard check-load`) y empaqueta en formato portable `.ripkg`.
* [**`idkfa`**](idkfa.md): Generador procedural de exámenes de tracing en C con compilación y ejecución GCC embebida para producir variantes anti-copia en Moodle XML.
* [**`alucarD`**](alucarD.md): Sintetizador de exámenes impresos de alta calidad tipográfica en Typst con integración de hojas OMR para corrección óptica.
* [**`moodle-toolbox`**](moodle-toolbox.md): Validador, formateador y conversor bidireccional (GIFT ↔ Moodle XML) para bancos de preguntas.
* [**`myst-tools`**](myst-tools.md): Herramientas para la gestión, cross-referencing y compilación de libros didácticos en MyST Markdown.

### 10. Criptografía y Empaquetado de Evaluaciones
* [**`keymaker`**](keymaker.md): Gestor criptográfico integral de confianza, firmas asimétricas Ed25519, sellado temporal Time-Lock y empaquetado seguro de exámenes.
* [**`scorm-tools`**](scorm-tools.md): Empaquetador y validador de cursos interactivos SCORM 1.2 / 2004 4th Edition para Moodle.
* [**`uatu-tools`**](uatu-tools.md): Validador forense (`uatu-audit`) y herramientas de cátedra (`uatu-admin`) de uatu, la proctorización Git-native de exámenes prácticos en VS Code.

### 11. Docencia Remota, Presentaciones y Telemetría de Clases
* [**`meet-tools`**](meet-tools.md): Sistema de control y monitoreo bidireccional para Google Meet desde dispositivos móviles Android y microcontroladores Wi-Fi.
* [**`slide-tools`**](slide-tools.md): Sistema de control remoto, sincronización de notas de orador y cronómetro para Google Slides.

### 12. Emulación y Sistemas Embebidos
* [**`hardboiled`**](hardboiled.md): Emulador pedagógico de un microcontrolador RISC-V de 32 bits (RV32I) bare-metal con depurador de C en la terminal y periféricos simulados (LEDs, switches, UART, timer con interrupciones).
