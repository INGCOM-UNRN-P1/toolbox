#!/usr/bin/env bash
# Smoke test estudiantil del ecosistema P1, con oráculos.
#
# Cada paso declara qué código de salida acepta y qué textos debe (o no debe)
# contener su salida. Antes el script solo corría los comandos bajo `set -e`:
# un paso que encontraba hallazgos legítimos (exit 1) abortaba todo, y si
# todos terminaban bien imprimía «todas las herramientas funcionan» sin mirar
# lo que decían. Ahora cada verificación fallida se informa y se cuenta, y el
# script sale con 1 si hubo alguna.
#
# Los pasos que necesitan una herramienta del sistema ausente (gdb, frama-c,
# valgrind, libasan) se informan como OMITIDOS en lugar de fallar.
set -uo pipefail
export NO_COLOR=1 TERM=dumb COLUMNS=200

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
mkdir -p build

FALLOS=0
VERIFICACIONES=0
OMITIDOS=0
SALIDA=""
RC=0

titulo() {
    echo ""
    echo "▶ $*"
}

fallo() {
    echo "✗ FALLO: $*"
    FALLOS=$((FALLOS + 1))
}

# ejecutar <códigos aceptados, separados por coma> <comando…>
ejecutar() {
    local aceptados="$1"
    shift
    VERIFICACIONES=$((VERIFICACIONES + 1))
    SALIDA="$("$@" 2>&1)"
    RC=$?
    printf '%s\n' "$SALIDA"
    if [[ ",$aceptados," != *",$RC,"* ]]; then
        fallo "«$*» salió con $RC (se esperaba $aceptados)"
    fi
}

debe_contener() {
    local texto
    for texto in "$@"; do
        VERIFICACIONES=$((VERIFICACIONES + 1))
        grep -qF -- "$texto" <<<"$SALIDA" || fallo "la salida no contiene «$texto»"
    done
}

no_debe_contener() {
    local texto
    for texto in "$@"; do
        VERIFICACIONES=$((VERIFICACIONES + 1))
        if grep -qF -- "$texto" <<<"$SALIDA"; then
            fallo "la salida contiene «$texto» y no debería"
        fi
    done
}

debe_existir() {
    local ruta
    for ruta in "$@"; do
        VERIFICACIONES=$((VERIFICACIONES + 1))
        [ -s "$ruta" ] || fallo "no se generó $ruta"
    done
}

# requiere <binario…>: si falta alguno, informa el paso como omitido y devuelve 1
requiere() {
    local binario
    for binario in "$@"; do
        if ! command -v "$binario" >/dev/null 2>&1; then
            echo "○ OMITIDO: falta «$binario» en el PATH"
            OMITIDOS=$((OMITIDOS + 1))
            return 1
        fi
    done
}

requiere_asan() {
    if ! printf 'int main(void) { return 0; }\n' | gcc -x c -fsanitize=address,undefined -o /dev/null - >/dev/null 2>&1; then
        echo "○ OMITIDO: gcc no puede enlazar ASan/UBSan (falta libasan o libubsan)"
        OMITIDOS=$((OMITIDOS + 1))
        return 1
    fi
}

echo "================================================================================"
echo "🚀 SMOKE TEST DE TODAS LAS HERRAMIENTAS DEL ECOSISTEMA P1"
echo "================================================================================"

titulo "1. [DAEDALUS] Compilación pedagógica y traducción de errores"
ejecutar 0 daedalus compile src/main.c src/data_structures.c src/parser.c -o build/app
debe_contener "Compilación Exitosa"
debe_existir build/app

titulo "2. [GAFF] Convenciones y estilo de cátedra (el ejemplo tiene incumplimientos a propósito)"
ejecutar 1 gaff check src/data_structures.c src/parser.c
debe_contener "0x200Ch"
# Falsos positivos corregidos (N-GAFF-01, N-GAFF-05): no deben volver.
no_debe_contener "0x000Eh" "0x000Fh" "0x2011h"

titulo "3. [KANEDA] Auditoría estática de seguridad (se espera detectar gets)"
ejecutar 1 kaneda audit src/security_sample.c
debe_contener "KAN001" "gets()"

titulo "4. [SPUNKMEYER] Antipatrones didácticos (se esperan hallazgos)"
ejecutar 1 spunkmeyer detect src/security_sample.c
debe_contener "0x3002h"

