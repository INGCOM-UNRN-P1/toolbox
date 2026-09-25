#!/usr/bin/env python3
"""Lector del manifiesto ecosistema.toml (N-P1TOOLS-02).

Una sola fuente de verdad para qué repositorios forman el ecosistema, de dónde
se instalan y en qué perfiles participan. La usan clone_repos.sh,
install_tools.sh, health_check.sh y el CI de integración.

Uso:
    ecosistema.py listar [--perfil P]... [--tipo T]... [--estado E]... [--formato F]
    ecosistema.py instalar [--perfil P]... [--editable RAIZ | --local RAIZ] [--simular]
    ecosistema.py sistema [--perfil P]...
    ecosistema.py verificar [--raiz DIR]

Formatos de `listar`: nombre (por defecto), url, carpeta, clonar ("carpeta url"),
ejecutables, ejecutable-principal (uno por repo), requisito (lo que recibe
`uv tool install` desde git), carpeta-extras ("carpeta[extras]" para instalar
en modo editable), json.

Solo usa la biblioteca estándar (Python ≥ 3.11).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

P1_TOOLS = Path(__file__).resolve().parents[1]
MANIFIESTO = P1_TOOLS / "ecosistema.toml"
TIPOS = {"cli", "biblioteca", "extension-vscode", "apps-script", "contenido", "plantilla",
         "libreria-c", "ejemplo", "entorno", "documentacion", "android", "especificacion"}
ESTADOS = {"activo", "deprecado", "especificacion", "ajeno"}
# Carpetas de dev/tools que no son repositorios del ecosistema.
NO_SON_REPOS = {"revision", "skills", "scripts", "generated", "guias", "node_modules", "htmlcov",
                "__pycache__", "scratch", "uatu-test", "plantillas", "librerias"}


@dataclass
class Repo:
    nombre: str
    tipo: str
    estado: str
    url: str = ""
    carpeta: str = ""
    paquete: str = ""
    ejecutables: list[str] = field(default_factory=list)
    extras: list[str] = field(default_factory=list)
    perfiles: list[str] = field(default_factory=list)
    plugin_ripley: str = ""
    sistema: list[str] = field(default_factory=list)

    @property
    def ruta(self) -> str:
        return self.carpeta or self.nombre

    @property
    def instalable(self) -> bool:
        return self.tipo == "cli" and self.estado in ("activo", "deprecado")

    def requisito_git(self) -> str:
        """Lo que recibe `uv tool install` para instalar desde el repositorio."""
        if self.extras:
            return f"{self.paquete}[{','.join(self.extras)}] @ git+{self.url}"
        return f"git+{self.url}"

    def requisito_editable(self, raiz: Path) -> str:
        ruta = raiz / self.ruta
        return f"{ruta}[{','.join(self.extras)}]" if self.extras else str(ruta)


def cargar(ruta: Path = MANIFIESTO) -> tuple[dict, list[Repo]]:
    datos = tomllib.loads(ruta.read_text(encoding="utf-8"))
    perfiles = datos.get("perfiles", {})
    repos = []
    errores = []
    nombres = set()
    for entrada in datos.get("repo", []):
        repo = Repo(**entrada)
        if repo.nombre in nombres:
            errores.append(f"{repo.nombre}: nombre repetido")
        nombres.add(repo.nombre)
        if repo.tipo not in TIPOS:
            errores.append(f"{repo.nombre}: tipo desconocido «{repo.tipo}»")
        if repo.estado not in ESTADOS:
            errores.append(f"{repo.nombre}: estado desconocido «{repo.estado}»")
        for perfil in repo.perfiles:
            if perfil not in perfiles:
                errores.append(f"{repo.nombre}: perfil desconocido «{perfil}»")
        if repo.tipo in ("cli", "biblioteca") and not repo.paquete:
            errores.append(f"{repo.nombre}: falta `paquete`")
        if repo.tipo == "cli" and not repo.ejecutables:
            errores.append(f"{repo.nombre}: falta `ejecutables`")
        if repo.instalable and not repo.url:
            errores.append(f"{repo.nombre}: una herramienta instalable necesita `url`")
        repos.append(repo)
    if errores:
        raise SystemExit("ecosistema.toml inválido:\n  " + "\n  ".join(errores))
    return perfiles, repos


def filtrar(repos: list[Repo], perfiles=None, tipos=None, estados=None) -> list[Repo]:
    salida = []
    for repo in repos:
        if perfiles and not set(perfiles) & set(repo.perfiles):
            continue
        if tipos and repo.tipo not in tipos:
            continue
        if estados and repo.estado not in estados:
            continue
        salida.append(repo)
    return salida


def cmd_listar(args, repos: list[Repo]) -> int:
    seleccion = filtrar(repos, args.perfil, args.tipo, args.estado)
    if args.formato == "json":
        print(json.dumps([r.__dict__ for r in seleccion], ensure_ascii=False, indent=2))
        return 0
    for repo in seleccion:
        if args.formato == "nombre":
            print(repo.nombre)
        elif args.formato == "url" and repo.url:
            print(repo.url)
        elif args.formato == "carpeta":
            print(repo.ruta)
        elif args.formato == "clonar" and repo.url:
            print(f"{repo.ruta} {repo.url}")
        elif args.formato == "ejecutables":
            for ejecutable in repo.ejecutables:
                print(ejecutable)
        elif args.formato == "requisito" and repo.instalable:
            print(repo.requisito_git())
        elif args.formato == "carpeta-extras" and repo.instalable:
            print(f"{repo.ruta}[{','.join(repo.extras)}]" if repo.extras else repo.ruta)
        elif args.formato == "ejecutable-principal" and repo.ejecutables:
            print(repo.ejecutables[0])
    return 0


def cmd_instalar(args, repos: list[Repo]) -> int:
    seleccion = [r for r in filtrar(repos, args.perfil, None, ["activo"]) if r.instalable]
    fallidos = []
    for repo in seleccion:
        if args.editable:
            comando = ["uv", "tool", "install", "--editable", repo.requisito_editable(Path(args.editable))]
        elif args.local:
            # Instalación no editable desde el clon local: el paquete queda en
            # site-packages, como lo instalaría cualquiera desde git. Sirve para
            # detectar dependencias no declaradas (imports de carpetas hermanas).
            comando = ["uv", "tool", "install", repo.requisito_editable(Path(args.local))]
        else:
            comando = ["uv", "tool", "install", repo.requisito_git()]
        print("$ " + " ".join(f'"{c}"' if " " in c else c for c in comando), flush=True)
        if args.simular:
            continue
        if subprocess.run(comando).returncode != 0:
            fallidos.append(repo.nombre)
    if fallidos:
        print(f"\nNo se pudieron instalar: {', '.join(fallidos)}", file=sys.stderr)
        return 1
    return 0


def cmd_sistema(args, repos: list[Repo]) -> int:
    requeridos = sorted({s for r in filtrar(repos, args.perfil, None, ["activo"]) for s in r.sistema})
    print("\n".join(requeridos))
    return 0


def _remoto(carpeta: Path) -> str:
    salida = subprocess.run(["git", "-C", str(carpeta), "remote", "get-url", "origin"],
                            capture_output=True, text=True)
    return salida.stdout.strip().removesuffix(".git") if salida.returncode == 0 else ""


def cmd_verificar(args, repos: list[Repo]) -> int:
    raiz = Path(args.raiz).resolve()
    problemas: list[str] = []
    avisos: list[str] = []
    por_ruta = {r.ruta: r for r in repos}

    # 1. Todo repo local con pyproject o .git debe figurar en el manifiesto.
    candidatos = [p for p in raiz.iterdir() if p.is_dir() and not p.name.startswith(".")]
    for sub in ("plantillas", "librerias"):
        if (raiz / sub).is_dir():
            candidatos += [p for p in (raiz / sub).iterdir() if p.is_dir()]
    for carpeta in sorted(candidatos):
        rel = str(carpeta.relative_to(raiz))
        if carpeta.name in NO_SON_REPOS or rel in NO_SON_REPOS:
            continue
        if ((carpeta / "pyproject.toml").exists() or (carpeta / ".git").exists()) and rel not in por_ruta:
            problemas.append(f"{rel}: existe en {raiz} pero no figura en ecosistema.toml")

    # 2. Coherencia de cada entrada con su repo local.
    for repo in repos:
        carpeta = raiz / repo.ruta
        if not carpeta.is_dir():
            avisos.append(f"{repo.nombre}: no está clonado en {carpeta}")
            continue
        if repo.url:
            remoto = _remoto(carpeta)
            if remoto and remoto != repo.url:
                problemas.append(f"{repo.nombre}: el remoto local es {remoto} y el manifiesto dice {repo.url}")
        pyproject = carpeta / "pyproject.toml"
        if repo.tipo in ("cli", "biblioteca"):
            if not pyproject.exists():
                problemas.append(f"{repo.nombre}: es {repo.tipo} pero no tiene pyproject.toml")
                continue
            proyecto = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]
            if proyecto.get("name") != repo.paquete:
                problemas.append(f"{repo.nombre}: el paquete se llama {proyecto.get('name')!r}, no {repo.paquete!r}")
            faltan = set(repo.ejecutables) - set(proyecto.get("scripts", {}))
            if faltan:
                problemas.append(f"{repo.nombre}: ejecutables inexistentes en pyproject: {sorted(faltan)}")
            plugins = proyecto.get("entry-points", {}).get("ripley.plugins", {})
            if repo.plugin_ripley and repo.plugin_ripley not in plugins:
                problemas.append(f"{repo.nombre}: no declara el plugin de ripley {repo.plugin_ripley!r}")
            if not repo.plugin_ripley and plugins:
                problemas.append(f"{repo.nombre}: declara plugins de ripley {sorted(plugins)} no registrados en el manifiesto")
            faltan_extras = set(repo.extras) - set(proyecto.get("optional-dependencies", {}))
            if faltan_extras:
                problemas.append(f"{repo.nombre}: extras inexistentes: {sorted(faltan_extras)}")

    for aviso in avisos:
        print(f"· {aviso}")
    for problema in problemas:
        print(f"✗ {problema}")
    if problemas:
        print(f"\n{len(problemas)} inconsistencia(s) entre ecosistema.toml y {raiz}.", file=sys.stderr)
        return 1
    print(f"✓ ecosistema.toml coherente con {raiz} ({len(repos)} repositorios).")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Consulta el manifiesto ecosistema.toml.")
    parser.add_argument("--manifiesto", default=str(MANIFIESTO))
    sub = parser.add_subparsers(dest="comando", required=True)

    p_listar = sub.add_parser("listar")
    p_listar.add_argument("--perfil", action="append")
    p_listar.add_argument("--tipo", action="append")
    p_listar.add_argument("--estado", action="append")
    p_listar.add_argument("--formato", default="nombre",
                          choices=["nombre", "url", "carpeta", "clonar", "ejecutables", "ejecutable-principal",
                                   "requisito", "carpeta-extras", "json"])

    p_instalar = sub.add_parser("instalar")
    p_instalar.add_argument("--perfil", action="append")
    modo = p_instalar.add_mutually_exclusive_group()
    modo.add_argument("--editable", metavar="RAIZ", help="instala en modo editable desde RAIZ/<carpeta>")
    modo.add_argument("--local", metavar="RAIZ", help="instala (no editable) desde el clon local RAIZ/<carpeta>")
    p_instalar.add_argument("--simular", action="store_true")

    p_sistema = sub.add_parser("sistema")
    p_sistema.add_argument("--perfil", action="append")

    p_verificar = sub.add_parser("verificar")
    p_verificar.add_argument("--raiz", default=str(P1_TOOLS.parent))

    args = parser.parse_args(argv)
    _, repos = cargar(Path(args.manifiesto))
    return {"listar": cmd_listar, "instalar": cmd_instalar, "sistema": cmd_sistema,
            "verificar": cmd_verificar}[args.comando](args, repos)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
