# Testing Strategy

This document outlines the automated testing strategy for the GabChat project.

## 1. Backend Unit/Integration Tests (`tests/backend`)

*   **Framework:** `pytest`
*   **Status:** Implemented and passing.
*   **Description:** These tests cover the entire Flask backend, including the `/verify-token` endpoint, all `/api/gemini-key` CRUD operations, and the `/api/chat` endpoint.
*   **Environment:** Tests are run against **Firebase Emulators** (Auth & Firestore). The `client_with_emulator_config` fixture in `tests/backend/test_main.py` is critical for ensuring the Firebase Admin SDK connects to the emulators during tests.
*   **How to Run:**
    1.  Start the emulators in a separate terminal: `sh start-emulators.sh`
    2.  Run the tests: `source .venv/bin/activate && PYTHONPATH=. python -m pytest -v tests/backend`

## 2. Frontend End-to-End (E2E) Tests (`tests/e2e`)

*   **Status:** Future Task (To be implemented after the React UI is stable).
*   **Goal:** Test the complete user authentication flow, API key management, and chat functionality from the UI perspective, interacting with the Firebase Auth Emulator and the React application.
*   **Tools:** Playwright or Cypress.
*   **Implementation Plan:**
    1.  **Install Playwright/Cypress** in the `src/react-app` project.
    2.  **Configure Frontend to use Auth Emulator:** In the React Firebase setup, connect to the Auth emulator for tests.
    3.  **Develop Test Scenarios:**
        *   Successful Sign-In & UI updates.
        *   Logout & UI updates.
        *   API Key Operations (Add, Verify, Delete).
        *   Core Chat Functionality (Sending messages, displaying history).
