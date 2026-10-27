# construct

IDE pedagógico y orquestador de máquina virtual del perfil estudiante: en Windows, macOS y Linux
corre todas las herramientas de la cátedra dentro de una VM Debian acelerada por hardware (KVM,
WHPX o HVF), con la misma experiencia en las tres.

## 🎯 Propósito y Alcance

construct saca la configuración del sistema del alumno del camino: en el Host sólo hacen falta
QEMU, Git y uv; gcc, gdb, valgrind, bubblewrap, el perfil estudiante completo y las librerías
`treadstone`, `bitmaps` y `sonido` viven en la imagen de la VM. No reimplementa ninguna
herramienta: es el *frontend* de daedalus, ripley (gaff, spunkmeyer, kaneda), nostromo, tetsuo,
hal, bishop, treadstone y jonesy, y lleva sus hallazgos a un mismo panel. Suma la telemetría de la
ejecución (espera activa, deadlocks, archivos sin `fclose`, memoria sin liberar), la sincronización
Host ↔ VM con fusión de 3 vías y los artefactos `.bmp`/`.wav` del programa.

## 💻 Instalación y Requisitos

Corre en el Host del alumno, nunca dentro de la VM. Requiere QEMU (≥ 8.2), Git y la
aceleración por hardware del sistema; el README trae los pasos para cada uno.

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/construct
construct setup     # baja la imagen de la VM y dice qué falta, con el comando exacto
construct doctor    # el Host y, con la VM arriba, el mother doctor de adentro
```

## 🚀 Guía de Uso

```bash
construct ui                 # IDE en la terminal: editor, hallazgos, memoria, consola, pruebas
construct build | check | run | test   # F7, F8, F5, F6 desde la línea de comandos
construct run --tetsuo       # con AddressSanitizer y UBSan
construct jonesy main.c      # jonesy dentro de la VM, en esta terminal
construct sync               # sincronización Host ↔ VM y artefactos
```

Atajos, configuración (`project.toml`) y modo desarrollo están en el
[README](https://github.com/INGCOM-UNRN-P1/construct#readme).
