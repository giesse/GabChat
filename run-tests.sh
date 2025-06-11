#!/bin/bash
set -e

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Running backend tests..."
PYTHONPATH=. python -m pytest -v tests/backend

echo "Tests finished."
