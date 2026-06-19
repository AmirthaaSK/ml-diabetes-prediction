Deploying this Flask app to Render

Steps:

1. Ensure `diabetes_model.pkl` and `scaler.pkl` are committed to the repository root.
2. Add any environment variables on Render (Settings > Environment) you want to set, e.g. `SECRET_KEY`.
3. Push this repository to GitHub.
4. On Render, create a new Web Service and connect your GitHub repo.
   - Build command: leave empty (Render will use pip install -r requirements.txt) or set `pip install -r requirements.txt`.
   - Start command: leave empty if Procfile exists, or set `gunicorn app:app --bind 0.0.0.0:$PORT`.
5. Set the instance plan and deploy.

Local testing:

Windows PowerShell commands:

```powershell
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
# Run locally with Flask development server:
python app.py
# Or run with Gunicorn (recommended to emulate production):
gunicorn app:app --bind 0.0.0.0:5000
```

Notes:
- For production on Render, Gunicorn will be used; the `if __name__ == "__main__"` block is only for local development.
- Keep the model files small-ish; large pickles can slow deploys.
- If you prefer an infra-as-code approach, I can add a render.yaml for automated deployments.
