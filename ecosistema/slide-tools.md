# slide-tools

Sistema de control remoto y telemetría bidireccional para Google Slides desde dispositivos externos (Android y hardware embebido Wi-Fi).

## 🎯 Propósito y Alcance

`slide-tools` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para controlar presentaciones de Google Slides mediante un daemon concentrador WebSocket en `0.0.0.0:8766` y una extensión WebExtensions MV3. Permite sincronización de notas de orador, cronómetro, avance de diapositivas y emparejamiento por PIN de 4 dígitos.

## 💻 Instalación y Requisitos

```bash
uv tool install git+https://github.com/martinvilu/slides-tools
```

## 🚀 Guía de Uso

```bash
slide-tools --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/martinvilu/slides-tools#referencia-rápida), generada desde `slide-tools --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `slide-tools <comando> -h`.

## ⚙️ Configuración y Opciones

* `--port`: Puerto de escucha del daemon de presentación (default: 8766).
* `--pin`: Código PIN de 4 dígitos para autorizar el emparejamiento de clientes remotos.
* Subcomando `simulate`: Emula una presentación activa con notas y diapositivas de prueba.
