---
name: hardboiled
description: Use when building, running or debugging bare-metal C programs on the RV32I microcontroller emulator (LEDs, switches, UART, timer).
---

# hardboiled — Emulador pedagógico RV32I bare-metal con depurador de código C, MMIO e interrupciones en una TUI

Emulador pedagógico de un microcontrolador **RISC-V 32 bits (RV32I) bare-metal** con depurador de código C en la terminal. Pensado para enseñar programación de bajo nivel, arquitectura de computadoras y sistemas embebidos: se ejecuta un programa C paso a paso, se inspeccionan registros y pila, y se interactúa con periféricos simulados (LEDs, switches, UART, timer con interrupciones).

## Instalación

```bash
uv tool install "hardboiled[zig] @ git+https://github.com/INGCOM-UNRN-P1/hardboiled"
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `hardboiled new` | crea un proyecto nuevo (main.c, Makefile, placa, editor) |
| `hardboiled build` | compila fuentes C a un ELF para la placa |
| `hardboiled run` | ejecuta un ELF en la TUI (o sin interfaz con --headless) |
| `hardboiled test` | ejecuta el programa con entradas dadas y compara la salida esperada |
| `hardboiled tutorial` | lecciones guiadas: LEDs, switches, UART, timer, ISR, depuración |
| `hardboiled examples` | lista, muestra o copia los ejemplos incluidos |
| `hardboiled demo` | compila y ejecuta un ejemplo (por defecto, la demo) |
| `hardboiled info` | muestra segmentos, símbolos y fuentes de un ELF |
| `hardboiled validate` | valida un board.toml (periféricos opcionales: `gpio` bidireccional, `adc` con potenciómetros y `bounce_cycles` en las entradas) |
| `hardboiled board` | crea o muestra placas (board.toml) |
| `hardboiled runtime` | imprime las rutas del runtime (include, linker script, crt0) |
| `hardboiled gen-header` | genera hardboiled.h (o el linker script) para una placa |
| `hardboiled config` | muestra o crea las preferencias del usuario |
| `hardboiled doctor` | verifica Python, emulador, runtime, compilador y terminal |
| `hardboiled explain` | explica una trampa o un aviso (sin tipo: la lista) |
| `hardboiled completion` | imprime el script de autocompletado de la shell |

Ayuda de cada comando: `hardboiled <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `hardboiled doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
