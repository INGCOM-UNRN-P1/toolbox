# scorm-tools

Empaquetador y validador de paquetes de aprendizaje interactivo SCORM 1.2 / 2004 para Moodle.

## 🎯 Propósito y Alcance

`scorm-tools` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee validación formal contra esquemas XSD oficiales, scaffolding de lecciones interactivas, empaquetado directo en formato ZIP compatible con Moodle y arnés de emulación de runtime.

## 💻 Instalación y Requisitos

```bash
uv tool install "scorm-tools[ecosistema] @ git+https://github.com/INGCOM-UNRN/scorm-tools"
```

## 🚀 Guía de Uso

```bash
scorm-tools --help
```

### Comandos

La tabla de comandos y opciones está en la **Referencia rápida** del
[README](https://github.com/INGCOM-UNRN/scorm-tools#referencia-rápida), generada desde `scorm-tools --help` y verificada en el CI
para que no quede desactualizada. La ayuda de cada comando: `scorm-tools <comando> -h`.

## ⚙️ Configuración y Opciones

* `init`: Genera la estructura de un nuevo paquete SCORM a partir de plantillas declarativas.
* `validate`: Valida un paquete contra los esquemas XSD de SCORM 1.2 o 2004 4th Edition.
* `build`: Empaqueta los contenidos interactivos en un archivo `.zip` listo para importar en Moodle.
