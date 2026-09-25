#!/usr/bin/env python3
"""Verifica el contrato de línea de comandos de LINEAMIENTOS §3.2 (N-ECO-04).

Para cada ejecutable comprueba:
  --help y -h           ayuda con código 0
  --version y -v        versión con código 0 (sin traceback)
  doctor                existe (código 0, o 1 si falta un componente crítico)
  doctor --json         JSON válido en stdout, con `schema_version`

Uso:
    verificar_contrato_cli.py [EJECUTABLE ...] [--json]

Sin ejecutables revisa el ejecutable principal de cada herramienta activa de
ecosistema.toml que esté en el PATH. Sale con 1 si algún ejecutable no cumple.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

from ecosistema import cargar, filtrar  # scripts/ecosistema.py (misma carpeta)

ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="200")


def correr(args: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=120, env=ENTORNO, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    return proc.returncode, proc.stdout, proc.stderr


def verificar(ejecutable: str) -> dict:
    resultado: dict = {"ejecutable": ejecutable}
    for etiqueta, args in (("--help", ["--help"]), ("-h", ["-h"]), ("--version", ["--version"]), ("-v", ["-v"])):
        rc, out, err = correr([ejecutable, *args])
        resultado[etiqueta] = rc == 0 and "Traceback" not in out + err
    rc, out, err = correr([ejecutable, "doctor"])
    resultado["doctor"] = rc in (0, 1) and "No such command" not in err and "Traceback" not in out + err
    rc, out, err = correr([ejecutable, "doctor", "--json"])
    try:
        datos = json.loads(out)
        resultado["doctor --json"] = isinstance(datos, dict) and "schema_version" in datos
    except json.JSONDecodeError:
        resultado["doctor --json"] = False
    resultado["cumple"] = all(v for k, v in resultado.items() if k != "ejecutable")
    return resultado


def main(argv: list[str]) -> int:
    como_json = "--json" in argv
    ejecutables = [a for a in argv if a != "--json"]
    if not ejecutables:
        _, repos = cargar()
        ejecutables = [r.ejecutables[0] for r in filtrar(repos, estados=["activo"]) if r.tipo == "cli"
                       and shutil.which(r.ejecutables[0])]
    resultados = [verificar(e) for e in ejecutables]
    if como_json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        columnas = ["--help", "-h", "--version", "-v", "doctor", "doctor --json"]
        print(f"{'ejecutable':16} " + " ".join(f"{c:>13}" for c in columnas))
        for r in resultados:
            print(f"{r['ejecutable']:16} " + " ".join(f"{'✓' if r[c] else '✗':>13}" for c in columnas))
        cumplen = sum(1 for r in resultados if r["cumple"])
        print(f"\nCumplen el contrato completo: {cumplen}/{len(resultados)}")
    return 0 if all(r["cumple"] for r in resultados) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
