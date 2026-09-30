#!/usr/bin/env python3
"""Verifica que los comandos citados en skills y documentación existan en las CLIs reales.

Recorre los bloques de código (```) de los Markdown indicados, toma cada línea
que empieza con el nombre de una herramienta del ecosistema instalada en el
PATH (`gaff check …`, `deckard verify fuzz …`) y comprueba contra el `--help`
real que cada subcomando exista, bajando por los subgrupos de Typer. Solo
valida la cadena de subcomandos, no las opciones.

Uso:
    verificar_comandos_docs.py [RUTA ...]

Sin argumentos revisa skills/ y ecosistema/ de p1-tools, y los MANUAL_*.md.
Sale con 1 si algún comando citado no existe y con 0 si todos existen.
Las herramientas que no están instaladas se informan y se omiten.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

RAIZ_P1 = Path(__file__).resolve().parents[1]
RE_BLOQUE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
RE_COMANDO_HELP = re.compile(r"^│ ([a-z][a-z0-9-]*)\s", re.MULTILINE)
RE_PANEL_COMANDOS = re.compile(r"\b(?:Commands|Comandos)\b")
ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="200")


def herramientas_del_ecosistema() -> list[str]:
    """Ejecutables de las herramientas hermanas (según sus pyproject) presentes en el PATH."""
    import tomllib

    nombres = set()
    for pyproject in RAIZ_P1.parent.glob("*/pyproject.toml"):
        try:
            scripts = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {}).get("scripts", {})
        except (OSError, tomllib.TOMLDecodeError):
            continue
        nombres.update(scripts)
    return sorted(n for n in nombres if shutil.which(n))


@lru_cache(maxsize=None)
def subcomandos(cadena: tuple[str, ...]) -> frozenset[str]:
    """Subcomandos que lista `<cadena> --help` (vacío si no es un grupo)."""
    try:
        salida = subprocess.run([*cadena, "--help"], capture_output=True, text=True, timeout=30, env=ENTORNO)
    except (OSError, subprocess.TimeoutExpired):
        return frozenset()
    texto = salida.stdout + salida.stderr
    # «Comandos»: las herramientas que usan yutani muestran la ayuda de Typer en español
    # (N-ECO-14). Sin esto, sus subcomandos no se veían y ninguna cita se verificaba.
    panel = RE_PANEL_COMANDOS.search(texto)
    if not panel:
        return frozenset()
    return frozenset(RE_COMANDO_HELP.findall(texto[panel.start():]))


def verificar_linea(linea: str, herramientas: set[str]) -> str | None:
    """Devuelve un mensaje de error si la línea cita un subcomando inexistente."""
    partes = linea.split()
    if not partes or partes[0] not in herramientas:
        return None
    cadena = [partes[0]]
    for parte in partes[1:]:
        if parte.startswith("-") or not re.fullmatch(r"[a-z][a-z0-9-]*", parte):
            break
        disponibles = subcomandos(tuple(cadena))
        if not disponibles:
            break  # la cadena ya es un comando final: lo que sigue son argumentos
        if parte not in disponibles:
            # Grupos con comando por defecto oculto (p. ej. deckard `export <id>`
            # delega en `export run <id>`): si `<cadena> <parte> --help` responde
            # sin error, `parte` es un argumento y la cadena es válida.
            if acepta_como_argumento(tuple(cadena), parte):
                return None
            return f"`{' '.join(cadena)} {parte}` no existe (disponibles: {', '.join(sorted(disponibles))})"
        cadena.append(parte)
    return None


@lru_cache(maxsize=None)
def acepta_como_argumento(cadena: tuple[str, ...], parte: str) -> bool:
    try:
        salida = subprocess.run([*cadena, parte, "--help"], capture_output=True, text=True, timeout=30, env=ENTORNO)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return salida.returncode == 0


def revisar(archivos: list[Path], herramientas: set[str]) -> list[str]:
    errores = []
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8", errors="replace")
        for bloque in RE_BLOQUE.finditer(texto):
            inicio = texto[: bloque.start(1)].count("\n") + 1
            for desplazamiento, linea in enumerate(bloque.group(1).splitlines()):
                linea = linea.strip().removeprefix("$ ")
                error = verificar_linea(linea, herramientas)
                if error:
                    errores.append(f"{archivo}:{inicio + desplazamiento}: {error}")
    return errores


def main(argv: list[str]) -> int:
    rutas = [Path(a) for a in argv] or [RAIZ_P1 / "skills", RAIZ_P1 / "ecosistema", *RAIZ_P1.glob("MANUAL_*.md")]
    archivos = []
    for ruta in rutas:
        archivos.extend(sorted(ruta.rglob("*.md")) if ruta.is_dir() else [ruta])
    herramientas = set(herramientas_del_ecosistema())
    if not herramientas:
        print("No hay herramientas del ecosistema en el PATH: nada que verificar.", file=sys.stderr)
        return 2
    errores = revisar(archivos, herramientas)
    for error in errores:
        print(error)
    if errores:
        print(f"\n{len(errores)} comando(s) citado(s) no existen.", file=sys.stderr)
        return 1
    print(f"✓ Todos los comandos citados existen ({len(archivos)} archivos, {len(herramientas)} herramientas).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
