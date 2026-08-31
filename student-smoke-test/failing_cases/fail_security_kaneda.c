/* Archivo C con vulnerabilidades críticas deliberadas para Kaneda */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void vulnerabilidad_critica(char *entrada_usuario) {
    char buffer[16];
    gets(buffer); /* Vulnerabilidad gets (0x5001h) */
    strcpy(buffer, entrada_usuario); /* Buffer overflow potencial (0x5002h) */
    sprintf(buffer, "%s", entrada_usuario); /* sprintf no seguro (0x5003h) */
    printf(entrada_usuario); /* Format string vulnerability (0x5004h) */
    system("ls -la /"); /* Inyección de comandos (0x5005h) */
}

int main(void) {
    char data[64] = "test";
    vulnerabilidad_critica(data);
    return 0;
}
