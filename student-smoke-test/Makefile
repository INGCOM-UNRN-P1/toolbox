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
        test-sandbox mock-fault verify-acsl fuzz callgraph diff-canon doctor-all

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
	callahan verify $(SRC_DIR)/data_structures.h

fuzz:
	@echo "\n💥 [DRAKE] Ejecutando fuzzing guiado por límites..."
	drake fuzz $(SRC_DIR)/fuzz_target.c --runs 10

callgraph:
	@echo "\n🌐 [GIGER] Generando Call Graph y detectando dead code..."
	giger callgraph $(SRC_DIR)/unused_sample.c

diff-canon:
	@echo "\n⚖️ [WEYL] Comparando AST semántico contra solución canónica..."
	weyl diff $(SRC_DIR)/data_structures.c $(CANON_DIR)/data_structures_canon.c

doctor-all:
	@echo "\n🩺 [DOCTOR] Verificando toolchain y dependencias..."
	daedalus doctor
	hal doctor
	nostromo doctor
	ripley doctor

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
	@echo "  make smoke               - Ejecuta el smoke test completo automatizado"
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
	@echo "  make doctor-all          - Diagnóstico de todas las herramientas"
	@echo "  make clean               - Limpia binarios generados"
