#include <stdio.h>

/*
 * El propio nombre de archivo es el caso límite: espacios y una ñ.
 * Verifica que ningún comando construya rutas sin comillas ni
 * asuma nombres ASCII simples al invocar subprocess/shell.
 */
int
main(void)
{
    printf("archivo con nombre raro\n");
    return 0;
}
