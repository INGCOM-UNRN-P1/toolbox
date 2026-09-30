#!/usr/bin/env python3
"""Bloque generado de los README: requisitos por sistema operativo y tabla de comandos (N-ECO-09).

Cada README de una herramienta activa lleva, entre las marcas
`<!-- p1:referencia:inicio -->` y `<!-- p1:referencia:fin -->`, un bloque que
se genera desde ecosistema.toml (programas del sistema que necesita) y desde
`<ejecutable> --help` (sus comandos, con la ayuda en inglés o en español).
Así la tabla de comandos no deriva: `verificar` falla si algún README quedó
desactualizado. Lo demás del README (propósito, ejemplos, instalación) se
escribe a mano; la instalación ya la controla verificar_docs_instalacion.py.

Uso:
    readme_generado.py actualizar [--raiz DIR] [HERRAMIENTA ...]
    readme_generado.py verificar  [--raiz DIR] [HERRAMIENTA ...]

Sin herramientas recorre las cli activas del manifiesto instaladas en el PATH.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

from ecosistema import Repo, cargar, filtrar  # scripts/ecosistema.py (misma carpeta)

INICIO = "<!-- p1:referencia:inicio — generado por p1-tools/scripts/readme_generado.py: no editar a mano -->"
FIN = "<!-- p1:referencia:fin -->"
RE_BLOQUE = re.compile(r"<!-- p1:referencia:inicio[^\n]*-->\n.*?<!-- p1:referencia:fin -->\n?", re.DOTALL)
RE_PANEL_COMANDOS = re.compile(r"\b(?:Commands|Comandos)\b")
RE_PANEL_OPCIONES = re.compile(r"╭─ (?:Options|Opciones) ─")
OPCIONES_ESTANDAR = {"--help", "--version", "--install-completion", "--show-completion"}
RE_FILA = re.compile(r"^│ ([a-z][a-z0-9-]*)\s+(.*?)\s*│?$")
RE_CONTINUACION = re.compile(r"^│\s{2,}(\S.*?)\s*│?$")
# Ayuda de argparse (hardboiled, uatu-tools): los subcomandos van después de la línea con las
# opciones entre llaves y las opciones de la raíz bajo «opciones:» (u «options:» en inglés).
# La línea de los subcomandos: sus nombres entre llaves o, con metavar (mother), p. ej. COMANDO.
RE_ARGPARSE_ELECCION = re.compile(r"^  (?:\{[^}]*\}|[A-ZÁÉÍÓÚÑ_]+)\s*$")
RE_ARGPARSE_COMANDO = re.compile(r"^    ([a-z][a-z0-9-]*)(?:\s{2,}(\S.*?))?\s*$")
RE_ARGPARSE_OPCIONES = re.compile(r"^(?:opciones|options|optional arguments):$")
RE_ARGPARSE_OPCION = re.compile(r"^  (-\S.*?)(?:\s{2,}(\S.*?))?\s*$")
RE_ARGPARSE_CONTINUACION = re.compile(r"^\s{6,}(\S.*?)\s*$")
RE_LICENCIA = re.compile(r"(?m)^## [^\n]*Licencia")
ENTORNO = dict(os.environ, NO_COLOR="1", TERM="xterm", COLUMNS="250")

# Cómo instalar cada programa del sistema. Windows: el entorno de la cátedra (entorno, MSYS2
# UCRT64) ya trae `mingw-w64-ucrt-x86_64-toolchain` (gcc, gdb) y git.
INSTALACION = {
    "gcc": {"Debian / Ubuntu": "`sudo apt install gcc`", "Fedora": "`sudo dnf install gcc`",
            "Windows": "incluido en el entorno de la cátedra (MSYS2 UCRT64)",
            "macOS": "`xcode-select --install` (clang como `gcc`)"},
    "gdb": {"Debian / Ubuntu": "`sudo apt install gdb`", "Fedora": "`sudo dnf install gdb`",
            "Windows": "incluido en el entorno de la cátedra (MSYS2 UCRT64)",
            "macOS": "`brew install gdb` (en Apple Silicon no está: usar `lldb`)"},
    "valgrind": {"Debian / Ubuntu": "`sudo apt install valgrind`", "Fedora": "`sudo dnf install valgrind`",
                 "Windows": "no existe: usar WSL", "macOS": "no existe en Apple Silicon"},
    "bwrap": {"Debian / Ubuntu": "`sudo apt install bubblewrap`", "Fedora": "`sudo dnf install bubblewrap`",
              "Windows": "no existe (solo Linux): usar WSL", "macOS": "no existe (solo Linux)"},
    "git": {"Debian / Ubuntu": "`sudo apt install git`", "Fedora": "`sudo dnf install git`",
            "Windows": "incluido en el entorno de la cátedra (MSYS2 UCRT64)", "macOS": "`xcode-select --install`"},
    "typst": {"Debian / Ubuntu": "binario de https://github.com/typst/typst/releases",
              "Fedora": "binario de https://github.com/typst/typst/releases",
              "Windows": "`winget install --id Typst.Typst`", "macOS": "`brew install typst`"},
    "frama-c": {"Debian / Ubuntu": "`opam install frama-c`", "Fedora": "`opam install frama-c`",
                "Windows": "no existe: usar WSL", "macOS": "`opam install frama-c`"},
}
SISTEMAS = ["Debian / Ubuntu", "Fedora", "Windows", "macOS"]


def _ayuda(ejecutable: str) -> str:
    salida = subprocess.run([ejecutable, "--help"], capture_output=True, text=True, timeout=60, env=ENTORNO,
                            stdin=subprocess.DEVNULL)
    return salida.stdout + salida.stderr


def opciones(ejecutable: str) -> list[tuple[str, str]]:
    """(opciones, descripción) propias de la raíz: las CLI que trabajan con opciones y no con
    subcomandos (p. ej., `alucard --definicion …`) no tendrían, si no, nada en la referencia."""
    texto = _ayuda(ejecutable)
    panel = RE_PANEL_OPCIONES.search(texto)
    if not panel:
        return _opciones_argparse(texto)
    filas: list[list[str]] = []
    for linea in texto[panel.start():].splitlines()[1:]:
        if linea.startswith("╰"):
            break
        cuerpo = linea.strip().strip("│").strip()
        if not cuerpo:
            continue
        campos = re.split(r"\s{2,}", cuerpo.lstrip("*").strip())
        if campos[0].startswith("--"):
            nombres = campos[0].split(",") + [c for c in campos[1:2] if re.fullmatch(r"-\w", c)]
            descripcion = campos[-1] if len(campos) > 1 and not re.fullmatch(r"-\w|<\w+>|[A-Z_]+", campos[-1]) else ""
            filas.append([", ".join(f"`{n.strip()}`" for n in nombres), descripcion])
        elif filas:  # continuación de la descripción anterior
            filas[-1][1] = (filas[-1][1] + " " + cuerpo).strip()
    return [(nombres, descripcion.replace("|", "\\|")) for nombres, descripcion in filas
            if not set(re.findall(r"--[\w-]+", nombres)) & OPCIONES_ESTANDAR]


def comandos(ejecutable: str) -> list[tuple[str, str]]:
    """(comando, descripción) del panel de comandos de `--help` (vacío si no tiene subcomandos)."""
    texto = _ayuda(ejecutable)
    panel = RE_PANEL_COMANDOS.search(texto)
    if not panel:
        return _comandos_argparse(texto)
    filas: list[list[str]] = []
    for linea in texto[panel.start():].splitlines()[1:]:
        if linea.startswith("╰"):
            break
        if m := RE_FILA.match(linea):
            filas.append([m.group(1), m.group(2).strip()])
        elif (m := RE_CONTINUACION.match(linea)) and filas:
            filas[-1][1] += " " + m.group(1).strip()
    # «Comandos» puede aparecer en la descripción de una CLI argparse: sin filas, se prueba así.
    return [(nombre, descripcion.replace("|", "\\|")) for nombre, descripcion in filas] or _comandos_argparse(texto)


def _filas_argparse(lineas: list[str], fila: re.Pattern[str]) -> list[list[str]]:
    filas: list[list[str]] = []
    for linea in lineas:
        if m := fila.match(linea):
            filas.append([m.group(1), (m.group(2) or "").strip()])
        elif (m := RE_ARGPARSE_CONTINUACION.match(linea)) and filas:
            filas[-1][1] = (filas[-1][1] + " " + m.group(1)).strip()
        else:
            break
    return filas


def _comandos_argparse(texto: str) -> list[tuple[str, str]]:
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if RE_ARGPARSE_ELECCION.match(linea):
            return [(nombre, descripcion.replace("|", "\\|"))
                    for nombre, descripcion in _filas_argparse(lineas[i + 1:], RE_ARGPARSE_COMANDO)]
    return []


def _opciones_argparse(texto: str) -> list[tuple[str, str]]:
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if RE_ARGPARSE_OPCIONES.match(linea):
            filas = _filas_argparse(lineas[i + 1:], RE_ARGPARSE_OPCION)
            break
    else:
        return []
    resultado = []
    for nombres, descripcion in filas:
        banderas = [parte.split()[0] for parte in nombres.split(", ")]  # sin el METAVAR
        if not set(banderas) & OPCIONES_ESTANDAR:
            resultado.append((", ".join(f"`{b}`" for b in banderas), descripcion.replace("|", "\\|")))
    return resultado


def python_minimo(pyproject: Path) -> str:
    """La versión mínima de Python que declara el paquete (`requires-python = ">=3.12"` → 3.12)."""
    try:
        requisito = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["requires-python"]
    except (OSError, KeyError, tomllib.TOMLDecodeError):
        return "3.11"
    m = re.search(r">=\s*(\d+\.\d+)", requisito)
    return m.group(1) if m else "3.11"


def bloque(repo: Repo, python: str = "3.11") -> str:
    """El bloque generado para el README de `repo`."""
    partes = [INICIO, "", "## Referencia rápida", "", "### Requisitos", "",
              f"- Python ≥ {python} y [uv](https://docs.astral.sh/uv/getting-started/installation/)."]
    conocidos = [s for s in repo.sistema if s in INSTALACION]
    if repo.sistema:
        partes.append("- Programas del sistema: " + ", ".join(f"`{s}`" for s in repo.sistema) + ".")
    if conocidos:
        partes += ["", "| Sistema | " + " | ".join(f"`{s}`" for s in conocidos) + " |",
                   "|:--|" + ":--|" * len(conocidos)]
        partes += [f"| {so} | " + " | ".join(INSTALACION[s][so] for s in conocidos) + " |" for so in SISTEMAS]
    vistos: set[tuple] = set()
    for ejecutable in repo.ejecutables:
        lista = tuple(comandos(ejecutable))
        propias = tuple(opciones(ejecutable))
        if (lista, propias) in vistos or not (lista or propias):  # alias del mismo punto de entrada
            continue
        vistos.add((lista, propias))
        if propias:
            partes += ["", f"### Opciones de `{ejecutable}`", "", "| Opción | Descripción |", "|:--|:--|"]
            partes += [f"| {nombres} | {descripcion} |" for nombres, descripcion in propias]
        if not lista:
            continue
        partes += ["", f"### Comandos de `{ejecutable}`" if len(repo.ejecutables) > 1 else "### Comandos", "",
                   "| Comando | Descripción |", "|:--|:--|"]
        # Los alias (mismo comando con dos nombres, p. ej. `hal check` y `hal run`) van en una fila.
        por_descripcion: dict[str, list[str]] = {}
        for nombre, descripcion in lista:
            por_descripcion.setdefault(descripcion, []).append(nombre)
        partes += ["| " + ", ".join(f"`{ejecutable} {n}`" for n in nombres) + f" | {descripcion} |"
                   for descripcion, nombres in por_descripcion.items()]
        partes += ["", f"Ayuda de cada comando: `{ejecutable} <comando> -h`."]
    partes += ["", FIN, ""]
    return "\n".join(partes)


def con_bloque(texto: str, nuevo: str) -> str:
    """El README con el bloque reemplazado o, si no lo tenía, antes de la licencia (o al final)."""
    if RE_BLOQUE.search(texto):
        return RE_BLOQUE.sub(lambda _: nuevo, texto, count=1)
    licencia = RE_LICENCIA.search(texto)
    if licencia:
        return texto[:licencia.start()] + nuevo + "\n" + texto[licencia.start():]
    return texto.rstrip("\n") + "\n\n" + nuevo


def seleccion(repos: list[Repo], nombres: list[str], raiz: Path) -> list[Repo]:
    activos = [r for r in filtrar(repos, estados=["activo"]) if r.tipo == "cli"
               and (raiz / r.ruta / "README.md").is_file() and all(shutil.which(e) for e in r.ejecutables)]
    return [r for r in activos if not nombres or r.nombre in nombres]


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accion", choices=["actualizar", "verificar"])
    parser.add_argument("herramientas", nargs="*")
    parser.add_argument("--raiz", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--manifiesto", type=Path)
    # intermixed: las herramientas pueden ir después de --raiz/--manifiesto; con parse_args, el
    # argparse de Python 3.12.3 (Ubuntu 24.04, el del CI) las rechazaba («unrecognized arguments»).
    args = parser.parse_intermixed_args(argv)
    _, repos = cargar(args.manifiesto) if args.manifiesto else cargar()
    desactualizados = []
    for repo in seleccion(repos, args.herramientas, args.raiz):
        readme = args.raiz / repo.ruta / "README.md"
        texto = readme.read_text(encoding="utf-8")
        nuevo = con_bloque(texto, bloque(repo, python_minimo(args.raiz / repo.ruta / "pyproject.toml")))
        if nuevo == texto:
            continue
        if args.accion == "actualizar":
            readme.write_text(nuevo, encoding="utf-8")
            print(f"✓ {readme}")
        else:
            import difflib
            diff = "".join(difflib.unified_diff(
                texto.splitlines(keepends=True),
                nuevo.splitlines(keepends=True),
                fromfile=f"a/{readme.name}",
                tofile=f"b/{readme.name}",
            ))
            desactualizados.append(f"{readme}\n{diff}")
    if desactualizados:
        print("README con la referencia generada desactualizada (correr `readme_generado.py actualizar`):")
        print("\n".join(f"✗ {r}" for r in desactualizados))
        return 1
    if args.accion == "verificar":
        print("✓ La referencia generada de los README está al día.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
