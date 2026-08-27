#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "============================================================"
echo "🧪 [HAL] Demostración de Diagnóstico Forense de Crashes"
echo "============================================================"

# 1. Ejecutar HAL sobre el archivo de fallo por Segfault explícito
echo "--- 1. Ejecutando HAL ante SIGSEGV (Desreferencia NULL) ---"
if hal run "src/crashes/crash_segv.c"; then
    echo "❌ Error: Se esperaba un crash diagnosticado."
    exit 1
else
    echo "✓ HAL diagnosticó correctamente la desreferencia a NULL."
fi

# 2. Ejecutar HAL sobre el archivo de fallo por FPE explícito
echo "--- 2. Ejecutando HAL ante SIGFPE (División por Cero) ---"
if hal run "src/crashes/crash_fpe.c"; then
    echo "❌ Error: Se esperaba un crash por SIGFPE."
    exit 1
else
    echo "✓ HAL diagnosticó correctamente la división por cero."
fi

echo "============================================================"
echo "✅ HAL Smoke Test Completado con Éxito"
echo "============================================================"
