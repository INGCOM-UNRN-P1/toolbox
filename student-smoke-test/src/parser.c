#include "parser.h"
#include <stdlib.h>
#include <limits.h>
#include <errno.h>

/* Parser robusto preparado para testing guiado por límites (DRAKE) */
int parsear_entero_seguro(const char* str, int* out_valor) {
    if (str == NULL || out_valor == NULL) {
        return -1;
    }

    char* endptr = NULL;
    errno = 0;
    long val = strtol(str, &endptr, 10);

    if (endptr == str || *endptr != '\0') {
        return -2; /* No es un número válido */
    }

    if (errno == ERANGE || val < INT_MIN || val > INT_MAX) {
        return -3; /* Fuera de rango */
    }

    *out_valor = (int)val;
    return 0;
}
