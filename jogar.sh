#!/usr/bin/env bash
# Abre o Valhen servido localmente (necessário para o jogo ler os assets de assets/).
cd "$(dirname "$0")"
PORT=8796
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/"; then
  python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
  sleep 1
fi
xdg-open "http://localhost:$PORT/" >/dev/null 2>&1 &
