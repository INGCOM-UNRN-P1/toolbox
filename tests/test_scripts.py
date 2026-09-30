"""Tests de los scripts de verificación del ecosistema (scripts/).

Los scripts son la red de seguridad del ecosistema (CI E2E, smoke, fuzz): un
error en ellos oculta regresiones en todas las herramientas. Se prueban con
manifiestos, documentos y ejecutables falsos creados en tmp_path.

Uso: uvx pytest tests
"""

from __future__ import annotations

import json
import os
import stat
import sys
import textwrap
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))  # los scripts se importan como módulos sueltos

import ecosistema  # noqa: E402
import fuzz_subcomandos  # noqa: E402
import readme_generado  # noqa: E402
import verificar_comandos_docs  # noqa: E402
import verificar_contrato_cli  # noqa: E402
import verificar_docs_instalacion  # noqa: E402
import verificar_enlaces_md  # noqa: E402

MANIFIESTO = """
[perfiles]
estudiante = "Herramientas del estudiante"

[[repo]]
nombre = "ripley"
tipo = "cli"
estado = "activo"
url = "https://github.com/INGCOM-UNRN-P1/ripley"
paquete = "ripley"
ejecutables = ["ripley"]
perfiles = ["estudiante"]

[[repo]]
nombre = "moodle-toolbox"
tipo = "cli"
estado = "activo"
url = "https://github.com/INGCOM-UNRN/moodle-toolbox"
paquete = "questions"
ejecutables = ["moodle-toolbox"]
extras = ["ai", "ui"]
perfiles = ["estudiante"]
"""


def _manifiesto(tmp_path: Path, texto: str = MANIFIESTO) -> Path:
    ruta = tmp_path / "ecosistema.toml"
    ruta.write_text(textwrap.dedent(texto), encoding="utf-8")
    return ruta


def _ejecutable(carpeta: Path, nombre: str, cuerpo: str) -> Path:
    ruta = carpeta / nombre
    ruta.write_text(f"#!{sys.executable}\nimport sys, json\nargs = sys.argv[1:]\n{textwrap.dedent(cuerpo)}\n",
                    encoding="utf-8")
    ruta.chmod(ruta.stat().st_mode | stat.S_IXUSR)
    return ruta


# --- ecosistema.py -----------------------------------------------------------------------

def test_requisito_git_con_y_sin_extras(tmp_path):
    _, repos = ecosistema.cargar(_manifiesto(tmp_path))
    por_nombre = {r.nombre: r for r in repos}
    assert por_nombre["ripley"].requisito_git() == "git+https://github.com/INGCOM-UNRN-P1/ripley"
    assert por_nombre["moodle-toolbox"].requisito_git() == (
        "questions[ai,ui] @ git+https://github.com/INGCOM-UNRN/moodle-toolbox")


@pytest.mark.parametrize("entrada, mensaje", [
    ('nombre = "x"\ntipo = "cli"\nestado = "activo"\nurl = "u"\npaquete = "x"', "falta `ejecutables`"),
    ('nombre = "x"\ntipo = "cli"\nestado = "activo"\nejecutables = ["x"]\npaquete = "x"', "necesita `url`"),
    ('nombre = "x"\ntipo = "inventado"\nestado = "activo"', "tipo desconocido"),
    ('nombre = "x"\ntipo = "contenido"\nestado = "activo"\nperfiles = ["nadie"]', "perfil desconocido"),
])
def test_manifiesto_invalido(tmp_path, entrada, mensaje):
    ruta = _manifiesto(tmp_path, f'[perfiles]\nestudiante = "e"\n\n[[repo]]\n{entrada}\n')
    with pytest.raises(SystemExit, match=mensaje):
        ecosistema.cargar(ruta)


