# Makefile para Smoke Test del Ecosistema de Herramientas del Estudiante
CC = gcc
CFLAGS = -Wall -Wextra -pedantic -std=c11 -g -O2
BUILD_DIR = build
SRC_DIR = src
CANON_DIR = canon

SOURCES = $(SRC_DIR)/main.c $(SRC_DIR)/data_structures.c $(SRC_DIR)/parser.c
TARGET = $(BUILD_DIR)/app

.PHONY: all build clean smoke help \
        check-style check-security check-antipatterns audit-padding \
        trace-recursion disasm-switch trace-memory diag-crash \
        test-sandbox mock-fault verify-acsl fuzz callgraph diff-canon \
        audit-abi lint-portability audit-headers audit-macros verify-tda \
        gen-datasets test-mutation gen-docs run-sanitizers inspect-bin profile-perf \
        explain-gcc inject-faults check-mcdc doctor-all kitchen-sink

all: build

build: $(TARGET)

$(TARGET): $(SOURCES)
	@mkdir -p $(BUILD_DIR)
	@echo "🛠️ Compilando aplicación con DAEDALUS..."
	daedalus compile $(SOURCES) -o $(TARGET)

clean:
	@rm -rf $(BUILD_DIR)
	@echo "🧹 Limpieza de binarios y temporales completada."

# ==============================================================================
# Targets de Demostración por Herramienta
# ==============================================================================

check-style:
	@echo "\n🔍 [GAFF] Verificando estilo y convenciones cátedra..."
	gaff check $(SRC_DIR)/data_structures.c $(SRC_DIR)/parser.c

check-security:
	@echo "\n🛡️ [KANEDA] Auditando seguridad y funciones prohibidas..."
	-kaneda audit $(SRC_DIR)/security_sample.c

check-antipatterns:
	@echo "\n⚠️ [SPUNKMEYER] Detectando antipatrones didácticos C..."
	-spunkmeyer detect $(SRC_DIR)/security_sample.c

audit-padding:
	@echo "\n📦 [BRETT] Auditando memoria y padding de structs..."
	brett audit $(SRC_DIR)/data_structures.h
	brett optimize $(SRC_DIR)/data_structures.h

trace-recursion:
	@echo "\n🌲 [SEBASTIAN] Analizando árbol de recursión y stack frames..."
	sebastian trace $(SRC_DIR)/main.c --function calcular_factorial
	sebastian analyze $(SRC_DIR)/data_structures.c

disasm-switch:
	@echo "\n🔬 [RACHEL] Desensamblando switch y verificando jump table O(1)..."
	rachel switch $(SRC_DIR)/data_structures.c
	rachel compare $(SRC_DIR)/data_structures.c

trace-memory:
	@echo "\n🥞 [BISHOP] Visualizando Stack, Heap y relaciones de punteros..."
	bishop trace $(SRC_DIR)/main.c
	bishop heap $(SRC_DIR)/main.c

diag-crash:
	@echo "\n🚨 [HAL] Ejecutando diagnóstico forense de crashes..."
	@bash scripts/test_crash_hal.sh

test-sandbox: build
	@echo "\n📦 [NOSTROMO] Evaluando casos de prueba en sandbox aislado..."
	nostromo test $(TARGET) testcases

mock-fault:
	@echo "\n🎭 [HOLDEN] Demostrando inyección de fallos vía mocks..."
	@bash scripts/test_mock_holden.sh

verify-acsl:
	@echo "\n📐 [CALLAHAN] Extrayendo y verificando contratos ACSL..."
	callahan extract $(SRC_DIR)/data_structures.h
	@bash scripts/test_callahan_verify.sh

fuzz:
	@echo "\n💥 [DRAKE] Ejecutando fuzzing guiado por límites..."
	drake fuzz $(SRC_DIR)/fuzz_target.c --runs 10

callgraph:
	@echo "\n🌐 [GIGER] Generando Call Graph y detectando dead code..."
	giger callgraph $(SRC_DIR)/unused_sample.c

