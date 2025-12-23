# Frontend (Simple HTML + JS)

This frontend is a plain HTML/JavaScript app that talks to the backend API.

Run locally:

1. Open `index.html` in a browser (no build step required).
2. Ensure `window.API_URL` points to your backend (default `http://localhost:8000`).

Deploy notes:
- CI sets `API_URL` on the deployed server using a small sed replacement in the GitHub Action.
