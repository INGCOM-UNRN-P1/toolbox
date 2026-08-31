/* Archivo C con antipatrones didácticos concentrados para Spunkmeyer */
#include <stdio.h>
#include <stdlib.h>

void procesar_archivo(FILE *f) {
    int *ptr = NULL;
    
    /* 0x300Ah: Cast redundante de malloc */
    /* 0x300Fh: sizeof(puntero) en malloc */
    ptr = (int *)malloc(sizeof(ptr));

    /* 0x4006h: fflush(stdin) */
    fflush(stdin);

    /* 0x4001h: while(!feof) */
    while (!feof(f)) {
        int c = fgetc(f);
        printf("%c", c);
    }

    /* 0x300Bh: Redundant NULL check before free */
    if (ptr != NULL) {
        free(ptr);
    }
}
