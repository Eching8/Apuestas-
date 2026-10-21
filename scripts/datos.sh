#!/usr/bin/env bash
# Guarda y recupera la base de datos y los informes en la rama "datos" del repositorio.
# Las sesiones en la nube empiezan con el disco vacío: así el historial crece día a día.
#
#   scripts/datos.sh restaurar   # rama datos -> data/apuestas.db, data/uso_api.json y reportes/
#   scripts/datos.sh guardar     # lo mismo -> rama datos (commit + push)
# uso_api.json es el registro de peticiones del día: sin él, cada sesión nueva no sabría cuánto se gastó.
set -euo pipefail
cd "$(dirname "$0")/.."
RAMA=datos

case "${1:-}" in
  restaurar)
    if ! git fetch -q origin "$RAMA" 2>/dev/null; then
      echo "Aún no existe la rama $RAMA: se empieza con una base vacía."
      exit 0
    fi
    mkdir -p data reportes
    for f in apuestas.db uso_api.json; do
      if git cat-file -e "origin/$RAMA:$f" 2>/dev/null; then
        git show "origin/$RAMA:$f" > "data/$f"
      fi
    done
    if git cat-file -e "origin/$RAMA:reportes" 2>/dev/null; then
      git archive "origin/$RAMA" reportes | tar -x -C .
    fi
    echo "Datos restaurados desde origin/$RAMA."
    ;;
  guardar)
    tmp=$(mktemp -d)
    trap 'git worktree remove --force "$tmp" 2>/dev/null || rm -rf "$tmp"' EXIT
    if git fetch -q origin "$RAMA" 2>/dev/null; then
      git worktree add -q --detach "$tmp" "origin/$RAMA"
    else
      git worktree add -q --detach "$tmp"
      (cd "$tmp" && git checkout -q --orphan "$RAMA" && git rm -rqf . && git clean -fdxq)
    fi
    for f in apuestas.db uso_api.json; do
      if [ -f "data/$f" ]; then cp "data/$f" "$tmp/$f"; fi
    done
    if [ -d reportes ]; then mkdir -p "$tmp/reportes" && cp -r reportes/. "$tmp/reportes/"; fi
    git -C "$tmp" add -A
    if git -C "$tmp" diff --cached --quiet; then
      echo "Sin cambios en los datos."
      exit 0
    fi
    git -C "$tmp" commit -qm "Datos $(date -u +%Y-%m-%dT%H:%MZ)"
    for espera in 2 4 8 16; do
      git -C "$tmp" push -q origin "HEAD:refs/heads/$RAMA" && { echo "Datos guardados en origin/$RAMA."; exit 0; }
      sleep "$espera"
    done
    echo "No se pudo subir la rama $RAMA." >&2
    exit 1
    ;;
  *)
    echo "Uso: $0 restaurar|guardar" >&2
    exit 2
    ;;
esac
