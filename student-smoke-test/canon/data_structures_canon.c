/* Solución canónica de referencia para comparación con WEYL */
#include <stdlib.h>

int calcular_factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * calcular_factorial(n - 1);
}

int procesar_comando(int comando) {
    switch (comando) {
        case 1: return 100;
        case 2: return 200;
        case 3: return 300;
        case 4: return 400;
        case 5: return 500;
        case 6: return 600;
        default: return -1;
    }
}
