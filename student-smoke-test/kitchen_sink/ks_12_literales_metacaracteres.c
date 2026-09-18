#include <stdio.h>

/*
 * Literales de cadena y carácter cargados de metacaracteres que suelen
 * romper analizadores basados en regex ingenuas: comillas escapadas,
 * barras invertidas, secuencias de escape, y símbolos con significado
 * especial en regex/shell/Markdown (., *, +, ?, [, ], (, ), |, $, ^, %).
 */
int
main(void)
{
    char comillas[] = "una \"cadena\" con comillas escapadas";
    char barras[] = "C:\\ruta\\con\\barras\\invertidas\\\\dobles";
    char escapes[] = "tab\ty salto\ny nulo\\0 y pitido\a y retorno\r";
    char metacaracteres_regex[] = "a.*b+c?[d](e)|f$g^h%i#j";
    char comilla_simple = '\'';
    char barra_simple = '\\';
    char nueva_linea = '\n';
    char *concatenados = "primera parte " "segunda parte " "tercera parte";

    printf("%s %s %s %s %c %c %d %s\n",
           comillas, barras, escapes, metacaracteres_regex,
           comilla_simple, barra_simple, nueva_linea, concatenados);
    return 0;
}