def test_instalar_local_reconstruye_el_paquete(tmp_path, capsys):
    """Sin --reinstall-package, uv reutiliza la rueda cacheada y se prueba código viejo."""
    codigo = ecosistema.main(["--manifiesto", str(_manifiesto(tmp_path)), "instalar", "--local", "/raiz", "--simular"])
    salida = capsys.readouterr().out
    assert codigo == 0
    assert "uv tool install --reinstall-package ripley /raiz/ripley" in salida
    assert "--reinstall-package questions" in salida


def test_repos_retirados_no_se_clonan_ni_se_instalan(tmp_path, capsys):
    manifiesto = MANIFIESTO + textwrap.dedent("""
        [[repo]]
        nombre = "esper"
        url = "https://github.com/INGCOM-UNRN-P1/esper"
        tipo = "cli"
        paquete = "esper"
        ejecutables = ["esper"]
        perfiles = ["estudiante"]
        estado = "retirado"
        """)
    ruta = str(_manifiesto(tmp_path, manifiesto))
    ecosistema.main(["--manifiesto", ruta, "listar", "--formato", "clonar"])
    ecosistema.main(["--manifiesto", ruta, "listar", "--formato", "requisito"])
    salida = capsys.readouterr().out
    assert "ripley" in salida and "esper" not in salida


def test_repos_sin_publicar_no_se_clonan(tmp_path, capsys):
    manifiesto = MANIFIESTO + textwrap.dedent("""
        [[repo]]
        nombre = "yutani"
        url = "https://github.com/INGCOM-UNRN-P1/yutani"
        tipo = "biblioteca"
        paquete = "yutani"
        estado = "sin-publicar"
        """)
    ecosistema.main(["--manifiesto", str(_manifiesto(tmp_path, manifiesto)), "listar", "--formato", "clonar"])
    salida = capsys.readouterr().out
    assert "ripley" in salida and "yutani" not in salida


def test_instalar_desde_git_nunca_por_nombre(tmp_path, capsys):
    ecosistema.main(["--manifiesto", str(_manifiesto(tmp_path)), "instalar", "--simular"])
    for linea in capsys.readouterr().out.splitlines():
        assert "git+https://" in linea


# --- verificar_docs_instalacion.py ----------------------------------------------------------

@pytest.mark.parametrize("linea, insegura", [
    ("uv tool install ripley", True),
    ("pipx install ripley", True),
    ("uv tool install --force ripley", True),
    ("uv tool install git+https://github.com/INGCOM-UNRN-P1/ripley", False),
    ('uv tool install "questions[ai] @ git+https://github.com/INGCOM-UNRN/moodle-toolbox"', False),
    ("uv tool install --from git+https://github.com/x/ripley ripley", False),
    ("uv tool install ruff", False),
])
def test_instalacion_por_nombre(linea, insegura):
    patron = verificar_docs_instalacion.patron_inseguro({"ripley", "questions"})
    assert bool(patron.search(linea)) is insegura


# --- verificar_enlaces_md.py ----------------------------------------------------------------

def test_enlaces(tmp_path):
    (tmp_path / "existe.md").write_text("# a\n")
    (tmp_path / "capitulo.md").write_text("# c\n")
    md = tmp_path / "doc.md"
    md.write_text(textwrap.dedent("""\
        [bien](existe.md) [ancla](existe.md#seccion) [myst](capitulo) [etiqueta](sec-intro)
        [web](https://example.com) [local](#arriba)
        [absoluto](file:///home/alguien/x.md)
        [roto](falta/archivo.c)
        `[en código](falta.md)`
        ```
        [en bloque](falta2.md)
        ```
        """))
    problemas = verificar_enlaces_md.revisar(md, solo_absolutos=False)
    assert [(tipo, destino) for tipo, _, destino in problemas] == [
        ("absoluto", "file:///home/alguien/x.md"),
        ("roto", "falta/archivo.c"),
    ]
    assert [p[1] for p in problemas] == [3, 4]


