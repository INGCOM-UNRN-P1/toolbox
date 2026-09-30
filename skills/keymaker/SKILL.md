---
name: keymaker
description: Use when encrypting, signing, verifying or splitting secrets for exam packages (.ripkg.enc) and managing the trust store.
---

# keymaker — Gestor de cifrado autenticado, integridad y desbloqueo temporal para paquetes de examen (.ripkg.enc)

Gestor de cifrado simétrico autenticado (AES-256-GCM / ChaCha20-Poly1305), firmas digitales Ed25519, Time-Lock y división de secretos de Shamir para paquetes de examen en C.

## Instalación

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/keymaker
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `keymaker encrypt`, `keymaker pack` | Empaqueta y cifra un examen o pauta en un bundle autenticado (.ripkg.enc). |
| `keymaker inspect` | Informa si un archivo está realmente cifrado por keymaker o viaja en claro. |
| `keymaker decrypt`, `keymaker unpack` | Descifra, verifica la integridad y extrae el contenido de un bundle (.ripkg.enc). |
| `keymaker gen-keys` | Genera un nuevo par de claves asimétricas Ed25519 para firma digital de exámenes. |
| `keymaker sign` | Firma un archivo con una clave privada Ed25519. |
| `keymaker verify` | Verifica la firma digital Ed25519 de un archivo consultando el Trust Store. |
| `keymaker split-secret` | Divide un secreto docente en N partes usando el esquema de Shamir (k de n). |
| `keymaker combine-shares` | Reconstruye un secreto a partir de K partes de Shamir. |
| `keymaker audit-passphrase` | Audita la entropía y robustez criptográfica de una frase de paso para exámenes. |
| `keymaker checksum` | Calcula el checksum SHA-256 de un archivo para control de integridad. |
| `keymaker doctor` | Ejecuta el diagnóstico integral del subsistema criptográfico. |
| `keymaker trust` | 🛡️ Gestión de claves públicas autorizadas y Lista de Revocación (CRL) en GitHub. |

Ayuda de cada comando: `keymaker <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `keymaker doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
