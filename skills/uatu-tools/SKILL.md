---
name: uatu-tools
description: Use when auditing uatu proctoring telemetry of an exam submission (uatu-audit) or managing teacher keys and signed configuration (uatu-admin).
---

# uatu-tools — Validador forense y herramientas de cátedra de uatu (auditoría criptográfica Git-native de exámenes)

Herramientas de línea de comandos de [uatu](https://github.com/INGCOM-UNRN-P1/uatu), el sistema de proctorización y auditoría criptográfica Git-native para exámenes prácticos en VS Code.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/uatu-tools
```

## Opciones de `uatu-audit`

| Opción | Descripción |
|:--|:--|
| `--repo` | Ruta del repositorio de la entrega |
| `--teacher-key` | Clave pública Ed25519 docente (hex) o identificador del almacén. Por omisión $UATU_TEACHER_PUBLIC_KEY |
| `--decrypt-key` | Clave privada docente X25519 (ruta PEM) o identificador del almacén, para descifrar la evidencia |
| `--key-id` | Clave docente del almacén de uatu-admin: usa su pública para verificar y su privada para descifrar. Sin --teacher-key ni --key-id se intenta con el crypto.teacher_key_id del manifiesto |
| `--keys-dir` | Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys) |
| `--md-out` | Reporte Markdown de salida |
| `--json-out` | Reporte JSON opcional para integraciones |
| `--user` | Auditar solo las sesiones de este usuario de GitHub |
| `--remote` | Remoto donde buscar las ramas (por omisión git.remote_name) |
| `--max-paste-chars` | Umbral heurístico de pegado masivo |
| `--grace-seconds` | Tolerancia posterior al deadline_utc |
| `--code-ref` | Referencia de código a correlacionar con la telemetría |

## Opciones de `uatu-admin`

| Opción | Descripción |
|:--|:--|
| `--keys-dir` | Almacén de claves (por omisión $UATU_KEYS_DIR o ~/.config/uatu/keys) |

## Comandos de `uatu-admin`

| Comando | Descripción |
|:--|:--|
| `uatu-admin doctor` | Verifica los requisitos (Python, cryptography, git, gh) |
| `uatu-admin root-keygen` | Genera la clave raíz institucional en el almacén |
| `uatu-admin keygen` | Genera las claves Ed25519/X25519 de un docente en el almacén |
| `uatu-admin keys` | Gestiona el almacén de claves y las exporta donde se usan |
| `uatu-admin registry-add` | Agrega un docente al registro de claves |
| `uatu-admin registry-sign` | Firma el registro con la clave raíz |
| `uatu-admin verify-registry` | Verifica la firma raíz del registro |
| `uatu-admin sign-config` | Firma .uatu.conf |
| `uatu-admin verify-config` | Verifica la firma de .uatu.conf |
| `uatu-admin protect-branches` | Impide borrar o reescribir las ramas de telemetría (ruleset de GitHub) |

Ayuda de cada comando: `uatu-admin <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `uatu-audit doctor --json` · `uatu-admin doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