diff-canon:
	@echo "\n⚖️ [WEYL] Comparando AST semántico contra solución canónica..."
	weyl diff $(SRC_DIR)/data_structures.c $(CANON_DIR)/data_structures_canon.c

audit-abi:
	@echo "\n📐 [PARKER] Auditando ABI y visibilidad de símbolos..."
	parker audit $(SRC_DIR)/data_structures.h

lint-portability:
	@echo "\n🌍 [CROWE] Verificando portabilidad multi-arquitectura..."
	crowe lint $(SRC_DIR)/data_structures.c

audit-headers:
	@echo "\n🌳 [WIERZBOWSKI] Auditando dependencias circulares y Makefiles..."
	wierzbowski audit .

audit-macros:
	@echo "\n🏷️ [ZHORA] Auditando seguridad en macros #define..."
	zhora audit $(SRC_DIR)/

verify-tda:
	@echo "\n🔒 [MOTOKO] Verificando encapsulamiento estricto de TDAs..."
	motoko verify $(SRC_DIR)/data_structures.h --client $(SRC_DIR)/main.c --impl $(SRC_DIR)/data_structures.c

gen-datasets:
	@echo "\n🎲 [TYRELL] Generando datasets sintéticos deterministas..."
	@mkdir -p $(BUILD_DIR)/tyrell_tests
	tyrell generate -n 5 -o $(BUILD_DIR)/tyrell_tests

test-mutation:
	@echo "\n🧬 [VASSILI] Evaluando efectividad de tests con Mutation Testing..."
	vassili mutate $(SRC_DIR)/fuzz_target.c --tests-dir testcases_fuzz --min-score 0

gen-docs:
	@echo "\n📚 [CORBEL] Scaffolding de comentarios y generación de documentación de APIs..."
	corbel scaffold $(SRC_DIR)/data_structures.h -o $(BUILD_DIR)/scaffolded.h
	corbel doc $(SRC_DIR)/data_structures.h -f markdown -o $(BUILD_DIR)/API.md

run-sanitizers: build
	@echo "\n🩺 [TETSUO] Verificando ejecución bajo sanitizers..."
	tetsuo run $(TARGET)

inspect-bin:
	@echo "\n💾 [KANE] Inspeccionando archivos binarios con struct mapping..."
	@python3 -c "import struct; open('$(BUILD_DIR)/sample.bin', 'wb').write(struct.pack('<if', 42, 9.5))"
	kane inspect $(BUILD_DIR)/sample.bin -s "int id, float nota"

profile-perf: build
	@echo "\n⚡ [FERRO] Perfilando rendimiento y hardware counters..."
	ferro profile $(TARGET) --inputs "100,500"

explain-gcc:
	@echo "\n🗣️ [ESPER] Explicando diagnósticos y advertencias de GCC..."
	esper explain "main.c:10: warning: unused variable 'x' [-Wunused-variable]"

inject-faults: build
	@echo "\n💉 [VASQUEZ] Inyectando fallos de memoria y disco vía LD_PRELOAD..."
	vasquez inject $(TARGET) --faults "malloc:1,fopen:1"

check-mcdc:
	@echo "\n📊 [DIETRICH] Validando cobertura lógica avanzada MC/DC..."
	dietrich analyze $(SRC_DIR)/parser.c

check-alucard:
	@echo "\n📄 [ALUCARD] Verificando sintetizador de exámenes Typst..."
	alucard --help > /dev/null

check-idkfa:
	@echo "\n🎮 [IDKFA] Verificando generador procedural Moodle XML..."
	idkfa --help > /dev/null

check-moodle:
	@echo "\n📦 [MOODLE-TOOLBOX] Verificando conversor y validador GIFT/XML..."
	moodle-toolbox --help > /dev/null

check-myst:
	@echo "\n📖 [MYST-TOOLS] Verificando gestor de apuntes MyST Markdown..."
	myst-tools --help > /dev/null

