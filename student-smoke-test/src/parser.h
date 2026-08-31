#ifndef PARSER_H
#define PARSER_H

#define BASE_DECIMAL 10
#define ERR_PARAM_INVALIDO -1
#define ERR_NUMERO_INVALIDO -2
#define ERR_FUERA_DE_RANGO -3

int parsear_entero_seguro(const char *str, int *out_valor);

#endif /* PARSER_H */
