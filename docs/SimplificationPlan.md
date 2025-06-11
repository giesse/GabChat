# Environment Simplification Plan

This document outlines the plan to simplify the local development environment for the GabChat project by removing Nix and the Python virtual environment in favor of a more standard devcontainer setup.

## Motivation

The current setup using Nix and a Python venv adds unnecessary complexity, especially when the devcontainer already provides a consistent and isolated environment. This simplification will make the project easier to set up, understand, and maintain.

## The Plan

1.  **Modify `.devcontainer/devcontainer.json`**
    *   Remove the `nix` feature.
    *   Add devcontainer features for `python`, `firebase`, `node`, and `java`.
    *   Update the `postCreateCommand` to install dependencies directly.

    **New `.devcontainer/devcontainer.json`:**
    ```json
    {
      "name": "GabChat Dev Container",
      "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
      "features": {
        "ghcr.io/devcontainers/features/python:1": {
          "version": "3.12"
        },
        "ghcr.io/devcontainers/features/firebase:1": {},
        "ghcr.io/devcontainers/features/node:1": {
          "version": "20"
        },
        "ghcr.io/devcontainers/features/java:1": {
          "version": "latest"
        }
      },
      "postCreateCommand": "pip install -r requirements.txt && cd src/react-app && yarn install && cd ../..",
      "customizations": {
        "vscode": {
          "extensions": [
            "ms-python.python",
            "ms-python.debugpy",
            "saoudrizwan.claude-dev"
          ]
        }
      }
    }
    ```

2.  **Delete `shell.nix`**
    *   This file will no longer be needed and should be deleted.

3.  **Update `docs/LocalSetup.md`**
    *   Remove all references to Nix and the Python venv.
    *   Describe the new, simpler setup process which only requires opening the project in a devcontainer-compatible editor.

4.  **Update Scripts**
    *   Review and update `devserver.sh`, `run-tests.sh`, and `start-emulators.sh`.
    *   Remove the `nix-shell --run` wrapper from the commands in these scripts.
