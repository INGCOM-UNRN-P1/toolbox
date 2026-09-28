"""Tests de scripts/version.py (SemVer, CHANGELOG y tags) sobre repos git temporales."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import version  # noqa: E402

LOCK = """version = 1
requires-python = ">=3.11"

[[package]]
name = "demo"
version = "{v}"
source = {{ editable = "." }}
dependencies = []

[[package]]
name = "otra"
version = "{v}"
source = {{ registry = "https://pypi.org/simple" }}
"""


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True).stdout


def _commit(repo: Path, mensaje: str) -> None:
    (repo / "archivo.txt").write_text(mensaje, encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", mensaje)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    raiz = tmp_path / "demo"
    (raiz / "src" / "demo").mkdir(parents=True)
    (raiz / "pyproject.toml").write_text('[project]\nname = "demo"\nversion = "0.1.0"\n', encoding="utf-8")
    (raiz / "src" / "demo" / "__init__.py").write_text('"""Demo."""\n\n__version__ = "0.1.0"\n', encoding="utf-8")
    (raiz / "uv.lock").write_text(LOCK.format(v="0.1.0"), encoding="utf-8")
    _git(raiz, "init", "-q", "-b", "main")
    _git(raiz, "config", "user.email", "prueba@example.com")
    _git(raiz, "config", "user.name", "Prueba")
    _commit(raiz, "chore: inicio")
    return raiz


def test_siguiente_segun_los_commits(repo):
    _commit(repo, "fix(cli): corregir algo")
    assert version.siguiente("0.1.0", version.commits(repo, None)) == "0.1.1"
    _commit(repo, "feat(cli): agregar algo")
    assert version.siguiente("0.1.0", version.commits(repo, None)) == "0.2.0"
    _commit(repo, "feat(api)!: cambiar la firma")
    assert version.siguiente("0.1.0", version.commits(repo, None)) == "0.2.0"
    assert version.siguiente("1.4.2", version.commits(repo, None)) == "2.0.0"


def test_publicar(repo, capsys):
    _commit(repo, "feat(cli): opción --json")
    _commit(repo, "fix: mensaje en español")
    _commit(repo, "docs(readme): instalación desde git")
    _commit(repo, "un commit sin formato")
    assert version.main(["publicar", str(repo), "--fecha", "2026-09-28"]) == 0

    assert 'version = "0.2.0"' in (repo / "pyproject.toml").read_text()
    assert '__version__ = "0.2.0"' in (repo / "src/demo/__init__.py").read_text()
    lock = (repo / "uv.lock").read_text()
    assert 'name = "demo"\nversion = "0.2.0"' in lock and 'name = "otra"\nversion = "0.1.0"' in lock
    changelog = (repo / "CHANGELOG.md").read_text()
    assert "## [0.2.0] - 2026-09-28" in changelog
    assert "### Agregado\n\n- **cli**: opción --json" in changelog
    assert "### Corregido\n\n- mensaje en español" in changelog
    assert "### Documentación" in changelog and "### Otros" in changelog
    assert "Primera versión con registro de cambios" in changelog
    assert _git(repo, "tag", "-l", "-n1").split() == ["v0.2.0", "demo", "0.2.0"]
    assert _git(repo, "log", "-1", "--format=%s").strip() == "chore(release): 0.2.0"


def test_la_segunda_version_solo_lista_lo_nuevo(repo):
    _commit(repo, "feat: primera")
    version.main(["publicar", str(repo), "--fecha", "2026-09-28"])
    _commit(repo, "fix: segunda")
    version.main(["publicar", str(repo), "--fecha", "2026-10-01"])
    changelog = (repo / "CHANGELOG.md").read_text()
    nueva, anterior = changelog.split("## [0.2.1] - 2026-10-01")[1].split("## [0.2.0]")
    assert "segunda" in nueva and "primera" not in nueva
    assert "Primera versión con registro" not in nueva
    assert changelog.index("[0.2.1]") < changelog.index("[0.2.0]")


def test_changelog_existente_conserva_su_historia(repo):
    (repo / "CHANGELOG.md").write_text(textwrap.dedent("""\
        # Changelog

        ## [5.10.1] - 2025-11-06

        - viejo
        """), encoding="utf-8")
    _commit(repo, "feat: nuevo")
    version.main(["publicar", str(repo), "--version", "5.11.0", "--fecha", "2026-09-28"])
    texto = (repo / "CHANGELOG.md").read_text()
    assert texto.startswith("# Changelog")
    assert texto.index("[5.11.0]") < texto.index("[5.10.1]") and "- viejo" in texto


def test_no_publica_con_cambios_sin_commitear(repo):
    (repo / "pyproject.toml").write_text('[project]\nname = "demo"\nversion = "0.1.0"\n# tocado\n')
    with pytest.raises(SystemExit, match="sin commitear"):
        version.main(["publicar", str(repo)])


def test_simular_no_modifica_nada(repo, capsys):
    _commit(repo, "feat: algo")
    version.main(["publicar", str(repo), "--simular"])
    assert "0.1.0 → 0.2.0" in capsys.readouterr().out
    assert not (repo / "CHANGELOG.md").exists() and _git(repo, "tag") == ""


def test_no_publica_si_el_changelog_esta_ignorado(repo):
    (repo / ".gitignore").write_text("/*.md\n")
    _commit(repo, "chore: ignorar los md de la raíz")
    _commit(repo, "feat: algo")
    with pytest.raises(SystemExit, match="!CHANGELOG.md"):
        version.main(["publicar", str(repo)])
    assert 'version = "0.1.0"' in (repo / "pyproject.toml").read_text()
