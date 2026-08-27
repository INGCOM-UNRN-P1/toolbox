/* Programa explícito para diagnóstico de desreferencia a NULL con HAL */
#include <stdio.h>
#include <stdlib.h>

void desreferenciar_nulo(void) {
    int* puntero_invalido = NULL;
    *puntero_invalido = 42;
}

int main(void) {
    desreferenciar_nulo();
    return 0;
}
