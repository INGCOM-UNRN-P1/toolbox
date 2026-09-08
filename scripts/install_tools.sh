#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# install_tools.sh — Instalación y configuración de herramientas del ecosistema P1
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================

(return 0 2>/dev/null) && IS_SOURCED=true || IS_SOURCED=false

USE_PIP=false
TARGET_DIR=""

usage() {
    cat <<EOF
Uso: [source] $0 [OPCIONES]

Instala todas las herramientas del ecosistema P1 y configura el autocompletado de comandos.

Opciones:
  -p, --pip           Usa 'uv pip install -e' dentro del venv activo en lugar de 'uv tool'.
  -t, --target DIR    Directorio que contiene las carpetas de las herramientas (por defecto el directorio padre).
  -h, --help          Muestra este mensaje de ayuda.

Nota: Para cargar el autocompletado en la terminal actual de forma inmediata, ejecutá:
  source $0
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--pip)
            USE_PIP=true
            shift
            ;;
        -t|--target)
            TARGET_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${TARGET_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

if ! command -v uv &>/dev/null; then
    echo "[ERROR] 'uv' no está instalado. Instálalo con:" >&2
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
    exit 1
fi

echo "==> Instalando herramientas desde: $ROOT_DIR"

if [ "$USE_PIP" = true ]; then
    echo "==> Modo: uv pip install -e en entorno virtual..."
    for dir in "$ROOT_DIR"/*/; do
        if [ -f "$dir/pyproject.toml" ]; then
            tool_name="$(basename "$dir")"
            echo "  -> Instalando $tool_name..."
            uv pip install -e "$dir"
        fi
    done
else
    echo "==> Modo: uv tool install --editable..."
    for dir in "$ROOT_DIR"/*/; do
        if [ -f "$dir/pyproject.toml" ]; then
            tool_name="$(basename "$dir")"
            echo "  -> Instalando $tool_name..."
            uv tool install "$dir" --editable "$@" --force 2>/dev/null || uv tool install "$dir" --editable "$@"
        fi
    done
fi

echo ""
echo "==> Configurando autocompletado en el shell..."

completion_tools=()

for dir in "$ROOT_DIR"/*/; do
    if [ -f "$dir/pyproject.toml" ]; then
        scripts="$(python3 -c '
import tomllib, sys
try:
    with open(sys.argv[1], "rb") as f:
        data = tomllib.load(f)
    for s in data.get("project", {}).get("scripts", {}).keys():
        print(s)
except Exception:
    pass
' "$dir/pyproject.toml")"

        for bin_name in $scripts; do
            if command -v "$bin_name" &>/dev/null; then
                if "$bin_name" --help 2>&1 | grep -q -- "--show-completion"; then
                    echo "  [+] $bin_name: Configurando autocompletado..."
                    completion_tools+=("$bin_name")
                    "$bin_name" --install-completion &>/dev/null || true

                    if [ "$IS_SOURCED" = true ]; then
                        eval "$("$bin_name" --show-completion 2>/dev/null)" || true
                    fi
                fi
            fi
        done
    fi
done

echo ""
if [ "$IS_SOURCED" = true ]; then
    echo "==> ¡Instalación completa! Autocompletado cargado en la sesión actual para: ${completion_tools[*]:-ninguna}"
else
    echo "==> ¡Instalación completa! Autocompletado registrado permanentemente en ~/.bash_completions/ o configuración de shell."
    echo "    Para activarlo en esta terminal sin reiniciar, ejecutá:"
    echo "    source $0"
fi
