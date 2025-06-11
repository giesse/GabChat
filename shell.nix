{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.firebase-tools
    pkgs.jdk
    pkgs.nodejs
    pkgs.yarn
    pkgs.vite
  ];
  shellHook = ''
    echo "Nix-shell environment for GabChat is ready."
  '';
}
