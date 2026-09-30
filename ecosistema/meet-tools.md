# meet-tools

Sistema de control y monitoreo bidireccional para Google Meet desde dispositivos externos (apps móviles Android y hardware embebido Wi-Fi).

## 🎯 Propósito y Alcance

`meet-tools` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para enlazar Google Meet mediante WebExtensions MV3 y un concentrador WebSocket local/LAN en `0.0.0.0:8765`, permitiendo telemetría en tiempo real (micrófono, cámara, manos levantadas, sala de espera) y control remoto seguro con Single-Session Lock.

## 💻 Instalación y Requisitos

```bash
uv tool install git+https://github.com/martinvilu/meet-tools
```

## 🚀 Guía de Uso

```bash
meet-tools --help
```

### Comandos disponibles

```text

```

## ⚙️ Configuración y Opciones

* `--port`: Puerto de escucha del concentrador WebSocket (default: 8765).
* `--host`: Interfaz de red de escucha (default: 0.0.0.0 para LAN y loopback).
* Subcomando `simulate`: Simula una pestaña de Google Meet para pruebas desatendidas y testing sin navegador.
