# Local Development Environment Setup

This document provides instructions for setting up the local development environment for the GabChat project using VS Code Dev Containers.

## Dev Container with Nix

This project is configured to use a VS Code Dev Container, which creates a consistent and isolated development environment. It uses [Nix](https://nixos.org/) to manage all tools and dependencies.

### How it Works

*   **`.devcontainer/devcontainer.json`**: This file instructs VS Code how to create and configure the development container.
*   **`shell.nix`**: This file tells the Nix package manager which packages to install in the environment (e.g., `python3`, `nodejs`, `yarn`, `vite`, `firebase-tools`).

### Getting Started

1.  **Open in VS Code:** When you open this project in VS Code, it will automatically detect the `.devcontainer` configuration.
2.  **Reopen in Container:** A dialog will appear asking if you want to "Reopen in Container". Click it.
3.  **Initial Setup:** The first time you open the container, it will build the environment and run the `postCreateCommand` defined in `devcontainer.json`. This command will:
    *   Create a Python virtual environment at `.venv`.
    *   Install the Python dependencies from `requirements.txt`.
    *   Install the Node.js dependencies for the React app.
4.  **Ready to Go:** Once the setup is complete, your VS Code terminal will be running inside the container with all the necessary tools available in the PATH.

## Manual Configuration

For the application to connect to your Firebase project, you must perform the following steps:

1.  **Firebase Service Account Key:** Download your service account key from the Firebase console (**Project settings > Service accounts > Generate new private key**). Save the file as `firebase-service-account-key.json` in the root of this project.
2.  **Enable Cloud Firestore API:** Ensure the Cloud Firestore API is enabled for your project in the Google Cloud Console. You can use this link, replacing `YOUR_PROJECT_ID` with your actual Firebase project ID:
    [https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID)

## Running the Application

Once inside the Dev Container, you can run the application using the provided scripts:

*   **Local Development Server:**
    ```bash
    ./devserver.sh
    ```
    This script starts both the Python Flask backend and the React frontend development server.

*   **Backend Tests:**
    ```bash
    ./run-tests.sh
    ```
    This script runs the backend `pytest` tests. *Note: This requires the Firebase emulators to be running.*

*   **Firebase Emulators:**
    ```bash
    ./start-emulators.sh
    ```
    This script starts the Firebase Auth and Firestore emulators for local testing. It should be run in a separate terminal before executing the tests.
