# Local Development Environment Setup

This document provides instructions for setting up the local development environment for the GabChat project using VS Code Dev Containers.

## Dev Container

This project is configured to use a VS Code Dev Container, which creates a consistent and isolated development environment.

### How it Works

The **`.devcontainer/devcontainer.json`** file instructs VS Code how to create and configure the development container. It uses devcontainer features to install all necessary tools like Python, Node.js, and Firebase CLI directly into the container.

### Getting Started

1.  **Open in VS Code:** When you open this project in VS Code, it will automatically detect the `.devcontainer` configuration.
2.  **Reopen in Container:** A dialog will appear asking if you want to "Reopen in Container". Click it.
3.  **Initial Setup:** The first time you open the container, it will build the environment and run the `postCreateCommand` defined in `devcontainer.json`. This command will install both the Python and Node.js dependencies.
4.  **Ready to Go:** Once the setup is complete, your VS Code terminal will be running inside the container, and all the necessary tools will be available in the `PATH` automatically. The container is also configured to install the recommended VS Code extensions, including the Cline AI assistant.

## Manual Configuration

For the application to connect to your Firebase project, you must perform the following steps:

1.  **Firebase Service Account Key:** Download your service account key from the Firebase console (**Project settings > Service accounts > Generate new private key**). Save the file as `firebase-service-account-key.json` in the root of this project.
2.  **Enable Cloud Firestore API:** Ensure the Cloud Firestore API is enabled for your project in the Google Cloud Console. You can use this link, replacing `YOUR_PROJECT_ID` with your actual Firebase project ID:
    [https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=YOUR_PROJECT_ID)

## Running the Application

Once inside the Dev Container, you can run the application using the provided scripts.

*   **Local Development Server:**
    ```bash
    ./devserver.sh
    ```
    This script starts both the Python Flask backend and the React frontend development server.

*   **Backend Tests:**
    ```bash
    ./run-tests.sh
    ```
    This script runs the backend `pytest` tests.

*   **Firebase Emulators:**
    ```bash
    ./start-emulators.sh
    ```
    This script starts the Firebase Auth and Firestore emulators for local testing. It should be run in a separate terminal before executing the tests.
