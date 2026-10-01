---
name: gaff
description: Use when linting, validating, or auto-fixing C source code against strict cátedra architectural and style conventions (naming, typedefs, globals, line/function length, header guards, keywords spacing).
---

# GAFF — Linter Pedagógico de Estilo y Arquitectura de Cátedra

GAFF audita código C y cabeceras H para garantizar el cumplimiento estricto de las convenciones arquitectónicas obligatorias de la cátedra de Programación en C.

## Reglas Principales

- **`GAFF001`**: Nombres de variables y funciones en `snake_case`.
- **`GAFF002`**: Nombres de `typedef` con prefijo `t_` o sufijo `_t`.
- **`GAFF003`**: Prohibición de variables globales mutables fuera de funciones.
- **`GAFF004`**: Longitud máxima de función $\le 50$ líneas.
- **`GAFF005`**: Guardas de inclusión obligatorias en cabeceras `.h` *(Autofix)*.
- **`GAFF006`**: Prohibición de números mágicos sin constante definida.
- **`GAFF007`**: Espaciado de palabras clave `if (`, `for (`, `while (` *(Autofix)*.
- **`GAFF008`**: Prohibición de la sentencia `goto`.
- **`GAFF009`**: Longitud de línea $\le 100$ caracteres.
- **`GAFF010`**: Limpieza de trailing whitespace y tabuladores duros *(Autofix)*.

## Comandos Principales

```bash
# 1. Auditar archivos o directorios
gaff check src/ main.c

# 2. Auditar y aplicar correcciones automáticas
gaff check src/ --fix

# 3. Aplicar correcciones automáticas directamente
gaff fix src/

# 4. Salida estructurada JSON para CI/CD
gaff check src/ --json

# 5. Listar o explicar reglas del catálogo
gaff rules
gaff explain GAFF001

# 6. Equivalencias sintácticas: a[i] ≡ *(a + i), p->x ≡ (*p).x, for ≡ while…
gaff explain-syntax main.c
gaff explain-syntax --code 'p->sig->v[i] -= 1;'
```
