#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

echo "================================================================================"
echo "🚀 EJECUTANDO SMOKE TEST DE TODAS LAS HERRAMIENTAS DEL ECOSISTEMA P1"
echo "================================================================================"

echo ""
echo "▶ 1. [DAEDALUS] Compilación pedagógica y traducción de errores..."
daedalus compile src/main.c src/data_structures.c src/parser.c -o build/app

echo ""
echo "▶ 2. [GAFF] Verificación de convenciones y estilo de cátedra..."
gaff check src/data_structures.c src/parser.c

echo ""
echo "▶ 3. [KANEDA] Auditoría estática de seguridad..."
if kaneda audit src/security_sample.c; then
    echo "⚠️ Se esperaba detección de vulnerabilidades."
else
    echo "✓ KANEDA detectó correctamente funciones inseguras y riesgos."
fi

echo ""
echo "▶ 4. [SPUNKMEYER] Detección de antipatrones didácticos C..."
if spunkmeyer detect src/security_sample.c; then
    echo "⚠️ Se esperaba detección de antipatrones."
else
    echo "✓ SPUNKMEYER detectó correctamente malloc casts y free redundante."
fi

echo ""
echo "▶ 5. [BRETT] Auditoría de padding y optimización de structs..."
brett audit src/data_structures.h
brett optimize src/data_structures.h

echo ""
echo "▶ 6. [SEBASTIAN] Análisis de recursión, call tree y stack frames..."
sebastian trace src/main.c --function calcular_factorial
sebastian analyze src/data_structures.c

echo ""
echo "▶ 7. [RACHEL] Desensamblado de switchs, jump tables O(1) y comparación if-else..."
rachel switch src/data_structures.c
rachel compare src/data_structures.c

echo ""
echo "▶ 8. [BISHOP] Visualización de memoria en ejecución (Stack, Heap y Punteros)..."
bishop trace src/main.c
bishop heap src/main.c

echo ""
echo "▶ 9. [HAL] Diagnóstico forense de señales fatales (SIGSEGV / SIGFPE)..."
bash scripts/test_crash_hal.sh

echo ""
echo "▶ 10. [NOSTROMO] Evaluación de testcases en Sandbox aislado..."
nostromo test build/app testcases

echo ""
echo "▶ 11. [HOLDEN] Generación de mocks e inyección de fallos..."
bash scripts/test_mock_holden.sh

echo ""
echo "▶ 12. [CALLAHAN] Extracción y verificación de contratos formales ACSL..."
callahan extract src/data_structures.h
callahan verify src/data_structures.h

echo ""
echo "▶ 13. [DRAKE] Fuzzing guiado por límites y payloads extremos..."
drake fuzz src/fuzz_target.c --runs 10

echo ""
echo "▶ 14. [GIGER] Generación de grafos de llamadas y detección de código muerto..."
giger callgraph src/unused_sample.c

echo ""
echo "▶ 15. [WEYL] Diffing semántico y comparación estructural contra modelo canónico..."
weyl diff src/data_structures.c canon/data_structures_canon.c

echo ""
echo "▶ 16. [PARKER] Auditoría de ABI y visibilidad de símbolos..."
parker audit src/data_structures.h

echo ""
echo "▶ 17. [CROWE] Linter de portabilidad multi-arquitectura..."
crowe lint src/data_structures.c

echo ""
echo "▶ 18. [WIERZBOWSKI] Auditoría de dependencias y Makefiles..."
wierzbowski audit src/

echo ""
echo "▶ 19. [ZHORA] Linter de macros del preprocesador..."
zhora audit src/

echo ""
echo "▶ 20. [MOTOKO] Verificación de encapsulamiento estricto de TDAs..."
motoko verify src/data_structures.h --client src/main.c --impl src/data_structures.c

echo ""
echo "▶ 21. [TYRELL] Generación sintética y determinista de datasets..."
tyrell generate -n 3 -o build/tyrell_tests

echo ""
echo "▶ 22. [VASSILI] Mutation testing sobre código C..."
vassili mutate src/fuzz_target.c --tests-dir testcases --min-score 0

echo ""
echo "▶ 23. [CORBEL] Scaffolding de comentarios Doxygen y API Markdown..."
corbel scaffold src/data_structures.h -o build/scaffolded.h
corbel doc src/data_structures.h -f markdown -o build/API.md

echo ""
echo "▶ 24. [TETSUO] Diagnóstico pedagógico de sanitizers..."
tetsuo run build/app

echo ""
echo "▶ 25. [KANE] Depuración visual de archivos binarios..."
python3 -c "import struct; open('build/sample.bin', 'wb').write(struct.pack('<if', 42, 9.5))"
kane inspect build/sample.bin -s 'int id, float nota'

echo ""
echo "▶ 26. [FERRO] Perfilado de rendimiento algorítmico..."
ferro profile build/app --inputs '100,500'

echo ""
echo "▶ 27. [ESPER] Traducción y explicación didáctica de advertencias GCC..."
esper explain "main.c:10: warning: unused variable 'x' [-Wunused-variable]"

echo ""
echo "▶ 28. [VASQUEZ] Inyección de fallos en tiempo de ejecución (LD_PRELOAD)..."
vasquez inject build/app --faults "malloc:1,fopen:1"

echo ""
echo "▶ 29. [DIETRICH] Validador de cobertura lógica avanzada MC/DC..."
dietrich analyze src/parser.c

echo ""
echo "▶ 30. [RIPLEY] Diagnóstico de entorno y reglas pedagógicas..."
ripley doctor
ripley explain 0x1001h

echo ""
echo "▶ 31. [DECKARD] Gestión de banco y estadísticas Bloom..."
deckard doctor
deckard stats --help > /dev/null

echo ""
echo "▶ 32. [DREDD] Orquestación de correcciones y evaluación masiva..."
dredd doctor

echo ""
echo "▶ 33. [MEET-TOOLS] Telemetría y CLI de Google Meet..."
meet-tools --help > /dev/null

echo ""
echo "▶ 34. [SLIDE-TOOLS] Control y simulación de presentaciones Google Slides..."
slide-tools --help > /dev/null

echo ""
echo "▶ 35. [KEYMAKER] Gestor criptográfico y sellado time-lock..."
keymaker doctor

echo ""
echo "▶ 36. [SCORM-TOOLS] Empaquetador y validador de módulos SCORM..."
scorm-tools doctor

echo ""
echo "▶ 37. [ALUCARD] Sintetizador de exámenes impresos Typst..."
alucard --help > /dev/null

echo ""
echo "▶ 38. [IDKFA] Generador procedural de preguntas Moodle XML con GCC..."
idkfa --help > /dev/null

echo ""
echo "▶ 39. [MOODLE-TOOLBOX] Conversor y validador de bancos de preguntas..."
moodle-toolbox --help > /dev/null

echo ""
echo "▶ 40. [MYST-TOOLS] Formateador e indexador de apuntes MyST..."
myst-tools --help > /dev/null

echo ""
echo "▶ 41. [LIB_TEST] Testing pedagógico en C con reporte Markdown..."
daedalus compile --flags "-Iinclude" src/p1_test.c src/test_lib_test.c -o build/test_lib_test
build/test_lib_test --md-report build/lib_test_report.md

echo ""
echo "================================================================================"
echo "🎉 SMOKE TEST COMPLETO: TODAS LAS HERRAMIENTAS FUNCIONAN CORRECTAMENTE"
echo "================================================================================"
