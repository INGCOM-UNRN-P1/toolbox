#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# health_check.sh — Auditoría de salud y dependencias del ecosistema P1
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Un ejecutable por herramienta activa, desde el manifiesto ecosistema.toml
# (N-P1TOOLS-02). Antes la lista fija cubría 17 de las 42 herramientas.
if ! mapfile -t TOOLS < <(python3 "$SCRIPT_DIR/ecosistema.py" listar --tipo cli --estado activo --formato ejecutable-principal); then
    echo "[ERROR] No se pudo leer ecosistema.toml con scripts/ecosistema.py (requiere Python >= 3.11)." >&2
    exit 1
fi

echo "=============================================================================="
echo " Auditoría de Salud del Ecosistema P1 (doctor)"
echo "=============================================================================="

ok_count=0
fail_count=0
missing_count=0

for tool in "${TOOLS[@]}"; do
    echo ""
    echo "──────────────────────────────────────────────────────────────────────────────"
    echo " Herramienta: $tool"
    echo "──────────────────────────────────────────────────────────────────────────────"

    if ! command -v "$tool" &>/dev/null; then
        echo " [NO INSTALADA] El ejecutable '$tool' no se encuentra en el PATH."
        missing_count=$((missing_count + 1))
        continue
    fi

    if "$tool" doctor 2>/dev/null; then
        echo " ✓ $tool doctor: OK"
        ok_count=$((ok_count + 1))
    else
        echo " ✖ $tool doctor: Reportó fallos o advertencias críticas."
        fail_count=$((fail_count + 1))
    fi
done

echo ""
echo "=============================================================================="
echo " Resumen de Auditoría:"
echo "   • Herramientas operativas (doctor OK): $ok_count"
echo "   • Herramientas con fallas:             $fail_count"
echo "   • Herramientas no encontradas:         $missing_count"
echo "=============================================================================="

if [ "$fail_count" -gt 0 ] || [ "$missing_count" -gt 0 ]; then
    exit 1
fi
exit 0
