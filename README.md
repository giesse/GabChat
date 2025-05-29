# GabChat Project

GabChat is a web application that allows users to chat with Google's Gemini AI. It uses Firebase for user authentication (Google Sign-In) and will manage user-specific Gemini API keys.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3
*   Flask
*   Firebase Admin SDK
*   A Firebase project with Google Sign-In enabled.
*   A `firebase-service-account-key.json` file from your Firebase project.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
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
    *   Place this file in the root directory of the project.
5.  **Update Firebase configuration in `src/index.html`:**
    *   Open `src/index.html`.
    *   Find the `firebaseConfig` JavaScript object.
    *   Replace the placeholder values with your Firebase project's configuration (Project settings > General > Your apps > Web app > SDK setup and configuration).

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
4.  (Upcoming feature) Input your Gemini API key when prompted.
5.  (Upcoming feature) Start chatting with the Gemini AI.

## Project Structure

*   `main.py`: The main Flask application file. Handles backend logic, including Firebase authentication and (soon) Gemini API interaction.
*   `src/index.html`: The frontend HTML, CSS, and JavaScript for the chat interface and Firebase integration.
*   `requirements.txt`: A list of Python dependencies for the project.
*   `firebase-service-account-key.json`: Firebase service account key (should be kept secure and not committed to public repositories if it contains sensitive credentials).
*   `TODO.md`: A list of tasks and future plans for the project.
*   `devserver.sh`: A shell script to easily run the development server.
*   `README.md`: This file.

## Key Features Implemented

*   User authentication via Google Sign-In using Firebase.
*   Backend ID token verification.
*   Basic frontend structure for sign-in and (placeholder) chat.

## Next Steps (from TODO.md)

*   **Gemini API Key Management:**
    *   Implement UI for API key input.
    *   Create a backend endpoint to securely store API keys.
    *   Implement JavaScript to send the API key to the backend.
*   **Chat Functionality:**
    *   Implement message sending from frontend to backend.
    *   Backend retrieves user's API key and calls Gemini API.
    *   Display chat messages in the UI.

## Contributing

Contributions are welcome! Please refer to `TODO.md` for current tasks and future plans. If you'd like to contribute, please fork the repository and submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

