# Task: Improve React UI

Date: 2025-06-13

## Objective

Refactor the existing React UI to be more user-friendly and align with standard application design patterns. This involves creating a user menu, an API key management modal, and integrating a dedicated library for the chat interface. This task consolidates the work from the previous "Implement React UI Components" task.

## Previous Actions Taken

*   **Update `AI-README.md`:** Added a "Current Project Status" section.
*   **Create `ApiKey.jsx` Component:** Implemented a basic form with an input field and a "Save" button (placeholder functionality).
*   **Create `Chat.jsx` Component:** Created a placeholder component.
*   **Update `App.jsx`:** Integrated the new `ApiKey` and `Chat` components.

## Consolidated Plan

1.  **Create a User Menu:**
    *   A new component `UserMenu.jsx` will be created.
    *   It will be positioned in the top-right corner of the application.
    *   It will display the user's name or avatar.
    *   On click, it will show a dropdown with two options:
        *   "Edit API Key"
        *   "Sign Out"

2.  **Implement API Key Modal:**
    *   The existing `ApiKey.jsx` will be converted into a modal `ApiKeyModal.jsx`.
    *   This modal will be used for both initially setting and later editing the Gemini API key.
    *   The modal will appear automatically on login if the user has not set an API key.
    *   It can be opened manually by clicking "Edit API Key" from the `UserMenu`.
    *   The component will handle the logic for saving the key to the backend.

3.  **Integrate a Chat Component Library:**
    *   The current placeholder `Chat.jsx` will be replaced.
    *   I will investigate and integrate a suitable React chat component library (e.g., `react-chat-elements`) using `yarn`.
    *   This will involve installing the new dependency and wrapping it in our `Chat` component.

4.  **Refactor `App.jsx`:**
    *   The main `App.jsx` component will be updated to integrate and manage the state for the new components.
    *   This includes managing the visibility of the `ApiKeyModal`.
    *   The main layout will be adjusted to accommodate the `UserMenu` in the header.

5.  **Review Vanilla JS Implementation:**
    *   As requested, I will review the original `src/script.js` to understand the existing logic for API key handling and chat.

6.  **Documentation:**
    *   Update `docs/Frontend.md` to specify the use of `yarn` as the package manager.

## File Changes

*   **Create:** `src/react-app/src/components/UserMenu.jsx`
*   **Rename/Modify:** `src/react-app/src/components/ApiKey.jsx` to `src/react-app/src/components/ApiKeyModal.jsx`
*   **Modify:** `src/react-app/src/App.jsx`
*   **Modify:** `src/react-app/src/components/Chat.jsx`
*   **Modify:** `src/react-app/src/App.css`
*   **Modify:** `src/react-app/package.json`
*   **Modify:** `docs/Frontend.md`
*   **Delete:** `docs/tasks/2025-06-13-implement-react-ui-components.md`

## Troubleshooting and Resolution (2025-06-13)

After implementing the initial chat component, the application was showing a blank page. The following steps were taken to diagnose and resolve the issues:

1.  **Initial Error:** The browser console showed `Uncaught SyntaxError: The requested module ... doesn't provide an export named: 'Nlux'`.
    *   **Action:** Investigated `Chat.jsx`.

2.  **Incorrect Component & Missing Dependency:** Based on user-provided documentation, it was determined that:
    *   The correct component was `AiChat`, not `Nlux`.
    *   The `@nlux/themes` package was a required dependency for styling.
    *   The chat adapter implementation was outdated.
    *   **Action:**
        *   Installed `@nlux/themes` using `yarn`.
        *   Updated `Chat.jsx` to import and use the `AiChat` component, import the `nova.css` theme, and refactor the adapter to use the `streamText` and `observer` pattern.

3.  **Frontend/Backend Communication Failure:** After fixing the component, the app would load but would not display the chat interface or the API key modal.
    *   **Diagnosis:** The React frontend (running on the Vite dev server port) could not communicate with the Flask backend (running on port 5000) due to Cross-Origin Resource Sharing (CORS) policy. The API call to `/api/check_api_key` was failing silently.
    *   **Solution:** Configured the Vite development server to act as a proxy.
    *   **Action:**
        *   Modified `src/react-app/vite.config.js` to add a `server.proxy` configuration.
        *   This change forwards any requests from the frontend to `/api/*` to the backend at `http://127.0.0.1:5000`, resolving the issue for the development environment.

This series of fixes should result in the application correctly showing the API key modal when a user is logged in but has not yet provided a key.

## API Correction (2025-06-13)

Upon further investigation, it was discovered that the React frontend was not using the correct backend API endpoints, causing the application to fail silently. The following corrections were made:

1.  **`App.jsx`:**
    *   The API call to check for an existing API key was changed from `/api/check_api_key` to the correct endpoint, `GET /api/gemini-key`.
    *   The component was updated to parse the correct `{"has_key": boolean}` response from the backend.

2.  **`ApiKeyModal.jsx`:**
    *   The API call to save a new API key was changed from `/api/set_api_key` to the correct endpoint, `POST /api/gemini-key`.

3.  **`Chat.jsx`:**
    *   The payload for sending a chat message was corrected. It now sends `{"message": "..."}` instead of `{"prompt": "..."}` to match the backend's expectation.

These changes align the frontend's API calls with the established backend endpoints, resolving the core communication issue.

## Chat UI Fix (2025-06-13)

The chat UI was displaying raw JSON instead of the parsed message.

1.  **Problem:** The `AiChat` component from `@nlux/react` was receiving a raw JSON string (`{"reply": "..."}`) instead of the message text.
2.  **Cause:** The streaming adapter logic in `Chat.jsx` was not parsing the incoming JSON stream. It was also not using the recommended `useStreamingAdapter` hook.
3.  **Solution:**
    *   Refactored `Chat.jsx` to use the `useStreamingAdapter` hook.
    *   Implemented a buffer and parsing logic within the adapter to handle newline-delimited JSON chunks.
    *   The adapter now correctly extracts the `reply` field from each JSON object and passes only the text to the `AiChat` component.
    *   Fixed minor linting errors in the `catch` blocks.

## NLUX Adapter Correction (2025-06-13)

1.  **Problem:** The browser console displayed a warning: `[nlux] API object passed was is not compatible with AiChat. Only use API objects created by the useAiChatApi() hook.`
2.  **Investigation:**
    *   Initial assumption was a mismatch between the adapter implementation (`useAsStreamAdapter`) and the library's expectation.
    *   However, upon user feedback and review of `main.py`, it was confirmed that the `/api/chat` endpoint is **non-streaming** (batch). It uses `model.generate_content()` and returns a single JSON response.
    *   The implementation in `src/react-app/src/components/Chat.jsx` correctly uses `useAsBatchAdapter`, which aligns with the backend.
3.  **Conclusion:** The console warning is likely a bug or a misleading message within the `@nlux/react` library itself. The current implementation is correct for the given backend architecture. No code changes are necessary. The warning will be ignored for now.
