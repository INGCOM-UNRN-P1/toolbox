#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

TOTAL_PASSED=0
TOTAL_FAILED=0

run_step() {
    local num="$1"
    local name="$2"
    local tool="$3"
    local cmd="$4"

    echo -e "\n${BLUE}================================================================================${NC}"
    echo -e "${CYAN}▶ Paso $num [${tool^^}]: ${name}${NC}"
    echo -e "${BLUE}Comando: ${YELLOW}$cmd${NC}"
    echo -e "${BLUE}--------------------------------------------------------------------------------${NC}"

    if eval "$cmd"; then
        echo -e "${GREEN}✓ Paso $num [$tool] OK${NC}"
        TOTAL_PASSED=$((TOTAL_PASSED + 1))
    else
        echo -e "${RED}✗ Paso $num [$tool] FALLÓ${NC}"
        TOTAL_FAILED=$((TOTAL_FAILED + 1))
    fi
}

mkdir -p build

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║          SMOKE TEST INTEGRAL DEL ECOSISTEMA DE HERRAMIENTAS EN C             ║"
echo "║                    LADO DEL ESTUDIANTE (CLIENTE CLI)                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 1. DAEDALUS
run_step 1 "Compilación pedagógica y traducción de advertencias" "daedalus" \
    "daedalus compile src/main.c src/data_structures.c src/parser.c -o build/app"

# 2. GAFF
run_step 2 "Linting estático, catálogo y verificación exhaustiva de reglas cátedra (0xXXXXh)" "gaff" \
    "gaff check src/data_structures.c src/parser.c && bash scripts/test_gaff_rules.sh"

# 3. KANEDA
run_step 3 "Auditoría de seguridad y funciones prohibidas" "kaneda" \
    "! kaneda audit src/security_sample.c"

# 4. SPUNKMEYER
run_step 4 "Detección de antipatrones didácticos C" "spunkmeyer" \
    "! spunkmeyer detect src/security_sample.c"

# 5. BRETT
run_step 5 "Auditoría de padding y optimización de structs" "brett" \
    "brett audit src/data_structures.h && brett optimize src/data_structures.h"

# 6. SEBASTIAN
run_step 6 "Trazado dinámico y análisis de recursión" "sebastian" \
    "sebastian trace src/main.c --function calcular_factorial && sebastian analyze src/data_structures.c"

# 7. RACHEL
run_step 7 "Desensamblado de switch y comparación Jump Table O(1)" "rachel" \
    "rachel switch src/data_structures.c && rachel compare src/data_structures.c"

# 8. BISHOP
run_step 8 "Visualización de Stack, Heap y punteros en memoria" "bishop" \
    "bishop trace src/main.c && bishop heap src/main.c"

# 9. HAL
run_step 9 "Diagnóstico forense de señales fatales (SIGSEGV/SIGFPE)" "hal" \
    "bash scripts/test_crash_hal.sh"

# 10. NOSTROMO
run_step 10 "Evaluación en Sandbox Bubblewrap con casos .in/.out" "nostromo" \
    "nostromo test build/app testcases"

# 11. HOLDEN
run_step 11 "Generación de mock de malloc e inyección de fallos" "holden" \
    "bash scripts/test_mock_holden.sh"

# 12. CALLAHAN
run_step 12 "Extracción y verificación de contratos ACSL" "callahan" \
    "callahan extract src/data_structures.h && callahan verify src/data_structures.h"

# 13. DRAKE
run_step 13 "Fuzzing guiado por límites y valores extremos" "drake" \
    "drake fuzz src/fuzz_target.c --runs 10"

# 14. GIGER
run_step 14 "Callgraph estático y detección de código muerto" "giger" \
    "giger callgraph src/unused_sample.c"

# 15. WEYL
run_step 15 "Diffing semántico de AST contra solución canónica" "weyl" \
    "weyl diff src/data_structures.c canon/data_structures_canon.c"

# 16. PARKER
run_step 16 "Auditoría de ABI y visibilidad de símbolos" "parker" \
    "parker audit src/data_structures.h"

# 17. CROWE
run_step 17 "Linter de portabilidad multi-arquitectura y endianness" "crowe" \
    "crowe lint src/data_structures.c"

# 18. WIERZBOWSKI
run_step 18 "Auditoría de dependencias circulares y Makefiles" "wierzbowski" \
    "wierzbowski audit src/"

# 19. ZHORA
run_step 19 "Linter de seguridad en macros del preprocesador" "zhora" \
    "zhora audit src/"

# 20. MOTOKO
run_step 20 "Verificación de encapsulamiento estricto de TDAs" "motoko" \
    "motoko verify src/data_structures.h --client src/main.c --impl src/data_structures.c"

# 21. TYRELL
run_step 21 "Generación sintética y determinista de datasets de prueba" "tyrell" \
    "tyrell generate -n 3 -o build/tyrell_tests"

# 22. VASSILI
run_step 22 "Mutation testing sobre código C y evaluación de tests" "vassili" \
    "vassili mutate src/fuzz_target.c --tests-dir testcases --min-score 0"

# 23. CORBEL
run_step 23 "Scaffolding de placeholders Doxygen y generación de documentación de APIs" "corbel" \
    "corbel scaffold src/data_structures.h -o build/scaffolded.h && corbel doc src/data_structures.h -f markdown -o build/API.md"

# 24. TETSUO
run_step 24 "Traducción y diagnóstico de sanitizers (ASan/UBSan)" "tetsuo" \
    "tetsuo run build/app"

# 25. KANE
run_step 25 "Depuración visual de archivos binarios y mapeo a structs" "kane" \
    "python3 -c \"import struct; open('build/sample.bin', 'wb').write(struct.pack('<if', 42, 9.5))\" && kane inspect build/sample.bin -s 'int id, float nota'"

