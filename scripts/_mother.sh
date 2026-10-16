# shellcheck shell=bash
# _mother.sh — Cómo encuentran a mother los scripts de p1-tools (install_tools.sh, health_check.sh).
#
# Orden: el clon local de mother junto a p1-tools (es el de la misma versión que este
# manifiesto y mother no tiene dependencias), el mother instalado en el PATH y, si no hay
# ninguno, mother desde git con uvx. Siempre con el ecosistema.toml de este p1-tools.

mother_cmd() {
    local raiz="$1" manifiesto="$2"
    if [ -f "$raiz/mother/src/mother/__main__.py" ]; then
        MOTHER=(env "PYTHONPATH=$raiz/mother/src" python3 -m mother)
    elif command -v mother &>/dev/null; then
        MOTHER=(mother)
    elif command -v uvx &>/dev/null; then
        MOTHER=(uvx --from "git+https://github.com/INGCOM-UNRN-P1/mother" mother)
    else
        echo "[ERROR] No se encontró mother (ni clonado en $raiz/mother, ni instalado, ni uv para traerlo)." >&2
        return 1
    fi
    MOTHER+=(--manifiesto "$manifiesto")
}
