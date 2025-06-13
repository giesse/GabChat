# Frontend Documentation

This document covers the frontend architecture and development for the GabChat project.

## Overview

The project is currently undergoing a migration from a vanilla HTML/CSS/JavaScript implementation to a modern **React** application using **Vite**.

## Legacy Frontend (To be phased out)

*   **Location:** `src/`
*   **Files:** `index.html`, `script.js`, `style.css`
*   **Functionality:** Implemented the initial UI for Google Sign-In, API key management, and chat. This is being replaced by the new React app.

## React Frontend (Current)

*   **Location:** `src/react-app`
*   **Framework:** React
*   **Build Tool:** Vite
*   **Key Decisions:**
    *   Adopted React for a more robust, component-based architecture.
    *   Chose Vite for its fast development server and build process.
*   **Development Server:**
    *   The React development server is started in the background by the `./devserver.sh` script.
    *   Logs are written to `react-dev-server.log` in the project root.
    *   It typically runs on its own port (e.g., 5173), and communicates with the backend via CORS, which is configured in the Flask server.

## Key File Locations

*   **Main React App Component:** `src/react-app/src/App.jsx`
*   **Vite Configuration:** `src/react-app/vite.config.js`
*   **Package Manager:** `yarn` is the preferred package manager for this project. All new dependencies should be added using `yarn add [package-name]`.
*   **Package Management:** `src/react-app/package.json`
