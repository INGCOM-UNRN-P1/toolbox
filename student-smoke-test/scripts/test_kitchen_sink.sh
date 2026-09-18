#!/usr/bin/env bash
# Kitchen-sink de sintaxis: no busca que los archivos compilen ni que sean
# "correctos" — busca que ninguna herramienta del pipeline (daedalus, gaff,
# ripley) reviente con un traceback sin manejar, un segfault, o un colgado,
# ante archivos y situaciones de archivo límite. Un exit code distinto de 0
# con un diagnóstico prolijo es un PASS; un traceback/crash es un FAIL.
set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

KS_DIR="kitchen_sink"
TIMEOUT_SECS=25

TOTAL=0
FALLOS=0

# Patrones que delatan un crash real (no un diagnóstico prolijo del propio
# CLI, que también puede imprimir "Error:" con salida no-cero legítima).
CRASH_PATTERN='Traceback \(most recent call last\)|RecursionError|Segmentation fault|core dumped|Fatal Python error|Aborted \(core dumped\)'

evaluar() {
    local etiqueta="$1"
    local objetivo="$2"
    shift 2
    local cmd=("$@")

    TOTAL=$((TOTAL + 1))
    local inicio fin duracion salida rc
    inicio=$(date +%s.%N)
    salida="$(timeout "$TIMEOUT_SECS" "${cmd[@]}" 2>&1)"
    rc=$?
    fin=$(date +%s.%N)
    duracion=$(awk -v a="$inicio" -v b="$fin" 'BEGIN { printf "%.1f", b - a }')

    if [ "$rc" -eq 124 ]; then
        echo "  ✗ [$etiqueta] $objetivo -> CUELGUE O EXTREMADAMENTE LENTO (excedió ${TIMEOUT_SECS}s)"
        FALLOS=$((FALLOS + 1))
    elif grep -qE "$CRASH_PATTERN" <<< "$salida"; then
        echo "  ✗ [$etiqueta] $objetivo -> CRASH sin manejar (exit=$rc, ${duracion}s)"
        echo "$salida" | grep -E "$CRASH_PATTERN" | head -1 | sed 's/^/      /'
        FALLOS=$((FALLOS + 1))
    else
        local nota=""
        awk -v d="$duracion" 'BEGIN { exit !(d+0 > 3) }' && nota="  ⚠ lento (${duracion}s)"
        echo "  ✓ [$etiqueta] $objetivo -> manejado con gracia (exit=$rc, ${duracion}s)${nota}"
    fi
}

echo "================================================================================"
echo "🍳 KITCHEN SINK DE SINTAXIS — clases de archivo y situaciones de archivo límite"
echo "================================================================================"

echo ""
echo "▶ 1. Archivos de contenido límite (${KS_DIR}/) vs daedalus, gaff y ripley"
for archivo in "$KS_DIR"/*; do
    nombre="$(basename "$archivo")"
    evaluar "daedalus" "$nombre" daedalus compile "$archivo" -o /tmp/ks_build_out
    evaluar "gaff"     "$nombre" gaff check "$archivo"
    evaluar "ripley"   "$nombre" ripley check "$archivo"
done

echo ""
echo "▶ 2. Situaciones de archivo (no contenido: filesystem)"

TMP_SITUACIONES="$(mktemp -d)"
trap 'rm -rf "$TMP_SITUACIONES"' EXIT

# a) Ruta inexistente
evaluar "daedalus" "ruta-inexistente.c"      daedalus compile "$TMP_SITUACIONES/no_existe.c" -o /tmp/ks_build_out
evaluar "gaff"     "ruta-inexistente.c"      gaff check "$TMP_SITUACIONES/no_existe.c"

# b) Directorio pasado en vez de archivo
evaluar "daedalus" "directorio-como-archivo" daedalus compile "$KS_DIR" -o /tmp/ks_build_out
evaluar "gaff"     "directorio-como-archivo" gaff check "$KS_DIR"

# c) Archivo sin permiso de lectura
SIN_PERMISO="$TMP_SITUACIONES/sin_permiso.c"
cp "$KS_DIR/ks_03_solo_comentario.c" "$SIN_PERMISO"
chmod 000 "$SIN_PERMISO"
evaluar "daedalus" "sin-permiso-lectura.c"   daedalus compile "$SIN_PERMISO" -o /tmp/ks_build_out
evaluar "gaff"     "sin-permiso-lectura.c"   gaff check "$SIN_PERMISO"
chmod 644 "$SIN_PERMISO"

# d) Symlink válido a un archivo real
SYMLINK_VALIDO="$TMP_SITUACIONES/symlink_valido.c"
ln -s "$ROOT_DIR/src/data_structures.c" "$SYMLINK_VALIDO"
evaluar "daedalus" "symlink-valido.c"        daedalus compile "$SYMLINK_VALIDO" -o /tmp/ks_build_out
evaluar "gaff"     "symlink-valido.c"        gaff check "$SYMLINK_VALIDO"

# e) Symlink roto (apunta a un destino que no existe)
SYMLINK_ROTO="$TMP_SITUACIONES/symlink_roto.c"
ln -s "$TMP_SITUACIONES/objetivo_que_nunca_existe.c" "$SYMLINK_ROTO"
evaluar "daedalus" "symlink-roto.c"          daedalus compile "$SYMLINK_ROTO" -o /tmp/ks_build_out
evaluar "gaff"     "symlink-roto.c"          gaff check "$SYMLINK_ROTO"

echo ""
echo "================================================================================"
echo "📊 RESUMEN KITCHEN SINK: $((TOTAL - FALLOS))/$TOTAL manejados con gracia"
echo "================================================================================"

if [ "$FALLOS" -eq 0 ]; then
    echo "🎉 Ninguna herramienta reventó ante archivos/situaciones límite."
    exit 0
else
    echo "❌ $FALLOS caso(s) provocaron un crash sin manejar (ver detalle arriba)."
    exit 1
fi
