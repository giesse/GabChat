# AI-README.md: GabChat Project Memory for Gemini Assistant

This document serves as a persistent memory for the AI assistant to keep track of the GabChat project's status, key decisions, setup, and next steps between development sessions.

## Project Goal

GabChat is a web application that allows users to authenticate using Firebase Google Sign-In and interact with a chat interface powered by a Large Language Model (LLM), using their own Gemini API key.

## Current State (as of last session)

*   **Firebase Project:** Set up and configured.
*   **Authentication:**
    *   Google Sign-In is enabled in Firebase.
    *   Frontend UI for "Sign in with Google" is implemented in `src/index.html` using the Firebase JavaScript SDK.
    *   Backend `/verify-token` endpoint in `main.py` (Flask) verifies ID tokens using Firebase Admin SDK.
    *   Auth-related tasks in `TODO.md` are complete.
*   **API Key Management (Backend):**
    *   Endpoints (`POST`, `GET`, `DELETE` for `/api/gemini-key`) are implemented in `main.py`.
    *   API keys are stored securely in **Firestore** (collection `user_gemini_keys`, document ID = Firebase UID).
    *   The backend logic uses the Firebase Admin SDK and Firestore client.
    *   The in-memory dictionary for API keys has been replaced.
*   **Automated Backend Testing:**
    *   `pytest` is used for backend tests located in `tests/backend/test_main.py`.
    *   Tests cover `/verify-token` and all `/api/gemini-key` CRUD operations.
    *   Tests run against **Firebase Emulators** (Auth and Firestore).
    *   The test environment is configured via a `pytest.ini` file (for markers) and a pytest fixture (`client_with_emulator_config`) that sets emulator environment variables and re-initializes the Firebase Admin SDK in `main.py` for the test session.
    *   All backend tests are currently **PASSING**.
*   **Frontend UI for API Key Management:** **NOT YET IMPLEMENTED.** Placeholder elements exist in `src/index.html`.

## Key Technologies & Decisions

*   **Backend:** Python, Flask.
*   **Frontend:** HTML, CSS, JavaScript (vanilla JS for now).
*   **Authentication:** Firebase Authentication (Google Sign-In).
*   **API Key Storage:** Firestore (emulator for tests and local dev with persistence, real Firestore for production).
*   **Testing:** `pytest` for backend, Firebase Emulators (Auth & Firestore).
*   **Development Server (`devserver.sh`):** Uses `python -m flask run ...` and connects to **real Firebase** by default (if service account key is present and emulator env vars are not set). It does *not* use `firebase emulators:exec` for data persistence by default, per user decision.
*   **Automated Test Execution:** Tests are run with `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`. Requires emulators to be running separately.

## Development Environment Setup Notes

*   **Virtual Environment:** Located at `.venv`. Activate with `source .venv/bin/activate`.
*   **Python Dependencies:** Listed in `requirements.txt`. Install with `pip install -r requirements.txt`.
*   **Firebase Emulators:**
    *   Configuration: `firebase.json` (Auth on port 9099, Firestore on port 8080, UI enabled).
    *   Start script: `start-emulators.sh` (starts Auth and Firestore). Should be run in a separate terminal.
    *   Data Persistence (for local development against emulators, if desired, but NOT the default for `devserver.sh`):
        `firebase emulators:exec --import=./firebase-emulator-data --export-on-exit=./firebase-emulator-data ".venv/bin/python main.py"`
*   **Running Backend Tests:** `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`.
*   **Running Local Dev Server (connects to real Firebase by default):** `./devserver.sh` (or `FLASK_DEBUG=1 ./devserver.sh` for debug mode).

## Key File Locations

*   **Main Flask App:** `main.py`
*   **Frontend:** `src/index.html`, `src/script.js`, `src/style.css`
*   **Backend Tests:** `tests/backend/test_main.py`
*   **TODO List:** `TODO.md`
*   **Emulator Config:** `firebase.json`
*   **Emulator Start Script:** `start-emulators.sh`
*   **Pytest Config:** `pytest.ini`
*   **Python Dependencies:** `requirements.txt`
*   **This AI Memory File:** `AI-README.md`

## Next Immediate Steps (from TODO.md)

1.  **Gemini API Key Management (Frontend):**
    *   Implement UI for API key input in `src/index.html` (making existing placeholder elements functional).
    *   Implement JavaScript in `src/script.js` to:
        *   Send the API key to the backend (`POST /api/gemini-key`) after user logs in and submits key.
        *   Retrieve and display the user's currently stored API key (or an indication of its presence) from the backend (`GET /api/gemini-key`) when the user info section is shown.
        *   Handle deletion of the API key via the UI and backend (`DELETE /api/gemini-key`).

## Notes for AI Assistant

*   Remember the testing command: `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`.
*   Emulators (`sh start-emulators.sh`) need to be running in a separate terminal for tests.
*   The `client_with_emulator_config` fixture in `tests/backend/test_main.py` is critical for ensuring Firebase Admin SDK in `main.py` uses the emulators during tests by deleting any existing default app and re-running `main.initialize_firebase()`.
*   `devserver.sh` connects to the *real* Firebase project by default, not the emulators with data persistence.
