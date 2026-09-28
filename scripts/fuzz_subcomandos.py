#!/usr/bin/env python3
"""Invoca cada subcomando de cada herramienta con entradas genéricas y busca tracebacks (N-ECO-05).

Una herramienta pedagógica no debería responder nunca con un traceback de
Python: ante una entrada que no corresponde tiene que explicar el problema.
Este script recorre los ejecutables activos de ecosistema.toml instalados en
el PATH, descubre sus subcomandos con `--help` y ejecuta cada uno con cuatro
formas de argumento (un .c, un .h, un directorio y dos .c), sobre una copia
descartable de los fuentes del smoke test.

Uso:
    fuzz_subcomandos.py [EJECUTABLE ...] [--salida informe.json] [--timeout SEG]

Sin ejecutables recorre todos los de las herramientas activas.

Sale con 1 si encontró algún traceback. Omite subcomandos que levantan
servidores, publican o modifican configuración global.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

P1_TOOLS = Path(__file__).resolve().parents[1]
FUENTES = P1_TOOLS / "student-smoke-test"
from ecosistema import cargar, filtrar  # scripts/ecosistema.py: Python agrega esta carpeta al path

OMITIR = {"serve", "daemon", "watch", "tui", "run-daemon", "start", "shell", "repl", "interactive", "ui",
          "browse", "record", "live", "stats", "hub", "pair", "sign", "publish", "push", "deploy", "install",
          "update", "upgrade", "init-repo", "completion", "sync", "clone", "fetch", "download", "upload",
          "send", "mail", "notify", "dashboard", "serve-dashboard", "unlock", "lock", "protect-branches",
          "install-hook", "lsp", "notify-batch", "publish-classroom", "config", "github", "moodle"}
FORMAS = [["src/data_structures.c"], ["src/data_structures.h"], ["src"], ["src/data_structures.c", "canon/data_structures_canon.c"]]
RE_TRACEBACK = re.compile(r"Traceback \(most recent call last\)")
RE_COMANDO = re.compile(r"^│ ([a-z][a-z0-9-]*)\s", re.MULTILINE)
ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="200")


def subcomandos(ejecutable: str) -> list[str]:
    salida = subprocess.run([ejecutable, "--help"], capture_output=True, text=True, timeout=60, env=ENTORNO)
    texto = salida.stdout + salida.stderr
    if "Commands" not in texto:
        return []
    return RE_COMANDO.findall(texto[texto.index("Commands"):])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ejecutables", nargs="*")
    parser.add_argument("--salida", type=Path)
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args(argv)

    _, repos = cargar()
    ejecutables = args.ejecutables or [e for r in filtrar(repos, estados=["activo"]) if r.tipo == "cli"
                                       for e in r.ejecutables if shutil.which(e)]
    resultados = []
    with tempfile.TemporaryDirectory(prefix="fuzz-subcomandos-") as tmp:
        base = Path(tmp)
        for ejecutable in ejecutables:
            for comando in subcomandos(ejecutable):
                if comando in OMITIR:
                    continue
                for forma in FORMAS:
                    trabajo = base / f"{ejecutable}-{comando}"
                    if not trabajo.exists():
                        shutil.copytree(FUENTES, trabajo, ignore=shutil.ignore_patterns("build"))
                    try:
                        proc = subprocess.run([ejecutable, comando, *forma], cwd=trabajo, capture_output=True,
                                              text=True, timeout=args.timeout, env=ENTORNO, stdin=subprocess.DEVNULL)
                        salida, rc = proc.stdout + proc.stderr, proc.returncode
                    except subprocess.TimeoutExpired:
                        salida, rc = "", "TIMEOUT"
                    traceback = bool(RE_TRACEBACK.search(salida))
                    excepcion = re.findall(r"^(\w+(?:Error|Exception)): (.*)$", salida, re.MULTILINE)
                    resultados.append({"ejecutable": ejecutable, "comando": comando, "args": forma, "rc": rc,
                                       "traceback": traceback, "excepcion": excepcion[-1] if excepcion else None})
                    if rc != 2:  # error de uso: se prueba la siguiente forma de argumentos
                        break

    con_traceback = [r for r in resultados if r["traceback"]]
    cuelgues = [r for r in resultados if r["rc"] == "TIMEOUT"]
    for r in con_traceback:
        print(f"✗ {r['ejecutable']} {r['comando']} {' '.join(r['args'])} → rc={r['rc']} {r['excepcion']}")
    for r in cuelgues:
        print(f"⏱ {r['ejecutable']} {r['comando']} {' '.join(r['args'])} → no terminó en {args.timeout}s")
    print(f"\nInvocaciones: {len(resultados)} · con traceback: {len(con_traceback)} · sin terminar: {len(cuelgues)}")
    if args.salida:
        args.salida.write_text(json.dumps(resultados, ensure_ascii=False, indent=1), encoding="utf-8")
    return 1 if con_traceback else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
