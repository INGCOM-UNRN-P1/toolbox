#!/usr/bin/env bash
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

FAILED=0
PASSED=0

assert_failure() {
    local test_name="$1"
    local cmd="$2"

    echo -e "\n${BLUE}--- [TEST DE FALLO INTENCIONAL] ${test_name} ---${NC}"
    echo -e "Comando: ${YELLOW}$cmd${NC}"
    if eval "$cmd"; then
        echo -e "${GREEN}✓ Correcto: El fallo deliberado fue detectado y rechazado.${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ Error: La herramienta NO detectó el fallo esperado.${NC}"
        FAILED=$((FAILED + 1))
    fi
}

echo -e "${CYAN}================================================================================${NC}"
echo -e "${CYAN}🧪 BATERÍA EXHAUSTIVA DE TESTS CON CASOS DE FALLO DELIBERADO${NC}"
echo -e "${CYAN}================================================================================${NC}"

# 1. Daedalus: Error de sintaxis y tipos
assert_failure "Daedalus rechaza código con errores de sintaxis y tipos incompatibles" \
    "! daedalus compile failing_cases/fail_syntax_daedalus.c -o /tmp/bad_app 2>/dev/null"

# 2. Gaff: Violaciones severas de estilo (Magic numbers, camelCase, longitud de línea)
assert_failure "Gaff detecta y rechaza violaciones severas de estilo de cátedra" \
    "! gaff check failing_cases/fail_style_gaff.c > /dev/null"

# 3. Kaneda: Funciones prohibidas y vulnerabilidades críticas
assert_failure "Kaneda detecta funciones inseguras (gets, strcpy, sprintf, system, format strings)" \
    "! kaneda audit failing_cases/fail_security_kaneda.c > /dev/null"

# 4. Spunkmeyer: Antipatrones didácticos (while !feof, casts en malloc, fflush stdin, sizeof ptr)
assert_failure "Spunkmeyer detecta y rechaza catálogo de antipatrones didácticos de C" \
    "! spunkmeyer detect failing_cases/fail_antipatterns_spunkmeyer.c > /dev/null"

# 5. HAL: Intercepción forense de Segfault (SIGSEGV)
assert_failure "HAL intercepta y diagnostica caída por SIGSEGV (Desreferencia NULL)" \
    "! hal run src/crashes/crash_segv.c > /dev/null 2>&1"

# 6. HAL: Intercepción forense de División por Cero (SIGFPE)
assert_failure "HAL intercepta y diagnostica caída por SIGFPE (División por cero)" \
    "! hal run src/crashes/crash_fpe.c > /dev/null 2>&1"

# 7. Brett: Auditoría de structs con padding excesivo
assert_failure "Brett detecta desperdicio de memoria y calcula padding ahorrable" \
    "! brett audit failing_cases/fail_padding_brett.c > /dev/null"

# 8. Giger: Detección de código muerto y funciones huérfanas
assert_failure "Giger detecta funciones huérfanas no invocadas (dead code)" \
    "giger check failing_cases/fail_deadcode_giger.c | grep 'funcion_nunca_invocada_b' > /dev/null"

# 9. Deckard: Rechazo de guías con sobrecarga excesiva de horas pedagógicas
assert_failure "Deckard rechaza guías que exceden el límite de carga horaria semanal" \
    "! deckard check-load failing_cases/fail_guide_overload.yaml --max-horas 4.0 > /dev/null 2>&1"

# 10. Callahan: Extracción de contratos ACSL contradictorios
assert_failure "Callahan extrae y analiza contratos ACSL con cláusulas de pre/post condición" \
    "callahan extract failing_cases/fail_contracts_callahan.c | grep 'requires: x > 0' > /dev/null"

# 11. Ripley: Verificación estricta con penalización de calificación ante código inseguro
assert_failure "Ripley check penaliza código con antipatrones y fallos de seguridad" \
    "! ripley check failing_cases/fail_security_kaneda.c --strict > /dev/null 2>&1"

echo -e "\n${CYAN}================================================================================${NC}"
echo -e "${CYAN}📊 RESUMEN DE TESTS DE FALLOS DELIBERADOS:${NC}"
echo -e "   • Pasos Exitosos: ${GREEN}${PASSED}${NC}"
echo -e "   • Pasos Fallidos: ${RED}${FAILED}${NC}"
echo -e "${CYAN}================================================================================${NC}"

if [ "$FAILED" -eq 0 ]; then
    echo -e "${GREEN}🎉 TODOS LOS CASOS DE FALLO DELIBERADO FUERON DETECTADOS EXITOSAMENTE (${PASSED}/${PASSED}).${NC}\n"
    exit 0
else
    echo -e "${RED}❌ ALGUNOS TESTS DE FALLO NO FUERON DETECTADOS CORRECTAMENTE.${NC}\n"
    exit 1
fi
