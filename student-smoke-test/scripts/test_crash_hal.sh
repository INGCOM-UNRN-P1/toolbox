#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo "🧪 [HAL] Demostración de Diagnóstico Forense de Crashes"
echo "============================================================"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# 1. Crear snippet con Segfault intencional
cat << 'EOF' > "$TMP_DIR/crash_segv.c"
#include <stdio.h>

void desreferenciar_nulo(void) {
    int *puntero_invalido = NULL;
    *puntero_invalido = 42;
}

int main(void) {
    desreferenciar_nulo();
    return 0;
}
EOF

echo "--- 1. Ejecutando HAL ante SIGSEGV (Desreferencia NULL) ---"
if hal run "$TMP_DIR/crash_segv.c"; then
    echo "❌ Error: Se esperaba un crash diagnosticado."
    exit 1
else
    echo "✓ HAL diagnosticó correctamente la desreferencia a NULL."
fi

# 2. Crear snippet con División por Cero
cat << 'EOF' > "$TMP_DIR/crash_fpe.c"
#include <stdio.h>

int dividir(int a, int b) {
    return a / b;
}

int main(void) {
    int x = 100;
    int y = 0;
    printf("Resultado: %d\n", dividir(x, y));
    return 0;
}
EOF

echo "--- 2. Ejecutando HAL ante SIGFPE (División por Cero) ---"
if hal run "$TMP_DIR/crash_fpe.c"; then
    echo "❌ Error: Se esperaba un crash por SIGFPE."
    exit 1
else
    echo "✓ HAL diagnosticó correctamente la división por cero."
fi

echo "============================================================"
echo "✅ HAL Smoke Test Completado con Éxito"
echo "============================================================"
