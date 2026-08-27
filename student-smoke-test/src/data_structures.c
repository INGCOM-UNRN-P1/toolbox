#include "data_structures.h"
#include <stdlib.h>

/* Función recursiva con caso base explícito (inspeccionable por SEBASTIAN) */
int calcular_factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * calcular_factorial(n - 1);
}

/* Switch con casos secuenciales densos (compilable como Jump Table O(1) analizada por RACHEL) */
int procesar_comando(int comando) {
    int resultado = 0;
    switch (comando) {
        case 1:
            resultado = 100;
            break;
        case 2:
            resultado = 200;
            break;
        case 3:
            resultado = 300;
            break;
        case 4:
            resultado = 400;
            break;
        case 5:
            resultado = 500;
            break;
        case 6:
            resultado = 600;
            break;
        default:
            resultado = -1;
            break;
    }
    return resultado;
}

/* Asignación en Heap para análisis de memoria con BISHOP */
t_nodo* crear_nodo(int valor) {
    t_nodo* nuevo = malloc(sizeof(t_nodo));
    if (nuevo == NULL) {
        return NULL;
    }
    nuevo->valor = valor;
    nuevo->siguiente = NULL;
    return nuevo;
}

t_nodo* crear_lista(int cantidad) {
    t_nodo* cabeza = NULL;
    for (int i = 0; i < cantidad; i++) {
        t_nodo* nuevo = crear_nodo(i * 10);
        if (nuevo != NULL) {
            nuevo->siguiente = cabeza;
            cabeza = nuevo;
        }
    }
    return cabeza;
}

void liberar_lista(t_nodo* cabeza) {
    t_nodo* actual = cabeza;
    while (actual != NULL) {
        t_nodo* temp = actual->siguiente;
        free(actual);
        actual = temp;
    }
}
