
# DroneOps QA V0.9.1 Polished Validation Demo

This version improves the validation demo UI.

## New in V0.9.1

- Better password screen
- Grouped sidebar navigation
- More polished landing page
- Operational summary cards
- Clearer form instructions
- More professional report page
- Validation feedback remains prominent
- Admin-only demo reset

## Required Streamlit secrets

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-publishable-key"
DEMO_PASSWORD = "choose-a-demo-password"
ADMIN_PASSWORD = "choose-a-separate-admin-password"
```

## Supabase feedback table

Run `SUPABASE_FEEDBACK_TABLE.sql` once if you have not already created the feedback table.
