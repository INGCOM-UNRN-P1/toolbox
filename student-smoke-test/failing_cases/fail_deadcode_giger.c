/* Código con funciones huérfanas / muertas y variables no alcanzables */
#include <stdio.h>

static void funcion_nunca_invocada_a(void) {
    printf("Nadie me llama jamás\n");
}

static void funcion_nunca_invocada_b(void) {
    funcion_nunca_invocada_a();
}

int main(void) {
    printf("Solo main se ejecuta\n");
    return 0;
}
