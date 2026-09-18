# Student Smoke Test Suite

Proyecto integral de demostración y suite de **Smoke Test** que ejercita todas las herramientas del ecosistema de C desde la perspectiva del estudiante, con código fuente 100% explícito (sin heredocs dinámicos ni generación en tiempo de ejecución en scripts).

---

## 🛠️ Herramientas Demostradas

| # | Herramienta | Rol / Funcionalidad Ejercitada | Archivos Involucrados |
|---|---|---|---|
| 1 | **DAEDALUS** | Compilación estricta y traducción pedagógica de errores a español. | `src/main.c`, `src/data_structures.c`, `src/parser.c` |
| 2 | **GAFF** | Linter de estilo y convenciones de cátedra C (snake_case, typedefs, guardas). | `src/data_structures.c`, `src/parser.c` |
| 3 | **KANEDA** | Auditoría estática de seguridad, funciones prohibidas (`gets`, `sprintf`, `scanf %s`) y syscalls. | `src/security_sample.c` |
| 4 | **SPUNKMEYER** | Detector de antipatrones didácticos C (`malloc` cast, `NULL` check antes de `free`, `== true`). | `src/security_sample.c` |
| 5 | **BRETT** | Auditoría de padding/alineación en structs de 64 bits y generación de layout optimizado. | `src/data_structures.h` |
| 6 | **SEBASTIAN** | Análisis de funciones recursivas, detección de caso base, árbol de llamadas y consumo de stack. | `src/data_structures.c` (`calcular_factorial`) |
| 7 | **RACHEL** | Desensamblado de sentencias `switch`, verificación de Jump Tables $O(1)$ vs comparaciones binarias/secuenciales. | `src/data_structures.c` (`procesar_comando`) |
| 8 | **BISHOP** | Visualizador de memoria Stack Frames, variables locales, bloques Heap y relaciones de punteros en runtime. | `src/main.c`, `src/data_structures.c` |
| 9 | **HAL** | Asistente forense de crash dumps (diagnóstico automático de `SIGSEGV`, `SIGFPE`, `SIGABRT` y variables culpables). | `src/crashes/crash_segv.c`, `src/crashes/crash_fpe.c` |
| 10 | **NOSTROMO** | Runner de casos de prueba (`.in`/`.out`) en Sandbox aislado (Bubblewrap / namespaces de Linux). | `testcases/01_basic.*`, `testcases/02_cmd3.*` |
| 11 | **HOLDEN** | Generador de mocks con wrapper de linker (`-Wl,--wrap=...`) e inyección de fallos (`malloc`, `fopen`, `rand`). | `src/mocks/holden_app.c`, `scripts/test_mock_holden.sh` |
| 12 | **CALLAHAN** | Extracción y verificación formal de contratos ACSL (`/*@ requires ... ensures ... */`) con Frama-C WP. | `src/data_structures.h`, `src/parser.h` |
| 13 | **DRAKE** | Fuzzer pedagógico guiado por límites (`INT_MAX`, `INT_MIN`, offsets extremos, mutaciones de buffer). | `src/fuzz_target.c` |
| 14 | **GIGER** | Generación de Call Graphs estáticos, detección de funciones huérfanas (dead code) y ciclos de llamadas. | `src/unused_sample.c` |
| 15 | **WEYL** | Diffing semántico y estructural de AST contra la solución canónica de referencia. | `src/data_structures.c` vs `canon/data_structures_canon.c` |
| 16 | **RIPLEY** | Orquestador del pipeline del cliente estudiante y diagnóstico del entorno de evaluación. | `ripley.yaml` |
| 17 | **ALUCARD** | Sintetizador de exámenes impresos, plantillas Typst y validación OMR. | CLI `alucard` |
| 18 | **IDKFA** | Generador procedural de preguntas Moodle XML y tracing con GCC. | CLI `idkfa` |
| 19 | **MOODLE-TOOLBOX** | Conversión bidireccional GIFT ↔ Moodle XML y validación de bancos de preguntas. | CLI `moodle-toolbox` |
| 20 | **MYST-TOOLS** | Formateo, corrección de anclas e indexado de apuntes MyST Markdown. | CLI `myst-tools` |
| 21 | **LIB_TEST** | Framework de testing pedagógico C: contadores de memoria sin fugas, mocks stdio, archivos temporales y reporte Markdown. | `src/test_lib_test.c`, `include/p1_test.h` |
| 22 | **KITCHEN SINK** | Robustez de Daedalus/Gaff/Ripley ante clases y situaciones de archivo límite (vacíos, BOM, CRLF, encoding no-UTF8, byte nulo, binario, trigrafos/dígrafos, anidamiento profundo, permisos, symlinks) — no busca corrección, busca que nada crashee ni cuelgue. | `kitchen_sink/`, `scripts/test_kitchen_sink.sh` |

