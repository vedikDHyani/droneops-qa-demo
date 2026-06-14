# DroneOps QA V0.8B Deployment Steps

## 1. Create GitHub repository

Repository name:

```text
droneops-qa-demo
```

Upload these files:

- app.py
- requirements.txt
- README.md
- .gitignore
- .streamlit/secrets.toml.example

Do not upload `.streamlit/secrets.toml`.

## 2. Deploy on Streamlit Cloud

Create a new app and select:

- Repository: droneops-qa-demo
- Branch: main
- Main file path: app.py

## 3. Add secrets in Streamlit Cloud

In app settings, add:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-publishable-key"
```

## 4. Test

- Open Fleet Dashboard
- Submit failed inspection
- Check Supabase table updates
- Submit maintenance issue
- Export readiness report

## 5. Security note

This is a demo. Before sharing with real companies, add authentication and Row Level Security.
