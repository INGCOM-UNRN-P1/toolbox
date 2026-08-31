/* Archivo C con errores de sintaxis y tipos deliberados para probar Daedalus */
#include <stdio.h>

int main(void) {
    int x = "cadena_invalida"; /* Error de tipo */
    int *ptr = 12345;          /* Incompatible pointer */
    if (x > 0 {                 /* Paréntesis sin cerrar */
        printf("Error de sintaxis\n")
    }
    return 0;
}
