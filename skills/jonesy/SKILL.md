---
name: jonesy
description: Use when a student edits, compiles, runs, tests or debugs C in the terminal IDE jonesy (gcc errors explained in Spanish, GDB debugger, valgrind/ASan, p1_test), or when diagnosing its environment with jonesy doctor.
---

# jonesy — IDE de terminal para Programación I

IDE de terminal (un único binario en Rust) para escribir, compilar, depurar y entregar C en el laboratorio, por SSH o en el examen, desde terminales de 80×24. Explica en español los errores de gcc y del enlazador, corre el programa en una terminal interna, depura sobre GDB/MI, revisa la memoria con valgrind (o AddressSanitizer en Windows), corre las pruebas de `p1_test` y usa como plugins ripley, gaff, kaneda y spunkmeyer.

## Instalación

No se instala con `uv` ni con mother: se distribuye como binario en los releases del repositorio (Linux, Linux musl y Windows, con `SHA256SUMS`), o se compila desde git:

```bash
cargo install --locked --git https://github.com/INGCOM-UNRN-P1/jonesy jonesy-bin
```

Requiere en el `PATH` `gcc`/`make` para compilar y `gdb` para depurar; `git`, `ripley` y `mem-trace` son opcionales (si faltan, esas funciones se desactivan).

## Comandos

| Comando | Descripción |
|:--|:--|
| `jonesy [directorio \| archivos…]` | abre el proyecto (la raíz es el ancestro con `.jonesy.toml` o `.git`) |
| `jonesy --exam` | modo examen (también `JONESY_EXAM_MODE=1`) |
| `jonesy --simulacro [min]` | simulacro de examen con cronómetro, sin entregar |
| `jonesy doctor [--rapido] [--json]` | salud del entorno: compilar, depurar, memoria, git, terminal, proyecto y ecosistema |
| `jonesy reporte [--salida archivo.md]` | informe para reportar un problema de jonesy |
| `jonesy replay <telemetry.log> [--resumen \| --json]` | reproduce o resume la bitácora de una sesión |
| `jonesy verificar <telemetry.log \| entrega.tar>` | código 1 si la cadena de la bitácora está rota |
| `jonesy config exportar \| importar` | lleva las preferencias a otra máquina |

## Teclas del ciclo de trabajo

- **F6** compila (Makefile o gcc) y salta a los errores, explicados en español; **F1** muestra la explicación con un ejemplo «así no / así sí».
- **Ctrl+F5** corre el programa en la terminal interna; si se corta, **F5** lo depura hasta la línea donde falló.
- **Ctrl+F6** corre las pruebas (`make test` con `p1_test`, u otro framework que informe en SARIF) y deja cada fallo en su línea.
- **Depurar → Revisar memoria con valgrind** explica accesos inválidos, `free` doble y fugas en la línea del alumno.

## Cuándo usarla

- El alumno no entiende un error de compilación o un corte del programa: abrir el proyecto con `jonesy`, F6 y F1.
- Verificar que el entorno del laboratorio sirve antes de una práctica o examen: `jonesy doctor`.
- Para la verificación de la entrega, el alumno usa `ripley run` (jonesy lo corre al guardar).
