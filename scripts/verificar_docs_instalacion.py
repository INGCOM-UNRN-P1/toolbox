#!/usr/bin/env python3
"""Verifica que la documentación instale las herramientas de cátedra solo desde git.

21 de los nombres de paquete del ecosistema (ripley, gaff, hal, nostromo, …)
pertenecen en PyPI a proyectos ajenos: una instrucción como
``uv tool install gaff`` instala código de terceros. Este chequeo falla si algún
documento indica instalar una herramienta propia por nombre en lugar de hacerlo
desde su repositorio (``uv tool install git+https://github.com/…`` o
``uv tool install "paquete[extra] @ git+https://…"``).

Uso:
    verificar_docs_instalacion.py [--raiz DIR] [RUTA ...]

Cada RUTA puede ser un archivo o un directorio (se recorre recursivamente). Sin
rutas revisa los repositorios de la raíz. La raíz (por defecto la carpeta que
contiene a p1-tools) es de donde se leen los nombres propios (pyproject.toml).
Sale con 0 si no hay instrucciones inseguras y con 1 si encuentra alguna.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

# Nombres propios que no aparecen como carpeta con pyproject (alias de scripts).
NOMBRES_EXTRA = {"alucard", "generador-examenes", "gift-linter", "questions", "moodle-toolbox",
                 "ripley-check", "uatu-audit", "uatu-admin", "mother", "yutani", "sulaco"}

INSTALADORES = r"(?:uv\s+tool\s+install|uvx|pipx\s+install|pip3?\s+install|uv\s+pip\s+install|uv\s+add)"
EXTENSIONES = {".md", ".sh", ".ps1", ".bat", ".txt", ".rst", ".yml", ".yaml"}
EXCLUIR_PARTES = {".git", ".venv", "node_modules", "_build", "historico", ".docs_backup", "revision", "build", "dist"}
# qol.md y CHANGELOG.md son historia; publicar.md describe un flujo de PyPI no vigente.
EXCLUIR_ARCHIVOS = {"qol.md", "CHANGELOG.md", "publicar.md"}


def nombres_propios(raiz: Path) -> set[str]:
    """Nombres de paquete y de ejecutable de las herramientas del ecosistema."""
    nombres = set(NOMBRES_EXTRA)
    for pyproject in raiz.glob("*/pyproject.toml"):
        try:
            datos = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        proyecto = datos.get("project", {})
        if proyecto.get("name"):
            nombres.add(proyecto["name"].lower())
        nombres.update(s.lower() for s in proyecto.get("scripts", {}))
        nombres.add(pyproject.parent.name.lower())
    return nombres


def patron_inseguro(nombres: set[str]) -> re.Pattern[str]:
    alternativas = "|".join(sorted((re.escape(n) for n in nombres), key=len, reverse=True))
    # instalador, opciones sueltas (no --from), comillas opcionales, nombre propio
    # con extras opcionales, y que NO siga una referencia directa "@ git+".
    return re.compile(
        rf"{INSTALADORES}(?:\s+-{{1,2}}(?!-)(?!from\b)[\w-]+(?:[= ][^\s\"']+)?)*\s+[\"']?"
        rf"(?P<nombre>{alternativas})(?:\[[\w,-]+\])?(?![\w./\[-])(?!\s*@\s*git\+)",
        re.IGNORECASE,
    )


def revisar(rutas: list[Path], nombres: set[str]) -> list[str]:
    """Revisa archivos sueltos o directorios completos (recursivamente)."""
    patron = patron_inseguro(nombres)
    hallazgos = []
    for base in rutas:
        candidatos = [base] if base.is_file() else sorted(base.rglob("*"))
        for archivo in candidatos:
            if (not archivo.is_file() or archivo.suffix.lower() not in EXTENSIONES
                    or archivo.name in EXCLUIR_ARCHIVOS
                    or EXCLUIR_PARTES & set(archivo.parts)):
                continue
            try:
                lineas = archivo.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for numero, linea in enumerate(lineas, 1):
                for m in patron.finditer(linea):
                    hallazgos.append(f"{archivo}:{numero}: instala «{m.group('nombre')}» por nombre: {linea.strip()}")
    return hallazgos


def main(argv: list[str]) -> int:
    raiz = Path(__file__).resolve().parents[2]
    if argv[:1] == ["--raiz"] and len(argv) >= 2:
        raiz = Path(argv[1]).resolve()
        argv = argv[2:]
    directorios = [Path(a).resolve() for a in argv] or sorted(p for p in raiz.iterdir() if p.is_dir())
    hallazgos = revisar(directorios, nombres_propios(raiz))
    for h in hallazgos:
        print(h)
    if hallazgos:
        print(f"\n{len(hallazgos)} instrucción(es) instalan herramientas propias por nombre. "
              "Usá `uv tool install git+https://github.com/<org>/<repo>` "
              "o `uv tool install \"paquete[extra] @ git+https://…\"`.", file=sys.stderr)
        return 1
    print("✓ La documentación instala las herramientas propias solo desde git.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
