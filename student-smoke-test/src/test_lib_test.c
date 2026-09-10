/**
 * @file test_lib_test.c
 * @brief Pruebas didácticas automatizadas para el smoke test integrando lib_test:
 *        - Aserciones de memoria con contadores y detección de fugas (ASSERT_NO_LEAKS)
 *        - Mocks de entrada/salida estándar (p1_stdio.h)
 *        - Manejo seguro de archivos temporales con limpieza automática (p1_files.h)
 *        - Pistas pedagógicas contextuales (ASSERT_*_HINT)
 *        - Emisión de reportes de evaluación en formato Markdown (--md-report)
 *
 * Cátedra de Programación 1 - Universidad Nacional de Río Negro
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "p1_test.h"
#include "p1_arrays.h"
#include "p1_files.h"
#include "p1_stdio.h"

/* 1. Gestión de memoria y aserciones de fugas (QoL 7) */
TEST(smoke_test_memoria_sin_fugas) {
    ASSERT_ALLOC_COUNT(0);
    ASSERT_FREE_COUNT(0);
    ASSERT_NO_LEAKS();

    void *ptr1 = p1_malloc(64);
    ASSERT_PTR_NOT_NULL(ptr1);
    ASSERT_ALLOC_COUNT(1);
    ASSERT_FREE_COUNT(0);

    void *ptr2 = p1_calloc(8, sizeof(int));
    ASSERT_PTR_NOT_NULL(ptr2);
    ASSERT_ALLOC_COUNT(2);

    void *ptr3 = p1_realloc(ptr1, 128);
    ASSERT_PTR_NOT_NULL(ptr3);
    ASSERT_ALLOC_COUNT(3);
    ASSERT_FREE_COUNT(1);

    p1_free(ptr2);
    p1_free(ptr3);
    ASSERT_FREE_COUNT(3);
    ASSERT_NO_LEAKS();
}

/* 2. Redirección y mocks de E/S estándar (QoL 8) */
static void imprimir_saludo(void) {
    printf("Bienvenido al entorno de evaluación de Programación 1.\n");
}

TEST(smoke_test_mocks_stdio) {
    ASSERT_STDOUT_CONTAINS(imprimir_saludo(), "Programación 1");

    p1_mock_stdin_feed("9876\n");
    int num = 0;
    int ret = scanf("%d\n", &num);
    ASSERT_INT_EQ(1, ret);
    ASSERT_INT_EQ(9876, num);
    ASSERT_STDIN_CONSUMED();
    p1_mock_stdin_restore();
}

/* 3. Archivos temporales con aislamiento y borrado automático (QoL 9) */
TEST(smoke_test_archivos_temporales) {
    const char *contenido = "clave=42\nparametro=prueba_smoke";
    const char *ruta = p1_temp_file_create(contenido);
    ASSERT_PTR_NOT_NULL(ruta);

    FILE *f = fopen(ruta, "r");
    ASSERT_PTR_NOT_NULL(f);

    char buffer[128] = {0};
    size_t leidos = fread(buffer, 1, sizeof(buffer) - 1, f);
    fclose(f);

    ASSERT_TRUE(leidos > 0);
    ASSERT_STR_EQ(contenido, buffer);
}

/* 4. Pistas pedagógicas orientativas (QoL 4) */
TEST(smoke_test_pistas_pedagogicas) {
    int valor = 100;
    ASSERT_INT_EQ_HINT(100, valor, "El valor debe inicializarse en 100.");
    ASSERT_TRUE_HINT(valor > 50, "El valor debe ser superior al umbral mínimo de 50.");
}

/* 5. Aserciones básicas y de arreglos */
TEST(smoke_test_aserciones_basicas) {
    int esperados[] = {10, 20, 30, 40};
    int obtenidos[] = {10, 20, 30, 40};

    ASSERT_ARRAY_INT_EQ(esperados, obtenidos, 4);
    ASSERT_STR_EQ("UNRN", "UNRN");
    ASSERT_DOUBLE_EQ(3.1415, 3.14159, 0.001);
}

int main(int argc, char **argv) {
    TEST_SUITE_BEGIN_ARGS("Suite de Smoke Test: Verificación de p1_test y Mejoras QoL", argc, argv);

    RUN_TEST(smoke_test_memoria_sin_fugas);
    RUN_TEST(smoke_test_mocks_stdio);
    RUN_TEST(smoke_test_archivos_temporales);
    RUN_TEST(smoke_test_pistas_pedagogicas);
    RUN_TEST(smoke_test_aserciones_basicas);

    return TEST_REPORT();
}
