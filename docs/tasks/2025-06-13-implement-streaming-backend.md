# Task: Implement Streaming Backend

Date: 2025-06-13

## Objective

Refactor the backend chat endpoint (`/api/chat`) to support streaming responses. This will improve the user experience by displaying the AI's response as it's being generated, rather than waiting for the entire response to complete.

## Plan

1.  **Modify `main.py`:**
    *   Update the `/api/chat` endpoint to use `model.generate_content(..., stream=True)`.
    *   Instead of `jsonify`, return a Flask `Response` object with a generator function.
    *   The generator function will iterate over the streaming response from the Gemini API.
    *   Each chunk from the Gemini response will be sent to the client as a Server-Sent Event (SSE).
    *   The response `mimetype` should be set to `text/event-stream`.

2.  **Update Frontend Adapter:**
    *   Once the backend is updated, the frontend `Chat.jsx` component will need to be reverted to use the `useStreamingAdapter`.
    *   The adapter logic will need to correctly handle the SSE stream.

3.  **Testing:**
    *   Thoroughly test the streaming functionality to ensure that responses are received and displayed correctly in the UI.
    *   Verify that error handling is still robust.
