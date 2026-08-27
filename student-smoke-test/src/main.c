#include <stdio.h>
#include <stdlib.h>
#include "data_structures.h"
#include "parser.h"

int main(int argc, char* argv[]) {
    int cmd = 1;
    if (argc > 1) {
        int parsed = 0;
        if (parsear_entero_seguro(argv[1], &parsed) == 0) {
            cmd = parsed;
        }
    }

    int resultado_cmd = procesar_comando(cmd);
    int fact = calcular_factorial(cmd > 0 && cmd <= 5 ? cmd : 3);

    printf("PROCESADO: cmd=%d resultado=%d factorial=%d\n", cmd, resultado_cmd, fact);

    /* Creación e inspección de memoria Heap (apuntada en BISHOP) */
    t_nodo* lista = crear_lista(3);
    liberar_lista(lista);

    return 0;
}
