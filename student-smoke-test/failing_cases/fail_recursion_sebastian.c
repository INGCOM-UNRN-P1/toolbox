/* Recursión descontrolada que provoca Stack Overflow */
#include <stdio.h>

int recursion_infinita(int n) {
    /* Sin caso base */
    return recursion_infinita(n + 1) + 1;
}

int main(void) {
    return recursion_infinita(0);
}