def test_enlaces_ignora_dependencias_y_carpetas_ocultas(tmp_path):
    for carpeta in ("node_modules/pkg", ".docs_backup", ".github", "docs"):
        (tmp_path / carpeta).mkdir(parents=True)
        (tmp_path / carpeta / "README.md").write_text("x")
    encontrados = {p.parent.name for p in verificar_enlaces_md.archivos_md(tmp_path)}
    assert encontrados == {".github", "docs"}


# --- verificar_contrato_cli.py y fuzz_subcomandos.py ----------------------------------------

HERRAMIENTA_QUE_CUMPLE = """
if args in (["-h"], ["--help"]):
    print("Usage: falsa [OPTIONS] COMMAND\\n╭─ Commands ─╮\\n│ doctor   Diagnóstico\\n│ analizar Analiza\\n╰────────────╯")
elif args in (["--version"], ["-v"]):
    print("falsa 1.0.0")
elif args[:1] == ["doctor"]:
    informe = {"schema_version": "1.0.0", "herramienta": "falsa", "ok": True, "chequeos": []}
    print(json.dumps(informe) if "--json" in args else "todo bien")
elif args[:1] == ["analizar"]:
    if args[1:] == ["--help"]:
        print("Usage: falsa analizar ARCHIVO")
    elif args[1:] and args[1].endswith(".c"):
        raise ValueError("no se pudo analizar")
else:
    print(f"No such command '{args[0]}'.", file=sys.stderr)
    sys.exit(2)
"""


# La misma herramienta con la ayuda de Typer en español, como las que usan yutani (N-ECO-14).
HERRAMIENTA_EN_ESPANOL = HERRAMIENTA_QUE_CUMPLE.replace("Usage:", "Uso:").replace("Commands", "Comandos").replace(
    "No such command '{args[0]}'.", "No existe el comando '{args[0]}'.")


