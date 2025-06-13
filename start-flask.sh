#!/bin/sh
# Start Flask dev server in the foreground
echo "Starting Flask dev server..."
python -m flask --app main run --debug
