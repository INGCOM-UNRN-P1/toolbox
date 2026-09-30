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
from pathlib import Path

from ecosistema import Repo, cargar, filtrar  # scripts/ecosistema.py (misma carpeta)

INICIO = "<!-- p1:referencia:inicio — generado por p1-tools/scripts/readme_generado.py: no editar a mano -->"
FIN = "<!-- p1:referencia:fin -->"
RE_BLOQUE = re.compile(r"<!-- p1:referencia:inicio[^\n]*-->\n.*?<!-- p1:referencia:fin -->\n?", re.DOTALL)
RE_PANEL_COMANDOS = re.compile(r"\b(?:Commands|Comandos)\b")
RE_FILA = re.compile(r"^│ ([a-z][a-z0-9-]*)\s+(.*?)\s*│?$")
RE_CONTINUACION = re.compile(r"^│\s{2,}(\S.*?)\s*│?$")
RE_LICENCIA = re.compile(r"(?m)^## [^\n]*Licencia")
ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="250")

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


def comandos(ejecutable: str) -> list[tuple[str, str]]:
    """(comando, descripción) del panel de comandos de `--help` (vacío si no tiene subcomandos)."""
    salida = subprocess.run([ejecutable, "--help"], capture_output=True, text=True, timeout=60, env=ENTORNO,
                            stdin=subprocess.DEVNULL)
    texto = salida.stdout + salida.stderr
    panel = RE_PANEL_COMANDOS.search(texto)
    if not panel:
        return []
    filas: list[list[str]] = []
    for linea in texto[panel.start():].splitlines()[1:]:
        if linea.startswith("╰"):
            break
        if m := RE_FILA.match(linea):
            filas.append([m.group(1), m.group(2).strip()])
        elif (m := RE_CONTINUACION.match(linea)) and filas:
            filas[-1][1] += " " + m.group(1).strip()
    return [(nombre, descripcion.replace("|", "\\|")) for nombre, descripcion in filas]


def bloque(repo: Repo) -> str:
    """El bloque generado para el README de `repo`."""
    partes = [INICIO, "", "## Referencia rápida", "", "### Requisitos", "",
              "- Python ≥ 3.11 y [uv](https://docs.astral.sh/uv/getting-started/installation/)."]
    conocidos = [s for s in repo.sistema if s in INSTALACION]
    if repo.sistema:
        partes.append("- Programas del sistema: " + ", ".join(f"`{s}`" for s in repo.sistema) + ".")
    if conocidos:
        partes += ["", "| Sistema | " + " | ".join(f"`{s}`" for s in conocidos) + " |",
                   "|:--|" + ":--|" * len(conocidos)]
        partes += [f"| {so} | " + " | ".join(INSTALACION[s][so] for s in conocidos) + " |" for so in SISTEMAS]
    vistos: set[tuple[tuple[str, str], ...]] = set()
    for ejecutable in repo.ejecutables:
        lista = tuple(comandos(ejecutable))
        if not lista or lista in vistos:  # alias del mismo punto de entrada (p. ej., alucard y generador-examenes)
            continue
        vistos.add(lista)
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
    args = parser.parse_args(argv)
    _, repos = cargar(args.manifiesto) if args.manifiesto else cargar()
    desactualizados = []
    for repo in seleccion(repos, args.herramientas, args.raiz):
        readme = args.raiz / repo.ruta / "README.md"
        texto = readme.read_text(encoding="utf-8")
        nuevo = con_bloque(texto, bloque(repo))
        if nuevo == texto:
            continue
        if args.accion == "actualizar":
            readme.write_text(nuevo, encoding="utf-8")
            print(f"✓ {readme}")
        else:
            desactualizados.append(str(readme))
    if desactualizados:
        print("README con la referencia generada desactualizada (correr `readme_generado.py actualizar`):")
        print("\n".join(f"✗ {r}" for r in desactualizados))
        return 1
    if args.accion == "verificar":
        print("✓ La referencia generada de los README está al día.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
