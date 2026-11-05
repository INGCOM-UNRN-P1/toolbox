#!/usr/bin/env python3
"""Control del tono de los mensajes de las CLI (Ola 43, LINEAMIENTOS §4.2).

Recorre los textos que ve quien usa la herramienta (cadenas y docstrings de comandos, que Typer
muestra en --help) y reporta tres cosas que se pueden afirmar sin leer el contexto:

    tuteo       conjugaciones de tú o usted («debes», «asegúrate»); «asegurate» es voseo
    lazo        «bucle» o «loop»: la cátedra dice lazo
    anglicismo  término en inglés con equivalente en el apunte (ver GLOSARIO)

Un término en inglés entre paréntesis se acepta: es la glosa que enseña el nombre con el que se
lo va a encontrar afuera, como «Desborde de pila (Stack Overflow)». Se saltean las expresiones
regulares (reconocen salida de gcc o Valgrind) y el código C de los ejemplos.

Uso:
    verificar_tono.py [--raiz DIR] [--perfil P]... [HERRAMIENTA ...]
Sin herramientas revisa las CLI activas del manifiesto (de esos perfiles, si se indican) que estén
clonadas. Sale con 1 si encuentra algo.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import ecosistema

GLOSARIO = {
    "timeout": "tiempo límite",
    "testcase": "caso de prueba",
    "test case": "caso de prueba",
    "warning": "advertencia",
    "segfault": "violación de segmento",
    "stack trace": "traza de llamadas",
    "backtrace": "traza de llamadas",
    "runtime": "ejecución",
    "crash": "falla",
    "stack overflow": "desborde de pila",
    "integer overflow": "desborde de entero",
    "memory leak": "fuga de memoria",
}
TUTEO = re.compile(r"\b(tienes|debes|puedes|quieres|necesitas|asegúrate|fíjate|acuérdate|usted)\b", re.I)
LAZO = re.compile(r"\b(bucles?|loops?)\b", re.I)
ANGLICISMO = re.compile(r"\b(" + "|".join(sorted(GLOSARIO, key=len, reverse=True)) + r")(?:e?s)?\b", re.I)
ESPANIOL = re.compile(r"[áéíóúñ¿¡]|\b(el|la|los|las|de|del|que|en|un|una|para|por|con|no|se)\b", re.I)
REGEX = re.compile(r"\(\?P<|\\[dswb]|^\^|\[\^|\.\*|\\\(")
CODIGO = re.compile(r"[{};]\s*(\n|$)|\bprintf\(|#include|\bint \w+|\bgoto \w+;|<div|<pre|</|\bclass=")
# Lo que se quita antes de buscar: glosas, código entre comillas invertidas, marcas y directivas.
NEUTRO = re.compile(r"\([^()]*\)|`[^`]*`|\[![A-Z]+\]|\[/?[a-z ]+\]|#pragma \w+|--[\w-]+")


@dataclass(frozen=True)
class Hallazgo:
    archivo: Path
    linea: int
    tipo: str
    termino: str
    texto: str

    def __str__(self) -> str:
        sugerencia = f" → {GLOSARIO[self.termino.lower().rstrip('s')]}" if self.tipo == "anglicismo" else ""
        return f"{self.archivo}:{self.linea}: {self.tipo} «{self.termino}»{sugerencia}: {self.texto[:80]!r}"


def _es_comando(nodo: ast.AST) -> bool:
    return any("command" in ast.unparse(d) or "callback" in ast.unparse(d)
               for d in getattr(nodo, "decorator_list", []))


def _textos(arbol: ast.AST):
    """(línea, texto) de cada cadena visible: sin docstrings salvo los de comandos, ni patrones de `re`."""
    fuera: set[int] = set()
    for nodo in ast.walk(arbol):
        cuerpo = getattr(nodo, "body", None)
        if (isinstance(nodo, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and cuerpo
                and isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant)
                and not _es_comando(nodo)):
            fuera.add(id(cuerpo[0].value))
        if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                and isinstance(nodo.func.value, ast.Name) and nodo.func.value.id == "re"):
            fuera.update(id(sub) for arg in nodo.args[:1] for sub in ast.walk(arg))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and id(nodo) not in fuera:
            yield nodo.lineno, nodo.value


def revisar_texto(texto: str) -> list[tuple[str, str]]:
    """Los (tipo, término) de una cadena; vacío si no es una frase en español o no hay nada."""
    if " " not in texto.strip() or REGEX.search(texto) or CODIGO.search(texto) or not ESPANIOL.search(texto):
        return []
    limpio = NEUTRO.sub(" ", texto)
    return [(tipo, m.group(1)) for tipo, patron in (("tuteo", TUTEO), ("lazo", LAZO), ("anglicismo", ANGLICISMO))
            for m in patron.finditer(limpio)]


def revisar_archivo(ruta: Path) -> list[Hallazgo]:
    try:
        arbol = ast.parse(ruta.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []
    return [Hallazgo(ruta, linea, tipo, termino, texto)
            for linea, texto in _textos(arbol) for tipo, termino in revisar_texto(texto)]


def revisar_herramienta(carpeta: Path) -> list[Hallazgo]:
    return [h for ruta in sorted((carpeta / "src").rglob("*.py")) for h in revisar_archivo(ruta)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Tono de los mensajes de las CLI.")
    parser.add_argument("--raiz", type=Path, default=ecosistema.P1_TOOLS.parent)
    parser.add_argument("--perfil", action="append")
    parser.add_argument("herramientas", nargs="*")
    args = parser.parse_args(argv)
    _, repos = ecosistema.cargar()
    nombres = args.herramientas or [r.nombre for r in ecosistema.filtrar(repos, args.perfil, ["cli"], ["activo"])]
    rutas = {r.nombre: r.ruta for r in repos}
    total = 0
    for nombre in nombres:
        carpeta = args.raiz / rutas.get(nombre, nombre)
        if not carpeta.is_dir():
            continue
        hallazgos = revisar_herramienta(carpeta)
        total += len(hallazgos)
        for hallazgo in hallazgos:
            print(f"✗ {hallazgo}")
    if total:
        print(f"\n{total} texto(s) fuera de LINEAMIENTOS §4.2.", file=sys.stderr)
        return 1
    print("✓ Los mensajes de las CLI respetan LINEAMIENTOS §4.2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
