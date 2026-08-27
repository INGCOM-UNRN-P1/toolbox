/* Programa explícito consumidor de fopen para verificación de inyección de fallos con HOLDEN */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE* f1 = fopen("/dev/null", "r");
    printf("Fopen 1: %s\n", f1 ? "OK" : "NULL");

    FILE* f2 = fopen("/dev/null", "r");
    printf("Fopen 2 (Inyectado): %s\n", f2 ? "OK" : "FALLO (NULL esperado)");

    if (f1 != NULL && f2 == NULL) {
        printf("✓ Inyección de fallo de fopen exitosa.\n");
        fclose(f1);
        return 0;
    }

    if (f1 != NULL) {
        fclose(f1);
    }
    if (f2 != NULL) {
        fclose(f2);
    }
    return 1;
}
