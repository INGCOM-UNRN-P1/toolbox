#!/usr/bin/env python3
"""Verifica los enlaces de la documentación Markdown del ecosistema (N-LIBRERIAS-01).

Un enlace a `file:///home/…` o a una ruta absoluta de la máquina del docente
funciona solo en esa máquina; un enlace relativo a un archivo que no existe
está roto para todos. Este script recorre los .md de cada repositorio de
ecosistema.toml y reporta:

  absoluto   enlace file:// o a /home, /Users, C:\\ (siempre es error)
  roto       enlace relativo a un archivo inexistente

Uso:
    verificar_enlaces_md.py [--raiz DIR] [--solo-absolutos] [--excluir REPO]... [RUTA ...]

Sin rutas revisa los repos del manifiesto bajo --raiz (por defecto, la carpeta
que contiene a p1-tools). Sale con 1 si encontró algún problema.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

from ecosistema import cargar  # scripts/ecosistema.py (misma carpeta)

P1_TOOLS = Path(__file__).resolve().parents[1]
IGNORAR = {".git", "node_modules", ".venv", "venv", "_build", "build", "dist", "site-packages", "__pycache__",
           ".pytest_cache", "htmlcov", ".tox"}
# [texto](destino "título") y <img src="destino">; se ignora el contenido de bloques de código.
RE_ENLACE = re.compile(r"!?\[[^\]\n]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
RE_BLOQUE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
RE_CODIGO = re.compile(r"`[^`\n]*`")
RE_ABSOLUTO = re.compile(r"^(file://|/home/|/Users/|[A-Za-z]:[\\/])")
ESQUEMAS = ("http://", "https://", "mailto:", "tel:", "data:", "ftp://")


def enlaces(texto: str) -> list[tuple[int, str]]:
    sin_bloques = RE_BLOQUE.sub(lambda m: "\n" * m.group(0).count("\n"), texto)
    resultado = []
    for n, linea in enumerate(sin_bloques.splitlines(), start=1):
        for m in RE_ENLACE.finditer(RE_CODIGO.sub("", linea)):
            resultado.append((n, m.group(1)))
    return resultado


def revisar(md: Path, solo_absolutos: bool) -> list[tuple[str, int, str]]:
    problemas = []
    for linea, destino in enlaces(md.read_text(encoding="utf-8", errors="replace")):
        if RE_ABSOLUTO.match(destino):
            problemas.append(("absoluto", linea, destino))
            continue
        if solo_absolutos or destino.startswith(ESQUEMAS) or destino.startswith("#") or "{" in destino:
            continue
        ruta = unquote(destino.split("#", 1)[0].split("?", 1)[0])
        if not ruta:
            continue
        objetivo = md.parent / ruta
        if objetivo.exists() or _documento_myst(objetivo):
            continue
        if "/" not in ruta and "." not in ruta:
            continue  # en MyST puede ser una etiqueta de referencia (se resuelve al compilar)
        problemas.append(("roto", linea, destino))
    return problemas


def _documento_myst(ruta: Path) -> bool:
    """MyST admite enlazar a un documento sin la extensión."""
    return any(ruta.with_name(ruta.name + ext).exists() for ext in (".md", ".ipynb"))


def archivos_md(raiz: Path) -> list[Path]:
    """Los .md del repo, sin dependencias, compilados ni carpetas ocultas (salvo .github)."""
    return sorted(
        p for p in raiz.rglob("*.md")
        if not IGNORAR & set(p.relative_to(raiz).parts[:-1])
        and not any(parte.startswith(".") and parte != ".github" for parte in p.relative_to(raiz).parts[:-1])
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("rutas", nargs="*", type=Path)
    parser.add_argument("--raiz", type=Path, default=P1_TOOLS.parent)
    parser.add_argument("--solo-absolutos", action="store_true", help="reportar solo enlaces absolutos o file://")
    parser.add_argument("--excluir", action="append", default=[], metavar="REPO",
                        help="no revisar este repo del manifiesto (se puede repetir)")
    args = parser.parse_args(argv)

    if args.rutas:
        repos = args.rutas
    else:
        _, manifiesto = cargar()
        repos = [args.raiz / r.ruta for r in manifiesto if r.estado != "ajeno" and (args.raiz / r.ruta).is_dir()
                 and r.nombre not in args.excluir]

    total = 0
    for repo in repos:
        mds = [repo] if repo.is_file() else archivos_md(repo)
        for md in mds:
            for tipo, linea, destino in revisar(md, args.solo_absolutos):
                print(f"{tipo:9} {md}:{linea}: {destino}")
                total += 1
    print(f"\nEnlaces con problemas: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
