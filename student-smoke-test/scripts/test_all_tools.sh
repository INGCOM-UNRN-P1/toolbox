#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

echo "================================================================================"
echo "🚀 EJECUTANDO SMOKE TEST DE TODAS LAS HERRAMIENTAS DEL ESTUDIANTE"
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
echo "▶ 16. [RIPLEY] Diagnóstico de entorno del cliente docente..."
ripley doctor

echo ""
echo "================================================================================"
echo "🎉 SMOKE TEST COMPLETO: TODAS LAS HERRAMIENTAS FUNCIONAN CORRECTAMENTE"
echo "================================================================================"
