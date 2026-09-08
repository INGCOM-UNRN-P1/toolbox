---
name: callahan
description: Use when verifying formal ACSL contracts (preconditions, postconditions, loop invariants) or deductive proof with Frama-C WP prover.
---

# CALLAHAN — Verificador Formal de Contratos ACSL en C

CALLAHAN realiza análisis y verificación deductiva de contratos formales en C (`/*@ requires ... ensures ... */`) integrándose con Frama-C WP y provers SMT.

## Comandos Principales

```bash
# Extraer contratos ACSL
callahan extract algoritmo.c

# Probar formalmente contratos con Frama-C WP
callahan verify algoritmo.c

# Salida estructurada JSON
callahan extract algoritmo.c --json
```
