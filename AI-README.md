# AI-README.md: GabChat Project Memory for Gemini Assistant

This document serves as a high-level summary and entry point for the AI assistant to understand the GabChat project. For detailed information, please refer to the files in the `docs/` directory.

# AI Assistant Workflow

To ensure a reliable and traceable workflow, please follow these steps for every task:

1.  **Acknowledge & Plan:**
    *   Thoroughly understand the assigned task.
    *   Create a new task documentation file in `docs/tasks/YYYY-MM-DD-brief-task-description.md`.
    *   In this file, outline your plan, including the files you'll modify and the steps you'll take. This file will serve as our persistent context for the task.

2.  **Update `TODO.md`:**
    *   Add a new entry to `docs/TODO.md` that links to the new task document.

3.  **Implement:**
    *   Execute the plan by creating or modifying the necessary files.
    *   Keep the task document updated with your actions and any important observations.

4.  **Verify:**
    *   Once you believe the task is complete, describe how I can verify the changes (e.g., by running specific tests, checking a feature in the browser, etc.).
    *   Wait for my confirmation that the task is verified.

5.  **Finalize:**
    *   After I have verified the task, move the entry from `docs/TODO.md` to `docs/DONE.md`.
    *   Commit the changes with a clear and descriptive commit message.

## Important Notes

*   **File System:** The file tree provided is not always complete. To see all files, including hidden ones, you can use the `ls -aR` command.
*   **Task Context:** The `docs/` directory is our shared memory. It is essential for resuming tasks and understanding our project history.

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
