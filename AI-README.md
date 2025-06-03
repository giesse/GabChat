# AI-README.md: GabChat Project Memory for Gemini Assistant

This document serves as a persistent memory for the AI assistant to keep track of the GabChat project's status, key decisions, setup, and next steps between development sessions.

## Project Goal

GabChat is a web application that allows users to authenticate using Firebase Google Sign-In and interact with a chat interface powered by a Large Language Model (LLM), using their own Gemini API key.

## Current State (as of this session)

*   **Firebase Project:** Set up and configured. `firebase-service-account-key.json` is required in the root for the dev server to connect to the real Firebase project. The Cloud Firestore API must be enabled in the Google Cloud Console for the project.
*   **Authentication:**
    *   Google Sign-In is enabled in Firebase.
    *   Frontend UI for "Sign in with Google" is implemented in `src/index.html` using the Firebase JavaScript SDK.
    *   Backend `/verify-token` endpoint in `main.py` (Flask) verifies ID tokens using Firebase Admin SDK.
*   **API Key Management (Backend & Frontend):**
    *   Endpoints (`POST`, `GET`, `DELETE` for `/api/gemini-key`) are implemented in `main.py` and fully functional.
    *   API keys are stored securely in **Firestore** (collection `user_gemini_keys`, document ID = Firebase UID).
    *   The `GET /api/gemini-key` endpoint returns `{"has_key": boolean}`.
    *   UI for API key input, status display, and deletion is implemented in `src/index.html` and `src/script.js` and is fully functional.
    *   All frontend API key operations include the Firebase ID token for authorization and handle responses correctly.
*   **Automated Backend Testing:**
    *   `pytest` is used for backend tests located in `tests/backend/test_main.py`.
    *   All 12 tests cover `/verify-token` and all `/api/gemini-key` CRUD operations, and are **PASSING** against Firebase Emulators.

## Key Technologies & Decisions

*   **Backend:** Python, Flask.
*   **Frontend:** HTML, CSS, JavaScript (vanilla JS for now).
*   **Authentication:** Firebase Authentication (Google Sign-In).
*   **API Key Storage:** Firestore.
*   **Testing:** `pytest` for backend. Firebase Emulators (Auth & Firestore) are used *only* for `pytest`.
*   **Development Server (`devserver.sh`):**
    *   Uses `python -m flask run ...`.
    *   Connects to the **real Firebase project**. Requires:
        1.  `firebase-service-account-key.json` in the project root.
        2.  The "Cloud Firestore API" to be enabled in the Google Cloud Console for the Firebase project.
    *   It does *not* use Firebase Emulators or `firebase emulators:exec`.
*   **Automated Test Execution:** Tests are run with `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`. Requires emulators to be running separately via `sh start-emulators.sh`.

## Development Environment Setup Notes

*   **Virtual Environment:** Located at `.venv`. Activate with `source .venv/bin/activate`.
*   **Python Dependencies:** Listed in `requirements.txt`. Install with `pip install -r requirements.txt`.
*   **Firebase Service Account Key:** For the local development server (`devserver.sh`) to connect to your real Firebase project, download your service account key JSON file from Firebase console (Project settings -> Service accounts -> Generate new private key) and save it as `firebase-service-account-key.json` in the root of this project.
*   **Enable Cloud Firestore API:** For the local development server to function, ensure the Cloud Firestore API is enabled for your project in the Google Cloud Console: [https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID) (replace `YOUR_PROJECT_ID` with your actual Firebase project ID).
*   **Firebase Emulators (for testing ONLY):**
    *   Configuration: `firebase.json` (Auth on port 9099, Firestore on port 8080, UI enabled).
    *   Start script: `start-emulators.sh` (starts Auth and Firestore). Should be run in a separate terminal *before running pytest*.
*   **Running Backend Tests:** `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`.
*   **Running Local Dev Server:** `./devserver.sh` (or `FLASK_DEBUG=1 ./devserver.sh` for debug mode). Ensure `firebase-service-account-key.json` is present and Cloud Firestore API is enabled.

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

1.  **Chat Functionality:**
    *   Develop the UI for users to type messages and display chat history in `src/index.html`.
    *   Implement JavaScript in `src/script.js` to send messages to a new backend endpoint and display responses.
    *   Implement a new backend endpoint in `main.py` that:
        *   Receives the user's message.
        *   Retrieves the authenticated user's Gemini API key from Firestore.
        *   Makes a request to the Gemini API using the key and the message.
        *   Returns the AI's response to the frontend.

## Notes for AI Assistant

*   The Firebase Emulators (`sh start-emulators.sh`) are **only for running `pytest`**. They should be started before running tests.
*   The local development server (`./devserver.sh`) connects to the **real Firebase project** and requires `firebase-service-account-key.json` in the project root and the Cloud Firestore API to be enabled. It does **not** use the emulators.
*   Remember the testing command: `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`.
*   The `client_with_emulator_config` fixture in `tests/backend/test_main.py` is critical for ensuring Firebase Admin SDK in `main.py` uses the emulators during tests.
