
# DroneOps QA V0.9 Validation Demo

This version is intended for sharing a validation demo link with selected testers.

## New in V0.9

- Optional demo password
- Optional admin password for demo reset
- Better product brief
- Validation feedback page
- QR workflow page
- Safer empty-table handling
- Clearer warnings that this is not production software

## Required Streamlit secrets

Add these in Streamlit Cloud > App settings > Secrets:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-publishable-key"

# Optional but recommended before sharing:
DEMO_PASSWORD = "choose-a-demo-password"
ADMIN_PASSWORD = "choose-a-separate-admin-password"
```

## Supabase table required for feedback

Run the SQL in `SUPABASE_FEEDBACK_TABLE.sql`.
