#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/Codigo"
source ../.venv/bin/activate
python -c "from main import app; app.run(debug=True, host='0.0.0.0', port=5001)"
