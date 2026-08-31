/* Contratos ACSL violados deliberadamente */

/*@ requires x > 0;
  @ ensures \result < 0;
  @*/
int funcion_contrato_falso(int x) {
    /* Retorna positivo violando el postcondición \result < 0 */
    return x * 2;
}
