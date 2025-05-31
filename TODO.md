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
    *   Design a secure way for authenticated users to submit and store their Gemini API key. This will likely involve creating a new database table/collection (e.g., in Firestore if you decide to use it) to associate API keys with user IDs.
    *   Create UI elements for users to input their API key after logging in.
    *   Implement backend logic to save and retrieve the API key for the authenticated user.
7.  **Chat Interface:**
    *   Develop the UI for users to type messages.
    *   Implement backend logic (`main.py`) that:
        *   Receives the user's message.
        *   Retrieves the authenticated user's Gemini API key.
        *   Makes a request to the Gemini API using the key and the message.
        *   Returns the AI's response to the frontend.
        *   Display the chat history (user messages and AI responses) in the UI.
8.  **Automated Testing:**
    *   **Backend Focus First:**
        *   Set up and configure the Firebase Emulator Suite (Auth, Firestore if used). (DONE - Emulator config, startup script, test dependencies added)
        *   Develop backend unit/integration tests for `main.py` (especially `/verify-token` and API key logic). (DONE - `/verify-token` tests implemented and passing)
    *   **(Future Task) Implement E2E UI tests:** For the authentication flow and core chat functionality using a framework like Playwright or Cypress.

## Next Immediate Tasks

1.  ~~**Create Firebase Project:** Go to the [Firebase console](https://console.firebase.google.com/) and create a new project for GabChat. (Manual Step)~~ (DONE)
2.  ~~**Enable Google Sign-In Method:** In the Firebase project, go to Authentication -> Sign-in method and enable Google. (Manual Step)~~ (DONE)
3.  ~~**Obtain Service Account Key:** In Firebase project settings -> Service accounts, generate a new private key JSON file. Save this securely in your project (e.g., as `firebase-service-account-key.json` and add it to `.gitignore`). (Manual Step)~~ (DONE)
4.  ~~**Add Firebase Admin SDK to `requirements.txt`**: Add `firebase-admin` to the file.~~ (DONE)
5.  ~~**Update `main.py` to initialize Firebase Admin SDK**: Add code to load the service account key and initialize the Firebase app.~~ (DONE)
6.  ~~**Create a basic HTML structure in `src/index.html`**: Include a "Sign in with Google" button and a placeholder for user information/chat interface.~~ (DONE)
7.  ~~**Draft JavaScript for Google Sign-In in `src/index.html`**: Add `<script>` tags to include Firebase JavaScript SDK and write initial code for the sign-in button to trigger Google authentication.~~ (DONE)
8.  ~~**Implement ID token verification in `/verify-token` endpoint in `main.py`**. (DONE)~~
9.  ~~**Update `src/index.html` with actual Firebase project configuration.** (DONE)~~

## Subsequent Tasks (Focus for next steps)

*   **Automated Backend Testing Implementation:** (Setup is complete)
    *   ~~**Install Firebase CLI:** If not already installed, run `npm install -g firebase-tools`.~~ (DONE - Assumed for subsequent steps)
    *   ~~**Initialize Firebase Emulators:** Run `firebase init emulators` and select "Authentication" (and "Firestore" if you decide to use it for API key storage). Configure ports if necessary.~~ (DONE - `firebase.json` created)
    *   ~~**Create a `firebase.json` configuration (if not already present/correct):** Ensure it correctly configures the emulators.~~ (DONE)
    *   ~~**Script for Starting Emulators:** Create a helper script (e.g., `start-emulators.sh`) to run `firebase emulators:start --only auth` (or `firebase emulators:start --only auth,firestore`).~~ (DONE)
    *   ~~**Add Test Dependencies to `requirements.txt`**: Add `pytest` and `mock`.~~ (DONE)
    *   ~~**Create Test Directory Structure:** e.g., `tests/backend`.~~ (DONE)
    *   ~~**Implement Backend Unit/Integration Tests (`tests/backend`):**~~ (DONE - `/verify-token` tests implemented and passing) 
*   **Gemini API Key Management:**
    *   Implement UI for API key input in `src/index.html` (already has placeholder elements).
    *   Create backend endpoint in `main.py` to securely store API keys (e.g., associated with Firebase UID. Consider Firestore or other database).
    *   Implement JavaScript in `src/index.html` to send the API key to the backend.
*   **Chat Functionality:**
    *   Implement message sending from frontend to a new backend endpoint.
    *   In the backend, retrieve the user's API key and use it to call the Gemini API.
    *   Display chat messages (user and AI) in the `src/index.html` UI.

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
    *   **(Future - When API Key storage is implemented)** Test API key storage/retrieval endpoints:
        *   Test successful storage of an API key for an authenticated user.
        *   Test retrieval of an API key for an authenticated user.
        *   Test that unauthenticated users cannot store/retrieve keys.
        *   Test that users cannot access other users' keys.
    *   **Setup/Teardown:** ~~Use `pytest` fixtures to set up the Flask test client and any necessary mocks before each test.~~ (DONE - Fixture implemented and used)

### 2. Frontend End-to-End (E2E) Tests (`tests/e2e`) - (Future Task)

*   **Goal:** Test the complete user authentication flow from the UI perspective, interacting with the Firebase Auth Emulator.
*   **Tools:** Playwright (recommended due to its robustness and auto-wait capabilities) or Cypress.
*   **Steps:**
    *   **Install Playwright:** `npm install --save-dev playwright` (or Cypress equivalent).
    *   **Configure Frontend to use Auth Emulator:**
        *   In `src/index.html`, modify the Firebase JavaScript SDK initialization. When running E2E tests (e.g., detected by an environment variable or a specific test build), configure `firebase.auth().useEmulator('http://localhost:9099');` (or your configured Auth emulator port).
    *   **Test Scenarios:**
        *   **Successful Sign-In:**
            *   Launch the application.
            *   Click the "Sign in with Google" button.
            *   (Playwright/Cypress will need to interact with the emulated Google Sign-In. For the emulator, you can often use its REST API to create a test user and then directly tell your frontend to sign in with specific credentials, or manipulate the emulator's state to simulate a successful Google Sign-In without actual UI interaction with Google's page). *This part needs careful setup with the emulator.*
            *   Verify that the UI updates:
                *   Sign-in button is hidden.
                *   User information (e.g., email) is displayed.
                *   Logout button is visible.
                *   (Future) API key input section becomes available.
        *   **Logout:**
            *   Perform a successful sign-in.
            *   Click the "Logout" button.
            *   Verify that the UI reverts to the signed-out state.
        *   **(Future - When API Key input is implemented)** Test API key submission.
        *   **(Future - When Chat is implemented)** Test sending a message and receiving a response.
    *   **Helper Scripts:**
        *   A script to run E2E tests: `npx playwright test` (after configuring `playwright.config.js`). This script should ensure the Firebase emulators and the dev server (`devserver.sh`) are running.

### 3. CI/CD Integration - (Align with testing strategy)

*   **Goal:** Automate the execution of all tests on every push or pull request.
*   **Steps:**
    *   Choose a CI/CD platform (e.g., GitHub Actions).
    *   Configure the CI workflow to:
        *   Checkout the code.
        *   Set up Python and Node.js environments.
        *   Install dependencies (`pip install -r requirements.txt`, `npm install` if/when E2E tests are added).
        *   Start Firebase Emulators (`firebase emulators:start --only auth,firestore &` - run in background).
        *   Run backend tests (`pytest tests/backend`).
        *   (Future) Start the dev server (`./devserver.sh &` - run in background).
        *   (Future) Run E2E tests (`npx playwright test`).
        *   Report test results.

This detailed plan should provide a good roadmap for implementing automated testing in the GabChat project.
