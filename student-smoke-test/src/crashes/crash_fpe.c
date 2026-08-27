/* Programa explícito para diagnóstico de división por cero con HAL */
#include <stdio.h>

int dividir(int a, int b) {
    return a / b;
}

int main(void) {
    int dividendo = 100;
    int divisor = 0;
    printf("Resultado: %d\n", dividir(dividendo, divisor));
    return 0;
}
