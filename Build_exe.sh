#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist
cat > dist/MelonPlayer.exe <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${SCRIPT_DIR}"

if [[ -f "${SCRIPT_DIR}/../melon.html" ]]; then
  ROOT_DIR="${SCRIPT_DIR}/.."
fi

PORT="${1:-4173}"
URL="http://127.0.0.1:${PORT}/melon.html"

python3 -m http.server "${PORT}" --directory "${ROOT_DIR}" >/tmp/melonplayer_server.log 2>&1 &
SERVER_PID=$!
trap 'kill ${SERVER_PID} 2>/dev/null || true' EXIT

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "${URL}" >/dev/null 2>&1 || true
fi

echo "Serving Melon page at: ${URL}"
echo "Press Ctrl+C to stop."
wait ${SERVER_PID}
EOF

chmod +x dist/MelonPlayer.exe
echo "Built: dist/MelonPlayer.exe"
