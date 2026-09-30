# mother

Instalador, actualizador y diagnóstico del ecosistema de herramientas de Programación 1.

## 🎯 Propósito y Alcance

`mother` instala, actualiza y diagnostica las herramientas del ecosistema **siempre desde git**
(varios nombres de paquete están tomados en PyPI por proyectos ajenos), por perfil: `estudiante`,
`analisis`, `docente`, `contenido` y `aula`. Lee el manifiesto único
[`ecosistema.toml`](../ecosistema.toml) y reemplaza a `clone_repos.sh`, `install_tools.sh` y
`health_check.sh`. No tiene dependencias: solo usa la biblioteca estándar de Python y `uv`.

## 💻 Instalación y Requisitos

Requiere Python ≥ 3.11 y `uv`.

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/mother
```

También se distribuye como un único archivo, `mother.pyz`, en los releases del repositorio.

## 🚀 Guía de Uso

```bash
mother instalar --perfil estudiante   # instala las herramientas del perfil desde git
mother doctor --perfil estudiante     # diagnóstico agregado: mother más el doctor de cada herramienta
mother versiones                      # versión instalada de cada herramienta
mother sistema --perfil analisis      # programas del sistema que hacen falta (gcc, gdb…)
```

La tabla completa de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/mother#referencia-rápida) (generada desde
`mother --help`).
