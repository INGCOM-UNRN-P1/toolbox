/* Código vulnerable a boundary inputs y desbordamiento en enteros extremos */
#include <stdio.h>
#include <limits.h>

void test_target(int x) {
    if (x == INT_MAX) {
        int *p = NULL;
        *p = 1; /* Crash deliberado en INT_MAX */
    }
}

int main(void) {
    int val = 0;
    if (scanf("%d", &val) == 1) {
        test_target(val);
    }
    return 0;
}
