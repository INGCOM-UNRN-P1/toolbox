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
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

P1_TOOLS = Path(__file__).resolve().parents[1]
MANIFIESTO = P1_TOOLS / "ecosistema.toml"
TIPOS = {"cli", "biblioteca", "extension-vscode", "apps-script", "contenido", "plantilla",
         "libreria-c", "ejemplo", "entorno", "documentacion", "android", "especificacion",
         "workflows", "datos", "binario"}
ESTADOS = {"activo", "deprecado", "retirado", "especificacion", "ajeno", "sin-publicar"}
# Repos creados localmente que todavía no están en GitHub: no se clonan ni se instalan.
SIN_PUBLICAR = "sin-publicar"
# Herramientas retiradas (reemplazadas y con el repo archivado): tampoco se clonan ni se instalan.
RETIRADO = "retirado"
NO_SE_CLONAN = {SIN_PUBLICAR, RETIRADO}
# Carpetas de dev/tools que no son repositorios del ecosistema.
NO_SON_REPOS = {"revision", "skills", "scripts", "generated", "guias", "node_modules", "htmlcov",
                "__pycache__", "scratch", "plantillas", "librerias"}


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
    ref: str = ""  # tag o commit fijo (mother lo instala así)

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
        if repo.ref and not RE_REF_FIJADA.match(repo.ref):
            errores.append(f"{repo.nombre}: ref = «{repo.ref}» no es un tag vX.Y.Z ni un commit completo")
        repos.append(repo)
    errores += revisar_cuatrimestres(datos, nombres)
    if errores:
        raise SystemExit("ecosistema.toml inválido:\n  " + "\n  ".join(errores))
    return perfiles, repos


def revisar_cuatrimestres(datos: dict, nombres: set[str]) -> list[str]:
    """La matriz de cada cuatrimestre sólo fija tags vX.Y.Z o commits completos (Ola 11): una rama
    (`main`) o un commit abreviado se mueven, y el curso dejaría de instalar lo mismo."""
    errores = []
    cuatrimestres = datos.get("cuatrimestres", {})
    for cuatrimestre, matriz in cuatrimestres.items():
        for nombre, ref in matriz.items():
            if nombre not in nombres:
                errores.append(f"cuatrimestre {cuatrimestre}: «{nombre}» no es un repo del manifiesto")
            elif not RE_REF_FIJADA.match(str(ref)):
                errores.append(f"cuatrimestre {cuatrimestre}: {nombre} = «{ref}» no es un tag vX.Y.Z ni un commit "
                               f"completo (una rama o un commit abreviado pueden moverse)")
    vigente = datos.get("cuatrimestre_vigente")
    if vigente and vigente not in cuatrimestres:
        errores.append(f"cuatrimestre_vigente = {vigente}, pero no hay [cuatrimestres.\"{vigente}\"]")
    return errores


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
        elif args.formato == "clonar" and repo.url and repo.estado not in NO_SE_CLONAN:
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
            # --reinstall-package: sin él, uv reutiliza la rueda cacheada de una
            # corrida anterior mientras no cambie pyproject.toml, y se prueba
            # código viejo.
            comando = ["uv", "tool", "install", "--reinstall-package", repo.paquete,
                       repo.requisito_editable(Path(args.local))]
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


RE_VERSION_LITERAL = re.compile(r'(?m)^__version__ = "([^"]+)"')
RE_SECCION_CHANGELOG = re.compile(r"(?m)^## \[(\d+\.\d+\.\d+)\]")
RE_VERSION_PLUGIN = re.compile(r'(?m)^\s+version\s*=\s*"(\d+\.\d+\.\d+)"')


def revisar_versionado(carpeta: Path, proyecto: dict) -> list[str]:
    """Política de LINEAMIENTOS §7: LICENSE, CHANGELOG y una sola versión (N-ECO-06)."""
    problemas = []
    version = proyecto.get("version", "")
    licencia = proyecto.get("license", {})
    licencia = licencia.get("text", "") if isinstance(licencia, dict) else str(licencia)
    if "GPL" in licencia and not any((carpeta / n).exists() for n in ("LICENSE", "LICENSE.md", "COPYING")):
        problemas.append(f"declara {licencia} pero no tiene el archivo LICENSE")
    changelog = carpeta / "CHANGELOG.md"
    if not changelog.exists():
        problemas.append("no tiene CHANGELOG.md")
    else:
        secciones = RE_SECCION_CHANGELOG.findall(changelog.read_text(encoding="utf-8"))
        if secciones and secciones[0] != version:
            problemas.append(f"la última versión del CHANGELOG es {secciones[0]} y pyproject dice {version}")
    for init in sorted((carpeta / "src").glob("*/__init__.py")) if (carpeta / "src").is_dir() else []:
        m = RE_VERSION_LITERAL.search(init.read_text(encoding="utf-8"))
        if m and m.group(1) != version:
            problemas.append(f"{init.relative_to(carpeta)} dice __version__ = {m.group(1)!r} y pyproject {version!r}")
    # Plugins de ripley con la versión escrita a mano (quedaba en 0.1.0 al publicar).
    plugins = [*(carpeta / "src").glob("*/ripley_plugin.py"), *(carpeta / "src").glob("*/plugins/*.py")] \
        if (carpeta / "src").is_dir() else []
    for plugin in sorted(plugins):
        for literal in RE_VERSION_PLUGIN.findall(plugin.read_text(encoding="utf-8")):
            if literal != version:
                problemas.append(f"{plugin.relative_to(carpeta)} declara version = {literal!r} y pyproject {version!r}")
    return problemas


