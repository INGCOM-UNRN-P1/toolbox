#include <stdio.h>

/*
 * Macro multilínea con continuación de línea via backslash-newline,
 * incluyendo una continuación con espacio en blanco final después del
 * backslash (variante que algunos preprocesadores tratan distinto) y
 * anidamiento de otra macro dentro de la expansión.
 */
#define CUADRADO(x) ((x) * (x))

#define REPORTAR_ESTADISTICAS(nombre, valor)             \
    do {                                                 \
        printf("%s: valor=%d cuadrado=%d\n",             \
               (nombre),                                 \
               (valor),                                  \
               CUADRADO(valor));                          \
    } while (0)

int
main(void)
{
    REPORTAR_ESTADISTICAS("contador", 7);
    return 0;
}
