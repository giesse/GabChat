# GabChat Project TODO

## Overall Plan

1.  **Set up Firebase Project:** (DONE)
2.  **Enable Google Sign-In:** (DONE)
3.  **Install Firebase SDKs:** (DONE)
4.  **Implement Backend Authentication Logic (Python/Flask):** (DONE)
5.  **Implement Frontend Authentication UI (Vanilla JS - `src/index.html`):** (DONE - To be replaced by React)
6.  **Gemini API Key Management (Backend & Vanilla JS Frontend):** (DONE - Frontend to be replaced by React)
7.  **Chat Interface (Backend & Vanilla JS Frontend):** (DONE - Frontend to be replaced by React)
8.  **Automated Backend Testing:** (DONE)
9.  **Frontend Overhaul to React (NEW):**
    *   Decision: Adopt React for a modern, component-based UI with chat widgets.
    *   Address CORS: Given Firebase Studio serves different ports on different domains:
        *   Add `Flask-CORS` to `requirements.txt`. (DONE - in previous step, just need to install & configure)
        *   Configure `Flask-CORS` in `main.py` to allow requests from the React development server's domain.
    *   Set up React Project:
        *   Choose a React setup (e.g., Vite or Create React App).
        *   Establish project structure (e.g., within `src/react-app`).
    *   Implement Core UI in React:
        *   Authentication flow (Google Sign-In with Firebase SDK for React).
        *   API Key management UI.
        *   Chat interface (message display, input, sending messages).
    *   Development Workflow: Ensure React dev server (with HMR) can run alongside Flask API server in Firebase Studio, handling separate domains.

## Next Immediate Tasks

1.  **Configure Flask-CORS for React Development:**
    *   Ensure `Flask-CORS` is in `requirements.txt` (should be from previous interaction).
    *   Run `pip install -r requirements.txt` (or equivalent for the IDE environment) to install it.
    *   Import and initialize `Flask-CORS` in `main.py`, configuring it to allow requests from the anticipated domain/port of the React dev server in Firebase Studio.
2.  **Set up Basic React Application:**
    *   Create a new directory for the React app (e.g., `src/react-app`).
    *   Initialize a new React project using Vite (recommended for speed) or Create React App.
    *   Verify that the basic React app can be served by its development server and accessed via the port/domain provided by Firebase Studio.
3.  **Implement Authentication Flow in React (Basic):**
    *   Integrate Firebase JavaScript SDK into the React app.
    *   Create a basic login component that triggers Firebase Google Sign-In.
    *   Verify that a token can be obtained and (manually for now, or via a simple test call) sent to the Flask backend's `/verify-token` endpoint (this will test the CORS setup).

## Subsequent Tasks (Beyond immediate focus)

*   Complete React UI migration (API Key Management, Chat Interface).
*   **(Future Task) Implement E2E UI tests (React):** For the new React-based authentication flow, API key management, and core chat functionality using a framework like Playwright or Cypress.
*   **(Future Task) Allow user to select Gemini model:** Implement UI and backend logic for model selection.
*   User session management (beyond simple token verification if needed for React state).
*   CI/CD Integration.

## Automated Testing - Detailed Plan

### 1. Backend Unit/Integration Tests (`tests/backend`) - (DONE & MAINTAIN)
*   Ensure existing backend tests continue to pass. Adapt if API contracts change due to React frontend needs.

### 2. Frontend End-to-End (E2E) Tests (`tests/e2e`) - (Future Task - Post React Migration)

*   **Goal:** Test the complete user authentication flow, API key management, and chat functionality from the UI perspective, interacting with the Firebase Auth Emulator and the React application.
*   **Tools:** Playwright or Cypress.
*   **Steps:**
    *   **Install Playwright/Cypress** in the React project.
    *   **Configure Frontend to use Auth Emulator:** In the React Firebase setup, connect to the Auth emulator for tests.
    *   **Test Scenarios (adapted for React components):**
        *   Successful Sign-In & UI updates.
        *   Logout & UI updates.
        *   API Key Operations.
        *   Chat Functionality.

This detailed plan should provide a good roadmap for implementing automated testing in the GabChat project.