RE_REFERENCIA_GIT = re.compile(r"@\s*git\+(?P<url>[^@\s;]+)(?:@(?P<ref>[^\s;]+))?")
RE_REF_FIJADA = re.compile(r"^(?:[0-9a-f]{40}|v\d+\.\d+\.\d+)$")


CARPETAS_QUE_NO_SE_INSTALAN = {"tests", "test", "scripts", "docs", "examples", "ejemplos", "build", "dist"}


def carpetas_del_paquete(carpeta: Path, pyproject: dict) -> list[Path]:
    """El código que se instala: las carpetas de la rueda de hatch, `src/` o los paquetes de la raíz."""
    rueda = pyproject.get("tool", {}).get("hatch", {}).get("build", {}).get("targets", {}).get("wheel", {})
    declaradas = [carpeta / ruta for ruta in rueda.get("packages", [])]
    if declaradas:
        return [d for d in declaradas if d.is_dir()]
    if (carpeta / "src").is_dir():
        return [carpeta / "src"]
    return sorted(d for d in carpeta.iterdir() if d.is_dir() and (d / "__init__.py").is_file()
                  and d.name not in CARPETAS_QUE_NO_SE_INSTALAN and not d.name.startswith("."))


def revisar_imports_hermanos(carpeta: Path, pyproject: dict) -> list[str]:
    """Código instalable que busca otras herramientas con sys.path.insert en carpetas hermanas (N-ECO-01).

    Mira también los paquetes que no están en `src/` (alucarD, idkfa): antes solo se revisaba `src/`.
    """
    ocultos = sorted(str(archivo.relative_to(carpeta)) for paquete in carpetas_del_paquete(carpeta, pyproject)
                     for archivo in paquete.rglob("*.py")
                     if "sys.path.insert" in archivo.read_text(encoding="utf-8", errors="replace"))
    if not ocultos:
        return []
    return [f"importa carpetas hermanas con sys.path.insert en {ocultos} "
            "(declarar la dependencia como extra con referencia git, N-ECO-01)"]


def revisar_dependencias(proyecto: dict) -> list[str]:
    """Dependencias entre herramientas: siempre `paquete @ git+…` fijada a un commit o tag (N-ECO-01)."""
    problemas = []
    requisitos = list(proyecto.get("dependencies", []))
    for extra, lista in proyecto.get("optional-dependencies", {}).items():
        requisitos += [f"{r}  (extra {extra})" for r in lista]
    for requisito in requisitos:
        m = RE_REFERENCIA_GIT.search(requisito)
        if m and not (m["ref"] and RE_REF_FIJADA.match(m["ref"])):
            problemas.append(f"la referencia git no está fijada a un commit completo ni a un tag vX.Y.Z: {requisito}")
    return problemas


def revisar_urls(proyecto: dict, url: str) -> list[str]:
    """Las URLs de GitHub de `[project.urls]` apuntan al repositorio del manifiesto (N-ECO-11).

    Siete paquetes declaraban un repo en INGCOM-UNRN-P1 que no existe (una mudanza que no se hizo).
    """
    base = url.removesuffix(".git").lower()
    ajenas = [f"{clave} = {valor}" for clave, valor in proyecto.get("urls", {}).items()
              if "github.com" in valor and not valor.removesuffix(".git").lower().startswith(base)]
    return [f"[project.urls] no apunta al repositorio del manifiesto ({url}): {', '.join(ajenas)}"] if ajenas else []


def _commit_existe(carpeta: Path, ref: str) -> bool:
    return subprocess.run(["git", "-C", str(carpeta), "cat-file", "-e", f"{ref}^{{commit}}"],
                          capture_output=True).returncode == 0


