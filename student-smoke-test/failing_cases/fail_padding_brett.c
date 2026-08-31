#include <stddef.h>

typedef struct {
    char a;       /* offset 0, 7 bytes padding */
    double b;     /* offset 8 */
    char c;       /* offset 16, 7 bytes padding */
    long d;       /* offset 24 */
    char e;       /* offset 32, 7 bytes padding */
} ineficiente_t;
