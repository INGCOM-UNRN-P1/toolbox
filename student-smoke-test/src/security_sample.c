/* Archivo de muestra didáctica para auditoría con KANEDA, SPUNKMEYER y GAFF */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void funcion_con_antipatrones_y_riesgos(void) {
    /* GAFF001: Identificador en camelCase */
    int MiVariableCamel = 10;

    /* KAN001 / KAN002: Funciones inseguras (gets/sprintf) */
    char buffer[32];
    gets(buffer);

    /* AP001: Cast innecesario de malloc */
    int* ptr = (int*)malloc(sizeof(int) * 10);

    /* AP004: Chequeo redundante de NULL antes de free */
    if (ptr != NULL) {
        free(ptr);
    }

    /* AP003: Comparación redundante con booleano */
    bool flag = true;
    if (flag == true) {
        MiVariableCamel++;
    }

    /* GAFF008: Sentencia goto */
    goto fin;

fin:
    return;
}
