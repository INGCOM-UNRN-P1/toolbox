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

### Comandos disponibles

```text
Usage: scorm-tools [OPTIONS] COMMAND [ARGS]...                                 
                                                                                
 Herramientas para crear, empaquetar y validar contenido SCORM compatible con   
 Moodle.                                                                        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -V        Muestra la versión de scorm-tools y sale.    │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ doctor            Verificá el estado del entorno, dependencias y esquemas    │
│                   XSD de scorm-tools.                                        │
│ init              Creá un curso SCORM de ejemplo listo para editar.          │
│ build             Generá imsmanifest.xml y empaquetá el curso en un .zip     │
│                   para Moodle.                                               │
│ validate          Validá un paquete SCORM contra el esquema XSD y reglas de  │
│                   Moodle.                                                    │
│ info              Mostrá un resumen de la estructura del curso definida en   │
│                   scorm.yaml.                                                │
│ check-sequencing  Verificá el grafo de secuenciamiento IMSSS y detectá       │
│                   ciclos o actividades huérfanas.                            │
│ check-size        Audita el peso del paquete y su desglose por tipo de       │
│                   contenido para Moodle.                                     │
│ moodle-config     Generá la configuración recomendada de actividad Moodle    │
│                   (moodle_settings.json).                                    │
│ from-deckard      Convertí una guía de ejercicios de Deckard a un curso      │
│                   SCORM interactivo.                                         │
│ from-gift         Convertí un banco de preguntas GIFT (Moodle) en un módulo  │
│                   SCORM interactivo autoevaluable.                           │
│ audit-c           Auditá fragmentos de código C embebidos en el contenido    │
│                   SCORM contra reglas Ripley.                                │
│ dredd-sync        Procesá registros de tracking de Moodle SCORM para         │
│                   integrarlos al calificador docente Dredd.                  │
│ diagram-memory    Generá un diagrama Mermaid de memoria Stack y Heap         │
│                   (Bishop/Sebastian) para lecciones SCORM.                   │
│ from-idkfa        Convertí una plantilla de tracing C de IDKFA a una lección │
│                   interactiva SCORM autoevaluable.                           │
│ playground        Generá un módulo SCORM interactivo con compilador C        │
│                   WebAssembly en el navegador.                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

* `init`: Genera la estructura de un nuevo paquete SCORM a partir de plantillas declarativas.
* `validate`: Valida un paquete contra los esquemas XSD de SCORM 1.2 o 2004 4th Edition.
* `build`: Empaqueta los contenidos interactivos en un archivo `.zip` listo para importar en Moodle.
