---
name: mother
description: Use when installing, updating or diagnosing the P1 ecosystem tools by profile (always from git), checking installed versions or the command-line contract of what is installed.
---

# mother — Instalador, actualizador y diagnóstico del ecosistema de herramientas de Programación 1 (siempre desde git)

Instala, actualiza y diagnostica las herramientas del ecosistema **siempre desde git** (varios nombres de paquete están tomados en PyPI por proyectos ajenos). Lee el manifiesto único `ecosistema.toml` de p1-tools y reemplaza a `clone_repos.sh`, `install_tools.sh` y `health_check.sh`. No tiene dependencias y también se distribuye como un único archivo, `mother.pyz` (`python3 mother.pyz instalar --perfil estudiante`).

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/mother
```

## Opciones de `mother`

| Opción | Descripción |
|:--|:--|
| `--manifiesto` | ruta o URL de ecosistema.toml (por defecto, el publicado en p1-tools) |
| `--sin-red` | no descargar el manifiesto: usar la caché o la copia incluida |

## Comandos

| Comando | Descripción |
|:--|:--|
| `mother listar` | herramientas del manifiesto y si están instaladas |
| `mother instalar` | instala las herramientas de un perfil desde git |
| `mother actualizar` | actualiza las herramientas instaladas |
| `mother doctor` | diagnóstico agregado: mother más el doctor de cada herramienta |
| `mother versiones` | versión instalada de cada herramienta |
| `mother autoprueba` | verifica el contrato de línea de comandos de lo instalado |
| `mother sistema` | programas del sistema que necesita un perfil (gcc, gdb…) |

Ayuda de cada comando: `mother <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `mother doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
