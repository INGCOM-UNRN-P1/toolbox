#include <stdio.h>

/*
 * Comentarios que contienen texto con forma de código roto o de
 * directivas de preprocesador, para verificar que ningún analizador
 * basado en regex ingenua "vea" código dentro de un comentario:
 *
 * #include "esto-no-existe.h"
 * int x = ;
 * if (a == b {
 * } */

// otro comentario de línea con una directiva falsa: #define X 1 } { ]
// y con un cierre de bloque falso: */

int
main(void)
{
    /* código real después de los comentarios trampa */
    printf("hola\n");
    return 0;
}
