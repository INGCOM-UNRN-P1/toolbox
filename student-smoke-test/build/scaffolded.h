/**
 * @file data_structures.h
 * @brief [Descripción general del módulo data_structures.h]
 */

#ifndef DATA_STRUCTURES_H
#define DATA_STRUCTURES_H

#include <stddef.h>

/* Estructura con padding ineficiente para auditoría con BRETT */
/**
 * @brief [Descripción de typedef struct t_alumno_desordenado]
 */
typedef struct
{
    char flag_activo;          /* 1 byte + 7 bytes padding */
    double promedio_notas;     /* 8 bytes */
    char turno_letra;          /* 1 byte + 7 bytes padding -> Total: 24 B (Ahorro posible: 8 B) */
} t_alumno_desordenado;

/* Estructura con layout optimizado */
/**
 * @brief [Descripción de typedef struct t_alumno]
 */
typedef struct
{
    double promedio_notas;     /* 8 bytes */
    char flag_activo;          /* 1 byte */
    char turno_letra;          /* 1 byte + 6 bytes padding -> Total: 16 B */
} t_alumno;

/* Nodo para visualización de Heap y Punteros en BISHOP */
/**
 * @brief [Descripción de typedef struct t_nodo]
 */
typedef struct s_nodo
{
    int valor;
    struct s_nodo *siguiente;
} t_nodo;

/*@
  @ requires n >= 0 && n <= 12;
  @ ensures 
esult >= 1;
  @*/
/**
 * @brief [Descripción breve de la función calcular_factorial]
 *
 * @param n [Descripción del parámetro n]
 * @return [Descripción del valor de retorno]
 * @pre [Precondiciones / requisitos previos]
 * @post [Postcondiciones / estado resultante]
 */
int calcular_factorial(int n);

/* Función para evaluación de Jump Table O(1) en RACHEL */
/**
 * @brief [Descripción breve de la función procesar_comando]
 *
 * @param comando [Descripción del parámetro comando]
 * @return [Descripción del valor de retorno]
 * @pre [Precondiciones / requisitos previos]
 * @post [Postcondiciones / estado resultante]
 */
int procesar_comando(int comando);

/* Funciones dinámicas para inspección de memoria en BISHOP */
/**
 * @brief [Descripción breve de la función crear_nodo]
 *
 * @param valor [Descripción del parámetro valor]
 * @return [Descripción del valor de retorno]
 * @pre [Precondiciones / requisitos previos]
 * @post [Postcondiciones / estado resultante]
 */
t_nodo *crear_nodo(int valor);
/**
 * @brief [Descripción breve de la función crear_lista]
 *
 * @param cantidad [Descripción del parámetro cantidad]
 * @return [Descripción del valor de retorno]
 * @pre [Precondiciones / requisitos previos]
 * @post [Postcondiciones / estado resultante]
 */
t_nodo *crear_lista(int cantidad);
/**
 * @brief [Descripción breve de la función liberar_lista]
 *
 * @param cabeza [Descripción del parámetro cabeza]
 * @pre [Precondiciones / requisitos previos]
 * @post [Postcondiciones / estado resultante]
 */
void liberar_lista(t_nodo *cabeza);

#define CMD_OP_1 1
#define CMD_OP_2 2
#define CMD_OP_3 3
#define CMD_OP_4 4
#define CMD_OP_5 5
#define CMD_OP_6 6

#define CMD_RESP_1 100
#define CMD_RESP_2 200
#define CMD_RESP_3 300
#define CMD_RESP_4 400
#define CMD_RESP_5 500
#define CMD_RESP_6 600
#define FACTOR_VALOR 10

#endif /* DATA_STRUCTURES_H */