titulo "5. [BRETT] Padding de structs (exit 1 = hay padding desperdiciado)"
ejecutar 1 brett audit src/data_structures.h
debe_contener "t_alumno_desordenado"
ejecutar 0 brett optimize src/data_structures.h
debe_contener "Layout Sugerido"

titulo "6. [SEBASTIAN] Recursión, call tree y stack frames"
ejecutar 0 sebastian trace src/main.c --function calcular_factorial
debe_contener "calcular_factorial"
ejecutar 0 sebastian analyze src/data_structures.c
debe_contener "Recursivas detectadas: 1"

titulo "7. [RACHEL] Desensamblado de switch y comparación con if-else"
ejecutar 0 rachel switch src/data_structures.c
debe_contener "procesar_comando"
ejecutar 0 rachel compare src/data_structures.c
debe_contener "O(1)"

titulo "8. [BISHOP] Memoria en ejecución (Stack, Heap y punteros)"
if requiere gdb; then
    ejecutar 0 bishop trace src/main.c
    debe_contener "main()"
    ejecutar 0 bishop heap src/main.c
fi

titulo "9. [HAL] Diagnóstico forense de señales fatales (SIGSEGV / SIGFPE)"
if requiere gdb; then
    ejecutar 0 bash scripts/test_crash_hal.sh
    debe_contener "HAL diagnosticó correctamente"
fi

titulo "10. [NOSTROMO] Casos de prueba en sandbox"
ejecutar 0 nostromo test build/app testcases
debe_contener "Aprobados: 2/2"

titulo "11. [HOLDEN] Mocks e inyección de fallos"
ejecutar 0 bash scripts/test_mock_holden.sh
debe_contener "Inyección de fallo de fopen exitosa"

titulo "12. [CALLAHAN] Contratos formales ACSL"
ejecutar 0 callahan extract src/data_structures.h
debe_contener "requires: n >= 0"
if requiere frama-c; then
    ejecutar 0 bash scripts/test_callahan_verify.sh
    debe_contener "verificados deductivamente"
fi

titulo "13. [DRAKE] Fuzzing guiado por límites"
ejecutar 0 drake fuzz src/fuzz_target.c --runs 10
debe_contener "Fuzzing completado"

titulo "14. [GIGER] Grafo de llamadas y código muerto"
ejecutar 0 giger callgraph src/unused_sample.c
debe_contener "funcion_huerfana_dos"

titulo "15. [WEYL] Diff semántico contra el modelo canónico"
ejecutar 0 weyl diff src/data_structures.c canon/data_structures_canon.c
debe_contener "IDENTICA"

titulo "16. [PARKER] ABI y visibilidad de símbolos"
ejecutar 0 parker audit src/data_structures.h
debe_contener "ABI Válida"

titulo "17. [CROWE] Portabilidad multi-arquitectura"
ejecutar 0 crowe lint src/data_structures.c
debe_contener "Portable"

titulo "18. [WIERZBOWSKI] Grafo de inclusión y Makefiles"
ejecutar 0 wierzbowski audit src/
debe_contener "data_structures.h"

titulo "19. [ZHORA] Macros del preprocesador"
ejecutar 0 zhora audit src/
debe_contener "Macros 100% Seguras"

titulo "20. [MOTOKO] Encapsulamiento de TDAs (el ejemplo expone campos a propósito)"
ejecutar 0 motoko verify src/data_structures.h --client src/main.c --impl src/data_structures.c
debe_contener "MOT001"

titulo "21. [TYRELL] Datasets sintéticos"
ejecutar 0 tyrell generate -n 3 -o build/tyrell_tests
debe_contener "3 testcases guardados"

titulo "22. [VASSILI] Mutation testing"
ejecutar 0 vassili mutate src/fuzz_target.c --tests-dir testcases_fuzz --min-score 0
debe_contener "Mutation Score"

titulo "23. [CORBEL] Scaffolding Doxygen y documentación de la API"
ejecutar 0 corbel scaffold src/data_structures.h -o build/scaffolded.h
debe_existir build/scaffolded.h
ejecutar 0 corbel doc src/data_structures.h -f markdown -o build/API.md
debe_existir build/API.md

