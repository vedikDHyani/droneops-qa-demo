
# DroneOps QA V0.10 QR + Language Demo

This version adds QR/barcode-style workflows and language switching.

## New in V0.10

- QR code generation for drone asset labels
- QR links can preselect Drone ID and Battery ID
- Direct QR workflows for:
  - Inspection Form
  - Flight Log Form
  - Maintenance Issue Form
  - Dashboard
- Language switch:
  - English
  - Deutsch
- Optional `APP_BASE_URL` secret for correct QR links
- More convenient navigation from scanned links

## Required Streamlit secrets

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-publishable-key"
DEMO_PASSWORD = "choose-a-demo-password"
ADMIN_PASSWORD = "choose-a-separate-admin-password"

# Recommended for QR generation:
APP_BASE_URL = "https://your-streamlit-app-url.streamlit.app"
```

## Notes

This is still a validation demo. Do not enter real confidential operational data.
