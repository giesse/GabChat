#!/bin/sh

# Start React dev server in the background
cd src/react-app
echo "Starting React dev server..."
nix-shell --run "yarn dev" > ../../react-dev-server.log 2>&1 &
cd ../..

# Start Flask dev server in the foreground
echo "Starting Flask dev server on port $PORT..."
nix-shell --run "python -m flask --app main run -p $PORT --debug"
