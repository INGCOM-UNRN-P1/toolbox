#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# clone_repos.sh — Descarga y sincronización de repositorios del ecosistema P1
# Cátedra de Programación 1 - Universidad Nacional de Río Negro
# ==============================================================================

USE_SSH=false
TARGET_DIR=""
DRY_RUN=false

usage() {
    cat <<EOF
Uso: $0 [OPCIONES]

Clona o actualiza todos los repositorios de herramientas del ecosistema P1.

Opciones:
  -s, --ssh           Usa protocolo SSH (git@github.com:...) en lugar de HTTPS.
  -t, --target DIR    Directorio destino donde clonar los repositorios (por defecto el directorio actual o padre).
  -d, --dry-run       Muestra las acciones sin ejecutar clones ni pulls.
  -h, --help          Muestra este mensaje de ayuda.

EOF
    exit 0
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -s|--ssh)
            USE_SSH=true
            shift
            ;;
        -t|--target)
            TARGET_DIR="$2"
            shift 2
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
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
BASE_DIR="${TARGET_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

# Lista de repositorios: "nombre_carpeta:organizacion:nombre_repo"
REPOSITORIOS=(
    # Core pedagógico y evaluación
    "dredd:INGCOM-UNRN-P1:dredd"
    "ripley:INGCOM-UNRN-P1:ripley"
    "daedalus:INGCOM-UNRN-P1:daedalus"
    "gaff:INGCOM-UNRN-P1:gaff"
    "hal:INGCOM-UNRN-P1:hal"
    "bishop:INGCOM-UNRN-P1:bishop"
    "spunkmeyer:INGCOM-UNRN-P1:spunkmeyer"
    "brett:INGCOM-UNRN-P1:brett"
    "kaneda:INGCOM-UNRN-P1:kaneda"
    "nostromo:INGCOM-UNRN-P1:nostromo"
    "drake:INGCOM-UNRN-P1:drake"
    "holden:INGCOM-UNRN-P1:holden"
    "rachel:INGCOM-UNRN-P1:rachel"
    "sebastian:INGCOM-UNRN-P1:sebastian"
    "callahan:INGCOM-UNRN-P1:callahan"
    "weyl:INGCOM-UNRN-P1:weyl"
    "giger:INGCOM-UNRN-P1:giger"
    "esper:INGCOM-UNRN-P1:esper"

    # Autoría docente y exámenes
    "deckard:INGCOM-UNRN:deckard"
    "alucarD:INGCOM-UNRN:alucarD"
    "idkfa:INGCOM-UNRN-P1:idkfa"
    "moodle-toolbox:INGCOM-UNRN:moodle-toolbox"
    "myst-tools:martinvilu:mystmd-tools"

    # Entorno y utilidades complementarias
    "entorno:INGCOM-UNRN-P1:entorno"
    "corbel:INGCOM-UNRN-P1:corbel"
    "crowe:INGCOM-UNRN-P1:crowe"
    "dietrich:INGCOM-UNRN-P1:dietrich"
    "ferro:INGCOM-UNRN-P1:ferro"
    "kane:INGCOM-UNRN-P1:kane"
    "motoko:INGCOM-UNRN-P1:motoko"
    "parker:INGCOM-UNRN-P1:parker"
    "tetsuo:INGCOM-UNRN-P1:tetsuo"
    "tyrell:INGCOM-UNRN-P1:tyrell"
    "vasquez:INGCOM-UNRN-P1:vasquez"
    "vassili:INGCOM-UNRN-P1:vassili"
    "wierzbowski:INGCOM-UNRN-P1:wierzbowski"
    "zhora:INGCOM-UNRN-P1:zhora"
)

echo "==> Directorio destino de repositorios: $BASE_DIR"
mkdir -p "$BASE_DIR"

total=${#REPOSITORIOS[@]}
actual=0
fallos=0

for item in "${REPOSITORIOS[@]}"; do
    actual=$((actual + 1))
    IFS=':' read -r dir_name org repo_name <<< "$item"
    target_path="$BASE_DIR/$dir_name"

    if [ "$USE_SSH" = true ]; then
        repo_url="git@github.com:${org}/${repo_name}.git"
    else
        repo_url="https://github.com/${org}/${repo_name}.git"
    fi

    echo "[$actual/$total] Procesando $dir_name ($org/$repo_name)..."

    if [ -d "$target_path/.git" ]; then
        echo "  -> Repositorio existente. Sincronizando con git pull..."
        if [ "$DRY_RUN" = true ]; then
            echo "  [DRY-RUN] git -C $target_path pull --ff-only"
        else
            if ! git -C "$target_path" pull --ff-only 2>/dev/null; then
                echo "  [AVISO] No se pudo hacer fast-forward en $dir_name. Se omite para no sobreescribir cambios locales."
            fi
        fi
    elif [ -d "$target_path" ]; then
        echo "  -> La carpeta $dir_name existe pero no contiene un repositorio Git. Omitiendo."
    else
        echo "  -> Clonando desde $repo_url..."
        if [ "$DRY_RUN" = true ]; then
            echo "  [DRY-RUN] git clone $repo_url $target_path"
        else
            if ! git clone "$repo_url" "$target_path" 2>/dev/null; then
                echo "  [ERROR] Falló la clonación de $repo_url" >&2
                fallos=$((fallos + 1))
            fi
        fi
    fi
done

echo ""
if [ "$fallos" -eq 0 ]; then
    echo "==> ¡Sincronización completada con éxito! Todos los repositorios procesados."
else
    echo "==> Sincronización finalizada con $fallos error(es). Revisá los permisos o accesos a los repositorios."
fi
