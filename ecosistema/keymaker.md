# keymaker

Gestor de cifrado e integridad de paquetes de examen para el ecosistema de cátedra.

## 🎯 Propósito y Alcance

`keymaker` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Gestiona cifrado simétrico autenticado (AES-256-GCM / ChaCha20-Poly1305), firmas digitales asimétricas Ed25519, Time-Lock, división de secretos de Shamir ($k$ de $n$) y verificación de claves autorizadas y listas de revocación (CRL).

## 💻 Instalación y Requisitos

```bash
uv tool install git+https://github.com/INGCOM-UNRN-P1/keymaker
```

## 🚀 Guía de Uso

```bash
keymaker --help
```

### Comandos disponibles

```text
Usage: keymaker [OPTIONS] COMMAND [ARGS]...                                    
                                                                                
 🔐 Keymaker — Gestor de cifrado simétrico autenticado (AES-GCM), firmas        
 Ed25519, Time-Lock y Trust Store.                                              
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de Keymaker y finaliza.   │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ encrypt           Empaqueta y cifra un examen o pauta en un bundle           │
│                   autenticado (.ripkg.enc).                                  │
│ pack              Empaqueta y cifra un examen o pauta en un bundle           │
│                   autenticado (.ripkg.enc).                                  │
│ decrypt           Descifra, verifica la integridad y extrae el contenido de  │
│                   un bundle (.ripkg.enc).                                    │
│ unpack            Descifra, verifica la integridad y extrae el contenido de  │
│                   un bundle (.ripkg.enc).                                    │
│ gen-keys          Genera un nuevo par de claves asimétricas Ed25519 para     │
│                   firma digital de exámenes.                                 │
│ sign              Firma un archivo con una clave privada Ed25519.            │
│ verify            Verifica la firma digital Ed25519 de un archivo            │
│                   consultando el Trust Store.                                │
│ split-secret      Divide un secreto docente en N partes usando el esquema de │
│                   Shamir (k de n).                                           │
│ combine-shares    Reconstruye un secreto a partir de K partes de Shamir.     │
│ audit-passphrase  Audita la entropía y robustez criptográfica de una frase   │
│                   de paso para exámenes.                                     │
│ checksum          Calcula el checksum SHA-256 de un archivo para control de  │
│                   integridad.                                                │
│ doctor            Ejecuta el diagnóstico integral del subsistema             │
│                   criptográfico.                                             │
│ trust             🛡️ Gestión de claves públicas autorizadas y Lista de       │
│                   Revocación (CRL) en GitHub.                                │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

* `keygen`: Genera pares de claves Ed25519 de cátedra.
* `encrypt`: Cifra paquetes de evaluación con sellado temporal o contraseñas seguras.
* `decrypt`: Descifra evaluaciones verificando firma y marcas de tiempo UTC.
* `sign`: Firma digitalmente enunciados o actas de calificación.
* `verify`: Comprueba la autenticidad e integridad criptográfica de archivos firmados.
