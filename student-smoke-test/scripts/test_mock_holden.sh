#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo "🧪 [HOLDEN] Generación de Mocks e Inyección de Fallos"
echo "============================================================"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# 1. Generar mock de fopen con Holden
echo "--- 1. Generando mock de fopen que falla al 2do llamado ---"
holden generate fopen -o "$TMP_DIR/fopen_mock.c" -n 2

# 2. Crear programa de prueba que consume fopen
cat << 'EOF' > "$TMP_DIR/app.c"
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE* f1 = fopen("/dev/null", "r");
    printf("Fopen 1: %s\n", f1 ? "OK" : "NULL");

    FILE* f2 = fopen("/dev/null", "r");
    printf("Fopen 2 (Inyectado): %s\n", f2 ? "OK" : "FALLO (NULL esperado)");

    if (f1 != NULL && f2 == NULL) {
        printf("✓ Inyección de fallo de fopen exitosa.\n");
        fclose(f1);
        return 0;
    }

    if (f1) fclose(f1);
    if (f2) fclose(f2);
    return 1;
}
EOF

# 3. Compilar con GCC usando el linker flag -Wl,--wrap=fopen
echo "--- 2. Compilando aplicación con wrapper de linker ---"
gcc -O0 "$TMP_DIR/app.c" "$TMP_DIR/fopen_mock.c" -Wl,--wrap=fopen -o "$TMP_DIR/test_holden_bin"

# 4. Ejecutar y verificar inyección
echo "--- 3. Ejecutando binario instrumentado ---"
"$TMP_DIR/test_holden_bin"

echo "============================================================"
echo "✅ HOLDEN Smoke Test Completado con Éxito"
echo "============================================================"