---

## 📂 Estructura del Proyecto

```
student-smoke-test/
├── Makefile                     # Targets modulares por herramienta y suite global
├── smoke_test.sh                # Script orquestador del Smoke Test automatizado
├── ripley.yaml                  # Manifiesto de configuración de pipeline
├── src/
│   ├── main.c                   # Programa principal integrador
│   ├── data_structures.h        # Structs con padding para Brett y contratos ACSL
│   ├── data_structures.c        # Implementación con recursión (Sebastian), switch (Rachel), Heap (Bishop)
│   ├── parser.h                 # Declaraciones de parsing seguro
│   ├── parser.c                 # Parser robusto
│   ├── fuzz_target.c            # Target autocontenido para fuzzing con Drake
│   ├── security_sample.c        # Muestra con antipatrones (Spunkmeyer, Kaneda, Gaff)
│   ├── unused_sample.c          # Muestra con código muerto para Giger
│   ├── crashes/
│   │   ├── crash_segv.c         # Código explícito con desreferencia a NULL para Hal
│   │   └── crash_fpe.c          # Código explícito con división por cero para Hal
│   └── mocks/
│       └── holden_app.c         # Aplicación explícita consumidora de fopen para Holden
├── canon/
│   └── data_structures_canon.c  # Referencia canónica para Weyl
├── testcases/                   # Casos del programa principal (build/app)
│   ├── 01_basic.in / .out       # Caso de prueba básico
│   └── 02_cmd3.in / .out        # Caso de prueba de comando
├── testcases_fuzz/              # Casos de fuzz_target.c (Vassili exige que la suite
│   │                            # apruebe sobre el original antes de puntuar mutantes)
│   ├── 01_en_rango.in / .out    # Valor dentro del rango aceptado
│   ├── 02_fuera_de_rango.in / .out # Valor fuera de rango
│   └── 03_cero.in / .out        # Borde inferior
├── failing_cases/               # Batería de archivos con fallos deliberados para validación negativa
│   ├── fail_syntax_daedalus.c   # Errores sintácticos y de tipos para Daedalus
│   ├── fail_style_gaff.c        # Violaciones severas de estilo y formato para Gaff
│   ├── fail_security_kaneda.c   # Funciones prohibidas y vulnerabilidades para Kaneda y Ripley
│   ├── fail_antipatterns_spunkmeyer.c # Antipatrones C para Spunkmeyer
│   ├── fail_padding_brett.c     # Padding ineficiente de memoria para Brett
│   ├── fail_recursion_sebastian.c # Recursión descontrolada para Sebastian
│   ├── fail_deadcode_giger.c    # Funciones huérfanas y código muerto para Giger
│   ├── fail_fuzz_drake.c        # Vulnerabilidad de desbordamiento en INT_MAX para Drake
│   ├── fail_contracts_callahan.c # Contratos contradictorios para Callahan
│   └── fail_guide_overload.yaml # Sobrecarga de carga horaria semanal para Deckard
├── kitchen_sink/                # Clases y situaciones de archivo límite (sin heredocs; todos explícitos)
│   ├── ks_01_vacio.c             # Archivo de 0 bytes
│   ├── ks_02_solo_whitespace.c   # Solo espacios/tabs/saltos de línea
│   ├── ks_03_solo_comentario.c   # Ninguna declaración ni función real
│   ├── ks_04_comentario_bloque_sin_cerrar.c # /* sin cerrar (EOF dentro de comentario)
│   ├── ks_05_bom_utf8.c          # BOM UTF-8 al inicio del archivo
│   ├── ks_06_crlf.c              # Finales de línea CRLF
│   ├── ks_07_mixed_eol.c         # Finales de línea LF/CRLF mezclados
│   ├── ks_08_sin_newline_final.c # Sin \n final en EOF
│   ├── ks_09_linea_extremadamente_larga.c # Una sola línea de ~4000 caracteres
│   ├── ks_10_anidamiento_profundo.c # 300 niveles de `if` anidados
│   ├── ks_11_trigrafos.c         # Trigrafos ??( ??) ??< ??> ??= (C89/99, retirados en C23)
│   ├── ks_12_literales_metacaracteres.c # Comillas/barras/regex-especiales en literales
│   ├── ks_13_macro_multilinea.c  # #define con continuación de línea (backslash-newline)
│   ├── ks_14_estilo_kr.c         # Definición de función estilo K&R pre-ANSI
│   ├── ks_15_comentario_con_codigo_falso.c # Directivas/código falso dentro de comentarios
│   ├── ks_16_digrafos.c          # Dígrafos <: :> <% %> %:
│   ├── ks_17_latin1_no_utf8.c    # Codificado en Latin-1, inválido como UTF-8
│   ├── ks_18_identificador_extenso.c # Identificador de >500 caracteres
│   ├── ks_19_byte_nulo_embebido.c # Byte NUL literal embebido en el archivo
│   ├── ks_20_binario_con_extension_c.c # Bytes binarios aleatorios con extensión .c
│   ├── ks_21_dead_code_if_0.c    # #if 0 con sintaxis inválida adentro (código muerto)
│   ├── "ks_22 archivo con espacios y ñ.c" # El nombre de archivo es el caso límite
│   └── ks_23_extension_incorrecta.txt # Código C real con extensión .txt
└── scripts/
    ├── test_all_tools.sh        # Ejecución secuencial de todas las CLIs
    ├── test_callahan_verify.sh  # Tolera 'verify' sin Frama-C (prover opcional, ver doctor)
    ├── test_crash_hal.sh        # Diagnóstico forense con Hal sobre archivos explícitos
    ├── test_failing_cases.sh    # Batería exhaustiva de detección y rechazo de fallos
    ├── test_kitchen_sink.sh     # Robustez ante clases y situaciones de archivo límite
    ├── test_gaff_rules.sh       # Verificación exhaustiva de códigos de regla de Gaff
    └── test_mock_holden.sh      # Vinculación del mock con holden_app.c
```

