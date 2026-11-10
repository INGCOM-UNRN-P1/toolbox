# Releases del ecosistema y del cuatrimestre

Cómo publicar las versiones de las herramientas y fijarlas para una cursada,
de modo que todo el curso instale las mismas versiones con `mother`. Las reglas
de cada versión (`<año-release.minor>`, `CHANGELOG.md`, tag anotado) están en
[LINEAMIENTOS §7](LINEAMIENTOS.md#7-versiones-changelog-y-releases); este
documento define el formato único y el procedimiento completo, en orden.

Los comandos se corren desde `p1-tools/`, con los repositorios clonados como
carpetas hermanas (`python3 scripts/ecosistema.py verificar` lo comprueba).

## Esquema uniforme de tags (`<año-release.minor>`)

Tanto los repositorios individuales como la matriz del ecosistema usan una
única gramática de versión y de tag anotado (sin prefijo `v`):

```text
<año>-<release>.<minor>
```

- **`año` (`AAAA`)**: año de lanzamiento (4 dígitos, por ejemplo `2026`, `2027`).
- **`release` (`A` | `B` | `C`)**: letra en mayúscula que identifica el lanzamiento dentro del año (`A` para el primer lanzamiento anual, `B` para el segundo, `C` para un tercero o ante una ruptura incompatible dentro del mismo año).
- **`minor` (`0`, `1`, `2`, …)**: entero no negativo para cambios menores y parches dentro del mismo release (siempre explícito desde `.0`).

Ejemplos: `2027-A.0` (lanzamiento inicial), `2027-A.1` (primer parche menor sobre `2027-A`), `2027-B.0` (segundo release del año).

## 1. Antes de empezar

- Todo commiteado y empujado: `mother fijar` lee lo **publicado** en GitHub, no
  los repositorios locales. Un commit sin push queda afuera de la matriz.
- El CI de cada repositorio en verde, **mirado por workflow, job y step**: un step con
  `continue-on-error: true` deja el run en «success» aunque falle (verificable con
  `python3 ../revision/evidencia/ci_scan.py`).
- El E2E de `p1-tools` (`.github/workflows/ecosistema-e2e.yml`) en verde.

## 2. Release de cada herramienta

Para cada repositorio con cambios desde su último tag:

```bash
python3 scripts/version.py siguiente ../gaff                 # qué versión <año-release.minor> corresponde
python3 scripts/version.py publicar ../gaff --simular        # CHANGELOG y tag, sin tocar nada
python3 scripts/version.py publicar ../gaff --probar "uv run pytest -q"
git -C ../gaff push --follow-tags
```

`publicar` crea el commit `chore(release): <año-release.minor>` y el tag anotado
`<año-release.minor>` (por ejemplo `2027-A.0`) localmente; con `--probar`, si
los tests fallan con la versión nueva, deshace todo. Para recorrer un perfil
entero:

```bash
for repo in $(python3 scripts/ecosistema.py listar --perfil estudiante --formato carpeta); do
    python3 scripts/version.py siguiente "../$repo"
done
```

Las dependencias entre herramientas se fijan a tags o commits publicados (por ejemplo
`yutani @ git+…@2027-A.0`): si se publica `yutani`, primero se suben las
fijaciones de quienes lo usan y después se hace el release de cada uno.

## 3. Fijar la matriz

```bash
mother fijar 2027-A.0 --tags > /tmp/matriz-2027-A.0.toml
```

Con `--tags`, cada herramienta queda fijada a su último tag publicado. Por
stderr avisa:

- `hay commits publicados después de <tag> (¿falta el release?)`: volver al
  paso 2 para esa herramienta, o aceptar el tag anterior a sabiendas;
- `sin tags de release, se fija el commit`: la herramienta no tiene releases; queda
  fijada a un commit completo (funciona, pero conviene publicar su versión `<año-release.minor>`).

Sin `--tags`, `mother fijar` toma el último commit de la rama principal de cada
repositorio.

## 4. Publicar la matriz

1. Pegar el bloque `[cuatrimestres."2027-A.0"]` en `ecosistema.toml` y poner
   `cuatrimestre_vigente = "2027-A.0"`.
2. `python3 scripts/ecosistema.py verificar`, `python3 -m pytest -q tests` y
   `mother --manifiesto ecosistema.toml auditar --remoto --exigir-vigente`: cada herramienta
   activa tiene que quedar fijada a un tag publicado o a un commit completo de 40 caracteres. Una rama
   (`main`) o un commit abreviado se mueven, y el E2E los rechaza (`ecosistema.py` al leer el
   manifiesto y `mother auditar --remoto` en el paso «Matriz del cuatrimestre sin ramas
   mutables»).
3. Commit, tag anotado y push de `p1-tools`:

   ```bash
   git commit -am "build(ecosistema): matriz de versiones del release 2027-A.0"
   git tag -a 2027-A.0 -m "Versiones del release 2027-A.0"
   git push --follow-tags
   ```

`mother instalar`, `actualizar` y `versiones` leen el manifiesto publicado en
`p1-tools`, así que desde ese momento instalan la matriz nueva.

## 5. mother sin red

`mother` trae una copia del manifiesto para cuando no hay red. Después del paso 4:

```bash
cp ecosistema.toml ../mother/src/mother/ecosistema.toml
git -C ../mother commit -am "build(manifiesto): matriz del release 2027-A.0"
python3 scripts/version.py publicar ../mother --probar "uv run pytest -q"
git -C ../mother push --follow-tags
(cd ../mother && python3 scripts/construir_zipapp.py --manifiesto ../p1-tools/ecosistema.toml)
gh release create 2027-A.0 ../mother/dist/mother.pyz --repo INGCOM-UNRN-P1/mother --notes-from-tag
```

El `mother.pyz` del release es el que usa `entorno` para instalar el perfil
estudiante. Para laboratorios sin conexión, `mother empaquetar-offline` genera
el archivo `.tar.gz` con las ruedas y zipapps verificados por suma de integridad
SHA-256.

## 6. Comprobar

En una máquina o contenedor limpio:

```bash
python3 mother.pyz instalar --perfil estudiante
mother versiones --perfil estudiante      # cada herramienta en la versión fijada
mother doctor --perfil estudiante
```

## 7. Inmutabilidad, parches y alcance de reproducibilidad

1. **Inmutabilidad de tags:** Un tag publicado en GitHub **nunca** se borra, mueve ni sobreescribe. Están prohibidos los tags livianos (`git tag <nombre>` sin `-a`) y el re-etiquetado forzado (`git tag -f`).
2. **Procedimiento de parche (`minor`):** Si se corrige un fallo durante la cursada sobre el release `2027-A.0`:
   - se publica la herramienta afectada con el siguiente número `minor` (`2027-A.1`);
   - se agrega un bloque nuevo `[cuatrimestres."2027-A.1"]` en `ecosistema.toml`, se actualiza `cuatrimestre_vigente = "2027-A.1"` y se crea un tag anotado nuevo `2027-A.1` en `p1-tools` (el bloque y el tag `2027-A.0` quedan intactos).
3. **Alcance de reproducibilidad:** La matriz congela las referencias Git de las herramientas del ecosistema. No fija el compilador ni las herramientas nativas del sistema operativo (`gcc`, `gdb`, `valgrind`, `bwrap`), ni las dependencias transitivas de PyPI cuando se instala desde la red; para congelar también las ruedas de dependencias de Python se usa el paquete generado por `mother empaquetar-offline` (con verificación de integridad SHA-256).