def _normalizar_url(url: str) -> str:
    return url.removesuffix(".git").rstrip("/").lower()


def pines_entre_repos(raiz: Path, repos: list[Repo]) -> tuple[list[str], dict[str, dict[str, list[str]]]]:
    """Referencias git a otras herramientas: las que apuntan a un commit que no existe en el clon de
    esa herramienta (no se hizo el push, o se reescribió la historia) y la divergencia de pines.

    En el CI los repos se clonan frescos desde GitHub: un commit que sólo existe en la máquina de
    quien subió el pin aparece acá. Pasó con cast-tools-common en la Ola 24.
    """
    por_url = {_normalizar_url(r.url): r for r in repos if r.url}
    problemas: list[str] = []
    divergencia: dict[str, dict[str, list[str]]] = {}
    for repo in repos:
        pyproject = raiz / repo.ruta / "pyproject.toml"
        if not pyproject.exists():
            continue
        proyecto = tomllib.loads(pyproject.read_text(encoding="utf-8")).get("project", {})
        requisitos = list(proyecto.get("dependencies", []))
        for lista in proyecto.get("optional-dependencies", {}).values():
            requisitos += lista
        for requisito in requisitos:
            m = RE_REFERENCIA_GIT.search(requisito)
            if not m or not m["ref"]:
                continue
            destino = por_url.get(_normalizar_url(m["url"]))
            if destino is None:
                continue
            divergencia.setdefault(destino.nombre, {}).setdefault(m["ref"], []).append(repo.nombre)
            clon = raiz / destino.ruta
            if (clon / ".git").exists() and not _commit_existe(clon, m["ref"]):
                problemas.append(f"{repo.nombre}: fija {destino.nombre} a {m['ref'][:12]}, que no existe en "
                                 f"{destino.url} (¿falta el push?)")
    return problemas, {k: v for k, v in divergencia.items() if len(v) > 1}


def copias_de_catedra(raiz: Path, repos: list[Repo]) -> tuple[list[str], list[str]]:
    """Librerías de la cátedra copiadas en otro repo (`libs/<nombre>/.catedra`, como p1_test en
    plantilla-TP): cada archivo tiene que ser el del commit declarado (problema si no) y se avisa
    si el repo de origen cambió `include/` o `src/` después de ese commit (Ola 30)."""
    por_url = {_normalizar_url(r.url): r for r in repos if r.url}
    problemas: list[str] = []
    avisos: list[str] = []
    for repo in repos:
        carpeta = raiz / repo.ruta
        for marca in sorted(carpeta.glob("libs/*/.catedra")) if carpeta.is_dir() else []:
            copia = marca.parent
            nombre = f"{repo.nombre}/{copia.relative_to(carpeta)}"
            try:
                datos = tomllib.loads(marca.read_text(encoding="utf-8"))
                url, commit = str(datos["repositorio"]), str(datos["commit"])
            except (tomllib.TOMLDecodeError, KeyError) as exc:
                problemas.append(f"{nombre}: .catedra inválido ({exc}); se espera repositorio = \"…\" y commit = \"…\"")
                continue
            origen = por_url.get(_normalizar_url(url))
            clon = raiz / origen.ruta if origen else None
            if clon is None or not (clon / ".git").exists():
                avisos.append(f"{nombre}: no se puede comparar con {url} (no está clonado)")
                continue
            if not _commit_existe(clon, commit):
                problemas.append(f"{nombre}: el commit {commit[:12]} no existe en {url}")
                continue
            for archivo in sorted(copia.rglob("*")):
                rel = archivo.relative_to(copia)
                if not archivo.is_file() or rel.name == ".catedra" or rel.parts[0] == "build":
                    continue
                original = subprocess.run(["git", "-C", str(clon), "show", f"{commit}:{rel.as_posix()}"],
                                          capture_output=True)
                if original.returncode != 0:
                    problemas.append(f"{nombre}: {rel} no está en {origen.nombre}@{commit[:12]}")
                elif original.stdout != archivo.read_bytes():
                    problemas.append(f"{nombre}: {rel} difiere de {origen.nombre}@{commit[:12]} (la copia no se edita)")
            cambios = _git(clon, "diff", "--name-only", commit, "HEAD", "--", "include", "src")
            if cambios:
                avisos.append(f"{nombre}: {origen.nombre} cambió después de {commit[:12]} "
                              f"({len(cambios.splitlines())} archivos en include/ o src/): conviene actualizar la copia")
    return problemas, avisos


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
            if repo.estado not in NO_SE_CLONAN:  # esos no se clonan: que falten es lo esperado
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
            datos = tomllib.loads(pyproject.read_text(encoding="utf-8"))
            proyecto = datos["project"]
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
            problemas += [f"{repo.nombre}: {p}" for p in revisar_versionado(carpeta, proyecto)]
            problemas += [f"{repo.nombre}: {p}" for p in revisar_urls(proyecto, repo.url)]
            problemas += [f"{repo.nombre}: {p}" for p in revisar_dependencias(proyecto)]
            if repo.estado == "activo":
                problemas += [f"{repo.nombre}: {p}" for p in revisar_imports_hermanos(carpeta, datos)]

    # 3. La copia del manifiesto que mother incluye (la usa con --sin-red y sin conexión) tiene
    #    que ser esta: si quedó vieja, mother instala o salta repos con estados viejos (N-ECO-25).
    copia_mother = raiz / "mother" / "src" / "mother" / "ecosistema.toml"
    if copia_mother.exists() and copia_mother.read_bytes() != Path(args.manifiesto).read_bytes():
        problemas.append(f"mother: la copia incluida ({copia_mother.relative_to(raiz)}) difiere de "
                         f"{args.manifiesto}; actualizala copiando el manifiesto encima")

    # 4. Modo estricto (CI programado): un repo activo que no se clonó es un error, y los pines a
    #    otras herramientas tienen que existir en su repositorio.
    if getattr(args, "estricto", False):
        problemas += avisos
        avisos = []
        pines, divergencia = pines_entre_repos(raiz, repos)
        problemas += pines
        copias, avisos_copias = copias_de_catedra(raiz, repos)
        problemas += copias
        for aviso in avisos_copias:
            print(f"· {aviso}")
        if divergencia:
            print("Pines distintos de una misma herramienta (informativo: cada una sube el suyo cuando lo necesita):")
            for nombre, refs in sorted(divergencia.items()):
                detalle = "; ".join(f"{ref[:8]} ← {', '.join(sorted(quienes))}" for ref, quienes in refs.items())
                print(f"  · {nombre}: {detalle}")

    for aviso in avisos:
        print(f"· {aviso}")
    for problema in problemas:
        print(f"✗ {problema}")
    if problemas:
        print(f"\n{len(problemas)} inconsistencia(s) entre ecosistema.toml y {raiz}.", file=sys.stderr)
        return 1
    print(f"✓ ecosistema.toml coherente con {raiz} ({len(repos)} repositorios).")
    return 0


