# uatu-tools

Herramientas de línea de comandos de [uatu](https://github.com/INGCOM-UNRN-P1/uatu), el sistema
de proctorización y auditoría criptográfica Git-native para exámenes prácticos en VS Code.

## 🎯 Propósito y Alcance

- `uatu-audit`: validador forense para el CI. Audita las ramas `uatu-audit/<usuario>/<sesión>`
  de una entrega (firmas Ed25519, cadena de hashes, micro-lotes, bloque génesis y ventana
  temporal), aplica heurísticas (pegados masivos, configuración del editor) y descifra los
  pegados con la clave docente. Códigos de salida: 0 íntegro, 1 falla de integridad, 2 alertas.
- `uatu-admin`: herramientas de cátedra: almacén de claves, registro público de claves docentes,
  firma de `.uatu.conf`, secretos de GitHub Actions y protección de las ramas de telemetría.

Pertenece a los perfiles `docente` y `aula` del manifiesto (`ecosistema.toml`). Su única
dependencia es `cryptography` y `audit.py` es autocontenido (PEP 723): también se puede copiar a
un repositorio y ejecutar con `uv run audit.py`.

## 💻 Instalación y Requisitos

Requiere `uv` y Python 3.9+.

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/uatu-tools
```

## 🚀 Guía de Uso

```bash
uatu-admin doctor               # requisitos (Python, cryptography, git, gh)
uatu-admin keygen --key-id docente-2026
uatu-audit --repo entrega/ --key-id docente-2026 --md-out informe.md
```

Las opciones y comandos completos están en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/uatu-tools#referencia-rápida) (generada desde
`--help`) y en su [manual de referencia](https://github.com/INGCOM-UNRN-P1/uatu-tools/blob/main/manual/index.md).
