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

# La lista sale del manifiesto único ecosistema.toml (N-P1TOOLS-02): cada
# línea es "carpeta url". Incluye plantillas y librerías (carpetas anidadas).
if ! mapfile -t REPOSITORIOS < <(python3 "$SCRIPT_DIR/ecosistema.py" listar --formato clonar); then
    echo "[ERROR] No se pudo leer ecosistema.toml con scripts/ecosistema.py (requiere Python >= 3.11)." >&2
    exit 1
fi

echo "==> Directorio destino de repositorios: $BASE_DIR"
mkdir -p "$BASE_DIR"

total=${#REPOSITORIOS[@]}
actual=0
fallos=0

for item in "${REPOSITORIOS[@]}"; do
    actual=$((actual + 1))
    read -r dir_name https_url <<< "$item"
    target_path="$BASE_DIR/$dir_name"

    if [ "$USE_SSH" = true ]; then
        repo_url="git@github.com:${https_url#https://github.com/}.git"
    else
        repo_url="${https_url}.git"
    fi

    echo "[$actual/$total] Procesando $dir_name (${https_url#https://github.com/})..."
    mkdir -p "$(dirname "$target_path")"

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
