#!/usr/bin/env python3
"""Benchmark de rendimiento, perfiles de memoria RSS y control de complejidad por satélite (N-ECO-03).

Ejecuta los satélites de análisis/compilación del ecosistema sobre una copia aislada de
`student-smoke-test` y sobre cargas sintéticas escaladas (1x vs 4x) para medir:
  - tiempo de ejecución en milisegundos (mediana de N repeticiones);
  - pico de memoria residente (RSS en KiB) del proceso hijo (`RUSAGE_CHILDREN`);
  - factor de crecimiento algorítmico al multiplicar por 4 el tamaño de la entrada.

Actualiza un histórico JSON acumulativo (`--historico`) y alerta (exit code 1) cuando el
aumento de complejidad algorítmica o la regresión frente a una línea base supera el 25%
(`--umbral`, por defecto 0.25).

Uso:
    benchmark_satelites.py [SATELITE ...] [--historico ruta.json] [--salida reporte.json]
                           [--base base.json] [--umbral 0.25] [--repeticiones 3]
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

P1_TOOLS = Path(__file__).resolve().parents[1]
FUENTES = P1_TOOLS / "student-smoke-test"
ENTORNO = dict(os.environ, NO_COLOR="1", TERM="dumb", COLUMNS="200")

# Comandos canónicos de cada satélite sobre el directorio de trabajo del smoke test
COMANDOS_SATELITES: dict[str, list[str]] = {
    "gaff": ["gaff", "check", "src/", "--json"],
    "spunkmeyer": ["spunkmeyer", "detect", "src/", "--json"],
    "kaneda": ["kaneda", "audit", "src/", "--json"],
    "zhora": ["zhora", "lint", "src/", "--json"],
    "hal": ["hal", "analyze", "src/", "--json"],
    "daedalus": [
        "daedalus",
        "compile",
        "src/data_structures.c",
        "tests/test_runner.c",
        "--flags",
        "-I src",
        "--output",
        "build/bench_bin",
        "--json",
    ],
}

# Comandos que aceptan un archivo C individual para medir escalamiento 1x -> 4x
COMANDOS_ESCALAMIENTO: dict[str, list[str]] = {
    "gaff": ["gaff", "check", "{archivo}", "--json"],
    "spunkmeyer": ["spunkmeyer", "detect", "{archivo}", "--json"],
    "kaneda": ["kaneda", "audit", "{archivo}", "--json"],
    "zhora": ["zhora", "lint", "{archivo}", "--json"],
    "hal": ["hal", "analyze", "{archivo}", "--json"],
    "daedalus": ["daedalus", "compile", "{archivo}", "--output", "build/escala_bin", "--json"],
}

HELPER_MEDICION = """
import json, resource, subprocess, sys, time
cmd = sys.argv[1:]
t0 = time.perf_counter()
proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
dt_ms = (time.perf_counter() - t0) * 1000.0
rss_kb = int(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
print(json.dumps({"rc": proc.returncode, "tiempo_ms": round(dt_ms, 3), "max_rss_kb": rss_kb}))
"""


def generar_fuente_escalado(ruta: Path, bloques: int) -> None:
    """Genera un archivo C válido con `bloques` funciones independientes para medir complejidad."""
    partes = [
        "#include <stdio.h>\n",
        "#define ESCALA_VALOR(x) ((x) + 1)\n\n",
    ]
    for i in range(bloques):
        partes.append(
            f"int funcion_escala_{i}(int entrada)\n"
            "{\n"
            f"    int acumulador = ESCALA_VALOR(entrada) + {i};\n"
            "    for (int j = 0; j < 8; j++)\n"
            "    {\n"
            "        acumulador += j;\n"
            "    }\n"
            "    return acumulador;\n"
            "}\n\n"
        )
    partes.append(
        "int main(void)\n"
        "{\n"
        "    return funcion_escala_0(1);\n"
        "}\n"
    )
    ruta.write_text("".join(partes), encoding="utf-8")


def medir_comando(cmd: list[str], cwd: Path, timeout: float = 60.0) -> tuple[float, int, int]:
    """Ejecuta `cmd` en un subproceso aislado y devuelve (tiempo_ms, max_rss_kb, returncode)."""
    proc = subprocess.run(
        [sys.executable, "-c", HELPER_MEDICION, *cmd],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=ENTORNO,
        stdin=subprocess.DEVNULL,
    )
    datos = json.loads(proc.stdout.strip().splitlines()[-1])
    return float(datos["tiempo_ms"]), int(datos["max_rss_kb"]), int(datos["rc"])


def medir_satelite(
    nombre: str,
    trabajo: Path,
    repeticiones: int = 3,
    timeout: float = 60.0,
) -> dict:
    """Mide tiempo mediano, pico de memoria RSS y factor de complejidad algorítmica de un satélite."""
    cmd = COMANDOS_SATELITES[nombre]
    tiempos: list[float] = []
    rss_valores: list[int] = []
    rc_final = 0
    for _ in range(max(1, repeticiones)):
        t_ms, rss_kb, rc = medir_comando(cmd, trabajo, timeout=timeout)
        tiempos.append(t_ms)
        rss_valores.append(rss_kb)
        rc_final = rc

    # Medición de escalamiento algorítmico: N=25 funciones (1x) vs N=100 funciones (4x).
    # En un analizador lineal O(n), cuadruplicar la entrada multiplica el tiempo a lo sumo por 4x
    # (factor_complejidad = (t_4x / t_1x) / 4.0 <= 1.0). Si supera 1.0 + umbral (1.25 = +25%
    # sobre el escalamiento lineal), o si crece > 25% respecto al histórico base, se emite alerta.
    factor_complejidad = 1.0
    plantilla = COMANDOS_ESCALAMIENTO.get(nombre)
    if plantilla:
        f_1x = trabajo / "build" / f"escala_1x_{nombre}.c"
        f_4x = trabajo / "build" / f"escala_4x_{nombre}.c"
        f_1x.parent.mkdir(parents=True, exist_ok=True)
        generar_fuente_escalado(f_1x, 25)
        generar_fuente_escalado(f_4x, 100)
        cmd_1x = [arg.format(archivo=str(f_1x.relative_to(trabajo))) for arg in plantilla]
        cmd_4x = [arg.format(archivo=str(f_4x.relative_to(trabajo))) for arg in plantilla]
        t_1x, _, _ = medir_comando(cmd_1x, trabajo, timeout=timeout)
        t_4x, _, _ = medir_comando(cmd_4x, trabajo, timeout=timeout)
        factor_complejidad = round((t_4x / max(t_1x, 1.0)) / 4.0, 3)

    return {
        "satelite": nombre,
        "comando": cmd,
        "rc": rc_final,
        "tiempo_ms": round(statistics.median(tiempos), 3),
        "max_rss_kb": max(rss_valores),
        "factor_complejidad": factor_complejidad,
    }


def evaluar_alertas(
    mediciones: list[dict],
    base_por_satelite: dict[str, dict],
    umbral: float = 0.25,
) -> list[dict]:
    """Genera alertas cuando la complejidad algorítmica o el tiempo aumentan más de `umbral` (25%)."""
    alertas: list[dict] = []
    for m in mediciones:
        sat = m["satelite"]
        fc = float(m.get("factor_complejidad", 1.0))
        if fc > 1.0 + umbral:
            exceso_pct = round((fc - 1.0) * 100.0, 2)
            alertas.append({
                "satelite": sat,
                "tipo": "complejidad_algoritmica",
                "aumento_pct": exceso_pct,
                "umbral_pct": round(umbral * 100.0, 2),
                "detalle": (
                    f"{sat}: factor de complejidad {fc:.3f} supera en +{exceso_pct}% "
                    f"el límite lineal (+{umbral * 100:.0f}%)"
                ),
            })

        ref = base_por_satelite.get(sat)
        if not ref:
            continue
        t_base = float(ref.get("tiempo_ms", 0.0))
        t_act = float(m.get("tiempo_ms", 0.0))
        if t_base > 0:
            delta_t = (t_act - t_base) / t_base
            if delta_t > umbral:
                pct = round(delta_t * 100.0, 2)
                alertas.append({
                    "satelite": sat,
                    "tipo": "regresion_tiempo",
                    "aumento_pct": pct,
                    "umbral_pct": round(umbral * 100.0, 2),
                    "detalle": (
                        f"{sat}: tiempo {t_act:.1f} ms vs base {t_base:.1f} ms "
                        f"(+{pct}% > +{umbral * 100:.0f}%)"
                    ),
                })
        fc_base = float(ref.get("factor_complejidad", 0.0))
        if fc_base > 0:
            delta_fc = (fc - fc_base) / fc_base
            if delta_fc > umbral:
                pct = round(delta_fc * 100.0, 2)
                alertas.append({
                    "satelite": sat,
                    "tipo": "regresion_complejidad",
                    "aumento_pct": pct,
                    "umbral_pct": round(umbral * 100.0, 2),
                    "detalle": (
                        f"{sat}: factor de complejidad {fc:.3f} vs base {fc_base:.3f} "
                        f"(+{pct}% > +{umbral * 100:.0f}%)"
                    ),
                })
    return alertas


def actualizar_historico(ruta_historico: Path, entrada: dict) -> dict:
    """Agrega la entrada de la corrida al archivo JSON de histórico."""
    if ruta_historico.is_file():
        try:
            historico = json.loads(ruta_historico.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            historico = {"schema_version": "1.0.0", "corridas": []}
    else:
        historico = {"schema_version": "1.0.0", "corridas": []}

    if "corridas" not in historico or not isinstance(historico["corridas"], list):
        historico["corridas"] = []
    historico["corridas"].append(entrada)
    ruta_historico.parent.mkdir(parents=True, exist_ok=True)
    ruta_historico.write_text(json.dumps(historico, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return historico


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("satelites", nargs="*", help="Satélites a medir (por defecto todos los instalados).")
    parser.add_argument(
        "--historico",
        type=Path,
        default=P1_TOOLS / "benchmarks" / "historico_satelites.json",
        help="Archivo JSON donde se acumula el histórico semanal de tiempos y memoria.",
    )
    parser.add_argument("--salida", type=Path, help="Ruta opcional para guardar el reporte de esta corrida.")
    parser.add_argument("--base", type=Path, help="Archivo JSON de línea base contra el cual comparar regresiones.")
    parser.add_argument("--umbral", type=float, default=0.25, help="Umbral máximo permitido de aumento (default: 0.25 = 25%%).")
    parser.add_argument("--repeticiones", type=int, default=3, help="Repeticiones por satélite para calcular la mediana.")
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    candidatos = args.satelites or list(COMANDOS_SATELITES.keys())
    seleccionados = [s for s in candidatos if s in COMANDOS_SATELITES and shutil.which(COMANDOS_SATELITES[s][0])]

    base_por_satelite: dict[str, dict] = {}
    if args.base and args.base.is_file():
        datos_base = json.loads(args.base.read_text(encoding="utf-8"))
        lista_base = datos_base.get("satelites", [])
        if not lista_base and datos_base.get("corridas"):
            lista_base = datos_base["corridas"][-1].get("satelites", [])
        base_por_satelite = {item["satelite"]: item for item in lista_base if "satelite" in item}

    mediciones: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="bench-satelites-") as tmp:
        trabajo = Path(tmp) / "smoke"
        shutil.copytree(FUENTES, trabajo, ignore=shutil.ignore_patterns("build"))
        (trabajo / "build").mkdir(exist_ok=True)
        for sat in seleccionados:
            med = medir_satelite(sat, trabajo, repeticiones=args.repeticiones, timeout=args.timeout)
            mediciones.append(med)
            print(
                f"✓ {sat:12s}  tiempo={med['tiempo_ms']:7.1f} ms  "
                f"max_rss={med['max_rss_kb']:6d} KiB  factor_complejidad={med['factor_complejidad']:.3f}"
            )

    alertas = evaluar_alertas(mediciones, base_por_satelite, umbral=args.umbral)
    entrada = {
        "schema_version": "1.0.0",
        "fecha_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "umbral_alerta_pct": round(args.umbral * 100.0, 2),
        "satelites": mediciones,
        "alertas": alertas,
    }

    if args.historico:
        actualizar_historico(args.historico, entrada)
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(json.dumps(entrada, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for alerta in alertas:
        print(f"✗ ALERTA (> {args.umbral * 100:.0f}%): {alerta['detalle']}", file=sys.stderr)

    print(f"\nSatélites medidos: {len(mediciones)} · alertas: {len(alertas)}")
    return 1 if alertas else 0


if __name__ == "__main__":
    sys.exit(main())
