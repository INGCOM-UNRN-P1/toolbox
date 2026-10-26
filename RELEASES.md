# Releases del cuatrimestre

Cómo publicar las versiones de las herramientas y fijarlas para un
cuatrimestre, de modo que todo el curso instale lo mismo con `mother`. Las
reglas de cada versión (SemVer, CHANGELOG, tag anotado) están en
[LINEAMIENTOS §7](LINEAMIENTOS.md#7-versiones-changelog-y-releases); esto es el
procedimiento completo, en orden.

Los comandos se corren desde `p1-tools/`, con los repositorios clonados como
carpetas hermanas (`python3 scripts/ecosistema.py verificar` lo comprueba).

## 1. Antes de empezar

- Todo commiteado y empujado: `mother fijar` lee lo **publicado** en GitHub, no
  los repositorios locales. Un commit sin push queda afuera de la matriz.
- El CI de cada repositorio en verde, **mirado por job**: un job con
  `continue-on-error` deja el run en «success» aunque falle.
- El E2E de p1-tools (`.github/workflows/ecosistema-e2e.yml`) en verde.

## 2. Release de cada herramienta

Para cada repositorio con cambios desde su último tag:

```bash
python3 scripts/version.py siguiente ../gaff                 # qué versión corresponde
python3 scripts/version.py publicar ../gaff --simular        # CHANGELOG y tag, sin tocar nada
python3 scripts/version.py publicar ../gaff --probar "uv run pytest -q"
git -C ../gaff push --follow-tags
```

`publicar` crea el commit `chore(release): X.Y.Z` y el tag anotado `vX.Y.Z`
localmente; con `--probar`, si los tests fallan con la versión nueva, deshace
todo. Para recorrer un perfil entero:

```bash
for repo in $(python3 scripts/ecosistema.py listar --perfil estudiante --formato carpeta); do
    python3 scripts/version.py siguiente "../$repo"
done
```

Las dependencias entre herramientas se fijan a commits publicados (por ejemplo
`yutani @ git+…@<commit>`): si se publica yutani, primero se suben las
fijaciones de quienes lo usan y después se hace el release de cada uno.

## 3. Fijar la matriz

```bash
mother fijar 2027-1 --tags > /tmp/matriz-2027-1.toml
```

Con `--tags`, cada herramienta queda fijada a su último `vX.Y.Z` publicado. Por
stderr avisa:

- `hay commits publicados después de vX.Y.Z (¿falta el release?)`: volver al
  paso 2 para esa herramienta, o aceptar el tag anterior a sabiendas;
- `sin tags vX.Y.Z, se fija el commit`: la herramienta no tiene releases; queda
  fijada a un commit (funciona, pero conviene publicar su primera versión).

Sin `--tags`, `mother fijar` toma el último commit de la rama principal de cada
repositorio.

## 4. Publicar la matriz

1. Pegar el bloque `[cuatrimestres."2027-1"]` en `ecosistema.toml` y poner
   `cuatrimestre_vigente = "2027-1"`.
2. `python3 scripts/ecosistema.py verificar`, `python3 -m pytest -q tests` y
   `mother --manifiesto ecosistema.toml auditar --remoto --exigir-vigente`: cada herramienta
   activa tiene que quedar fijada a un tag `vX.Y.Z` publicado o a un commit completo. Una rama
   (`main`) o un commit abreviado se mueven, y el E2E los rechaza (`ecosistema.py` al leer el
   manifiesto y `mother auditar --remoto` en el paso «Matriz del cuatrimestre sin ramas
   mutables»).
3. Commit, tag y push de p1-tools:

   ```bash
   git commit -am "build(ecosistema): matriz de versiones del cuatrimestre 2027-1"
   git tag -a cuatrimestre-2027-1 -m "Versiones del cuatrimestre 2027-1"
   git push --follow-tags
   ```

`mother instalar`, `actualizar` y `versiones` leen el manifiesto publicado en
p1-tools, así que desde ese momento instalan la matriz nueva.

## 5. mother sin red

mother trae una copia del manifiesto para cuando no hay red. Después del paso 4:

```bash
cp ecosistema.toml ../mother/src/mother/ecosistema.toml
git -C ../mother commit -am "build(manifiesto): matriz del cuatrimestre 2027-1"
python3 scripts/version.py publicar ../mother --probar "uv run pytest -q"
git -C ../mother push --follow-tags
(cd ../mother && python3 scripts/construir_zipapp.py --manifiesto ../p1-tools/ecosistema.toml)
gh release create vX.Y.Z ../mother/dist/mother.pyz --repo INGCOM-UNRN-P1/mother --notes-from-tag
```

El `mother.pyz` del release es el que usa `entorno` para instalar el perfil
estudiante.

## 6. Comprobar

En una máquina o contenedor limpio:

```bash
python3 mother.pyz instalar --perfil estudiante
mother versiones --perfil estudiante      # cada herramienta en la versión fijada
mother doctor --perfil estudiante
```
