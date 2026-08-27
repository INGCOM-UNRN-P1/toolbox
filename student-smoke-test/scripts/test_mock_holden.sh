#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p build

echo "============================================================"
echo "🧪 [HOLDEN] Generación de Mocks e Inyección de Fallos"
echo "============================================================"

# 1. Generar mock de fopen con Holden
echo "--- 1. Generando mock de fopen que falla al 2do llamado ---"
holden generate fopen -o "build/fopen_mock.c" -n 2

# 2. Compilar aplicación explícita vinculada al wrapper generado
echo "--- 2. Compilando aplicación explícita con wrapper de linker ---"
gcc -O0 "src/mocks/holden_app.c" "build/fopen_mock.c" -Wl,--wrap=fopen -o "build/test_holden_bin"

# 3. Ejecutar binario instrumentado
echo "--- 3. Ejecutando binario instrumentado ---"
"build/test_holden_bin"

echo "============================================================"
echo "✅ HOLDEN Smoke Test Completado con Éxito"
echo "============================================================"
