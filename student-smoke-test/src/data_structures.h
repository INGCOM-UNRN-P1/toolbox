#ifndef DATA_STRUCTURES_H
#define DATA_STRUCTURES_H

#include <stddef.h>

/* Estructura con padding ineficiente para auditoría con BRETT */
typedef struct
{
    char flag_activo;          /* 1 byte + 7 bytes padding */
    double promedio_notas;     /* 8 bytes */
    char turno_letra;          /* 1 byte + 7 bytes padding -> Total: 24 B (Ahorro posible: 8 B) */
} t_alumno_desordenado;

/* Estructura con layout optimizado */
typedef struct
{
    double promedio_notas;     /* 8 bytes */
    char flag_activo;          /* 1 byte */
    char turno_letra;          /* 1 byte + 6 bytes padding -> Total: 16 B */
} t_alumno;

/* Nodo para visualización de Heap y Punteros en BISHOP */
typedef struct s_nodo
{
    int valor;
    struct s_nodo *siguiente;
} t_nodo;

/*@
  @ requires n >= 0 && n <= 12;
  @ ensures \result >= 1;
  @*/
int calcular_factorial(int n);

/* Función para evaluación de Jump Table O(1) en RACHEL */
int procesar_comando(int comando);

/* Funciones dinámicas para inspección de memoria en BISHOP */
t_nodo *crear_nodo(int valor);
t_nodo *crear_lista(int cantidad);
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
