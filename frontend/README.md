# Frontend (Simple HTML + JS) 🎨

A minimal static frontend that calls the backend API to show customers and submit payments.

Run locally

1. Open `index.html` in your browser (no build required).
2. Make sure `window.API_URL` points to your backend (default `http://localhost:8000`). You can set this directly in `script.js` or let the deploy replace it automatically.

Deploy notes
- The deploy CI replaces `window.API_URL` with your production API URL during deployment.
- For a richer user interface, see the Streamlit app in `frontend_streamlit/` (run with `streamlit run frontend_streamlit/streamlit_app.py`).

Troubleshooting
- If API calls fail, check the browser console for network errors and confirm `API_URL` is correct.
