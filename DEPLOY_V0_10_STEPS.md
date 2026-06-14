
# Deploy V0.10

Upload these files to GitHub:

- app.py
- requirements.txt
- README.md
- SUPABASE_FEEDBACK_TABLE.sql
- DEPLOY_V0_10_STEPS.md
- .streamlit/config.toml

Then in Streamlit Cloud, update secrets:

SUPABASE_URL
SUPABASE_KEY
DEMO_PASSWORD
ADMIN_PASSWORD
APP_BASE_URL

Reboot the app.

Test:
1. Password page appears.
2. Language switch works.
3. QR / Barcode Workflow generates a QR code.
4. Scan/open generated link and confirm the correct form opens with Drone ID preselected.
5. Feedback form saves to Supabase.
