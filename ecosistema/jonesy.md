# jonesy

IDE de terminal para la cátedra de Programación I: un único binario en Rust (ratatui + crossterm)
para escribir, compilar, depurar y entregar C en el laboratorio, en un servidor por SSH o en el
examen, desde terminales de 80×24.

## 🎯 Propósito y Alcance

jonesy concentra en un editor el ciclo de trabajo del alumno: compilar y entender los errores de
gcc (unos 60, explicados en español), correr el programa en una terminal interna, depurar sobre
GDB/MI, revisar la memoria con valgrind (o AddressSanitizer donde no hay valgrind) y correr las
pruebas de `p1_test`. No reimplementa el análisis del ecosistema: ripley, gaff, kaneda y
spunkmeyer corren como plugins al guardar, y tetsuo, motoko y otras se ofrecen como acciones.

## 💻 Instalación y Requisitos

Es el único componente que no se instala con `uv tool` ni con mother (tipo `binario` en
[`ecosistema.toml`](../ecosistema.toml)): cada release del repositorio trae el binario para
Linux, Linux musl (estático) y Windows, con `SHA256SUMS`. Desde git, con Rust ≥ 1.85:

```bash
cargo install --locked --git https://github.com/INGCOM-UNRN-P1/jonesy jonesy-bin
```

En tiempo de ejecución usa lo que haya en el `PATH`: `gcc`/`make` para compilar, `gdb` para
depurar y, si están, `git`, `ripley` y `mem-trace`.

## 🚀 Guía de Uso

```bash
jonesy                    # proyecto en el directorio actual
jonesy lista.c lista.h    # archivos; la raíz es el ancestro con .jonesy.toml o .git
jonesy --exam             # modo examen
jonesy doctor             # ¿falta algo en el entorno?
```

Atajos, configuración, modo examen y telemetría están en el
[README](https://github.com/INGCOM-UNRN-P1/jonesy#readme).
