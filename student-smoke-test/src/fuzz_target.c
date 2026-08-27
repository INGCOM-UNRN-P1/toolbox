#include <stdio.h>
#include <stdlib.h>

int main(void) {
    char buffer[128];
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        long val = strtol(buffer, NULL, 10);
        if (val > 0 && val < 1000) {
            printf("Valor en rango procesado: %ld\n", val);
        } else {
            printf("Valor fuera de rango\n");
        }
    }
    return 0;
}
