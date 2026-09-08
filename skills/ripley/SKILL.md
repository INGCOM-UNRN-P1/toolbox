---
name: ripley
description: Use when performing static pedagogical analysis, checking cátedra P1 coding rules (0xXXXXh), translating GCC/linker errors to plain Spanish, or sandboxing and evaluating C code.
---

# Ripley — Motor de Verificación Pedagógica y Análisis Estático para C

## Overview
`ripley` es el motor pedagógico y CLI de verificación para código C universitario. Analiza el cumplimiento estricto de las reglas de cátedra P1 (códigos `0x0001h` - `0xEEEEh`), convenciones de estilo, nombres, números mágicos y complejidad ciclomática. Además, traduce errores crípticos del compilador GCC o del enlazador (`ld`) a explicaciones didácticas en español con recomendaciones de corrección, y provee sandboxing con compilación protegida (AddressSanitizer / UndefinedBehaviorSanitizer).

## Cuándo Usar
- Para evaluar la validez sintáctica, técnica y de estilo de un archivo o proyecto en C según las normas de cátedra (`ripley check`).
- Para obtener diagnósticos estructurados en formato JSON para integración en scripts o pipelines (`ripley analyze`).
- Para traducir errores crípticos de GCC a explicaciones en español orientadas a estudiantes (`ripley explain` o `ripley gcc-explain`).
- Para ejecutar un bucle interactivo de desarrollo guiado por pruebas (TDD) en C (`ripley watch`).
- Para verificar el estado de los compiladores, sanitizers y herramientas instaladas en el sistema (`ripley doctor`).

## Comandos CLI

### 1. Verificación de Código C (`check`)
```bash
# Verificar un archivo C individual
ripley check solucion.c

# Verificar proyecto completo en modo estricto
ripley check src/ --strict
```

### 2. Análisis Estructurado para Automatizaciones (`analyze`)
```bash
# Emitir diagnóstico completo en formato JSON
ripley analyze src/ --format json
```

### 3. Modo Live TDD (`watch`)
```bash
# Ejecutar verificación automática ante cualquier cambio guardado en archivos
ripley watch src/
```

### 4. Traductor Didáctico de Errores GCC (`explain` / `gcc-explain`)
```bash
# Traducir un mensaje o log de error directo
ripley explain "error: dereferencing pointer to incomplete type 'struct Node'"

# Pipear salida de compilación GCC directamente al traductor
gcc -Wall -Wextra main.c 2>&1 | ripley gcc-explain -
```

### 5. Inspección de Paquetes de Práctica (`show`)
```bash
# Inspección completa (metadatos, checks, consigna, pistas y testcases)
ripley show paquete.ripkg

# Control granular de secciones
ripley show paquete.ripkg -e           # Solo enunciado / consigna Markdown
ripley show paquete.ripkg -t           # Solo casos de prueba públicos
ripley show paquete.ripkg -p           # Solo pistas / pautas
ripley show paquete.ripkg -c           # Solo checks pedagógicos y reglas activas
ripley show paquete.ripkg -f           # Solo listado de archivos del payload e integridad SHA-256
ripley show paquete.ripkg -m           # Solo metadatos y flags de compilación
ripley show paquete.ripkg --todos --raw # Todo en texto plano sin formato Rich (para piping)
```

### 6. Ejecución contra Paquetes de Práctica (`run`)
```bash
# Verificar código del alumno contra un paquete de cátedra
ripley run solucion.c --practica paquete.ripkg
```

### 7. Diagnóstico del Entorno
```bash
# Comprobar compiladores instalados (gcc, clang), herramientas y sanitizers
ripley doctor
```

## Reglas de Cátedra Principales (Códigos P1)
- `0x0001h`: Prohibición de variables globales mutables.
- `0x0002h`: Declaración de prototipos de funciones faltantes.
- `0x0003h`: Uso de funciones prohibidas o inseguras (`gets`, `scanf` sin límite de buffer, `goto`).
- `0x0004h`: Números mágicos no parametrizados con `#define` o `enum`.
- `0x0005h`: Fugas de memoria o ausencia de `free` tras `malloc`/`calloc`.
- `0x0006h`: Violación de convenciones de nomenclatura (variables, funciones, constantes).
