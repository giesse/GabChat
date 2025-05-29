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

*   **Gemini API Key Management:** 
    *   Implement UI for API key input in `src/index.html` (already has placeholder elements).
    *   Create backend endpoint in `main.py` to securely store API keys (e.g., associated with Firebase UID. Consider Firestore or other database).
    *   Implement JavaScript in `src/index.html` to send the API key to the backend.
*   **Chat Functionality:**
    *   Implement message sending from frontend to a new backend endpoint.
    *   In the backend, retrieve the user's API key and use it to call the Gemini API.
    *   Display chat messages (user and AI) in the `src/index.html` UI.