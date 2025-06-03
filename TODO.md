# GabChat Project TODO

## Overall Plan

1.  **Set up Firebase Project:** Create a new project in the Firebase console. (DONE)
2.  **Enable Google Sign-In:** Configure Google Sign-In as an authentication method in the Firebase project. (DONE)
3.  **Install Firebase SDKs:**
    *   Add the Firebase Admin SDK (`firebase-admin`) to the Python backend (`requirements.txt`). (DONE)
    *   Include the Firebase JavaScript SDK in `src/index.html` for frontend authentication. (DONE)
4.  **Implement Backend Authentication Logic (Python/Flask):**
    *   Initialize Firebase Admin SDK in `main.py`. (DONE)
    *   Create an API endpoint (`/verify-token`) in `main.py` that receives an ID token from the client. (DONE)
    *   Verify the ID token using the Firebase Admin SDK in `/verify-token` to authenticate the user. (DONE)
    *   Manage user sessions (e.g., using Flask sessions or JWTs). (Future Task)
5.  **Implement Frontend Authentication UI (`src/index.html` and JavaScript):**
    *   Add a "Sign in with Google" button to `src/index.html`. (DONE)
    *   Use the Firebase JavaScript SDK to initiate the Google Sign-In popup/redirect flow. (DONE)
    *   Add Firebase project configuration to `src/index.html`. (DONE)
    *   On successful sign-in, get the ID token and send it to the backend `/verify-token` endpoint. (DONE)
    *   Handle UI changes based on authentication status (e.g., show user info, logout button). (DONE)
6.  **Gemini API Key Management:**
    *   ~~**Design a secure way for authenticated users to submit and store their Gemini API key.** This will likely involve creating a new database table/collection (e.g., in Firestore if you decide to use it) to associate API keys with user IDs.~~ (DONE - Used Firestore collection `user_gemini_keys` keyed by Firebase UID)
    *   ~~Create UI elements for users to input their API key after logging in.~~ (DONE)
    *   ~~**Implement backend logic to save and retrieve the API key for the authenticated user.**~~ (DONE - Endpoints `POST, GET, DELETE /api/gemini-key` implemented in `main.py` using Firestore, `GET` returns `{"has_key": boolean}` an `DELETE` is also functional)
    *   ~~**Gemini API Key Management (Frontend):** Implement UI for API key input in `src/index.html`. Implement JavaScript in `src/script.js` to send the API key to the backend (`POST /api/gemini-key`), retrieve/display its status (`GET /api/gemini-key`), and delete it (`DELETE /api/gemini-key`).~~ (DONE)
7.  **Chat Interface:** (In Progress)
    *   Develop the UI for users to type messages and display chat history in `src/index.html`.
    *   Implement JavaScript in `src/script.js` to send messages to a new backend endpoint and display responses.
    *   Implement a new backend endpoint in `main.py` that:
        *   Receives the user's message.
        *   Retrieves the authenticated user's Gemini API key from Firestore.
        *   Makes a request to the Gemini API using the key and the message.
        *   Returns the AI's response to the frontend.
8.  **Automated Testing:**
    *   **Backend Focus First:**
        *   Set up and configure the Firebase Emulator Suite (Auth, Firestore if used). (DONE - Emulator config, startup script, test dependencies added)
        *   Develop backend unit/integration tests for `main.py` (especially `/verify-token` and API key logic). (DONE - `/verify-token` and API key management tests implemented and passing, updated for `has_key` logic)
    *   **(Future Task) Implement E2E UI tests:** For the authentication flow and core chat functionality using a framework like Playwright or Cypress.

## Next Immediate Tasks

1.  **Chat Functionality:**
    *   Develop the UI for users to type messages and display chat history in `src/index.html`.
    *   Implement JavaScript in `src/script.js` to send messages to a new backend endpoint and display responses.
    *   Implement a new backend endpoint in `main.py` that:
        *   Receives the user's message.
        *   Retrieves the authenticated user's Gemini API key from Firestore.
        *   Makes a request to the Gemini API using the key and the message.
        *   Returns the AI's response to the frontend.

