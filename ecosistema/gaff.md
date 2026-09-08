# gaff

Linter pedagógico de estilo arquitectónico y convenciones obligatorias de cátedra con autofix

## 🎯 Propósito y Alcance

`gaff` forma parte del ecosistema de herramientas de la cátedra de Programación 1. Provee mecanismos especializados para análisis, diagnóstico o evaluación pedagógica en C.

## 💻 Instalación y Requisitos

La herramienta se distribuye como un paquete estándar gestionado con `uv`:

```bash
uv tool install --editable /home/mrtin/dev/tools/gaff
```

## 🚀 Guía de Uso

### Invocación básica

```bash
gaff --help
```

### Salida de ayuda y comandos disponibles

```text
Usage: gaff [OPTIONS] COMMAND [ARGS]...                                        
                                                                                
 📏 GAFF — Linter pedagógico de estilo arquitectónico y convenciones            
 obligatorias de cátedra con autofix.                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --version             -v        Muestra la versión de GAFF.                  │
│ --install-completion            Install completion for the current shell.    │
│ --show-completion               Show completion for the current shell, to    │
│                                 copy it or customize the installation.       │
│ --help                          Show this message and exit.                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ check    Audita archivos de código C comprobando las reglas de estilo y      │
│          arquitectura de la cátedra.                                         │
│ fix      Aplica correcciones automáticas de estilo directamente sobre los    │
│          archivos.                                                           │
│ rules    Lista todas las reglas de estilo y arquitectura del catálogo de     │
│          GAFF.                                                               │
│ explain  Explica en detalle una regla de cátedra con ejemplos de código      │
│          correctos e incorrectos.                                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## ⚙️ Configuración y Opciones

`gaff` puede configurarse mediante parámetros de línea de comandos, variables de entorno o archivos de configuración locales del proyecto.

### Parámetros principales

* `--help`: Muestra la ayuda interactiva y las opciones disponibles.
* `--version`: Muestra la versión actual instalada de `gaff`.

## 📖 Documentación y Detalles Técnicos

# 📏 GAFF — Linter Pedagógico de Estilo y Arquitectura Cátedra

GAFF es un linter pedagógico de código C y cabeceras H diseñado para hacer cumplir de forma automatizada las convenciones de nomenclatura, diseño estructurado y arquitectura obligatorias de la cátedra de Programación en C.

## Reglas Principales

- **`0x0001h`**: Identificadores descriptivos (sin variables cortas no canónicas).
- **`0x0007h`**: Nombres de variables y funciones en `snake_case`.
- **`0x3004h`**: Nombres de `typedef` con prefijo `t_` o sufijo `_t`.
- **`0x2004h`**: Prohibición de variables globales mutables fuera de funciones.
- **`0x2005h`**: Longitud máxima de función $\le 50$ líneas.
- **`0x5003h`**: Guardas de inclusión obligatorias en cabeceras `.h` *(Autofix)*.
- **`0x300Dh`**: Prohibición de números mágicos sin constante definida.
- **`0x0004h`**: Espaciado correcto de palabras clave `if (`, `for (` *(Autofix)*.
- **`0x1006h`**: Prohibición de la sentencia `goto`.
- **`0x0009h`**: Longitud de línea $\le 100$ caracteres.
- **`0x0005h`**: Limpieza de trailing whitespace y tabuladores duros *(Autofix)*.

## Uso Rápido

```bash
# 1. Auditar archivos o directorios
gaff check src/ main.c

# 2. Auditar y aplicar correcciones automáticas
gaff check src/ --fix

# 3. Aplicar correcciones automáticas directamente
gaff fix src/

# 4. Salida estructurada JSON para CI/CD
gaff check src/ --json

# 5. Listar o explicar reglas del catálogo
gaff rules
gaff explain 0x0001h
```


## 📊 Formatos de Salida

`gaff` soporta diversos formatos de reporte:
* **Terminal interactiva / Rich:** Salida con colores, tablas y diagnósticos en español rioplatense.
* **Markdown / MyST:** Reportes legibles estructurados para integración en informes de corrección.
* **JSON:** Salida estructurada serializable para integración en pipelines automáticos.

---
*Cátedra de Programación 1 · UNRN Sede Andina*
