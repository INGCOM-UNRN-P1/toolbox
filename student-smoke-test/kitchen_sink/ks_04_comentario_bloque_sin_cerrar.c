#include <stdio.h>

/* Este comentario de bloque se abre pero nunca se cierra, a propósito.
 * El objetivo es verificar que el compilador y los linters informen un
 * diagnóstico claro (EOF dentro de comentario) en vez de colgarse o
 * consumir el resto del archivo de forma silenciosa.

int
main(void)
{
    printf("nunca se llega a compilar esto\n");
    return 0;
}
