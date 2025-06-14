# Completed Tasks

This file archives tasks that have been completed.

- **Set up Firebase Project:** (DONE)
- **Enable Google Sign-In:** (DONE)
- **Install Firebase SDKs:** (DONE)
- **Implement Backend Authentication Logic (Python/Flask):** (DONE)
- **Implement Frontend Authentication UI (Vanilla JS - `src/index.html`):** (DONE - To be replaced by React)
- **Gemini API Key Management (Backend & Vanilla JS Frontend):** (DONE - Frontend to be replaced by React)
- **Chat Interface (Backend & Vanilla JS Frontend):** (DONE - Frontend to be replaced by React)
- **Automated Backend Testing:** (DONE)
- **Configure Flask-CORS for React Development:** (DONE)
- **Set up Basic React Application:** (DONE)
- **Set up local development environment:** (DONE)
    - Create a `.devcontainer` directory and `devcontainer.json` file.
    - Create a `shell.nix` file to define the development environment.
    - Update `docs/LocalSetup.md` with the new instructions.
- **Simplify local development environment:** (DONE)
    - Removed Nix and Python venv in favor of a standard devcontainer setup.
    - Updated `.devcontainer/devcontainer.json`.
    - Deleted `shell.nix`.
    - Updated `docs/LocalSetup.md`.
    - Updated `devserver.sh`, `run-tests.sh`, and `start-emulators.sh`.
- Local environment setup
    - Fixed devcontainer build and dependency installation issues by switching to a pre-built Python image.
- **Split devserver.sh into start-flask.sh and start-vite.sh:** (DONE)
- **Fixed Vite connection issue:** (DONE)
    - Configured Vite to listen on all network interfaces to work with VSCode's port forwarding.
- **Resolved Local Setup Issues:** (DONE)
    - Fixed Firebase Google Sign-In on localhost by adding a `signInWithPopup` option.
- **Fix VSCode Hanging Issue:** [Fix VSCode Hanging Issue](tasks/2025-06-13-fix-vscode-hanging-issue.md) (DONE)
- **Implement Core React UI (Authentication):** See [docs/tasks/2025-06-13-implement-react-ui.md](tasks/2025-06-13-implement-react-ui.md) for details. (DONE)
- **Update Google Sign-In Button:** [Update Google Sign-In Button](tasks/2025-06-13-update-google-signin-button.md) (DONE)
- **Fix CSS Warnings in SignIn.css:** [Fix CSS Warnings in SignIn.css](tasks/2025-06-13-fix-css-user-select-warning.md) (DONE)
- [Improve React UI](tasks/2025-06-13-improve-react-ui.md) (Mostly done)
    *   Fix application layout to use full window space.
    *   Update favicon to match the original application.
    *   Relocate user menu to the top-right corner.
    *   Improve chat component look for better usability
* The "Sign Out" item in the menu doesn't work (can't click on it)
* Let's use the user profile picture for the user menu instead of a button with the user full name