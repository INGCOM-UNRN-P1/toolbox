# slide-tools

Sistema de control remoto y telemetría bidireccional para Google Slides desde dispositivos externos (Android y hardware embebido Wi-Fi).

## 🎯 Propósito y Alcance

`slide-tools` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para controlar presentaciones de Google Slides mediante un daemon concentrador WebSocket en `0.0.0.0:8766` y una extensión WebExtensions MV3. Permite sincronización de notas de orador, cronómetro, avance de diapositivas y emparejamiento por PIN de 4 dígitos.

## 💻 Instalación y Requisitos

```bash
uv tool install --editable /home/mrtin/dev/tools/slide-tools
```

## 🚀 Guía de Uso

```bash
slide-tools --help
```

### Comandos disponibles

```text
Usage: slide-tools [OPTIONS] COMMAND [ARGS]...                                 
                                                                                
 Sistema de control remoto para Google Slides.                                  
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ daemon       Inicia el daemon concentrador WebSocket en primer plano.        │
│ status       Muestra el estado consolidado de la presentación activa.        │
│ next         Avanza a la siguiente diapositiva o animación (NEXT_SLIDE).     │
│ prev         Retrocede a la diapositiva o animación anterior (PREV_SLIDE).   │
│ first        Salta a la primera diapositiva (FIRST_SLIDE).                   │
│ last         Salta a la última diapositiva (LAST_SLIDE).                     │
│ goto         Salta directamente a una diapositiva específica (GO_TO_SLIDE).  │
│ blackout     Conmuta pantalla en negro (TOGGLE_BLACKOUT).                    │
│ whiteout     Conmuta pantalla en blanco (TOGGLE_WHITEOUT).                   │
│ laser        Conmuta puntero láser virtual (TOGGLE_LASER).                   │
│ timer-reset  Reinicia el temporizador (TIMER_RESET).                         │
│ timer-pause  Pausa o reanuda el temporizador (TIMER_TOGGLE_PAUSE).           │
│ monitor      Monitorea en tiempo real cambios de diapositiva, notas y        │
│              cronómetro.                                                     │
│ mock-slides  Simula una sesión de Google Slides conectada al daemon para     │
│              pruebas.                                                        │
│ pack         Empaqueta la extensión WebExtensions para Chrome (.zip) y       │
│              Firefox (.xpi).                                                 │
│ sign         Valida y firma digitalmente el addon para Firefox utilizando    │
│              Mozilla web-ext.                                                │
│ qr           Muestra el código QR para emparejamiento directo con la app     │
│              Android.                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

* `--port`: Puerto de escucha del daemon de presentación (default: 8766).
* `--pin`: Código PIN de 4 dígitos para autorizar el emparejamiento de clientes remotos.
* Subcomando `simulate`: Emula una presentación activa con notas y diapositivas de prueba.
