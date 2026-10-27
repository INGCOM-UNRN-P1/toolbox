---
name: construct
description: Use when a student works through construct (the course IDE and hardware-accelerated VM on Windows, macOS or Linux): setting it up, diagnosing the host with construct doctor, compiling, auditing, running, testing or debugging C inside the VM, syncing files, or opening jonesy in it.
---

# construct — IDE y máquina virtual del perfil estudiante

Corre todas las herramientas de la cátedra dentro de una VM Debian acelerada (KVM en Linux, WHPX en Windows, HVF en macOS) y las muestra en un IDE de terminal. En el Host sólo hacen falta QEMU, Git y uv: gcc, gdb y el perfil estudiante están en la imagen.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/construct
construct setup     # carpetas, diagnóstico con el comando exacto para cada sistema y descarga de la imagen
construct doctor    # todo en verde: listo (con la VM arriba, también el mother doctor de adentro)
```

Lo que falte en el Host (QEMU, Git, la plataforma del hipervisor de Windows, el grupo `kvm` en Linux) lo indica `construct doctor` con el comando exacto.

## Comandos

| Comando | Descripción |
|:--|:--|
| `construct ui` | IDE de cuatro paneles: editor con hallazgos, memoria de bishop y artefactos, hallazgos con «Explicar», consola, pruebas y recursos |
| `construct build` / `check` / `fix` | daedalus (F7), ripley (F8) y el autofix de gaff, con rutas del Host |
| `construct run [--tetsuo \| --aislado]` | F5: ejecuta con telemetría; ante un crash, hal explica la causa |
| `construct test` | F6: suites de treadstone (`tests/test_*.c`) |
| `construct jonesy [archivo]` | jonesy dentro de la VM, en esta terminal; al salir, lo editado vuelve al Host |
| `construct sync [subir \| bajar \| artefactos \| estado]` | sincronización con fusión de 3 vías; artefactos en `.construct/artefactos/` |
| `construct vm start \| stop \| status \| exec` | la máquina virtual (arranca sola con cualquier comando) |

## Cuándo usarla

- El alumno no puede instalar gcc/gdb/valgrind en su sistema, o su sistema da resultados distintos al del laboratorio: `construct setup` y `construct ui`.
- Diagnosticar por qué no anda: `construct doctor` (y `construct doctor --json` para adjuntarlo a un reporte).
- Un programa se corta, pierde memoria o deja archivos abiertos: `construct run` (hal y la telemetría lo explican en su línea).
