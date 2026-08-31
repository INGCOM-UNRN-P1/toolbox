/* Violaciones de estilo severas: Magic numbers, identación con tabs, líneas > 100 caracteres, camelCase */
#include <stdio.h>

typedef struct {
    int valor;
} MiEstructuraInvalida; // Falta sufijo _t

int funcionCamelCase(int parametroA, int parametroB) {
	if (parametroA > 9999) { // Tabulación y magic number
		if (parametroB < 8888) { // Anidación excesiva
			if (parametroA == 7777) {
				if (parametroB == 6666) {
					printf("Esta es una linea intencionalmente larguisima que sobrepasa con creces el limite de ochenta caracteres por columna permitido por la catedra de programacion\n");
				}
			}
		}
	}
	return parametroA + 42; // Magic number
}