## Subsequent Tasks (Beyond immediate focus)

*   Full Gemini API integration in the backend (if not fully covered by the immediate chat task).
*   User session management (beyond simple token verification if needed).
*   E2E UI tests.
*   CI/CD Integration.

## Automated Testing - Detailed Plan

### 1. Backend Unit/Integration Tests (`tests/backend`) - **PRIORITY**

*   **Goal:** Test the Flask API endpoints in `main.py`, especially token verification and any logic related to API key management.
*   **Tools:** `pytest`, `mock` (for mocking Firebase Admin SDK calls).
*   **Steps:**
    *   **Test `/verify-token` endpoint:** (DONE)
        *   ~~Write tests that simulate requests with:~~ (DONE)
            *   ~~A valid ID token (mock `auth.verify_id_token()` to return a valid user).~~ (DONE)
            *   ~~An invalid/expired ID token (mock `auth.verify_id_token()` to raise an exception).~~ (DONE)
            *   ~~No ID token.~~ (DONE)
        *   ~~Assert that the responses are correct (e.g., status codes, JSON payloads).~~ (DONE)
    *   ~~**Test API key storage/retrieval/deletion endpoints (using Firestore Emulator):**~~ (DONE)
        *   ~~Test successful storage of an API key for an authenticated user.~~ (DONE)
        *   ~~Test retrieval of an API key status for an authenticated user.~~ (DONE)
        *   ~~Test that unauthenticated users cannot store/retrieve/delete keys.~~ (DONE)
        *   ~~Test that users cannot access other users' keys.~~ (DONE - Implicitly handled by UID-based storage)
        *   ~~Test deletion of API key for an authenticated user.~~ (DONE)
        *   ~~Test behavior when no key is stored (GET/DELETE).~~ (DONE)
    *   **Setup/Teardown:** ~~Use `pytest` fixtures to set up the Flask test client and any necessary mocks before each test.~~ (DONE - Fixture implemented and used, including Firebase Admin SDK re-initialization for emulators)
    *   **(Future) Test new `/api/chat` endpoint.**

### 2. Frontend End-to-End (E2E) Tests (`tests/e2e`) - (Future Task)

*   **Goal:** Test the complete user authentication flow and API key management from the UI perspective, interacting with the Firebase Auth Emulator.
*   **Tools:** Playwright (recommended due to its robustness and auto-wait capabilities) or Cypress.
*   **Steps:**
    *   **Install Playwright:** `npm install --save-dev playwright` (or Cypress equivalent).
    *   **Configure Frontend to use Auth Emulator:**
        *   In `src/index.html` or `src/script.js`, modify the Firebase JavaScript SDK initialization. When running E2E tests (e.g., detected by an environment variable or a specific test build), configure `firebase.auth().useEmulator('http://localhost:9099');` (or your configured Auth emulator port).
    *   **Test Scenarios:**
        *   **Successful Sign-In:**
            *   Launch the application.
            *   Click the "Sign in with Google" button.
            *   (Playwright/Cypress will need to interact with the emulated Google Sign-In.)
            *   Verify UI updates: Sign-in button hidden, user info displayed, logout button visible, API key input section becomes available.
        *   **Logout:**
            *   Perform sign-in, click "Logout", verify UI reverts.
        *   **API Key Operations (E2E):**
            *   Test successful API key submission after sign-in.
            *   Test API key status display.
            *   Test API key deletion.
        *   **(Future - When Chat is implemented)** Test sending a message and receiving a response.
    *   **Helper Scripts:**
        *   A script to run E2E tests: `npx playwright test`.

### 3. CI/CD Integration - (Align with testing strategy)

*   **Goal:** Automate the execution of all tests on every push or pull request.
*   **Steps:**
    *   Choose a CI/CD platform (e.g., GitHub Actions).
    *   Configure CI workflow: checkout, setup environments, install dependencies, start emulators, run backend tests, (future) start dev server, (future) run E2E tests, report results.

This detailed plan should provide a good roadmap for implementing automated testing in the GabChat project.