def _git(carpeta: Path, *args: str) -> str:
    salida = subprocess.run(["git", "-C", str(carpeta), *args], capture_output=True, text=True)
    return salida.stdout.strip() if salida.returncode == 0 else ""


def estado_local(carpeta: Path) -> dict:
    """Versión, último tag, commits desde el tag, sin push y sin commitear, y último commit."""
    version = ""
    if (carpeta / "pyproject.toml").exists():
        version = tomllib.loads((carpeta / "pyproject.toml").read_text(encoding="utf-8")).get("project", {}).get("version", "")
    tag = _git(carpeta, "describe", "--tags", "--abbrev=0")
    ultimo = _git(carpeta, "log", "-1", "--format=%h%x09%cs%x09%s")
    hash_, fecha, mensaje = (ultimo.split("\t", 2) + ["", "", ""])[:3]
    sin_push = _git(carpeta, "rev-list", "--count", "@{upstream}..HEAD")
    return {
        "version": version,
        "tag": tag,
        "publicada": bool(version) and tag in (f"v{version}", version),
        "desde_tag": int(_git(carpeta, "rev-list", "--count", f"{tag}..HEAD") or 0) if tag else None,
        "sin_push": int(sin_push) if sin_push else None,
        "sin_commitear": len([ln for ln in _git(carpeta, "status", "--porcelain").splitlines() if ln.strip()]),
        "ultimo_commit": {"hash": hash_, "fecha": fecha, "mensaje": mensaje},
    }


