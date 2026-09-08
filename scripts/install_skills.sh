#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# install_skills.sh — Instalación de skills pedagógicas para agentes de IA
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================

USE_SYMLINK=false
WORKSPACE_ONLY=false
CUSTOM_TARGET=""

usage() {
    cat <<EOF
Uso: $0 [OPCIONES]

Instala las definiciones de skills pedagógicas en las ubicaciones estándar de agentes de IA.

Opciones:
  -s, --symlink       Crea enlaces simbólicos en lugar de copiar archivos.
  -w, --workspace     Instala solo en el workspace actual (.agents/skills).
  -t, --target DIR    Instala en un directorio destino personalizado.
  -h, --help          Muestra este mensaje de ayuda.

Ubicaciones estándar atendidas automáticamente:
  - ~/.gemini/skills/
  - ~/.gemini/config/skills/
  - ~/.agents/skills/
  - ~/.claude/skills/
EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--symlink)
            USE_SYMLINK=true
            shift
            ;;
        -w|--workspace)
            WORKSPACE_ONLY=true
            shift
            ;;
        -t|--target)
            CUSTOM_TARGET="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Opción desconocida: $1" >&2
            usage
            ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/../skills"

if [ ! -d "$SKILLS_SRC" ]; then
    echo "[ERROR] No se encontró el directorio de skills en $SKILLS_SRC" >&2
    exit 1
fi

install_skill_dir() {
    local dest_base="$1"
    mkdir -p "$dest_base"

    for skill_path in "$SKILLS_SRC"/*; do
        if [ -d "$skill_path" ]; then
            local skill_name
            skill_name="$(basename "$skill_path")"
            local target_skill_dir="$dest_base/$skill_name"

            if [ "$USE_SYMLINK" = true ]; then
                rm -rf "$target_skill_dir"
                ln -sf "$skill_path" "$target_skill_dir"
                echo "  [SYMLINK] $skill_name -> $target_skill_dir"
            else
                rm -rf "$target_skill_dir"
                mkdir -p "$target_skill_dir"
                cp -r "$skill_path"/* "$target_skill_dir/"
                echo "  [COPY]    $skill_name -> $target_skill_dir"
            fi
        fi
    done
}

if [ -n "$CUSTOM_TARGET" ]; then
    echo "==> Instalando skills en destino personalizado: $CUSTOM_TARGET"
    install_skill_dir "$CUSTOM_TARGET"
    echo "==> ¡Instalación completada!"
    exit 0
fi

if [ "$WORKSPACE_ONLY" = true ]; then
    WORKSPACE_DEST="$(pwd)/.agents/skills"
    echo "==> Instalando skills en el workspace actual: $WORKSPACE_DEST"
    install_skill_dir "$WORKSPACE_DEST"
    echo "==> ¡Instalación completada!"
    exit 0
fi

TARGET_DIRS=(
    "$HOME/.gemini/skills"
    "$HOME/.gemini/config/skills"
    "$HOME/.agents/skills"
    "$HOME/.claude/skills"
)

echo "==> Instalando skills en ubicaciones estándar del usuario..."
for target in "${TARGET_DIRS[@]}"; do
    echo " -> Directorio: $target"
    install_skill_dir "$target"
done

echo ""
echo "==> ¡Todas las skills fueron instaladas exitosamente!"
