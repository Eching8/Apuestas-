#!/usr/bin/env bash
# Deja el repositorio en la última versión del código y con las dependencias instaladas.
# Usa main si ya incluye el chequeo de alineaciones; si no, la rama de desarrollo.
set -euo pipefail
cd "$(dirname "$0")/.."
DESARROLLO=claude/modelo-historico-futbol
git fetch -q origin main
if git cat-file -e origin/main:apuestas/chequeo.py 2>/dev/null; then
  git checkout -q -B main origin/main
else
  git fetch -q origin "$DESARROLLO"
  git checkout -q -B "$DESARROLLO" "origin/$DESARROLLO"
fi
python3 -m pip install -q -r requirements.txt
echo "Código listo en $(git rev-parse --abbrev-ref HEAD) ($(git rev-parse --short HEAD))."
