
# Deploy V0.9

1. Upload these files to your GitHub repository:
   - app.py
   - requirements.txt
   - README.md
   - SUPABASE_FEEDBACK_TABLE.sql
   - .gitignore

2. In Supabase SQL Editor, run:
   - SUPABASE_FEEDBACK_TABLE.sql

3. In Streamlit Cloud:
   - Go to app settings
   - Replace secrets with:
     SUPABASE_URL
     SUPABASE_KEY
     DEMO_PASSWORD
     ADMIN_PASSWORD

4. Reboot the app.

5. Test:
   - login with demo password
   - submit inspection
   - submit validation feedback
   - unlock demo controls with admin password
