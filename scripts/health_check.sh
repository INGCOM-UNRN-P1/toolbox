#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# health_check.sh — Auditoría de salud y dependencias del ecosistema P1
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================

TOOLS=(
    daedalus
    gaff
    hal
    bishop
    spunkmeyer
    brett
    kaneda
    nostromo
    drake
    holden
    ripley
    dredd
    deckard
    alucard
    idkfa
    moodle-toolbox
    myst-tools
)

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
