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
  '';
}
