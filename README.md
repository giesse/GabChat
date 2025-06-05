# GabChat Project

GabChat is a web application that allows users to chat with Google's Gemini AI. It uses Firebase for user authentication (Google Sign-In) and Firestore to securely store and manage user-specific Gemini API keys, enabling personalized AI interaction.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3
*   Flask
*   Firebase Admin SDK
*   A Firebase project with Google Sign-In enabled.
*   A `firebase-service-account-key.json` file from your Firebase project (required for connecting to a live Firebase project; optional if using local Firebase Emulators).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/giesse/GabChat.git
    cd gabchat-project
    ```
2.  **Set up a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Place your Firebase service account key:**
    *   Download your `firebase-service-account-key.json` from the Firebase console (Project settings > Service accounts > Generate new private key).
    *   Place this file in the root directory of the project. This file is not strictly required if you intend to run primarily against local Firebase Emulators, as the backend can initialize without it in emulator mode.
5.  **Update Firebase configuration in `src/index.html`:**
    *   Open `src/index.html`.
    *   Find the `firebaseConfig` JavaScript object.
    *   Replace the placeholder values with your Firebase project's configuration (Project settings > General > Your apps > Web app > SDK setup and configuration). Note: This configuration is for the current vanilla JavaScript frontend. This process will differ when the project migrates to React.

## Usage

1.  **Run the Flask development server:**
    ```bash
    ./devserver.sh
    ```
    Or directly using Flask:
    ```bash
    flask run --host=0.0.0.0 --port=8080 
    ```
    (Ensure `main.py` is set up to be runnable as a Flask app, or adjust the command accordingly. The `devserver.sh` script likely handles this.)

2.  Open your browser and navigate to `http://localhost:8080` (or the port specified).
3.  Sign in with your Google account.
4.  Input your Gemini API key when prompted.
5.  Start chatting with the Gemini AI.

## Project Structure

*   `main.py`: The main Flask application file. Handles backend logic, including Firebase authentication, Firestore operations for API keys, and Gemini API interaction.
*   `src/`: Contains the frontend files for the current vanilla JavaScript application.
    *   `index.html`: The main HTML file for the user interface.
    *   `script.js`: JavaScript for frontend logic, Firebase integration (auth, Firestore), and API calls.
    *   `style.css`: CSS styles for the application.
*   `requirements.txt`: A list of Python dependencies for the project.
*   `firebase-service-account-key.json`: Firebase service account key. Required for connecting to a live Firebase project; optional if using local Firebase Emulators. (Ensure this is not committed to public repositories if it contains sensitive credentials).
*   `TODO.md`: A list of tasks, current progress, and future plans for the project.
*   `devserver.sh`: A shell script to easily run the Flask development server.
*   `firebase.json`: Configuration for Firebase Hosting and Emulators.
*   `pytest.ini`: Configuration file for Pytest.
*   `tests/`: Contains automated tests.
    *   `backend/`: Backend unit and integration tests for the Flask application.
*   `README.md`: This file.

## Key Features Implemented

*   **User Authentication:** Secure sign-in with Google via Firebase Authentication.
*   **Backend Token Verification:** Robust verification of Firebase ID tokens on the backend.
*   **Gemini API Key Management:**
    *   Secure storage of user-specific Gemini API keys in Firestore, linked to their Firebase UID.
    *   Functionality for users to add, update (by re-saving), and delete their API key.
    *   Backend endpoints (`/api/gemini-key`) for managing API keys.
*   **AI Chat Functionality:**
    *   Interaction with the Gemini API using the user's stored API key.
    *   Backend endpoint (`/api/chat`) to handle chat requests and communicate with the Gemini API.
*   **Vanilla JS Frontend:** A functional frontend (`src/index.html`, `src/script.js`) providing UI for all implemented features.

## Next Steps

The project is currently focused on a significant frontend overhaul. The most up-to-date and detailed plans can be found in `TODO.md`. Key upcoming developments include:

*   **Frontend Migration to React:**
    *   The existing vanilla JavaScript frontend will be replaced with a modern, component-based UI using React.
    *   This involves setting up a new React project (e.g., using Vite) within the `src/` directory.
*   **Flask-CORS Integration:**
    *   Configure `Flask-CORS` in `main.py` to allow requests from the React development server, which will run on a different port/domain during development.
*   **React Component Development:**
    *   Re-implement core UI features in React, including:
        *   Authentication flow (Google Sign-In with Firebase SDK for React).
        *   Gemini API Key management UI.
        *   Chat interface (message display, input, sending messages).
*   **Development Workflow Adjustments:**
    *   Establish a workflow where the React development server (with Hot Module Replacement) runs alongside the Flask API server.

For more granular tasks and future considerations, please refer to `TODO.md`.

## Automated Testing

The project includes automated tests to ensure reliability and catch regressions:

*   **Backend Unit/Integration Tests:**
    *   Located in the `tests/backend/` directory.
    *   These tests use Pytest to verify the functionality of the Flask API endpoints, authentication logic, and Firestore interactions in `main.py`.
    *   They are designed to be run regularly during development.

*   **Frontend End-to-End (E2E) Tests:**
    *   These are planned for implementation after the migration to the React frontend.
    *   The goal will be to test user flows such as authentication, API key management, and chat functionality from the UI perspective.
    *   Tools like Playwright or Cypress are being considered. (Refer to `TODO.md` for specifics).

## Contributing

Contributions are welcome! Please refer to `TODO.md` for current tasks and future plans. If you'd like to contribute, please fork the repository and submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

