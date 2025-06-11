{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.firebase-tools
    pkgs.jdk
    pkgs.nodejs
    pkgs.yarn
    pkgs.vite
    pkgs.stdenv.cc.cc.lib
  ];
  shellHook = ''
    echo "Nix-shell environment for GabChat is ready."
    # Activate Python virtual environment if it exists
    if [ -d ".venv" ]; then
      echo "Activating Python venv..."
      source .venv/bin/activate
    else
      echo "Python venv not found. Please run the setup."
    fi
  '';
}
