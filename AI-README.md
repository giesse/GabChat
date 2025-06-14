# AI-README.md: GabChat Project Memory for Gemini Assistant

This document serves as a high-level summary and entry point for an AI assistant to understand the GabChat project. For detailed information, please refer to the files in the `docs/` directory.

## Project Goal

GabChat is a web application that allows users to authenticate using Firebase Google Sign-In and interact with a chat interface powered by a Large Language Model (LLM), using their own Gemini API key.

## Current Project Status (as of 2025-06-14)

The project is in the process of migrating its frontend from a legacy vanilla JavaScript implementation to a modern React application.

*   **Backend:** The Python/Flask backend is **complete and tested**. It provides endpoints for user authentication, API key management, and chat functionality. For details, see `docs/Backend.md`.

*   **Frontend (React):** The new React frontend has a **complete authentication flow**. Users can sign in and out using their Google accounts. The basic component structure is in place.

*   **Immediate Goal:** The next step is to build the React components for **API Key Management** and the **Chat Interface**, connecting them to the existing, functional backend endpoints.

## Key Technologies

*   **Backend:** Python, Flask, Google Generative AI (Gemini)
*   **Frontend:** React (Vite)
*   **Authentication:** Firebase Authentication (Google Sign-In)
*   **Database:** Firestore
*   **Testing:** `pytest` for backend, Playwright/Cypress planned for E2E.

## Documentation

For detailed information about the project, please see the following documents:

*   **[docs/Organization.md](docs/Organization.md):** An overview of how the project documentation is structured.
*   **[docs/LocalSetup.md](docs/LocalSetup.md):** Instructions for setting up the local development environment.
*   **[docs/Backend.md](docs/Backend.md):** Detailed information about the Python/Flask backend.
*   **[docs/Frontend.md](docs/Frontend.md):** Information about the React-based frontend.
*   **[docs/Testing.md](docs/Testing.md):** The project's testing strategy.
*   **[docs/TODO.md](docs/TODO.md):** A list of pending tasks.
*   **[docs/DONE.md](docs/DONE.md):** An archive of completed tasks.
