#include "data_structures.h"
#include <stdlib.h>

/* Función recursiva con caso base explícito (inspeccionable por SEBASTIAN) */
int calcular_factorial(int n)
{
    if (n <= 1)
    {
        return 1;
    }
    return n * calcular_factorial(n - 1);
}

/* Switch con casos secuenciales densos
 * (compilable como Jump Table O(1) analizada por RACHEL) */
int procesar_comando(int comando)
{
    int resultado = 0;
    switch (comando)
    {
        case CMD_OP_1:
            resultado = CMD_RESP_1;
            break;
        case CMD_OP_2:
            resultado = CMD_RESP_2;
            break;
        case CMD_OP_3:
            resultado = CMD_RESP_3;
            break;
        case CMD_OP_4:
            resultado = CMD_RESP_4;
            break;
        case CMD_OP_5:
            resultado = CMD_RESP_5;
            break;
        case CMD_OP_6:
            resultado = CMD_RESP_6;
            break;
        default:
            resultado = -1;
            break;
    }
    return resultado;
}

/* Asignación en Heap para análisis de memoria con BISHOP */
t_nodo *crear_nodo(int valor)
{
    t_nodo *nuevo = malloc(sizeof(t_nodo));
    if (nuevo == NULL)
    {
        return NULL;
    }
    nuevo->valor = valor;
    nuevo->siguiente = NULL;
    return nuevo;
}

t_nodo *crear_lista(int cantidad)
{
    t_nodo *cabeza = NULL;
    for (int i = 0; i < cantidad; i++)
    {
        t_nodo *nuevo = crear_nodo(i * FACTOR_VALOR);
        if (nuevo != NULL)
        {
            nuevo->siguiente = cabeza;
            cabeza = nuevo;
        }
    }
    return cabeza;
}

void liberar_lista(t_nodo *cabeza)
{
    t_nodo *actual = cabeza;
    while (actual != NULL)
    {
        t_nodo *temp = actual->siguiente;
        free(actual);
        actual = temp;
    }
}
