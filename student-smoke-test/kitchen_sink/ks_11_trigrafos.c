#include <stdio.h>

/*
 * Trigrafos de C89/C99 (eliminados en C23, pero históricamente válidos y
 * a veces reintroducidos accidentalmente al pegar código de otra fuente).
 * ??( == [   ??) == ]   ??< == {   ??> == }   ??= == #   ??! == |   ??/ == \
 * El objetivo es que el compilador los rechace o traduzca con un
 * diagnóstico claro, y que el resto del pipeline (gaff, bishop, etc.)
 * no interprete mal las columnas/offsets por la sustitución de trigrafos.
 */
int
main(void)
??<
    int vector??(3??) = ??<1, 2, 3??>;
    printf("%d\n", vector??(0??));
    return 0;
??>
