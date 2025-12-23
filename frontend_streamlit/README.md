# Streamlit frontend

This Streamlit app provides a simple UI for the Loan Payment backend.

Run locally:

```bash
API_URL=http://localhost:8000 streamlit run frontend_streamlit/streamlit_app.py
```

Deployment: the standard `scripts/deploy_to_ec2.sh` will copy this folder to the server and a `systemd` service will be installed to run it on port 8501.