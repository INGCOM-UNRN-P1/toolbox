---
name: idkfa
description: Use when generating randomized, anti-cheating Moodle XML questionnaires and multiple-choice C code tracing variants from C source templates with automated GCC execution.
---

# IDKFA — Generador de Cuestionarios Moodle desde Plantillas C

## Overview
`idkfa` es una herramienta CLI para generar cuestionarios XML para Moodle a partir de plantillas en lenguaje C. Permite definir rangos de variables dinámicas, compilar y ejecutar cada variante con GCC para calcular automáticamente la respuesta correcta y generar distractores plausibles basados en errores conceptuales típicos. También incluye sustitución de caracteres invisibles o equivalentes Unicode para prevenir copypasteo directo a compiladores durante exámenes.

## Cuándo Usar
- Para crear bancos de preguntas de opción múltiple en formato Moodle XML con variantes numéricas aleatorias.
- Para verificar el comportamiento y compilar variantes C en modo depuración (`--generate-only`).
- Para generar preguntas de trazas de código C donde la clave de respuesta esté garantizada por la ejecución real del binario.

## Comandos CLI

### 1. Generación de Cuestionario XML
```bash
# Procesar todas las plantillas en templates/ y generar archivo XML
idkfa -s templates/ -o cuestionario_moodle.xml -n 5 -c "Programacion1/Parcial1"

# Procesar una plantilla específica
idkfa -t templates/punteros/aritmetica.c -o test_punteros.xml -n 3
```

### 2. Modo Verificación y Depuración de Código C
```bash
# Generar solo el código fuente C de las variantes en generated/ sin crear el XML
idkfa -g -t templates/punteros/aritmetica.c -n 3

# Compilar todas las variantes generadas usando el Makefile emitido
cd generated && make
```

## Anatomía de una Plantilla C (`templates/.../*.c`)

Una plantilla válida en C combina código ejecutable con metadatos estructurados:

```c
// Analizá el siguiente código. ¿Cuál es el valor final de 'x'?
#include <stdio.h>

//# --- Macros para desarrollo local (removidas automáticamente por idkfa) ---
#define __val_a__ 10
#define __val_b__ 5
//# --------------------------------------------------------------------------

int main(void) {
    int a = __val_a__;
    int b = __val_b__;
    int x = (a * 2) + b;
    printf("%d\n", x);
    return 0;
}
// ¿Qué valor se imprime en la terminal?

/*name
Operaciones Aritméticas Básicas
*/

/*var
__val_a__ = random.randint(3, 12)
__val_b__ = random.choice([2, 4, 6, 8])
*/

/*explanation
La operación multiplica 'a' por 2 antes de sumar 'b' debido a la precedencia de operadores.
*/
```

## Opciones Principales
- `-s, --source <DIR>`: Directorio raíz de plantillas `.c` (default: `templates`).
- `-t, --template <FILE>`: Ruta a una plantilla `.c` puntual.
- `-o, --output <FILE>`: Nombre del archivo XML de salida (default: `cuestionario_moodle.xml`).
- `-n, --num <N>`: Cantidad de variantes a generar por plantilla (default: 5).
- `-c, --category <NAME>`: Categoría raíz en Moodle (default: `programacion1_gen_codigo`).
- `-g, --generate-only`: Genera únicamente los archivos `.c` con un `Makefile` en `generated/` para inspección.
