#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# run.sh — Start the Student Management API locally
# Usage: bash scripts/run.sh [--seed]
# ─────────────────────────────────────────────────────────────────────────────

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "════════════════════════════════════════"
echo "  🎓 Student Management API"
echo "════════════════════════════════════════"

# Load .env if it exists
if [ -f ".env" ]; then
    echo "📄 Loading .env..."
    export $(grep -v '^#' .env | xargs)
fi

# Optional seed
if [[ "$1" == "--seed" ]]; then
    echo "🌱 Seeding database..."
    python scripts/seed_data.py
fi

echo ""
echo "🚀 Starting server at http://localhost:8000"
echo "📖 API Docs:  http://localhost:8000/docs"
echo "❤️  Health:    http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop."
echo ""

uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --reload-dir app