titulo "24. [TETSUO] Sanitizers"
# Un binario compilado sin sanitizers no puede declararse limpio (N-TETSUO-01).
ejecutar 1 tetsuo run build/app
debe_contener "no está instrumentado"
if requiere_asan; then
    ejecutar 0 daedalus compile src/main.c src/data_structures.c src/parser.c --flags "-fsanitize=address,undefined" -o build/app_asan
    ejecutar 0 tetsuo run build/app_asan
    debe_contener "Ejecución Limpia"
fi

titulo "25. [KANE] Archivos binarios"
python3 -c "import struct; open('build/sample.bin', 'wb').write(struct.pack('<if', 42, 9.5))"
ejecutar 0 kane inspect build/sample.bin -s 'int id, float nota'
debe_contener "9.5"

titulo "26. [FERRO] Perfilado de rendimiento"
ejecutar 0 ferro profile build/app --inputs '100,500'
debe_contener "Complejidad Empírica"

titulo "27. [ESPER] Explicación de advertencias de GCC"
ejecutar 0 esper explain "main.c:10: warning: unused variable 'x' [-Wunused-variable]"
debe_contener "¿Qué significa?"

titulo "28. [VASQUEZ] Inyección de fallos (LD_PRELOAD)"
ejecutar 0 vasquez inject build/app --faults "malloc:1,fopen:1"
debe_contener "Robustness Passed"

titulo "29. [DIETRICH] Cobertura MC/DC"
ejecutar 0 dietrich analyze src/parser.c
debe_contener "Cobertura MC/DC"

titulo "30. [RIPLEY] Diagnóstico de entorno y reglas pedagógicas"
ejecutar 0 ripley doctor
# Descripciones del catálogo único (N-RIPLEY-01): la vieja copia describía mal a tetsuo y vassili.
debe_contener "sanitizers"
no_debe_contener "Benchmarking pedagógico" "Análisis de mutación y calidad pedagógica"
ejecutar 0 ripley explain 0x1001h
debe_contener "0x1001h"

titulo "31. [DECKARD] Banco de ejercicios"
ejecutar 0 deckard doctor
ejecutar 0 deckard stats --help

titulo "32. [DREDD] Corrección masiva"
ejecutar 0 dredd doctor

titulo "33. [MEET-TOOLS] CLI de Google Meet"
ejecutar 0 meet-tools --help
debe_contener "meet-tools [OPTIONS]"  # igual en la ayuda en inglés y en español (yutani)

titulo "34. [SLIDE-TOOLS] CLI de Google Slides"
ejecutar 0 slide-tools --help
debe_contener "slide-tools [OPTIONS]"

titulo "35. [KEYMAKER] Cifrado y time-lock"
ejecutar 0 keymaker doctor

titulo "36. [SCORM-TOOLS] Paquetes SCORM"
ejecutar 0 scorm-tools doctor

titulo "37. [ALUCARD] Exámenes impresos"
ejecutar 0 alucard --help

titulo "38. [IDKFA] Cuestionarios Moodle XML"
ejecutar 0 idkfa --help
ejecutar 0 idkfa --version
debe_contener "idkfa "

titulo "39. [MOODLE-TOOLBOX] Bancos de preguntas"
ejecutar 0 moodle-toolbox --help

titulo "40. [MYST-TOOLS] Apuntes MyST"
ejecutar 0 myst-tools --help

titulo "41. [LIB_TEST] Biblioteca de pruebas p1_test"
ejecutar 0 daedalus compile --flags "-Iinclude" src/p1_test.c src/test_lib_test.c -o build/test_lib_test
ejecutar 0 build/test_lib_test --md-report build/lib_test_report.md
debe_contener "PASÓ"
debe_existir build/lib_test_report.md

echo ""
echo "================================================================================"
echo "Verificaciones: $VERIFICACIONES · Fallos: $FALLOS · Pasos omitidos: $OMITIDOS"
if [ "$FALLOS" -gt 0 ]; then
    echo "✗ SMOKE TEST CON FALLOS"
    echo "================================================================================"
    exit 1
fi
if [ "$OMITIDOS" -gt 0 ]; then
    echo "✓ Sin fallos (con pasos omitidos por herramientas del sistema ausentes)"
else
    echo "🎉 SMOKE TEST COMPLETO: todas las verificaciones pasaron"
fi
echo "================================================================================"
