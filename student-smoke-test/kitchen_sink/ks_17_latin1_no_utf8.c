#include <stdio.h>

/* comentario con acentos en Latin-1: ñ á é í ó ú, codificado en
 * ISO-8859-1 en vez de UTF-8 a proposito, para que cualquier lectura
 * ingenua con .decode("utf-8") reviente con UnicodeDecodeError. */
int
main(void)
{
    printf("ñoño\n");
    return 0;
}
