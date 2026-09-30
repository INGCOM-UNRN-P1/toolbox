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

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN-P1/keymaker#referencia-rápida), generada desde `keymaker --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `keymaker <comando> -h`.

## ⚙️ Configuración y Opciones

* `keygen`: Genera pares de claves Ed25519 de cátedra.
* `encrypt`: Cifra paquetes de evaluación con sellado temporal o contraseñas seguras.
* `decrypt`: Descifra evaluaciones verificando firma y marcas de tiempo UTC.
* `sign`: Firma digitalmente enunciados o actas de calificación.
* `verify`: Comprueba la autenticidad e integridad criptográfica de archivos firmados.
