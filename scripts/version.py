#!/usr/bin/env python3
"""Versionado de las herramientas: SemVer, CHANGELOG y tags anotados (N-ECO-06).

Política (LINEAMIENTOS §8):
  - La versión vive en pyproject.toml; si el paquete define `__version__` como
    literal, tiene que coincidir (lo controla `ecosistema.py verificar`).
  - La versión siguiente sale de los Conventional Commits desde el último tag
    `v*`: `feat` sube la menor, `fix` y el resto la de parche, y un cambio
    incompatible (`tipo!:` o `BREAKING CHANGE`) la mayor (la menor mientras la
    versión sea 0.y.z).
  - Cada versión tiene su sección en CHANGELOG.md (Keep a Changelog) y un tag
    anotado `vX.Y.Z` sobre el commit `chore(release): X.Y.Z`.

Uso:
    version.py siguiente REPO [--desde REF|FECHA]
    version.py changelog REPO [--version X.Y.Z] [--desde REF|FECHA]
    version.py publicar REPO [--version X.Y.Z] [--desde REF|FECHA] [--probar COMANDO] [--simular]

`publicar` no empuja nada: el commit y el tag quedan locales. Con `--probar`
corre los tests con la versión ya cambiada y, si fallan, deshace todo (así
aparece un test que fija la versión vieja antes de crear el tag).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

RE_SEMVER = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?$")
RE_CONVENCIONAL = re.compile(r"^(?P<tipo>[a-z]+)(?:\((?P<alcance>[^)]*)\))?(?P<rompe>!)?: (?P<descripcion>.+)$")
SECCIONES = [
    ("feat", "Agregado"),
    ("fix", "Corregido"),
    ("perf", "Cambiado"),
    ("refactor", "Cambiado"),
    ("docs", "Documentación"),
    ("test", "Mantenimiento"),
    ("build", "Mantenimiento"),
    ("ci", "Mantenimiento"),
    ("chore", "Mantenimiento"),
    ("style", "Mantenimiento"),
]
ORDEN = ["Incompatible", "Agregado", "Cambiado", "Corregido", "Documentación", "Mantenimiento", "Otros"]
ENCABEZADO = """# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/);
versiones según [SemVer](https://semver.org/lang/es/).
"""


@dataclass
class Commit:
    hash: str
    asunto: str
    cuerpo: str

    @property
    def convencional(self) -> re.Match[str] | None:
        return RE_CONVENCIONAL.match(self.asunto)

    @property
    def rompe(self) -> bool:
        m = self.convencional
        return bool(m and m["rompe"]) or "BREAKING CHANGE" in self.cuerpo


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def version_actual(repo: Path) -> str:
    return tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]


def ultimo_tag(repo: Path) -> str | None:
    tags = [t for t in git(repo, "tag", "--merged", "HEAD").split() if RE_SEMVER.match(t)]
    return max(tags, key=lambda t: tuple(int(x or 0) for x in RE_SEMVER.match(t).groups())) if tags else None


def commits(repo: Path, desde: str | None) -> list[Commit]:
    """Commits desde un tag/commit o desde una fecha (AAAA-MM-DD); sin `desde`, desde el último tag."""
    desde = desde or ultimo_tag(repo)
    if desde and re.fullmatch(r"\d{4}-\d{2}-\d{2}", desde):
        rango = ["--since", desde, "HEAD"]
    elif desde:
        rango = [f"{desde}..HEAD"]
    else:
        rango = ["HEAD"]
    salida = git(repo, "log", "--no-merges", "--format=%h%x1f%s%x1f%b%x1e", *rango)
    lista = []
    for registro in salida.split("\x1e"):
        if registro.strip():
            h, asunto, cuerpo = (registro.strip("\n").split("\x1f") + ["", ""])[:3]
            if not asunto.startswith("chore(release)"):
                lista.append(Commit(h, asunto, cuerpo))
    return lista


def siguiente(actual: str, lista: list[Commit]) -> str:
    mayor, menor, parche = (int(x or 0) for x in RE_SEMVER.match(actual).groups())
    tipos = {c.convencional["tipo"] for c in lista if c.convencional}
    if any(c.rompe for c in lista):
        return f"{mayor + 1}.0.0" if mayor > 0 else f"0.{menor + 1}.0"
    if "feat" in tipos:
        return f"{mayor}.{menor + 1}.0"
    return f"{mayor}.{menor}.{parche + 1}"


def seccion(version: str, lista: list[Commit], fecha: str, sin_registro_previo: bool) -> str:
    grupos: dict[str, list[str]] = {}
    titulos = dict(SECCIONES)
    for c in lista:
        m = c.convencional
        if m is None:
            grupos.setdefault("Otros", []).append(f"- {c.asunto} (`{c.hash}`)")
            continue
        titulo = "Incompatible" if c.rompe else titulos.get(m["tipo"], "Otros")
        alcance = f"**{m['alcance']}**: " if m["alcance"] else ""
        grupos.setdefault(titulo, []).append(f"- {alcance}{m['descripcion']} (`{c.hash}`)")
    partes = [f"## [{version}] - {fecha}", ""]
    if sin_registro_previo:
        partes += ["Primera versión con registro de cambios; lo anterior está en el historial de git.", ""]
    for titulo in ORDEN:
        if titulo in grupos:
            partes += [f"### {titulo}", "", *grupos[titulo], ""]
    return "\n".join(partes).rstrip() + "\n"


def escribir_changelog(repo: Path, texto_seccion: str) -> None:
    ruta = repo / "CHANGELOG.md"
    if not ruta.exists():
        ruta.write_text(f"{ENCABEZADO}\n{texto_seccion}", encoding="utf-8")
        return
    actual = ruta.read_text(encoding="utf-8")
    m = re.search(r"^## \[", actual, re.MULTILINE)
    if m is None:
        ruta.write_text(actual.rstrip() + "\n\n" + texto_seccion, encoding="utf-8")
    else:
        ruta.write_text(actual[: m.start()] + texto_seccion + "\n" + actual[m.start():], encoding="utf-8")


def actualizar_version(repo: Path, anterior: str, nueva: str) -> list[Path]:
    """pyproject, `__version__` literal y la entrada del propio paquete en uv.lock."""
    cambiados = []
    pyproject = repo / "pyproject.toml"
    texto = pyproject.read_text(encoding="utf-8")
    texto, n = re.subn(r'(?m)^version = "[^"]+"', f'version = "{nueva}"', texto, count=1)
    if n != 1:
        raise SystemExit(f"{pyproject}: no se encontró `version = \"…\"`")
    pyproject.write_text(texto, encoding="utf-8")
    cambiados.append(pyproject)

    paquete = tomllib.loads(texto)["project"]["name"]
    for init in (repo / "src").glob("*/__init__.py") if (repo / "src").is_dir() else []:
        contenido = init.read_text(encoding="utf-8")
        nuevo, n = re.subn(r'(?m)^__version__ = "[^"]+"', f'__version__ = "{nueva}"', contenido)
        if n and nuevo != contenido:
            init.write_text(nuevo, encoding="utf-8")
            cambiados.append(init)

    lock = repo / "uv.lock"
    if lock.exists():
        contenido = lock.read_text(encoding="utf-8")
        patron = re.compile(
            r'(\[\[package\]\]\nname = "' + re.escape(paquete) + r'"\nversion = ")[^"]+("\nsource = \{ (?:editable|virtual) = "\." \})')
        nuevo, n = patron.subn(rf"\g<1>{nueva}\g<2>", contenido)
        if n == 1 and nuevo != contenido:
            lock.write_text(nuevo, encoding="utf-8")
            cambiados.append(lock)
    return cambiados


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accion", choices=["siguiente", "changelog", "publicar"])
    parser.add_argument("repo", type=Path)
    parser.add_argument("--version", dest="version_forzada")
    parser.add_argument("--desde", help="tag, commit o fecha AAAA-MM-DD (por defecto, el último tag v*)")
    parser.add_argument("--fecha", default=dt.date.today().isoformat())
    parser.add_argument("--simular", action="store_true")
    parser.add_argument("--probar", metavar="COMANDO",
                        help="comando de tests a correr con la versión nueva antes de commitear "
                             "(p. ej. \"uv run pytest -q\"); si falla, se deshacen los cambios")
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    actual = version_actual(repo)
    lista = commits(repo, args.desde)
    nueva = args.version_forzada or siguiente(actual, lista)
    if not RE_SEMVER.match(nueva):
        raise SystemExit(f"versión inválida: {nueva}")
    texto = seccion(nueva, lista, args.fecha, sin_registro_previo=not (repo / "CHANGELOG.md").exists())

    if args.accion == "siguiente":
        print(nueva)
        return 0
    if args.accion == "changelog" or args.simular:
        print(texto)
        if args.simular:
            print(f"(simulado) {repo.name}: {actual} → {nueva}; tag v{nueva}")
        return 0

    if git(repo, "status", "--porcelain", "--untracked-files=no").strip():
        raise SystemExit(f"{repo}: hay cambios sin commitear; publicá sobre un árbol limpio.")
    if f"v{nueva}" in git(repo, "tag").split():
        raise SystemExit(f"{repo}: el tag v{nueva} ya existe.")
    ignorado = subprocess.run(["git", "-C", str(repo), "check-ignore", "-q", "CHANGELOG.md"]).returncode == 0
    if ignorado:
        raise SystemExit(f"{repo}: .gitignore ignora CHANGELOG.md; agregá la excepción «!CHANGELOG.md».")
    changelog_existia = (repo / "CHANGELOG.md").exists()
    cambiados = actualizar_version(repo, actual, nueva) if nueva != actual else []
    escribir_changelog(repo, texto)
    if args.probar:
        # Los tests corren con la versión ya cambiada: un test que fija la versión vieja
        # (o un __version__ repetido en otro módulo) aparece acá y no después del tag.
        prueba = subprocess.run(args.probar, shell=True, cwd=repo)
        if prueba.returncode != 0:
            git(repo, "checkout", "--", *(str(p.relative_to(repo)) for p in cambiados))
            if changelog_existia:
                git(repo, "checkout", "--", "CHANGELOG.md")
            else:
                (repo / "CHANGELOG.md").unlink()
            raise SystemExit(f"{repo}: «{args.probar}» falló con la versión {nueva}; no se publicó nada.")
    git(repo, "add", "CHANGELOG.md", *(str(p.relative_to(repo)) for p in cambiados))
    git(repo, "commit", "-q", "-m", f"chore(release): {nueva}\n\nVersión {nueva} según los Conventional Commits desde "
        f"{args.desde or ultimo_tag(repo) or 'el inicio'}; sección nueva en CHANGELOG.md (N-ECO-06).")
    nombre = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))["project"]["name"]
    git(repo, "tag", "-a", f"v{nueva}", "-m", f"{nombre} {nueva}")
    print(f"✓ {repo.name}: {actual} → {nueva} (commit {git(repo, 'rev-parse', '--short', 'HEAD').strip()}, tag v{nueva})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
