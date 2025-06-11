#!/bin/bash
set -e


echo "Running backend tests..."
PYTHONPATH=. python -m pytest -v tests/backend

echo "Tests finished."
