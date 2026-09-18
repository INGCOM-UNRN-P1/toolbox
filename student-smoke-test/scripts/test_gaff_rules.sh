#!/usr/bin/env bash
set -euo pipefail

echo "=== 1. Verificando detección exhaustiva de reglas de cátedra en C ==="
out_json=$(gaff check --json gaff_cases/violaciones_estilo.c 2>&1 || true)

# Comprobar presencia de códigos canónicos
for code in "0x2004h" "0x0005h" "0x5001h" "0x300Bh" "0x0004h" "0x0007h" "0x1001h" "0x1003h" "0x5006h" "0x5004h" "0x1006h"; do
    if ! grep -q "\"codigo\": \"$code\"" <<< "$out_json"; then
        echo "[ERROR] No se detectó la regla $code en violaciones_estilo.c"
        exit 1
    fi
done
echo "✓ Todas las reglas de sintaxis, control, memoria y modularización fueron detectadas (0x2004h, 0x0005h, 0x5001h, 0x300Bh, 0x0004h, 0x0007h, 0x1001h, 0x1003h, 0x5006h, 0x5004h, 0x1006h)."

echo "=== 2. Verificando reglas de cabecera (.h) ==="
out_h_json=$(gaff check --json gaff_cases/cabecera_invalida.h 2>&1 || true)
if ! grep -q "\"codigo\": \"0x5003h\"" <<< "$out_h_json"; then
    echo "[ERROR] No se detectó la regla 0x5003h (guardas de inclusión)"
    exit 1
fi
if ! grep -q "\"codigo\": \"0x301Dh\"" <<< "$out_h_json"; then
    echo "[ERROR] No se detectó la regla 0x301Dh (definición de struct en .h, ex-0x0035h)"
    exit 1
fi
echo "✓ Reglas de cabecera 0x5003h y 0x301Dh detectadas exitosamente."

echo "=== 3. Verificando regla 0x0104h (nombre de archivo con espacios/mayúsculas, ex-0x000Ch) ==="
out_fn_json=$(gaff check --json "gaff_cases/Nombre Con Espacios.c" 2>&1 || true)
if ! grep -q "\"codigo\": \"0x0104h\"" <<< "$out_fn_json"; then
    echo "[ERROR] No se detectó la regla 0x0104h (snake_case en nombres de archivo)"
    exit 1
fi
echo "✓ Regla 0x0104h detectada exitosamente."

echo "=== 4. Verificando autoformateo Allman y autofixes (gaff fix) ==="
tmp_fix_dir=$(mktemp -d)
trap 'rm -rf "$tmp_fix_dir"' EXIT
cp gaff_cases/violaciones_estilo.c "$tmp_fix_dir/test_fix.c"

gaff fix "$tmp_fix_dir/test_fix.c" >/dev/null 2>&1 || true
fixed_content=$(cat "$tmp_fix_dir/test_fix.c")

# Verificar espaciado de keywords
if ! grep -q "if (n > 0)" <<< "$fixed_content"; then
    echo "[ERROR] gaff fix no corrigió 'if(n > 0)' a 'if (n > 0)'"
    exit 1
fi

# Verificar espaciado de punteros
if ! grep -q "int \*ptr_malo" <<< "$fixed_content"; then
    echo "[ERROR] gaff fix no corrigió 'int* ptr_malo' a 'int *ptr_malo'"
    exit 1
fi

# Verificar llaves Allman
if ! grep -A 1 "if (n > 0)" <<< "$fixed_content" | grep -q "{"; then
    echo "[ERROR] gaff fix no colocó la llave en línea independiente estilo Allman"
    exit 1
fi
echo "✓ Autofixes y autoformateo Allman verificados exitosamente."

echo "=== 5. Verificando catálogo y explicaciones didácticas de GAFF ==="
gaff rules >/dev/null
gaff explain 0x0104h >/dev/null
gaff explain 0x1001h >/dev/null
echo "✓ Catálogo de reglas y explicaciones didácticas funcionando correctamente."
