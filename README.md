
# DroneOps QA V0.8A Supabase Cloud Prototype

This version stores app data in Supabase instead of local CSV files.

## 1. Add Supabase credentials

Create this file inside the project folder:

```text
.streamlit/secrets.toml
```

Use this structure:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-or-publishable-key"
```

Do not commit real keys to GitHub.

## 2. Run locally

```bash
cd DroneOps_QA_V0_8_Supabase
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 3. Deploy later on Streamlit Cloud

Add the same secrets in Streamlit Cloud under:

App settings > Secrets

## Security note

This is a demo. Before sharing with real companies, add authentication, Row Level Security and role-based permissions.
