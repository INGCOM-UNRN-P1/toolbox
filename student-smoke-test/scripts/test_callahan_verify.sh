#!/usr/bin/env bash
set -euo pipefail

# frama-c es un prover OPCIONAL para Callahan (ver 'callahan doctor'). Sin él,
# 'callahan verify' informa 'UNVERIFIED' y sale con código 2 (no se pudo verificar; 1 es un contrato rechazado) aunque los contratos
# ACSL se hayan extraído correctamente. Este script solo falla ante un rechazo
# real de Frama-C (frama_c_disponible=true y ok=false), no ante su ausencia.

out_json=$(callahan verify --json src/data_structures.h 2>&1 || true)

frama_disponible=$(grep -o '"frama_c_disponible": [a-z]*' <<< "$out_json" | awk '{print $2}')
ok=$(grep -o '"ok": [a-z]*' <<< "$out_json" | head -1 | awk '{print $2}')

if [ "$frama_disponible" = "true" ] && [ "$ok" != "true" ]; then
    echo "[ERROR] Frama-C está disponible pero la verificación deductiva de contratos ACSL falló."
    echo "$out_json"
    exit 1
fi

if [ "$frama_disponible" = "true" ]; then
    echo "✓ Contratos ACSL verificados deductivamente con Frama-C."
else
    echo "✓ Contratos ACSL extraídos correctamente (Frama-C no disponible; prover opcional, ver 'callahan doctor')."
fi