# 26. FERRO
run_step 26 "Perfilado de rendimiento algorítmico y ciclos CPU" "ferro" \
    "ferro profile build/app --inputs '100,500'"

# 27. ESPER
run_step 27 "Explicación didáctica y traducción de advertencias GCC" "esper" \
    "esper explain \"main.c:10: warning: unused variable 'x' [-Wunused-variable]\""

# 28. VASQUEZ
run_step 28 "Inyección de fallos en tiempo de ejecución (LD_PRELOAD)" "vasquez" \
    "vasquez inject build/app --faults 'malloc:1,fopen:1'"

# 29. DIETRICH
run_step 29 "Validador de cobertura lógica avanzada MC/DC" "dietrich" \
    "dietrich analyze src/parser.c"

# 30. RIPLEY
run_step 30 "Diagnóstico global del entorno Ripley y explicación de reglas pedagógicas" "ripley" \
    "ripley doctor && ripley explain 0x1001h"

# 31. DECKARD
run_step 31 "Gestión de banco, estadísticas Bloom, doctor y browser en Deckard" "deckard" \
    "deckard doctor && deckard stats --help && deckard browse --help && deckard export-classroom --help"

# 32. DREDD
run_step 32 "Orquestación de correcciones, doctor y caché en Dredd" "dredd" \
    "dredd doctor && dredd init --help && dredd rerun --help && dredd eval --help"

# 33. RIPLEY QoL (SARIF y Badges SVG)
run_step 33 "Exportación SARIF y generación de Badges SVG pedagógicos en Ripley" "ripley" \
    "ripley check --format=sarif src/parser.c > /dev/null && ripley badge src/parser.c -o /tmp/smoke_badge.svg"

# 34. DAEDALUS QoL (Doctor, Preprocess y Explain-Opt)
run_step 34 "Diagnóstico de toolchain y explicador de optimizaciones en Daedalus" "daedalus" \
    "daedalus doctor && daedalus explain-opt O2 > /dev/null && daedalus preprocess src/main.c -o /tmp/smoke_main.i"

# 35. GAFF QoL (Doctor y Exportación de Guía de Estilo)
run_step 35 "Diagnóstico del entorno y exportación de manual de estilo Markdown en Gaff" "gaff" \
    "gaff doctor && gaff export-rules -o /tmp/smoke_rules.md"

# 36. HAL QoL (Doctor y Generación de Reproductor Autónomo)
run_step 36 "Diagnóstico forense y generación de script reproductor autónomo en HAL" "hal" \
    "hal doctor && hal generate-reproducer src/main.c -o /tmp/smoke_reproducer.sh"

# 37. SPUNKMEYER QoL (Doctor y Catálogo de Antipatrones)
run_step 37 "Diagnóstico de parser Tree-Sitter y catálogo de vicios en Spunkmeyer" "spunkmeyer" \
    "spunkmeyer doctor && spunkmeyer catalog > /dev/null"

# 38. WEYL QoL (Doctor, Diff Side-by-Side y Seguimiento Evolutivo)
run_step 38 "Diagnóstico de diffing semántico y visualización lado a lado en Weyl" "weyl" \
    "weyl doctor && weyl diff src/parser.c src/parser.c --side-by-side > /dev/null"

# 39. DECKARD QoL Extendido (Notebooks, Carga Horaria, Variantes y Auditoría)
run_step 39 "Exportación de Jupyter Notebooks C, calibración de carga y variantes en Deckard" "deckard" \
    "deckard export-notebook --help > /dev/null && deckard check-load --help > /dev/null && deckard variant --help > /dev/null && deckard audit-guide --help > /dev/null"

# 40. RIPLEY QoL Extendido (LSP, Watcher, Autofix y Conformidad de Estilo)
run_step 40 "Servidor LSP, auto-corrección interactiva, histórico y conformidad de estilo en Ripley" "ripley" \
    "ripley lsp --help > /dev/null && ripley style-check src/main.c && ripley history . > /dev/null"

# 41. DREDD QoL Extendido (SIU Guaraní, Dashboard, Auditoría Git y Plagio Histórico)
run_step 41 "Exportación a SIU Guaraní, Dashboard web, auditoría Git y plagio histórico en Dredd" "dredd" \
    "dredd export-guarani --help > /dev/null && dredd dashboard --help > /dev/null && dredd audit-git . > /dev/null"

# 42. BATERÍA EXHAUSTIVA DE FALLOS DELIBERADOS
run_step 42 "Detección y rechazo de archivos con fallos, vulnerabilidades y antipatrones deliberados" "ecosistema" \
    "bash scripts/test_failing_cases.sh"

echo -e "\n${BLUE}================================================================================${NC}"
echo -e "${CYAN}📊 RESUMEN FINAL DEL SMOKE TEST:${NC}"
echo -e "   • Pasos Exitosos: ${GREEN}${TOTAL_PASSED}${NC}"
echo -e "   • Pasos Fallidos: ${RED}${TOTAL_FAILED}${NC}"
echo -e "${BLUE}================================================================================${NC}"

if [ "$TOTAL_FAILED" -eq 0 ]; then
    echo -e "${GREEN}🎉 TODAS LAS HERRAMIENTAS SUPERARON EL SMOKE TEST EXITOSAMENTE (${TOTAL_PASSED}/${TOTAL_PASSED}).${NC}\n"
    exit 0
else
    echo -e "${RED}❌ ALGUNOS PASOS DEL SMOKE TEST FALLARON.${NC}\n"
    exit 1
fi