test-libtest:
	@echo "\n🧪 [LIB_TEST] Compilando y ejecutando suite pedagógica con Daedalus..."
	daedalus compile --flags "-Iinclude" $(SRC_DIR)/p1_test.c $(SRC_DIR)/test_lib_test.c -o $(BUILD_DIR)/test_lib_test
	$(BUILD_DIR)/test_lib_test --md-report $(BUILD_DIR)/lib_test_report.md

doctor-all:
	@echo "\n🩺 [DOCTOR] Verificando toolchain y dependencias..."
	daedalus doctor
	hal doctor
	nostromo doctor
	ripley doctor

kitchen-sink:
	@echo "\n🍳 [KITCHEN SINK] Verificando robustez ante clases y situaciones de archivo límite..."
	@bash scripts/test_kitchen_sink.sh

# ==============================================================================
# Suite Completa de Smoke Test
# ==============================================================================

smoke: build
	@bash smoke_test.sh

help:
	@echo "Makefile de demostración del ecosistema de herramientas de cátedra C"
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make build               - Compila el proyecto con Daedalus"
	@echo "  make smoke               - Ejecuta el smoke test completo automatizado (53 pasos)"
	@echo "  make test-libtest        - lib_test: ejecución de suite con aserciones de memoria y reporte Markdown"
	@echo "  make check-style         - Gaff: linter y convenciones de estilo"
	@echo "  make check-security      - Kaneda: auditoría de seguridad"
	@echo "  make check-antipatterns  - Spunkmeyer: antipatrones didácticos"
	@echo "  make audit-padding       - Brett: optimización y alineación de structs"
	@echo "  make trace-recursion     - Sebastian: árbol de recursión y stack"
	@echo "  make disasm-switch       - Rachel: análisis de switch y jump tables O(1)"
	@echo "  make trace-memory        - Bishop: visualización de Stack y Heap"
	@echo "  make diag-crash          - Hal: diagnóstico forense de crashes/segfaults"
	@echo "  make test-sandbox        - Nostromo: test runner en sandbox Bubblewrap"
	@echo "  make mock-fault          - Holden: generación de mocks e inyección de fallos"
	@echo "  make verify-acsl         - Callahan: contratos formales ACSL"
	@echo "  make fuzz                - Drake: fuzzer de límites"
	@echo "  make callgraph           - Giger: mapas de llamadas y código muerto"
	@echo "  make diff-canon          - Weyl: diffing semántico contra modelo"
	@echo "  make audit-abi           - Parker: auditoría de ABI y visibilidad"
	@echo "  make lint-portability    - Crowe: portabilidad multi-arquitectura"
	@echo "  make audit-headers       - Wierzbowski: dependencias y Makefiles"
	@echo "  make audit-macros        - Zhora: linter de macros #define"
	@echo "  make verify-tda          - Motoko: encapsulamiento de TDAs opacos"
	@echo "  make gen-datasets        - Tyrell: generador de testcases deterministas"
	@echo "  make test-mutation       - Vassili: motor de mutation testing"
	@echo "  make gen-docs            - Corbel: generador de documentación API"
	@echo "  make run-sanitizers      - Tetsuo: explicador pedagógico de sanitizers"
	@echo "  make inspect-bin         - Kane: depuración visual de archivos binarios"
	@echo "  make profile-perf        - Ferro: perfilador de rendimiento y ciclos"
	@echo "  make check-alucard       - AlucarD: sintetizador de exámenes Typst"
	@echo "  make check-idkfa         - IDKFA: generador de preguntas Moodle XML"
	@echo "  make check-moodle        - Moodle-toolbox: herramientas de preguntas GIFT/XML"
	@echo "  make check-myst          - MyST-tools: gestor de apuntes y guías MyST"
	@echo "  make doctor-all          - Diagnóstico de todas las herramientas"
	@echo "  make kitchen-sink        - Robustez ante clases/situaciones de archivo límite (sin crashes/cuelgues)"
	@echo "  make clean               - Limpia binarios generados"
