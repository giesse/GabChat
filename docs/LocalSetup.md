# Local Development Environment Setup

This document provides instructions for setting up the local development environment for the GabChat project.

## Dependencies and Configuration

*   **Virtual Environment:** Located at `.venv`. Activate with `source .venv/bin/activate`.
*   **Python Dependencies:** Listed in `requirements.txt`. Install with `pip install -r requirements.txt`.
*   **Node.js, Yarn, and Vite:** Included in the Nix environment (`.idx/dev.nix`) for React development. Dependencies are installed via `yarn install` in the `src/react-app` directory during workspace setup.
*   **Firebase Service Account Key:** For the local development server (`devserver.sh`) to connect to your real Firebase project, download your service account key JSON file from Firebase console (Project settings -> Service accounts -> Generate new private key) and save it as `firebase-service-account-key.json` in the root of this project.
*   **Enable Cloud Firestore API:** For the local development server to function, ensure the Cloud Firestore API is enabled for your project in the Google Cloud Console: [https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID) (replace `YOUR_PROJECT_ID` with your actual Firebase project ID).

## Running the Application

*   **Firebase Emulators (for testing ONLY):**
    *   Configuration: `firebase.json` (Auth on port 9099, Firestore on port 8080, UI enabled).
    *   Start script: `start-emulators.sh` (starts Auth and Firestore). Should be run in a separate terminal *before running pytest*.
*   **Running Backend Tests:** `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`.
*   **Running Local Dev Server:** Run `./devserver.sh`.
    *   This script now starts both the Python Flask backend (foreground, on `$PORT`) and the React frontend dev server (background, typically on a port like 5173, logs to `react-dev-server.log`).
    *   Ensure `firebase-service-account-key.json` is present in the project root and the Cloud Firestore API is enabled for your Firebase project for the backend to function correctly.

## Troubleshooting

### vite: command not found

*   **Description:** When trying to run the React development server (e.g., via `./devserver.sh` or manually with `yarn dev` in `src/react-app`), you might encounter an error message similar to "vite: command not found". This means the Vite executable is not available in your environment's PATH.
*   **Solution:** The Vite package (`pkgs.vite`) was added to the `packages` list in the `.idx/dev.nix` file. If you pulled this change into an existing workspace, you might need to force a re-evaluation of the Nix environment. In Firebase Studio, you can try "Nix: Rebuild Environment" or restarting the workspace.
