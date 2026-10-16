#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# health_check.sh — Auditoría de salud y dependencias del ecosistema P1
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================
#
# Delega en `mother doctor`: el diagnóstico agregado (python, uv, git y el doctor
# de cada herramienta activa de ecosistema.toml, con cómo resolver lo que falta).
# Acepta las opciones de mother doctor:
#
#   scripts/health_check.sh                      # todas las herramientas
#   scripts/health_check.sh --perfil estudiante  # solo un perfil (repetible)
#   scripts/health_check.sh --json               # informe JSON con schema_version
#
# Sale con 0 si está todo lo requerido y con 1 si falta algo.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_mother.sh
source "$SCRIPT_DIR/_mother.sh"
mother_cmd "$(cd "$SCRIPT_DIR/../.." && pwd)" "$SCRIPT_DIR/../ecosistema.toml" || exit 1
exec "${MOTHER[@]}" doctor "$@"
