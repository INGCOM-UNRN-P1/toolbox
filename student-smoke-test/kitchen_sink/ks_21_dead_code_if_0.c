#include <stdio.h>

/*
 * Bloques `#if 0 ... #endif` con sintaxis deliberadamente inválida
 * adentro (código muerto que el preprocesador debe descartar sin que
 * el compilador ni los linters intenten parsearlo como C real).
 * También incluye #if 0 anidado y un #elif que sí se activa.
 */
#if 0
    esto no es C válido en absoluto { ] ) ( sintaxis rota sin sentido
    #include <un_header_que_no_existe_ni_nunca_existira.h>
    int x = ; // expresión vacía, error de sintaxis si se compilara
    #if 0
        más código roto anidado *** &&& |||
    #endif
#elif 1
static const char *MENSAJE = "rama viva del #elif";
#else
    otro bloque muerto con basura +++ === !!!
#endif

int
main(void)
{
#if 0
    printf("esto nunca se compila\n");
#endif
    printf("%s\n", MENSAJE);
    return 0;
}
