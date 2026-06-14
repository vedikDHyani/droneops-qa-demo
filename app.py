
import streamlit as st
import pandas as pd
from datetime import date, datetime
from supabase import create_client

st.set_page_config(page_title="DroneOps QA Validation Demo", page_icon="🛩️", layout="wide")

STATUS = ["Ready", "Limited", "Not Ready", "Under Maintenance", "Retired"]
CHECK = ["Pass", "Fail", "Needs Review"]
YESNO = ["Yes", "No"]
SEVERITY = ["Low", "Medium", "High", "Critical"]
ISSUE_STATUS = ["Open", "In Progress", "On Hold", "Closed"]
MISSION_TYPES = ["Inspection", "Surveillance", "Mapping", "Training", "Test Flight", "Maintenance Check", "Other"]

SEED = {
    "drones": [
        {"drone_id":"DRN-001","drone_name":"AeroInspect-1","manufacturer":"DJI","model":"Matrice 300 RTK","owner_team":"Inspection Team A","assigned_pilot":"Anna Keller","location":"Chemnitz","next_inspection_due":"2026-07-10","current_status":"Ready","notes":"Primary inspection drone"},
        {"drone_id":"DRN-002","drone_name":"SurveyLite-1","manufacturer":"DJI","model":"Mavic 3 Enterprise","owner_team":"Inspection Team B","assigned_pilot":"Max Richter","location":"Chemnitz","next_inspection_due":"2026-07-08","current_status":"Limited","notes":"Propeller review needed"},
        {"drone_id":"DRN-003","drone_name":"ThermalEye-1","manufacturer":"Autel","model":"EVO II Dual 640T","owner_team":"Inspection Team A","assigned_pilot":"Lena Hoffmann","location":"Workshop","next_inspection_due":"2026-07-01","current_status":"Not Ready","notes":"Motor issue open"},
        {"drone_id":"DRN-004","drone_name":"Training-1","manufacturer":"DJI","model":"Mini 4 Pro","owner_team":"Training Team","assigned_pilot":"Vedik Dhyani","location":"Chemnitz","next_inspection_due":"2026-07-12","current_status":"Ready","notes":"Training unit"},
        {"drone_id":"DRN-005","drone_name":"CustomMap-1","manufacturer":"Custom","model":"Quad X4","owner_team":"Workshop","assigned_pilot":"Technician","location":"Storage","next_inspection_due":"2026-07-05","current_status":"Ready","notes":"Custom mapping prototype"},
    ],
    "batteries": [
        {"battery_id":"BAT-001","compatible_drone_id":"DRN-001","battery_type":"LiPo","cycle_count":42,"health_status":"Good","current_status":"Available","storage_location":"Storage Room","notes":"Normal"},
        {"battery_id":"BAT-002","compatible_drone_id":"DRN-001","battery_type":"LiPo","cycle_count":96,"health_status":"Needs Review","current_status":"Available","storage_location":"Storage Room","notes":"High cycle count"},
        {"battery_id":"BAT-003","compatible_drone_id":"DRN-002","battery_type":"LiPo","cycle_count":130,"health_status":"Weak","current_status":"Available","storage_location":"Workshop","notes":"Review before use"},
        {"battery_id":"BAT-004","compatible_drone_id":"DRN-002","battery_type":"LiPo","cycle_count":38,"health_status":"Good","current_status":"Available","storage_location":"Storage Room","notes":"Normal"},
        {"battery_id":"BAT-005","compatible_drone_id":"DRN-003","battery_type":"LiPo","cycle_count":155,"health_status":"Replace","current_status":"Damaged","storage_location":"Workshop","notes":"Swelling observed"},
        {"battery_id":"BAT-006","compatible_drone_id":"DRN-003","battery_type":"LiPo","cycle_count":71,"health_status":"Good","current_status":"Charging","storage_location":"Charging Station","notes":"Normal"},
        {"battery_id":"BAT-007","compatible_drone_id":"DRN-004","battery_type":"LiPo","cycle_count":21,"health_status":"Good","current_status":"Available","storage_location":"Storage Room","notes":"Normal"},
        {"battery_id":"BAT-008","compatible_drone_id":"DRN-004","battery_type":"LiPo","cycle_count":24,"health_status":"Good","current_status":"Available","storage_location":"Storage Room","notes":"Normal"},
        {"battery_id":"BAT-009","compatible_drone_id":"DRN-005","battery_type":"LiPo","cycle_count":84,"health_status":"Needs Review","current_status":"Available","storage_location":"Workshop","notes":"Check connector"},
        {"battery_id":"BAT-010","compatible_drone_id":"DRN-005","battery_type":"LiPo","cycle_count":60,"health_status":"Good","current_status":"Available","storage_location":"Storage Room","notes":"Normal"},
    ],
    "flights": [
        {"flight_id":"FLT-001","flight_date":"2026-06-01","drone_id":"DRN-001","battery_id":"BAT-001","pilot_name":"Anna Keller","mission_type":"Inspection","flight_duration_min":24,"location":"Chemnitz","pre_flight_result":"Pass","post_flight_result":"Pass","issue_reported":"No","remarks":"Normal roof inspection"},
        {"flight_id":"FLT-002","flight_date":"2026-06-02","drone_id":"DRN-002","battery_id":"BAT-004","pilot_name":"Max Richter","mission_type":"Mapping","flight_duration_min":37,"location":"Chemnitz","pre_flight_result":"Pass","post_flight_result":"Needs Review","issue_reported":"Yes","remarks":"Propeller vibration noticed"},
    ],
    "inspections": [
        {"inspection_id":"INS-001","inspection_date":"2026-06-10","drone_id":"DRN-001","battery_id":"BAT-001","pre_flight_check":"Pass","propeller_check":"Pass","motor_check":"Pass","camera_check":"Pass","gps_check":"Pass","controller_check":"Pass","damage_found":"No","inspector":"Anna Keller","final_result":"Pass","notes":"Normal"},
        {"inspection_id":"INS-002","inspection_date":"2026-06-08","drone_id":"DRN-002","battery_id":"BAT-004","pre_flight_check":"Pass","propeller_check":"Needs Review","motor_check":"Pass","camera_check":"Pass","gps_check":"Pass","controller_check":"Pass","damage_found":"No","inspector":"Max Richter","final_result":"Needs Review","notes":"Propeller check needed"},
    ],
    "maintenance_issues": [
        {"issue_id":"MNT-001","date_reported":"2026-06-05","drone_id":"DRN-003","issue_type":"Motor vibration","severity":"High","action_required":"Inspect motor and vibration source","responsible_person":"Technician","status":"Open","closure_date":None,"notes":"Drone grounded until repair"},
        {"issue_id":"MNT-002","date_reported":"2026-06-02","drone_id":"DRN-002","issue_type":"Propeller damage","severity":"Critical","action_required":"Replace propeller set","responsible_person":"Max Richter","status":"Open","closure_date":None,"notes":"Issue found after mapping flight"},
    ],
}