def estado_ci(url: str) -> dict:
    """Último CI de main con gh: resultado general y por sistema (jobs con windows/ubuntu/linux/macos)."""
    repo = url.removeprefix("https://github.com/").removesuffix(".git")
    corrida = subprocess.run(["gh", "run", "list", "-R", repo, "-b", "main", "-L", "1",
                              "--json", "databaseId,conclusion,status,workflowName"], capture_output=True, text=True)
    if corrida.returncode != 0:
        return {"error": (corrida.stderr.strip().splitlines() or ["gh falló"])[-1]}
    lista = json.loads(corrida.stdout or "[]")
    if not lista:
        return {"resultado": "sin CI"}
    ultima = lista[0]
    resultado = {"resultado": ultima.get("conclusion") or ultima.get("status"), "workflow": ultima.get("workflowName")}
    # El sistema sale de las etiquetas de `runs-on` (ubuntu-24.04, windows-latest…): el nombre del
    # job no siempre lo dice.
    trabajos = subprocess.run(["gh", "api", f"repos/{repo}/actions/runs/{ultima['databaseId']}/jobs?per_page=100"],
                              capture_output=True, text=True)
    if trabajos.returncode == 0:
        for job in json.loads(trabajos.stdout).get("jobs", []):
            etiquetas = " ".join([job.get("name", ""), *job.get("labels", [])]).lower()
            for sistema, claves in (("windows", ("windows",)), ("linux", ("ubuntu", "linux")), ("macos", ("macos",))):
                if any(c in etiquetas for c in claves):
                    previo = resultado.get(sistema)
                    # Con varios jobs del mismo sistema, uno que falla manda.
                    if previo in (None, "success", "skipped"):
                        resultado[sistema] = job.get("conclusion") or job.get("status")
    return resultado


_ICONOS = {"success": "✓", "failure": "✗", "cancelled": "∅", "skipped": "–", None: "·"}


def cmd_tablero(args, repos: list[Repo]) -> int:
    from concurrent.futures import ThreadPoolExecutor

    raiz = Path(args.raiz).resolve()
    elegidos = [r for r in filtrar(repos, args.perfil, None, ["activo"]) if (raiz / r.ruta / ".git").exists()]
    filas = [{"repo": r.nombre, **estado_local(raiz / r.ruta)} for r in elegidos]
    if args.ci:
        if not shutil.which("gh"):
            print("Falta gh (GitHub CLI) para --ci.", file=sys.stderr)
            return 2
        with ThreadPoolExecutor(max_workers=8) as pool:
            for fila, ci in zip(filas, pool.map(lambda r: estado_ci(r.url), elegidos), strict=True):
                fila["ci"] = ci
    if args.json:
        print(json.dumps({"schema_version": "1.0.0", "repos": filas}, ensure_ascii=False, indent=2))
        return 0

    columnas = ["repo", "versión", "tag", "+tag", "sin push", "local", "último commit"] + (["CI", "Linux", "Win"] if args.ci else [])
    tabla = []
    for f in filas:
        fila = [f["repo"], f["version"] or "—", (f["tag"] or "—") + ("" if f["publicada"] or not f["version"] else " ≠"),
                "—" if f["desde_tag"] is None else str(f["desde_tag"]),
                "—" if f["sin_push"] is None else str(f["sin_push"]),
                str(f["sin_commitear"]) if f["sin_commitear"] else "",
                f"{f['ultimo_commit']['hash']} {f['ultimo_commit']['fecha']}"]
        if args.ci:
            ci = f.get("ci", {})
            fila += [ci.get("error", "")[:18] or _ICONOS.get(ci.get("resultado"), str(ci.get("resultado"))),
                     _ICONOS.get(ci.get("linux"), str(ci.get("linux"))),
                     _ICONOS.get(ci.get("windows"), str(ci.get("windows")))]
        tabla.append(fila)
    anchos = [max(len(str(x)) for x in col) for col in zip(columnas, *tabla, strict=False)]
    print("  ".join(c.ljust(a) for c, a in zip(columnas, anchos, strict=True)))
    print("  ".join("─" * a for a in anchos))
    for fila in tabla:
        print("  ".join(str(x).ljust(a) for x, a in zip(fila, anchos, strict=True)))
    sin_push = [f["repo"] for f in filas if f["sin_push"]]
    sin_publicar = [f["repo"] for f in filas if f["version"] and not f["publicada"]]
    print(f"\n{len(filas)} repos · {len(sin_push)} con commits sin push · {len(sin_publicar)} con versión sin tag"
          " (≠: el último tag no es la versión del pyproject)")
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
    p_verificar.add_argument("--estricto", action="store_true",
                             help="un repo activo sin clonar es error y los pines a otras herramientas tienen que existir")

    p_tablero = sub.add_parser("tablero", help="estado de cada repositorio: versión, tag, commits sin push, CI")
    p_tablero.add_argument("--raiz", default=str(P1_TOOLS.parent))
    p_tablero.add_argument("--perfil", action="append")
    p_tablero.add_argument("--ci", action="store_true", help="consultar con gh el último CI de main (Linux y Windows)")
    p_tablero.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    _, repos = cargar(Path(args.manifiesto))
    return {"listar": cmd_listar, "instalar": cmd_instalar, "sistema": cmd_sistema,
            "verificar": cmd_verificar, "tablero": cmd_tablero}[args.comando](args, repos)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
