# hardboiled

Emulador pedagógico de un microcontrolador RISC-V de 32 bits (RV32I) bare-metal, con depurador de
código C en la terminal.

## 🎯 Propósito y Alcance

`hardboiled` permite ejecutar un programa C paso a paso sobre un microcontrolador emulado,
inspeccionar registros y pila, e interactuar con periféricos simulados (LEDs, switches, UART,
timer con interrupciones). Está pensado para programación de bajo nivel, arquitectura de
computadoras y sistemas embebidos: la CPU se emula con Unicorn Engine, así que el programa nunca
toca recursos del host, y la depuración es a nivel de fuente con la información DWARF del ELF.

Pertenece al perfil `contenido` del manifiesto (`ecosistema.toml`). Usa argparse en lugar de
Typer y tiene su propio sistema de idiomas (español por defecto, inglés con `HARDBOILED_LANG=en`).

## 💻 Instalación y Requisitos

Requiere Python 3.12+ y `uv`. No se publica en PyPI: se instala siempre desde el repositorio.

```bash
# herramienta + compilador C para RV32I (zig)
uv tool install "hardboiled[zig] @ git+https://github.com/INGCOM-UNRN-P1/hardboiled"
# sólo la herramienta (si ya tenés riscv*-gcc)
uv tool install git+https://github.com/INGCOM-UNRN-P1/hardboiled
```

## 🚀 Guía de Uso

```bash
hardboiled new mi-tp            # main.c, Makefile, board.toml y compile_flags.txt
cd mi-tp && hardboiled run main.c   # compila y lo ejecuta en la TUI (o --headless)
hardboiled build programa.c     # sólo compilar: programa.elf
hardboiled doctor               # verifica Python, emulador, runtime, compilador y terminal
```

La tabla completa de comandos está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/hardboiled#referencia-rápida) (generada desde
`hardboiled --help`); la guía detallada, en su
[manual](https://github.com/INGCOM-UNRN-P1/hardboiled/blob/main/MANUAL.md).
