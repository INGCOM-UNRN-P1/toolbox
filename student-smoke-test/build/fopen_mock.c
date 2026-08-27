// Mock para fopen() generado por HOLDEN
#include <stdio.h>

static int __holden_fopen_calls = 0;
static int __holden_fopen_fail_at = 2;

FILE* __real_fopen(const char* pathname, const char* mode);

FILE* __wrap_fopen(const char* pathname, const char* mode) {
    __holden_fopen_calls++;
    if (__holden_fopen_fail_at > 0 && __holden_fopen_calls >= __holden_fopen_fail_at) {
        return NULL; // Inyección de fallo de apertura de archivo
    }
    return __real_fopen(pathname, mode);
}