@pytest.fixture
def herramienta_falsa(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _ejecutable(bin_dir, "falsa", HERRAMIENTA_QUE_CUMPLE)
    _ejecutable(bin_dir, "falsa-es", HERRAMIENTA_EN_ESPANOL)
    _ejecutable(bin_dir, "incumple", 'print("sin contrato"); sys.exit(0 if args in (["--help"],) else 2)')
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr(verificar_contrato_cli, "ENTORNO", dict(os.environ))
    monkeypatch.setattr(fuzz_subcomandos, "ENTORNO", dict(os.environ))
    monkeypatch.setattr(verificar_comandos_docs, "ENTORNO", dict(os.environ))
    monkeypatch.setattr(readme_generado, "ENTORNO", dict(os.environ))
    verificar_comandos_docs.subcomandos.cache_clear()
    verificar_comandos_docs.acepta_como_argumento.cache_clear()
    return bin_dir


def test_contrato_cli(herramienta_falsa):
    assert verificar_contrato_cli.verificar("falsa")["cumple"] is True
    resultado = verificar_contrato_cli.verificar("incumple")
    assert resultado["cumple"] is False
    assert resultado["--help"] is True and resultado["-h"] is False


def test_fuzz_descubre_subcomandos_y_detecta_tracebacks(herramienta_falsa, tmp_path, capsys):
    assert fuzz_subcomandos.subcomandos("falsa") == ["doctor", "analizar"]
    salida = tmp_path / "fuzz.json"
    codigo = fuzz_subcomandos.main(["falsa", "--salida", str(salida)])
    assert codigo == 1
    resultados = json.loads(salida.read_text(encoding="utf-8"))
    con_traceback = [r for r in resultados if r["traceback"]]
    assert [(r["comando"], r["args"][0]) for r in con_traceback] == [("analizar", "src/data_structures.c")]
    assert con_traceback[0]["excepcion"] == ["ValueError", "no se pudo analizar"]


def test_fuzz_lista_los_subcomandos_que_aceptan_rutas_inexistentes(herramienta_falsa, tmp_path, capsys):
    """`falsa doctor no_existe_p1.c` sale con 0 (ignora el argumento): se lista para revisarlo."""
    codigo = fuzz_subcomandos.main(["falsa", "--rutas-inexistentes"])
    salida = capsys.readouterr().out
    assert codigo == 1  # por el traceback de `analizar`, no por las rutas
    assert "? falsa doctor no_existe_p1.c → 0" in salida
    assert "aceptan una ruta inexistente: 1" in salida


def test_comandos_citados(herramienta_falsa):
    herramientas = {"falsa"}
    assert verificar_comandos_docs.verificar_linea("falsa analizar main.c", herramientas) is None
    assert verificar_comandos_docs.verificar_linea("otra cosa", herramientas) is None
    error = verificar_comandos_docs.verificar_linea("falsa inexistente", herramientas)
    assert error is not None and "no existe" in error


def test_ayuda_en_espanol(herramienta_falsa):
    """Con la ayuda de Typer en español (yutani) los subcomandos se siguen viendo: antes se buscaba
    «Commands» y, al no encontrarlo, ninguna cita se verificaba ni se fuzzeaba ningún subcomando."""
    assert verificar_comandos_docs.verificar_linea("falsa-es analizar main.c", {"falsa-es"}) is None
    error = verificar_comandos_docs.verificar_linea("falsa-es inexistente", {"falsa-es"})
    assert error is not None and "no existe" in error
    assert fuzz_subcomandos.subcomandos("falsa-es") == ["doctor", "analizar"]
    assert verificar_contrato_cli.verificar("falsa-es")["cumple"] is True


# --- dependencias entre herramientas (ecosistema.py verificar) -------------------------------

def test_revisar_dependencias_exige_referencias_fijadas():
    sha = "cd3eb998193cd5bd9ea881aa9a0e19f5fe6d9a86"
    proyecto = {
        "dependencies": ["typer>=0.12", f"daedalus @ git+https://github.com/INGCOM-UNRN-P1/daedalus@{sha}"],
        "optional-dependencies": {
            "ecosistema": ["nostromo @ git+https://github.com/INGCOM-UNRN-P1/nostromo@v0.2.0"],
            "flojo": ["gaff @ git+https://github.com/INGCOM-UNRN-P1/gaff",
                      "kaneda @ git+https://github.com/INGCOM-UNRN-P1/kaneda@main"],
        },
    }
    problemas = ecosistema.revisar_dependencias(proyecto)
    assert len(problemas) == 2
    assert all("extra flojo" in p for p in problemas)


HERMANO = 'import sys\nsys.path.insert(0, "../daedalus/src")\n'


@pytest.mark.parametrize("disposicion, pyproject, archivo", [
    ("src", {}, "src/herramienta/core.py"),
    ("rueda de hatch", {"tool": {"hatch": {"build": {"targets": {"wheel": {"packages": ["herramienta"]}}}}}},
     "herramienta/core.py"),
    ("paquete en la raíz", {}, "herramienta/core.py"),
])
def test_revisar_imports_hermanos(tmp_path, disposicion, pyproject, archivo):
    """sys.path.insert en el código instalable, esté o no en src/ (alucarD e idkfa no usan src/)."""
    ruta = tmp_path / archivo
    ruta.parent.mkdir(parents=True)
    (ruta.parent / "__init__.py").write_text("", encoding="utf-8")
    ruta.write_text(HERMANO, encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "__init__.py").write_text(HERMANO, encoding="utf-8")  # los tests no se instalan

    problemas = ecosistema.revisar_imports_hermanos(tmp_path, pyproject)
    assert len(problemas) == 1 and archivo in problemas[0], disposicion

    ruta.write_text("import daedalus\n", encoding="utf-8")
    assert ecosistema.revisar_imports_hermanos(tmp_path, pyproject) == []


# --- política de versiones (ecosistema.py verificar) -----------------------------------------

def test_revisar_versionado(tmp_path):
    repo = tmp_path / "demo"
    (repo / "src" / "demo").mkdir(parents=True)
    proyecto = {"name": "demo", "version": "0.2.0", "license": {"text": "GPL-3.0-or-later"}}
    (repo / "src" / "demo" / "__init__.py").write_text('__version__ = "0.1.0"\n')
    problemas = ecosistema.revisar_versionado(repo, proyecto)
    assert any("LICENSE" in p for p in problemas)
    assert any("CHANGELOG" in p for p in problemas)
    assert any("__version__ = '0.1.0'" in p for p in problemas)

    (repo / "LICENSE").write_text("GPL")
    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## [0.2.0] - 2026-09-28\n\n## [0.1.0] - 2026-01-01\n")
    (repo / "src" / "demo" / "__init__.py").write_text('__version__ = "0.2.0"\n')
    assert ecosistema.revisar_versionado(repo, proyecto) == []

    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## [5.10.1] - 2025-11-06\n")
    assert ecosistema.revisar_versionado(repo, proyecto) == [
        "la última versión del CHANGELOG es 5.10.1 y pyproject dice 0.2.0"]


def test_revisar_versionado_plugin_con_version_fija(tmp_path):
    repo = tmp_path / "demo"
    (repo / "src" / "demo").mkdir(parents=True)
    (repo / "LICENSE").write_text("GPL")
    (repo / "CHANGELOG.md").write_text("# Changelog\n\n## [0.2.0] - 2026-09-28\n")
    (repo / "src" / "demo" / "ripley_plugin.py").write_text('class P:\n    name = "x"\n    version = "0.1.0"\n')
    proyecto = {"name": "demo", "version": "0.2.0", "license": {"text": "GPL-3.0-or-later"}}
    assert ecosistema.revisar_versionado(repo, proyecto) == [
        "src/demo/ripley_plugin.py declara version = '0.1.0' y pyproject '0.2.0'"]


# --- README: bloque generado (readme_generado.py) --------------------------------------------

def test_readme_generado(herramienta_falsa, tmp_path, capsys):
    """Requisitos por sistema y tabla de comandos desde `--help` (N-ECO-09), idempotente."""
    assert readme_generado.comandos("falsa") == [("doctor", "Diagnóstico"), ("analizar", "Analiza")]
    assert readme_generado.comandos("falsa-es") == readme_generado.comandos("falsa")  # ayuda en español

    manifiesto = MANIFIESTO + textwrap.dedent("""
        [[repo]]
        nombre = "falsa"
        url = "https://github.com/INGCOM-UNRN-P1/falsa"
        tipo = "cli"
        paquete = "falsa"
        ejecutables = ["falsa"]
        perfiles = ["estudiante"]
        sistema = ["gcc", "valgrind"]
        estado = "activo"
        """)
    raiz = tmp_path / "tools"
    (raiz / "falsa").mkdir(parents=True)
    readme = raiz / "falsa" / "README.md"
    readme.write_text("# falsa\n\nPropósito.\n\n## Licencia\n\nGPL\n", encoding="utf-8")
    ruta = str(_manifiesto(tmp_path, manifiesto))
    argumentos = ["--raiz", str(raiz), "--manifiesto", ruta, "falsa"]

    assert readme_generado.main(["verificar", *argumentos]) == 1
    assert readme_generado.main(["actualizar", *argumentos]) == 0
    texto = readme.read_text(encoding="utf-8")
    assert texto.index("## Referencia rápida") < texto.index("## Licencia")  # antes de la licencia
    assert "| `falsa doctor` | Diagnóstico |" in texto and "`sudo apt install valgrind`" in texto
    assert "no existe: usar WSL" in texto  # valgrind en Windows
    assert readme_generado.main(["verificar", *argumentos]) == 0
    assert readme_generado.main(["actualizar", *argumentos]) == 0
    assert readme.read_text(encoding="utf-8") == texto  # idempotente
