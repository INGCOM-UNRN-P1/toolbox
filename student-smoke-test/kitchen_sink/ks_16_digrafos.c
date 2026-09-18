/*
 * Dígrafos de C95: <: :> equivalen a [ ] ; <% %> equivalen a { } ; %:
 * equivale a #. Menos agresivos que los trigrafos pero igual de raros
 * de encontrar en código real (a veces aparecen por teclados con
 * layouts sin ciertos símbolos, o por copiar/pegar de fuentes viejas).
 */
%:include <stdio.h>

int
main(void)
<%
    int vector<:3:> = <% 1, 2, 3 %>;
    printf("%d\n", vector<:0:>);
    return 0;
%>
