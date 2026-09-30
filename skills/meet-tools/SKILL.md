---
name: meet-tools
description: Use when remotely controlling Google Meet (microphone, camera, raised hand, admit or mute everyone, leave) through the browser extension and the local daemon, or packaging and signing that extension.
---

# meet-tools — Sistema de control y monitoreo externo para Google Meet mediante WebExtensions y daemon concentrador

Sistema de control y monitoreo bidireccional para Google Meet desde dispositivos externos (apps móviles Android y hardware embebido Wi-Fi) mediante una extensión de navegador WebExtensions y un daemon concentrador local/LAN.

## Instalación

```bash
uv tool install git+https://github.com/martinvilu/meet-tools
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `meet-tools daemon` | Inicia el daemon concentrador WebSocket en primer plano. |
| `meet-tools status` | Consulta y muestra el estado actual consolidado de la sesión de Google Meet. |
| `meet-tools mic` | Conmuta el micrófono propio (TOGGLE_MIC). |
| `meet-tools cam` | Conmuta la cámara propia (TOGGLE_CAM). |
| `meet-tools hand` | Conmuta levantar/bajar la mano (TOGGLE_HAND). |
| `meet-tools admit-all` | Acciona 'Admitir a todos' en la sala de espera (ADMIT_ALL). |
| `meet-tools mute-all` | Acciona 'Silenciar a todos' los participantes (MUTE_ALL). |
| `meet-tools leave` | Abandona la reunión (LEAVE_CALL). |
| `meet-tools monitor` | Escucha y muestra en tiempo real todos los eventos y telemetría de Meet. |
| `meet-tools mock-tab` | Simula una pestaña de Google Meet con la extensión para pruebas locales. |
| `meet-tools pack` | Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi). |
| `meet-tools sign` | Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext. |
| `meet-tools qr` | Muestra el código QR para emparejamiento directo con la app Android. |
| `meet-tools doctor` | Verifica el estado del entorno de MEET-TOOLS (Python, web-ext opcional). |

Ayuda de cada comando: `meet-tools <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `meet-tools doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