def secret_value(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

@st.cache_resource
def get_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        st.error("Missing Supabase credentials. Add them in Streamlit Secrets.")
        st.code('SUPABASE_URL = "https://your-project-id.supabase.co"\nSUPABASE_KEY = "your-publishable-key"')
        st.stop()
    return create_client(url, key)

def fetch(table):
    res = get_supabase().table(table).select("*").execute()
    return pd.DataFrame(res.data).fillna("")

def insert(table, payload):
    return get_supabase().table(table).insert(payload).execute()

def update(table, key, val, payload):
    return get_supabase().table(table).update(payload).eq(key, val).execute()

def delete_all(table, key):
    return get_supabase().table(table).delete().neq(key, "__never__").execute()

def next_id(prefix, df, col):
    nums = []
    if col in df.columns:
        for x in df[col].astype(str):
            if x.startswith(prefix + "-"):
                try:
                    nums.append(int(x.split("-")[-1]))
                except Exception:
                    pass
    return f"{prefix}-{max(nums + [0]) + 1:03d}"

def safe_counts(df, col, values):
    if col not in df.columns:
        return pd.Series([0] * len(values), index=values)
    return df[col].value_counts().reindex(values, fill_value=0)

def kpis(drones, batteries, flights, issues):
    total = len(drones)
    ready = int((drones.get("current_status", pd.Series(dtype=str)) == "Ready").sum())
    limited = int((drones.get("current_status", pd.Series(dtype=str)) == "Limited").sum())
    not_ready = int((drones.get("current_status", pd.Series(dtype=str)) == "Not Ready").sum())
    open_issues = int(issues.get("status", pd.Series(dtype=str)).isin(["Open", "In Progress", "On Hold"]).sum())
    critical = int(((issues.get("severity", pd.Series(dtype=str)) == "Critical") & issues.get("status", pd.Series(dtype=str)).isin(["Open", "In Progress", "On Hold"])).sum())
    battery_review = int(batteries.get("health_status", pd.Series(dtype=str)).isin(["Needs Review", "Weak", "Replace"]).sum())
    hours = round(pd.to_numeric(flights.get("flight_duration_min", pd.Series(dtype=float)), errors="coerce").fillna(0).sum() / 60, 1)
    readiness = round((ready / total * 100) if total else 0, 0)
    return total, ready, limited, not_ready, open_issues, critical, battery_review, hours, readiness

def reset_demo():
    for table, key in [
        ("maintenance_issues", "issue_id"),
        ("inspections", "inspection_id"),
        ("flights", "flight_id"),
        ("batteries", "battery_id"),
        ("drones", "drone_id"),
    ]:
        delete_all(table, key)
    for table in ["drones", "batteries", "flights", "inspections", "maintenance_issues"]:
        insert(table, SEED[table])

def report_text(drones, batteries, flights, inspections, issues):
    total, ready, limited, not_ready, open_issues, critical, battery_review, hours, readiness = kpis(drones, batteries, flights, issues)
    lines = [
        "# DroneOps QA Validation Readiness Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## KPIs",
        f"- Total drones: {total}",
        f"- Ready drones: {ready}",
        f"- Limited drones: {limited}",
        f"- Not ready drones: {not_ready}",
        f"- Fleet readiness: {readiness}%",
        f"- Open maintenance issues: {open_issues}",
        f"- Critical open issues: {critical}",
        f"- Batteries needing review: {battery_review}",
        f"- Total flight hours: {hours}",
        "",
        "## Drone Status",
    ]
    for _, r in drones.iterrows():
        lines.append(f"- {r.get('drone_id','')}: {r.get('drone_name','')}, {r.get('current_status','')}, next inspection {r.get('next_inspection_due','')}")
    return "\n".join(lines)

def require_demo_access():
    demo_password = secret_value("DEMO_PASSWORD", "")
    if not demo_password:
        return
    if st.session_state.get("demo_access_granted"):
        return
    st.markdown('<div class="big-title">DroneOps QA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Validation demo access</div>', unsafe_allow_html=True)
    st.info("Enter the demo password to access the prototype.")
    with st.form("demo_login"):
        pw = st.text_input("Demo password", type="password")
        submitted = st.form_submit_button("Enter demo")
    if submitted and pw == demo_password:
        st.session_state.demo_access_granted = True
        st.rerun()
    elif submitted:
        st.error("Incorrect password.")
    st.stop()

def admin_ok():
    admin_password = secret_value("ADMIN_PASSWORD", "")
    if not admin_password:
        return True
    return st.session_state.get("admin_access_granted", False)

st.markdown("""
<style>
.block-container {padding-top: 1.4rem;}
.big-title {font-size: 40px; font-weight: 850;}
.subtitle {color: #64748b; margin-bottom: 1.2rem; font-size: 16px;}
.section {font-size: 22px; font-weight: 750; margin-top: 1.2rem;}
.small-note {color: #64748b; font-size: 13px;}
.hero-card {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    border: 1px solid rgba(148,163,184,0.25);
    background: rgba(148,163,184,0.08);
}
</style>
""", unsafe_allow_html=True)

require_demo_access()

st.sidebar.title("DroneOps QA")
st.sidebar.caption("Validation Demo V0.9")
if st.sidebar.button("Refresh data"):
    st.rerun()

page = st.sidebar.radio("Navigation", [
    "Product Brief", "Fleet Dashboard", "Drone Register", "Battery Management",
    "Inspection Form", "Flight Log Form", "Maintenance Issue Form",
    "Readiness Report", "Validation Feedback", "QR Workflow", "Demo Controls"
])

st.markdown('<div class="big-title">DroneOps QA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Validation demo for drone fleet readiness, battery health, inspections, flight logs and maintenance traceability.</div>', unsafe_allow_html=True)

try:
    drones = fetch("drones")
    batteries = fetch("batteries")
    flights = fetch("flights")
    inspections = fetch("inspections")
    issues = fetch("maintenance_issues")
except Exception as e:
    st.error("Could not connect to Supabase or read tables.")
    st.exception(e)
    st.stop()

if page == "Product Brief":
    st.markdown('<div class="section">What problem this solves</div>', unsafe_allow_html=True)
    st.write("Drone teams often manage aircraft status, inspection results, battery health and maintenance issues across separate spreadsheets, chats or paper records. That creates readiness uncertainty before missions.")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="hero-card"><b>Readiness</b><br>Know which drones are ready, limited or grounded.</div>', unsafe_allow_html=True)
    c2.markdown('<div class="hero-card"><b>Traceability</b><br>Connect inspections, maintenance issues and flight records.</div>', unsafe_allow_html=True)
    c3.markdown('<div class="hero-card"><b>Battery control</b><br>Track health, cycle count and availability.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section">Validation goal</div>', unsafe_allow_html=True)
    st.write("This version is for testing whether drone operators consider the workflow useful enough to adopt, not for production deployment.")
    st.warning("This demo uses a shared database. Do not enter confidential or real operational data.")

elif page == "Fleet Dashboard":
    total, ready, limited, not_ready, open_issues, critical, battery_review, hours, readiness = kpis(drones, batteries, flights, issues)
    c = st.columns(6)
    c[0].metric("Fleet Readiness", f"{readiness}%")
    c[1].metric("Ready", ready)
    c[2].metric("Limited", limited)
    c[3].metric("Not Ready", not_ready)
    c[4].metric("Open Issues", open_issues)
    c[5].metric("Battery Reviews", battery_review)

    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section">Drone readiness</div>', unsafe_allow_html=True)
        st.bar_chart(safe_counts(drones, "current_status", STATUS))
    with right:
        st.markdown('<div class="section">Battery health</div>', unsafe_allow_html=True)
        st.bar_chart(safe_counts(batteries, "health_status", ["Good", "Needs Review", "Weak", "Replace"]))

    st.markdown('<div class="section">Fleet status</div>', unsafe_allow_html=True)
    show_cols = [c for c in ["drone_id","drone_name","model","assigned_pilot","location","next_inspection_due","current_status","notes"] if c in drones.columns]
    st.dataframe(drones[show_cols], use_container_width=True, hide_index=True)
    st.markdown('<div class="section">Open maintenance issues</div>', unsafe_allow_html=True)
    if "status" in issues.columns:
        st.dataframe(issues[issues["status"].isin(["Open", "In Progress", "On Hold"])], use_container_width=True, hide_index=True)

elif page == "Drone Register":
    tab1, tab2 = st.tabs(["Update drone", "Add new drone"])
    with tab1:
        st.dataframe(drones, use_container_width=True, hide_index=True)
        with st.form("update_drone"):
            drone_id = st.selectbox("Drone ID", drones["drone_id"].tolist())
            row = drones.loc[drones["drone_id"] == drone_id].iloc[0]
            current = row["current_status"]
            status = st.selectbox("Status", STATUS, index=STATUS.index(current) if current in STATUS else 0)
            location = st.text_input("Location", row["location"])
            notes = st.text_area("Notes", row["notes"])
            if st.form_submit_button("Update drone"):
                update("drones", "drone_id", drone_id, {"current_status": status, "location": location, "notes": notes})
                st.success("Drone updated.")
    with tab2:
        with st.form("add_drone"):
            drone_id = st.text_input("Drone ID", next_id("DRN", drones, "drone_id"))
            drone_name = st.text_input("Drone Name")
            manufacturer = st.text_input("Manufacturer")
            model = st.text_input("Model")
            owner_team = st.text_input("Owner Team")
            pilot = st.text_input("Assigned Pilot")
            location = st.text_input("Location")
            due = st.date_input("Next Inspection Due", date.today())
            status = st.selectbox("Status", STATUS)
            notes = st.text_area("Notes")
            if st.form_submit_button("Add drone"):
                insert("drones", {"drone_id": drone_id, "drone_name": drone_name, "manufacturer": manufacturer, "model": model, "owner_team": owner_team, "assigned_pilot": pilot, "location": location, "next_inspection_due": str(due), "current_status": status, "notes": notes})
                st.success("Drone added.")

elif page == "Battery Management":
    tab1, tab2 = st.tabs(["Update battery", "Add new battery"])
    with tab1:
        st.dataframe(batteries, use_container_width=True, hide_index=True)
        with st.form("update_battery"):
            battery_id = st.selectbox("Battery ID", batteries["battery_id"].tolist())
            old = batteries.loc[batteries["battery_id"] == battery_id].iloc[0]
            health_opts = ["Good","Needs Review","Weak","Replace"]
            status_opts = ["Available","In Use","Charging","Damaged","Retired"]
            health = st.selectbox("Health Status", health_opts, index=health_opts.index(old["health_status"]) if old["health_status"] in health_opts else 0)
            status = st.selectbox("Current Status", status_opts, index=status_opts.index(old["current_status"]) if old["current_status"] in status_opts else 0)
            cycle = st.number_input("Cycle Count", min_value=0, value=int(old["cycle_count"]))
            notes = st.text_area("Notes", old["notes"])
            if st.form_submit_button("Update battery"):
                update("batteries", "battery_id", battery_id, {"health_status": health, "current_status": status, "cycle_count": int(cycle), "notes": notes})
                st.success("Battery updated.")
    with tab2:
        with st.form("add_battery"):
            battery_id = st.text_input("Battery ID", next_id("BAT", batteries, "battery_id"))
            drone_id = st.selectbox("Compatible Drone ID", drones["drone_id"].tolist())
            btype = st.text_input("Battery Type", "LiPo")
            cycle = st.number_input("Cycle Count", min_value=0, value=0)
            health = st.selectbox("Health Status", ["Good","Needs Review","Weak","Replace"])
            status = st.selectbox("Current Status", ["Available","In Use","Charging","Damaged","Retired"])
            storage = st.text_input("Storage Location")
            notes = st.text_area("Notes")
            if st.form_submit_button("Add battery"):
                insert("batteries", {"battery_id": battery_id, "compatible_drone_id": drone_id, "battery_type": btype, "cycle_count": int(cycle), "health_status": health, "current_status": status, "storage_location": storage, "notes": notes})
                st.success("Battery added.")

elif page == "Inspection Form":
    st.info("Demo scenario: set Motor Check = Fail and Final Result = Fail. The selected drone will be marked Not Ready.")
    with st.form("inspection"):
        d = st.date_input("Inspection Date", date.today())
        drone_id = st.selectbox("Drone ID", drones["drone_id"].tolist())
        battery_id = st.selectbox("Battery ID", batteries["battery_id"].tolist())
        inspector = st.text_input("Inspector", "Vedik Dhyani")
        pre = st.selectbox("Pre-flight Check", CHECK)
        prop = st.selectbox("Propeller Check", CHECK)
        motor = st.selectbox("Motor Check", CHECK)
        camera = st.selectbox("Camera Check", CHECK)
        gps = st.selectbox("GPS Check", CHECK)
        controller = st.selectbox("Controller Check", CHECK)
        damage = st.selectbox("Damage Found?", YESNO)
        final = st.selectbox("Final Result", CHECK)
        notes = st.text_area("Notes")
        auto = st.checkbox("Automatically set drone Not Ready if Final Result = Fail", True)
        if st.form_submit_button("Submit inspection"):
            inspection_id = next_id("INS", inspections, "inspection_id")
            insert("inspections", {"inspection_id": inspection_id, "inspection_date": str(d), "drone_id": drone_id, "battery_id": battery_id, "pre_flight_check": pre, "propeller_check": prop, "motor_check": motor, "camera_check": camera, "gps_check": gps, "controller_check": controller, "damage_found": damage, "inspector": inspector, "final_result": final, "notes": notes})
            if auto and final == "Fail":
                update("drones", "drone_id", drone_id, {"current_status": "Not Ready"})
            st.success("Inspection saved.")

elif page == "Flight Log Form":
    with st.form("flight"):
        d = st.date_input("Flight Date", date.today())
        drone_id = st.selectbox("Drone ID", drones["drone_id"].tolist())
        battery_id = st.selectbox("Battery ID", batteries["battery_id"].tolist())
        pilot = st.text_input("Pilot", "Vedik Dhyani")
        mission = st.selectbox("Mission Type", MISSION_TYPES)
        duration = st.number_input("Flight Duration in Minutes", min_value=0, value=30)
        location = st.text_input("Location", "Chemnitz")
        pre = st.selectbox("Pre-flight Result", CHECK)
        post = st.selectbox("Post-flight Result", CHECK)
        issue = st.selectbox("Issue Reported?", YESNO)
        remarks = st.text_area("Remarks")
        if st.form_submit_button("Submit flight log"):
            flight_id = next_id("FLT", flights, "flight_id")
            insert("flights", {"flight_id": flight_id, "flight_date": str(d), "drone_id": drone_id, "battery_id": battery_id, "pilot_name": pilot, "mission_type": mission, "flight_duration_min": int(duration), "location": location, "pre_flight_result": pre, "post_flight_result": post, "issue_reported": issue, "remarks": remarks})
            st.success("Flight log saved.")

elif page == "Maintenance Issue Form":
    st.info("Demo scenario: create a Critical Open issue. The selected drone will be marked Not Ready.")
    with st.form("issue"):
        d = st.date_input("Date Reported", date.today())
        drone_id = st.selectbox("Drone ID", drones["drone_id"].tolist())
        issue_type = st.selectbox("Issue Type", ["Propeller damage","Battery issue","Motor issue","Camera/sensor issue","GPS issue","Controller issue","Frame damage","Software/firmware issue","Other"])
        severity = st.selectbox("Severity", SEVERITY)
        action = st.text_area("Action Required")
        person = st.text_input("Responsible Person", "Technician")
        status = st.selectbox("Status", ISSUE_STATUS)
        notes = st.text_area("Notes")
        auto = st.checkbox("Automatically set drone Not Ready for High/Critical open issue", True)
        if st.form_submit_button("Submit issue"):
            issue_id = next_id("MNT", issues, "issue_id")
            insert("maintenance_issues", {"issue_id": issue_id, "date_reported": str(d), "drone_id": drone_id, "issue_type": issue_type, "severity": severity, "action_required": action, "responsible_person": person, "status": status, "closure_date": None, "notes": notes})
            if auto and status != "Closed" and severity in ["High", "Critical"]:
                update("drones", "drone_id", drone_id, {"current_status": "Not Ready"})
            st.success("Maintenance issue saved.")

elif page == "Readiness Report":
    txt = report_text(drones, batteries, flights, inspections, issues)
    st.text_area("Report preview", txt, height=420)
    st.download_button("Download report", txt, f"DroneOps_QA_Validation_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.md", "text/markdown")

elif page == "Validation Feedback":
    st.markdown('<div class="section">Validation feedback</div>', unsafe_allow_html=True)
    st.write("Use this page after showing the prototype to a drone user, pilot, trainer or operations manager.")
    with st.form("feedback"):
        respondent = st.text_input("Respondent name or initials")
        org_type = st.selectbox("Type of user/team", ["Drone inspection company", "Industrial maintenance team", "Security team", "Emergency/rescue team", "University/research team", "Training school", "Hobby/prosumer", "Other"])
        current_method = st.text_area("How do you currently track drone readiness, batteries and maintenance?")
        usefulness = st.slider("How useful is this workflow?", 1, 5, 3)
        missing = st.text_area("What is missing before you would use this?")
        willingness = st.selectbox("Would you test this with real non-confidential data?", ["Yes", "Maybe", "No"])
        contact = st.text_input("Optional contact email")
        submitted = st.form_submit_button("Submit feedback")
        if submitted:
            payload = {
                "submitted_at": datetime.now().isoformat(),
                "respondent": respondent,
                "org_type": org_type,
                "current_method": current_method,
                "usefulness": usefulness,
                "missing_features": missing,
                "willingness_to_test": willingness,
                "contact": contact
            }
            try:
                insert("validation_feedback", payload)
                st.success("Feedback saved. Thank you.")
            except Exception as e:
                st.error("Could not save feedback. Make sure the validation_feedback table exists in Supabase.")
                st.exception(e)

elif page == "QR Workflow":
    st.markdown('<div class="section">QR workflow</div>', unsafe_allow_html=True)
    st.write("For validation, create QR codes that point to the deployed app URL. In later versions, QR links can open pre-filled pages for a specific Drone ID.")
    st.code("Suggested QR label:\n\nDroneOps QA\nScan before flight\n1. Open Inspection Form\n2. Select Drone ID\n3. Select Battery ID\n4. Complete checklist\n5. Submit result\n\nIf Final Result = Fail, drone must not fly.")
    st.warning("Current Streamlit pages do not yet support direct deep links to a specific form state. That should be a later improvement.")

elif page == "Demo Controls":
    st.markdown('<div class="section">Demo controls</div>', unsafe_allow_html=True)
    admin_password = secret_value("ADMIN_PASSWORD", "")
    if admin_password and not st.session_state.get("admin_access_granted"):
        with st.form("admin_login"):
            pw = st.text_input("Admin password", type="password")
            if st.form_submit_button("Unlock demo controls"):
                if pw == admin_password:
                    st.session_state.admin_access_granted = True
                    st.rerun()
                else:
                    st.error("Incorrect admin password.")
        st.stop()

    st.warning("These controls modify the shared Supabase demo database.")
    if st.button("Reset cloud demo database"):
        reset_demo()
        st.success("Database reset to demo baseline.")
