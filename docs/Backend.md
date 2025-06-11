# Backend Documentation

This document provides details about the Python/Flask backend for the GabChat project.

## Key Technologies

*   **Framework:** Flask
*   **Language:** Python
*   **Authentication:** Firebase Authentication (via Firebase Admin SDK)
*   **Database:** Firestore (for storing user Gemini API keys)
*   **LLM:** Google Generative AI (Gemini)

## API Endpoints

### Authentication

*   **`/verify-token`**
    *   **Method:** POST
    *   **Description:** Verifies a Firebase ID token sent from the frontend to authenticate the user.

### Gemini API Key Management

*   **`/api/gemini-key`**
    *   **Method:** `POST`
    *   **Description:** Saves a user's Gemini API key to Firestore.
    *   **Authorization:** Requires a valid Firebase ID token.
*   **`/api/gemini-key`**
    *   **Method:** `GET`
    *   **Description:** Checks if the authenticated user has a Gemini API key stored. Returns `{"has_key": boolean}`.
    *   **Authorization:** Requires a valid Firebase ID token.
*   **`/api/gemini-key`**
    *   **Method:** `DELETE`
    *   **Description:** Deletes the authenticated user's Gemini API key from Firestore.
    *   **Authorization:** Requires a valid Firebase ID token.

### Chat

*   **`/api/chat`**
    *   **Method:** POST
    *   **Description:** Takes a user message, retrieves the user's Gemini API key from Firestore, interacts with the Gemini API, and returns the AI's response.
    *   **Authorization:** Requires a valid Firebase ID token.
    *   **Error Handling:** Includes checks for missing messages, empty messages, and missing API keys.

## Development Server

The backend is started as part of the `./devserver.sh` script. It runs in the foreground on the `$PORT` specified by the environment. It connects to the **real Firebase project**, which requires:

1.  A `firebase-service-account-key.json` file in the project root.
2.  The "Cloud Firestore API" to be enabled in the Google Cloud Console for the Firebase project.

**CORS** is configured using `Flask-CORS` to allow requests from the frontend development server.
