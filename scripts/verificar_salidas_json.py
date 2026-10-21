#!/usr/bin/env python3
"""Verifica que las salidas `--json` de los analizadores cumplan la forma común de los hallazgos
(yutani.hallazgos, Ola 7 de la hoja de ruta de la revisión).

Corre gaff, daedalus, tetsuo, ripley y hal sobre los casos del smoke test estudiantil y valida
cada salida con `yutani.hallazgos.validar_salida`: la lista plana `hallazgos`, con las claves,
tipos, severidades y categorías comunes, y el `archivo` de cada uno relativo al directorio de
trabajo, con `/` y sin `./`. Es lo que consume jonesy (y cualquier otro cliente) sin distinguir
de qué herramienta vino.

Uso (yutani tiene que poder importarse, por ejemplo con uv):

    uv run --no-project --with "yutani @ git+https://github.com/INGCOM-UNRN-P1/yutani" \\
        python3 scripts/verificar_salidas_json.py [--dir student-smoke-test] [--json]

Sale con 1 si alguna salida no cumple y con 2 si yutani no tiene el validador.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="200")
SMOKE = Path(__file__).resolve().parents[1] / "student-smoke-test"


@dataclass
class Caso:
    nombre: str
    comando: list[str]
    # Texto para la entrada estándar; una función recibe el directorio de trabajo.
    entrada: str | Callable[[Path], str] | None = None
    # Los casos con errores conocidos tienen que dar al menos un hallazgo (si no, la validación
    # pasaría sin validar nada); los que dependen del entorno (libasan) no.
    exige_hallazgos: bool = True
    # Archivos (relativos al directorio de trabajo) que tienen que aparecer como `archivo`.
    archivos: set[str] = field(default_factory=set)


def _informe_asan(dir_trabajo: Path) -> str:
    """Un informe real de ASan con la ruta absoluta con la que se compiló (como lo imprime el
    programa del alumno corriendo en jonesy)."""
    fuente = (dir_trabajo / "src" / "main.c").as_posix()
    return (
        "==4242==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x502000000020 at pc 0x55d4 bp 0x7ffd "
        "sp 0x7ffc\n"
        "WRITE of size 4 at 0x502000000020 thread T0\n"
        f"    #0 0x55d4c0a1b2c3 in main {fuente}:12\n"
        "    #1 0x7f2a1b029d8f  (/lib64/libc.so.6+0x29d8f)\n\n"
        "0x502000000020 is located 0 bytes after 16-byte region [0x502000000010,0x502000000020)\n"
        "SUMMARY: AddressSanitizer: heap-buffer-overflow\n"
    )


def _stderr_gcc(fuente: str) -> Callable[[Path], str]:
    def generar(dir_trabajo: Path) -> str:
        proc = subprocess.run(["gcc", "-std=c11", "-Wall", "-Wextra", "-fsyntax-only", fuente], cwd=dir_trabajo,
                              capture_output=True, text=True, env=ENTORNO)
        return proc.stderr
    return generar


ESTILO = "failing_cases/fail_style_gaff.c"
SINTAXIS = "failing_cases/fail_syntax_daedalus.c"
CRASH = "src/crashes/crash_segv.c"

CASOS = [
    Caso("gaff check", ["gaff", "check", ESTILO, "--json"], archivos={ESTILO}),
    Caso("gaff check --stdin", ["gaff", "check", "--stdin", "--stdin-filename", ESTILO, "--json"],
         entrada=lambda d: (d / ESTILO).read_text(encoding="utf-8"), archivos={ESTILO}),
    Caso("daedalus compile", ["daedalus", "compile", SINTAXIS, "--json", "--primer-error"], archivos={SINTAXIS}),
    Caso("daedalus translate", ["daedalus", "translate", "--json", "--primer-error"], entrada=_stderr_gcc(SINTAXIS),
         archivos={SINTAXIS}),
    Caso("tetsuo translate", ["tetsuo", "translate", "--json"], entrada=_informe_asan, archivos={"src/main.c"}),
    Caso("tetsuo run", ["tetsuo", "run", CRASH, "--json"], exige_hallazgos=False),
    Caso("ripley check", ["ripley", "check", ESTILO, "--format", "json"], archivos={ESTILO}),
    Caso("hal check", ["hal", "check", CRASH, "--json"], archivos={CRASH}),
]


def validador() -> Callable[..., list[str]] | None:
    try:
        from yutani.hallazgos import validar_salida
    except ImportError:
        return None
    return validar_salida


def verificar(caso: Caso, dir_trabajo: Path, validar: Callable[..., list[str]]) -> dict[str, Any]:
    resultado: dict[str, Any] = {"caso": caso.nombre, "comando": " ".join(caso.comando), "problemas": []}
    if shutil.which(caso.comando[0]) is None:
        resultado["problemas"].append(f"{caso.comando[0]} no está en el PATH")
        return resultado
    entrada = caso.entrada(dir_trabajo) if callable(caso.entrada) else caso.entrada
    try:
        proc = subprocess.run(caso.comando, cwd=dir_trabajo, input=entrada, capture_output=True, text=True,
                              timeout=300, env=ENTORNO, stdin=None if entrada is not None else subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        resultado["problemas"].append("no terminó en 5 minutos")
        return resultado
    salida = proc.stdout
    inicio = salida.find("{")
    try:
        datos = json.loads(salida[inicio:]) if inicio >= 0 else None
    except json.JSONDecodeError as e:
        datos = None
        resultado["problemas"].append(f"la salida no es JSON ({e})")
    if datos is None:
        if not resultado["problemas"]:
            resultado["problemas"].append(f"no emitió JSON (código {proc.returncode}): {proc.stderr.strip()[:200]}")
        return resultado
    resultado["problemas"] += validar(datos, dir_trabajo)
    hallazgos = datos.get("hallazgos") if isinstance(datos, dict) else None
    if isinstance(hallazgos, list):
        resultado["hallazgos"] = len(hallazgos)
        if caso.exige_hallazgos and not hallazgos:
            resultado["problemas"].append("no informó ningún hallazgo en un caso con errores conocidos")
        sin_archivo = [h.get("id") for h in hallazgos if isinstance(h, dict) and not h.get("archivo")]
        if sin_archivo:
            resultado["problemas"].append(f"hallazgos sin «archivo»: {', '.join(map(str, sin_archivo[:5]))}")
        informados = {h.get("archivo") for h in hallazgos if isinstance(h, dict)}
        if hallazgos and caso.archivos and not caso.archivos & informados:
            resultado["problemas"].append(f"esperaba el archivo {sorted(caso.archivos)}; informó {sorted(map(str, informados))}")
    return resultado


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dir", type=Path, default=SMOKE, help="Directorio de trabajo con los casos.")
    parser.add_argument("--json", action="store_true", help="Resultado en JSON.")
    args = parser.parse_args(argv)
    validar = validador()
    if validar is None:
        print("yutani.hallazgos no tiene validar_salida: instalá yutani desde git (ver el uso).", file=sys.stderr)
        return 2
    dir_trabajo = args.dir.resolve()
    resultados = [verificar(c, dir_trabajo, validar) for c in CASOS]
    if args.json:
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        for r in resultados:
            marca = "✓" if not r["problemas"] else "✗"
            print(f"{marca} {r['caso']}: {r.get('hallazgos', 0)} hallazgo(s)")
            for p in r["problemas"][:10]:
                print(f"    {p}")
    return 1 if any(r["problemas"] for r in resultados) else 0


if __name__ == "__main__":
    raise SystemExit(main())
