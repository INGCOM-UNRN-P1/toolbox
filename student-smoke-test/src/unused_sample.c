/* Funciones huérfanas / dead code para detección con GIGER */
#include <stdio.h>

void funcion_huerfana_uno(void) {
    printf("Esta función nunca es invocada desde main\n");
}

void funcion_huerfana_dos(void) {
    funcion_huerfana_uno();
}
