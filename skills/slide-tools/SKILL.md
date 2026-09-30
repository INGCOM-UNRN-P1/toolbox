---
name: slide-tools
description: Use when remotely controlling Google Slides presentations (next/previous/go-to slide, blackout, laser, timer) through the browser extension and the local daemon, or packaging and signing that extension.
---

# slide-tools — Sistema de control remoto y telemetría para Google Slides mediante WebExtensions y daemon concentrador local/LAN

Sistema de control remoto y telemetría bidireccional para Google Slides desde dispositivos externos (aplicación nativa Android y hardware embebido Wi-Fi operando en simultáneo) mediante una extensión de navegador WebExtensions y un daemon concentrador local/LAN.

## Instalación

```bash
uv tool install git+https://github.com/martinvilu/slides-tools
```

## Comandos

| Comando | Descripción |
|:--|:--|
| `slide-tools daemon` | Inicia el daemon concentrador WebSocket en primer plano. |
| `slide-tools status` | Muestra el estado consolidado de la presentación activa. |
| `slide-tools next` | Avanza a la siguiente diapositiva o animación (NEXT_SLIDE). |
| `slide-tools prev` | Retrocede a la diapositiva o animación anterior (PREV_SLIDE). |
| `slide-tools first` | Salta a la primera diapositiva (FIRST_SLIDE). |
| `slide-tools last` | Salta a la última diapositiva (LAST_SLIDE). |
| `slide-tools goto` | Salta directamente a una diapositiva específica (GO_TO_SLIDE). |
| `slide-tools blackout` | Conmuta pantalla en negro (TOGGLE_BLACKOUT). |
| `slide-tools whiteout` | Conmuta pantalla en blanco (TOGGLE_WHITEOUT). |
| `slide-tools laser` | Conmuta puntero láser virtual (TOGGLE_LASER). |
| `slide-tools timer-reset` | Reinicia el temporizador (TIMER_RESET). |
| `slide-tools timer-pause` | Pausa o reanuda el temporizador (TIMER_TOGGLE_PAUSE). |
| `slide-tools monitor` | Monitorea en tiempo real cambios de diapositiva, notas y cronómetro. |
| `slide-tools mock-slides` | Simula una sesión de Google Slides conectada al daemon para pruebas. |
| `slide-tools pack` | Empaqueta la extensión WebExtensions para Chrome (.zip) y Firefox (.xpi). |
| `slide-tools sign` | Valida y firma digitalmente el addon para Firefox utilizando Mozilla web-ext. |
| `slide-tools qr` | Muestra el código QR para emparejamiento directo con la app Android. |
| `slide-tools doctor` | Verifica el estado del entorno de SLIDE-TOOLS (Python, web-ext opcional). |

Ayuda de cada comando: `slide-tools <comando> -h`.

Diagnóstico del entorno (JSON con `schema_version`): `slide-tools doctor --json`. Detalle y ejemplos: el `README.md` y el
`MANUAL.md` del repositorio.
