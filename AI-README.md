# AI-README.md: GabChat Project Memory for Gemini Assistant

This document serves as a high-level summary and entry point for the AI assistant to understand the GabChat project. For detailed information, please refer to the files in the `docs/` directory.

## Important instructions for the AI assistant

- Always keep the documentation up to date! This is your long term memory. Anything you learn needs to be stored in it so that you don't have to re-learn it every time, or ask me the same questions every time.
- If you are asked to perform a new task, update TODO.md first!
- When tasks are done, move them from TODO.md to DONE.md!

## Project Goal

GabChat is a web application that allows users to authenticate using Firebase Google Sign-In and interact with a chat interface powered by a Large Language Model (LLM), using their own Gemini API key.

## Documentation

For detailed information about the project, please see the following documents:

*   **[docs/Organization.md](docs/Organization.md):** An overview of how the project documentation is structured.
*   **[docs/LocalSetup.md](docs/LocalSetup.md):** Instructions for setting up the local development environment.
*   **[docs/Backend.md](docs/Backend.md):** Detailed information about the Python/Flask backend.
*   **[docs/Frontend.md](docs/Frontend.md):** Information about the React-based frontend.
*   **[docs/Testing.md](docs/Testing.md):** The project's testing strategy.
*   **[docs/TODO.md](docs/TODO.md):** A list of pending tasks.
*   **[docs/DONE.md](docs/DONE.md):** An archive of completed tasks.

## Key Technologies

*   **Backend:** Python, Flask, Google Generative AI (Gemini)
*   **Frontend:** React (Vite)
*   **Authentication:** Firebase Authentication (Google Sign-In)
*   **Database:** Firestore
*   **Testing:** `pytest` for backend, Playwright/Cypress planned for E2E.

## Next Immediate Steps

The primary focus is on completing the frontend migration to React. See **[docs/TODO.md](docs/TODO.md)** for specific tasks.