---

## 🚀 Modos de Ejecución

### 1. Smoke Test Automatizado Completo

```bash
# Vía script Bash
./smoke_test.sh

# O vía Makefile
make smoke
```

### 2. Ejecución Individual de Cada Herramienta

```bash
make build               # Compila con Daedalus
make check-style         # Audita estilo con Gaff
make check-security      # Audita seguridad con Kaneda
make check-antipatterns  # Detecta antipatrones con Spunkmeyer
make audit-padding       # Audita y optimiza structs con Brett
make trace-recursion     # Traza árbol de llamadas con Sebastian
make disasm-switch       # Analiza Jump Tables O(1) con Rachel
make trace-memory        # Visualiza Stack y Heap con Bishop
make diag-crash          # Diagnostica crashes explícitos con Hal
make test-sandbox        # Evalúa en Sandbox con Nostromo
make mock-fault          # Inyecta fallos de fopen con Holden
make verify-acsl         # Extrae contratos ACSL con Callahan
make fuzz                # Ejecuta fuzzer con Drake
make callgraph           # Genera grafo de llamadas con Giger
make diff-canon          # Compara AST con Weyl
make test-libtest        # Ejecuta suite didáctica lib_test con reporte Markdown
make check-alucard       # Verifica CLI de AlucarD
make check-idkfa         # Verifica CLI de IDKFA
make check-moodle        # Verifica CLI de Moodle-toolbox
make check-myst          # Verifica CLI de MyST-tools
make doctor-all          # Diagnóstico de todas las herramientas
make kitchen-sink        # Robustez ante clases/situaciones de archivo límite (sin crashes/cuelgues)
```
