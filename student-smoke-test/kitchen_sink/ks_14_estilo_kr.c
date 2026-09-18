#include <stdio.h>

/*
 * Definiciones de función en estilo K&R pre-ANSI: sin prototipo, con la
 * lista de parámetros declarada por separado antes de la llave de
 * apertura, y con "int" implícito. Sintaxis legal en C89 pero rechazada
 * bajo -std=c11 -pedantic; el objetivo es un diagnóstico claro y no un
 * traceback del analizador.
 */
suma(a, b)
    int a;
    int b;
{
    return a + b;
}

main()
{
    printf("%d\n", suma(2, 3));
    return 0;
}
