# import os
# import streamlit as st
# import pandas as pd
# import numpy as np
# import folium
# from folium.plugins import HeatMap
# import plotly.express as px
# import datetime
# import joblib
# from sklearn.preprocessing import LabelEncoder

# if "page" not in st.session_state:
#     st.session_state.page = "Home"
# if "auth_mode" not in st.session_state:
#     st.session_state.auth_mode = None

# st.set_page_config(page_title="🛡️ Sakhi Women Safety", layout="wide")

# # -------------------- UI / CSS --------------------
# st.markdown("""
# <style>
# :root {
#     --brand:#0b3d91;
#     --accent:#1abc9c;
#     --muted:#6b7280;
#     --card-bg: #ffffff;
# }
# .stApp {
#     background-color: #f4f7fb;
#     color: #0b1b3a;
#     font-family: 'Segoe UI', sans-serif;
# }

# /* Navigation */
# .nav-pill {
#     background: white;
#     border-radius: 12px;
#     padding: 8px 20px;
#     margin: 0 14px;
#     border: 1px solid rgba(11,61,145,0.08);
#     box-shadow: 0 4px 14px rgba(11,61,145,0.03);
#     color: var(--brand);
#     font-weight: 600;
#     transition: all 0.2s ease;
# }
# .nav-pill:hover {
#     background: var(--accent);
#     color: white;
#     transform: translateY(-2px);
# }
# .nav-active {
#     background: var(--brand);
#     color: white;
#     box-shadow: 0 6px 18px rgba(11,61,145,0.2);
# }

# /* Cards */
# .card {
#     background: rgba(255,255,255,0.9);
#     border-radius: 16px;
#     padding: 20px;
#     box-shadow: 0 8px 24px rgba(0,0,0,0.05);
#     margin-bottom: 20px;
#     border: 1px solid rgba(11,61,145,0.12);
#     backdrop-filter: blur(6px);
#     transition: all 0.25s ease;
# }
# .card:hover {
#     transform: translateY(-4px) scale(1.02);
#     box-shadow: 0 12px 28px rgba(0,0,0,0.12);
#     border-color: var(--accent);
# }

# /* Metrics */
# .metric-box {
#     background: linear-gradient(135deg, #1abc9c, #16a085);
#     color: white;
#     padding: 16px;
#     border-radius: 14px;
#     text-align: center;
#     font-weight: 600;
#     box-shadow: 0 6px 16px rgba(0,0,0,0.1);
# }
# .metric-value {
#     font-size: 28px;
#     margin-top: 8px;
# }

# /* Buttons */
# .stButton>button {
#     background: linear-gradient(90deg, var(--brand), var(--accent));
#     color: white;
#     font-weight:600;
#     border-radius: 10px;
#     padding: 10px 20px;
#     border: none;
#     box-shadow: 0 4px 10px rgba(0,0,0,0.15);
#     transition: all 0.2s ease;
# }
# .stButton>button:hover {
#     background: linear-gradient(90deg, var(--accent), var(--brand));
#     transform: translateY(-2px);
# }

# /* Footer */
# .footer-note {
#     text-align: center;
#     font-size: 12px;
#     color: #6b7280;
#     margin-top: 50px;
#     padding: 10px 0;
# }
# </style>
# """, unsafe_allow_html=True)

# # -------------------- Data and Utils --------------------
# def load_data():
#     df = pd.read_csv('vadodara_crime_dataset_expanded (2).csv')
#     df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
#     df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
#     df["Lon"] = pd.to_numeric(df["Lon"], errors="coerce")
#     if "Victim_Age_Group" in df.columns and "Victim_Age" not in df.columns:
#         def parse_age(s):
#             if pd.isna(s): return np.nan
#             s = str(s).lower().strip()
#             if "-" in s:
#                 a, b = s.split("-", 1)
#                 try: return (float(a) + float(b))/2
#                 except: return np.nan
#             if s.endswith("+"):
#                 try: return float(s[:-1]) + 5.0
#                 except: return np.nan
#             if "teen" in s: return 16.0
#             try: return float(s)
#             except: return np.nan
#         df["Victim_Age"] = df["Victim_Age_Group"].apply(parse_age)
#     return df

# def load_model(path="zone_risk_xgb.pkl"):
#     model, ref_agg = joblib.load(path)
#     return model, ref_agg

# def load_zone_status():
#     try:
#         return pd.read_csv("zone_status.csv")
#     except:
#         return pd.DataFrame(columns=["Area","Status","Officer","Timestamp"])

# def save_zone_status(df):
#     df.to_csv("zone_status.csv", index=False)


# # -------------------- App Entry Logic --------------------
# if st.session_state.auth_mode is None:
#     st.image("https://img.icons8.com/fluency/48/000000/security-checked.png", width=60)
#     st.title("🛡️ Sakhi — Women Safety Platform")
#     st.markdown("> Login below if you are police or government officer, or continue as public access user.")
#     c1, c2 = st.columns(2)
#     with c1:
#         if st.button("👮 Officer Login"):
#             st.session_state.auth_mode = "police"
#     with c2:
#         if st.button("🙋 Public Access"):
#             st.session_state.auth_mode = "public"
#     st.stop()

# # Police login page
# if st.session_state.auth_mode == "police" and "logged_in" not in st.session_state:
#     st.title("👮 Police Login")
#     u = st.text_input("Username")
#     p = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if u in ["admin","officer"] and ((u=="admin" and p=="password123") or (u=="officer" and p=="securepwd")):
#             st.session_state.logged_in = True
#             st.session_state.officer = u
#             st.success(f"Welcome {u.capitalize()}!")
#             st.experimental_rerun()
#         else:
#             st.error("❌ Invalid credentials")
#     st.stop()

# # # Public dashboard
# # if st.session_state.auth_mode == "public":
# #     st.title("🕊️ Sakhi — Women Safety Dashboard")
# #     st.markdown("It is for community awareness and safety reporting.")

# #     data = load_data()



# #     st.title("🛡️ Women Safety — Vadodara")

# #     # Emergency quick call buttons with tel: links (for mobile click-to-call)
# #     st.header("🚨 Emergency Quick Calls")
# #     if st.button("📞 Call Police (100)"):
# #         st.markdown('<a href="tel:100">Click here if call not initiated automatically</a>', unsafe_allow_html=True)
# #     if st.button("📞 Call Women’s Helpline (1091)"):
# #         st.markdown('<a href="tel:1091">Click here if call not initiated automatically</a>', unsafe_allow_html=True)
# #     if st.button("📞 Call Ambulance (108)"):
# #         st.markdown('<a href="tel:108">Click here if call not initiated automatically</a>', unsafe_allow_html=True)

# #     # Trusted contacts inputs
# #     st.header("👥 Trusted Contacts Setup")
# #     contact1 = st.text_input("Trusted Contact 1 Name")
# #     phone1 = st.text_input("Trusted Contact 1 Phone Number")
# #     contact2 = st.text_input("Trusted Contact 2 Name (Optional)")
# #     phone2 = st.text_input("Trusted Contact 2 Phone Number (Optional)")
# #     contact3 = st.text_input("Trusted Contact 3 Name (Optional)")
# #     phone3 = st.text_input("Trusted Contact 3 Phone Number (Optional)")

# #     if st.button("📲 Generate Quick SOS Message"):
# #         contacts = []
# #         if contact1 and phone1:
# #             contacts.append(f"{contact1}: {phone1}")
# #         if contact2 and phone2:
# #             contacts.append(f"{contact2}: {phone2}")
# #         if contact3 and phone3:
# #             contacts.append(f"{contact3}: {phone3}")
# #         if contacts:
# #             msg = "SOS! I need help. Please contact immediately:\n" + "\n".join(contacts) + "\nLocation: [Share your Google Maps link here]"
# #             st.text_area("Copy this message and send it instantly when needed:", value=msg, height=120)
# #         else:
# #             st.warning("Please enter at least one trusted contact and phone number.")

# #     # Nearest safe spot finder - example contacts
# #     st.header("📍 Nearest Safe Spots")
# #     SAFE_SPOTS = {
# #         "Alkapuri": {"Police Station": "Alkapuri PS, 0265-XXXXXXX", "Shelter": "Alkapuri Women Shelter, 1800-XXX-XXXX"},
# #         "Sayajigunj": {"Police Station": "Sayajigunj PS, 0265-YYYYYYY", "Shelter": "Sayajigunj Shelter, 1800-YYY-YYYY"},
# #         # Add more as needed
# #     }
# #     area_choice = st.selectbox("Select Your Area", list(SAFE_SPOTS.keys()))
# #     if area_choice:
# #         spots = SAFE_SPOTS[area_choice]
# #         for place, contact in spots.items():
# #             st.write(f"**{place}:** {contact}")

# #     st.info("Call 100 or 1091 immediately in case of emergency.")

# #     # Safe-travel checklist
# #     st.header("✅ Safe-Travel Self-Checklist")
# #     c1 = st.checkbox("Informed trusted person about my route")
# #     c2 = st.checkbox("Phone is charged")
# #     c3 = st.checkbox("Shared live location with trusted contact")
# #     c4 = st.checkbox("Carrying self-defense items (pepper spray/whistle)")

# #     if c1 and c2 and c3 and c4:
# #         st.success("You are well-prepared! Stay safe on your journey! 🌟")
# #     else:
# #         st.warning("Please complete all checklist items before going out.")

# #     # One-click copy example location link
# #     st.header("📌 Copy Location Link to Share")
# #     example_location = "https://maps.google.com/?q=22.3072,73.1812"
# #     if st.button("📋 Copy Example Location Link"):
# #         # Uses JS clipboard api via Streamlit component
# #         st.experimental_set_query_params(location=example_location)
# #         st.success("Example location link copied to clipboard! Paste it in your message app.")
# #     else:
# #         st.code(example_location)


# #     st.subheader("📅 Monthly Crime Reports")
# #     last_year = data[data.Date > (pd.Timestamp.today() - pd.Timedelta(days=365))]
# #     monthly = last_year.groupby(last_year["Date"].dt.to_period("M")).size()
# #     fig = px.bar(x=monthly.index.astype(str), y=monthly.values, labels={"x":"Month", "y":"Number of Incidents"}, title="Monthly Crime Reports")
# #     st.plotly_chart(fig, use_container_width=True)

# #     st.subheader("🙋 Submit a Safety Concern")
# #     msg = st.text_area("Describe your concern or report anonymously (goes to authorities):")
# #     if st.button("📬 Submit Report"):
# #         if msg.strip():
# #             pd.DataFrame([{"msg": msg, "time": str(pd.Timestamp.now())}]).to_csv("public_concerns.csv", mode="a", index=False, header=False)
# #             st.success("Thank you for your report!")
# #         else:
# #             st.warning("Please enter a message before submitting.")

# #     if st.button("⬅️ Home / Log Out"):
# #         for k in ["auth_mode", "logged_in", "officer"]:
# #             if k in st.session_state:
# #                 del st.session_state[k]
# #         st.experimental_rerun()

# # Police dashboard

# if st.session_state.auth_mode == "police":

#     if "nav_page" not in st.session_state:
#         st.session_state.nav_page = "dashboard"

#     # Navigation cards (horizontal)
#     nav_items = [
#         ("🏙️ Dashboard", "dashboard"),
#         ("🔮 Zone Prediction", "zone-pred"),
#         ("🛡️ Zone Management", "zone-mgmt"),
#         ("💬 Improvement Suggestions", "suggestions"),
#     ]
#     cols = st.columns(len(nav_items))
#     for idx, (label, key) in enumerate(nav_items):
#         classes = "nav-active" if st.session_state.nav_page == key else "nav-pill"
#         if cols[idx].button(label, key=key):
#             st.session_state.nav_page = key
#         #cols[idx].markdown(f"<div class='{classes}'>{label}</div>", unsafe_allow_html=True)

#     data = load_data()
#     status_df = load_zone_status()
#     model, ref_agg = load_model()

#     if st.session_state.nav_page == "dashboard":
#         st.title("🏙️ Citywide Crime Map")
#         m = folium.Map(location=[data["Lat"].mean(), data["Lon"].mean()], zoom_start=12)
#         for _, row in data.iterrows():
#             color = "red" if row["Severity"] == "High" else "orange" if row["Severity"]=="Medium" else "green"
#             folium.CircleMarker(
#                 [row["Lat"], row["Lon"]],
#                 radius=6,
#                 color=color,
#                 fill=True,
#                 fill_opacity=0.7,
#                 popup=f"Crime: {row['Type_of_Crime']}<br>Date/Time: {row['Date']} {row['Time']}<br>Severity: {row['Severity']}"
#             ).add_to(m)
#         st.components.v1.html(m._repr_html_(), height=700)

#     elif st.session_state.nav_page == "zone-pred":
#         st.title("🔮 Zone-wise Risk Prediction")
#         area = st.selectbox("Area", sorted(data["Area"].unique()))
#         min_age, max_age = int(data["Victim_Age"].min()), int(data["Victim_Age"].max())
#         age_range = st.slider("Victim Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
#         times_of_day = ["All","Morning (6-12)","Afternoon (12-17)","Evening (17-21)","Night (21-6)"]
#         tod = st.selectbox("Time of Day", times_of_day)
#         days = ["All"] + list(data["Day"].dropna().unique())
#         weekday = st.selectbox("Day", days)

#         filtered = data[data["Area"] == area].copy()
#         filtered = filtered[filtered["Victim_Age"].between(*age_range)]
#         if weekday != "All":
#             filtered = filtered[filtered["Day"] == weekday]
#         if tod != "All":
#             hour = filtered["Time"].astype(str).str[:2].astype(int)
#             if tod == "Morning (6-12)":
#                 filtered = filtered[(hour >= 6) & (hour < 12)]
#             elif tod == "Afternoon (12-17)":
#                 filtered = filtered[(hour >= 12) & (hour < 17)]
#             elif tod == "Evening (17-21)":
#                 filtered = filtered[(hour >= 17) & (hour < 21)]
#             elif tod == "Night (21-6)":
#                 filtered = filtered[(hour >= 21) | (hour < 6)]

#         m = folium.Map(location=[filtered["Lat"].mean(), filtered["Lon"].mean()], zoom_start=14)
#         for _, row in filtered.iterrows():
#             color = "red" if row["Severity"] == "High" else "orange" if row["Severity"] == "Medium" else "green"
#             popup_html = f"""<b>ID:</b> {row['Incident_ID']}<br>
#                              <b>Crime:</b> {row['Type_of_Crime']}<br>
#                              <b>Date/Time:</b> {row['Date']} {row['Time']}<br>
#                              <b>Day:</b> {row['Day']}<br>
#                              <b>Victim Age:</b> {row['Victim_Age']}<br>
#                              <b>Severity:</b> {row['Severity']}"""
#             folium.CircleMarker([row["Lat"], row["Lon"]], radius=7, color=color,
#                                 fill=True, fill_opacity=0.7, popup=popup_html).add_to(m)
#         st.components.v1.html(m._repr_html_(), height=600)

#         if st.button("🔮 Predict Zone Severity"):
#             total = len(filtered)
#             high_ct = (filtered["Severity"] == "High").sum()
#             reason = ""
#             if total == 0:
#                 zone_risk = "No data"
#                 reason = "No matching incidents in this selection."
#             elif high_ct >= 3:
#                 zone_risk = "🔴 High"
#                 reason = f"{high_ct} high severity incidents among {total} selected cases."
#             elif high_ct == 2:
#                 zone_risk = "🟠 Medium"
#                 reason = "2 high severity incidents recently."
#             else:
#                 zone_risk = "🟢 Low"
#                 reason = f"Only {high_ct} high severity incident(s)."

#             st.success(f"Predicted Severity: {zone_risk}\n\nReason: {reason}")

#             if total > 0:
#                 m2 = folium.Map(location=[filtered["Lat"].mean(), filtered["Lon"].mean()], zoom_start=14)
#                 for _, row in filtered.iterrows():
#                     folium.CircleMarker([row["Lat"], row["Lon"]], radius=7, color="grey", fill=True, fill_opacity=0.3).add_to(m2)
#                 folium.Circle([filtered["Lat"].mean(), filtered["Lon"].mean()], radius=600,
#                               color="red" if "🔴" in zone_risk else "orange" if "🟠" in zone_risk else "green",
#                               fill=True, fill_opacity=0.2).add_to(m2)
#                 st.components.v1.html(m2._repr_html_(), height=600)

#     elif st.session_state.nav_page == "zone-mgmt":
#         st.title("🛡️ Zone Management")
#         area = st.selectbox("Select Zone", sorted(data["Area"].unique()))
#         status_options = ["⚠️ Unsafe", "🟡 Under Observation", "🟢 Safe"]
#         sel_status = st.selectbox("Set Zone Status", status_options)
#         if st.button("💾 Save Status"):
#             now = str(datetime.datetime.now())
#             status_df = status_df[status_df["Area"] != area]
#             new_row = pd.DataFrame([{"Area": area, "Status": sel_status,
#                                       "Officer": st.session_state.get("officer", ""),
#                                       "Timestamp": now}])
#             status_df = pd.concat([status_df, new_row], ignore_index=True)
#             save_zone_status(status_df)
#             st.success(f"Zone '{area}' status set to {sel_status}")
#         st.markdown("### Zone Status Log")
#         st.dataframe(status_df.sort_values("Timestamp", ascending=False))

#     elif st.session_state.nav_page == "suggestions":
#         st.title("💬 Improvement Suggestions & Notices")
#         suggestion_file = "improvement_suggestions.csv"
#         if "suggestions_df" not in st.session_state:
#             try:
#                 st.session_state.suggestions_df = pd.read_csv(suggestion_file)
#             except FileNotFoundError:
#                 st.session_state.suggestions_df = pd.DataFrame(columns=["User", "Message", "Timestamp"])
#         user_msg = st.text_area("Enter message for colleagues/officers:")
#         if st.button("Send Message"):
#             if user_msg.strip():
#                 new_row = {"User": st.session_state.get("officer", "Unknown"),
#                            "Message": user_msg.strip(),
#                            "Timestamp": str(datetime.datetime.now())}
#                 st.session_state.suggestions_df = pd.concat([st.session_state.suggestions_df, pd.DataFrame([new_row])], ignore_index=True)
#                 st.session_state.suggestions_df.to_csv(suggestion_file, index=False)
#                 st.success("Message sent!")
#                 st.experimental_rerun()
#             else:
#                 st.warning("Please enter a message before sending.")
#         st.markdown("### Past Messages")
#         for _, row in st.session_state.suggestions_df.sort_values("Timestamp", ascending=False).iterrows():
#             st.markdown(f"- **{row['User']}** ({row['Timestamp']}): {row['Message']}")

# # Footer
# from datetime import datetime
# year_now = datetime.now().year
# st.markdown(f"<div class='footer-note'>© {year_now} Sakhi. All rights reserved.</div>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.express as px
import datetime
import joblib

st.set_page_config(page_title="🛡️ Sakhi Women Safety", layout="wide")

# CSS Styles, keep yours here...
st.markdown("""
<style>
<style>
:root {
    --brand:#0b3d91;
    --accent:#1abc9c;
    --muted:#6b7280;
    --card-bg: #ffffff;
}
.stApp {
    background-color: #f4f7fb;
    color: #0b1b3a;
    font-family: 'Segoe UI', sans-serif;
}

/* Navigation */
.nav-pill {
    background: linear-gradient(90deg, #0b3d91 0%, #1abc9c 100%);
    border-radius: 12px;
    padding: 8px 20px;
    margin: 0 14px;
    border: none;
    color: white;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(11,61,145,0.09);
    transition: all 0.2s ease;
}
.nav-pill:hover {
    background: linear-gradient(90deg, #1abc9c 0%, #0b3d91 100%);
    color: white;
    transform: translateY(-2px);
}
.nav-active {
    background: linear-gradient(90deg, #166d9c, #13bd93);
    color: white;
    box-shadow: 0 6px 20px rgba(11,61,145,0.21);
}


/* Cards */
.card {
    background: rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.05);
    margin-bottom: 20px;
    border: 1px solid rgba(11,61,145,0.12);
    backdrop-filter: blur(6px);
    transition: all 0.25s ease;
}
.card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 28px rgba(0,0,0,0.12);
    border-color: var(--accent);
}

/* Metrics */
.metric-box {
    background: linear-gradient(135deg, #1abc9c, #16a085);
    color: white;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    font-weight: 600;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 28px;
    margin-top: 8px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, var(--brand), var(--accent));
    color: blue
    font-weight:600;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: all 0.2s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, var(--accent), var(--brand));
    transform: translateY(-2px);
}

/* Footer */
.footer-note {
    text-align: center;
    font-size: 12px;
    color: #6b7280;
    margin-top: 50px;
    padding: 10px 0;
}
</style>
""", unsafe_allow_html=True)
def load_data():
    df = pd.read_csv('vadodara_crime_dataset_expanded (2).csv')
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Lat"] = pd.to_numeric(df["Lat"], errors="coerce")
    df["Lon"] = pd.to_numeric(df["Lon"], errors="coerce")
    if "Victim_Age_Group" in df.columns and "Victim_Age" not in df.columns:
        def parse_age(s):
            if pd.isna(s): return np.nan
            s = str(s).lower().strip()
            if "-" in s:
                a, b = s.split("-", 1)
                try: return (float(a) + float(b))/2
                except: return np.nan
            if s.endswith("+"):
                try: return float(s[:-1]) + 5.0
                except: return np.nan
            if "teen" in s: return 16.0
            try: return float(s)
            except: return np.nan
        df["Victim_Age"] = df["Victim_Age_Group"].apply(parse_age)
    return df

def load_model(path="zone_risk_xgb.pkl"):
    model, ref_agg = joblib.load(path)
    return model, ref_agg

def load_zone_status():
    try:
        return pd.read_csv("zone_status.csv")
    except:
        return pd.DataFrame(columns=["Area","Status","Officer","Timestamp"])

def save_zone_status(df):
    df.to_csv("zone_status.csv", index=False)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

if not st.session_state.logged_in:
    # Splash UI
    st.markdown("""
    <style>
    .splash-logo-outer {
        margin-top: 80px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .splash-logo-bg {
        width: 80px;
        height: 80px;
        border-radius: 40px;
        background: radial-gradient(circle at 30% 30%, #4ef0d3 20%, #2a68ba 70%);
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        box-shadow: 0 0 30px #0b3d9177 inset, 0 4px 40px #1abc9c44;
    }
   @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');

    .splash-sakhi {
        font-family: 'Montserrat', sans-serif;
        font-size: 60px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        background: linear-gradient(90deg, #0b3d91, #1abc9c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 6px 32px rgba(11, 61, 145, 0.25);
        animation: fadein 2s;
    }

    .splash-tagline {
        font-family: 'Segoe UI', sans-serif;
        font-size: 22px;
        margin-top: 10px;
        color: #13bd93;
    }
    @keyframes fadein {
        from { opacity: 0; transform: scale(0.95);}
        to { opacity: 1; transform: scale(1);}
    }
    .stButton>button {
        background: linear-gradient(90deg, #0b3d91 0%, #1abc9c 100%) !important;
        color: white !important;
        font-weight:600 !important;
        border-radius: 12px !important;
        padding: 14px 38px !important;
        font-size: 20px !important;
        border: none !important;
        box-shadow: 0 4px 14px #0b3d9115 !important;
        transition: all 0.2s ease !important;
        margin: 0 auto;
        display: block;
        margin-top: 36px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1abc9c 0%, #0b3d91 100%) !important;
        transform: translateY(-2px) !important;
    }
   </style>
""", unsafe_allow_html=True)

# ✅ Add this small Python block right here
    # from PIL import Image
    # import streamlit as st

    # try:
    #     logo = Image.open("0b3d91.JPG")  # make sure the file is in same folder as this .py

    #     # ✅ Correct center alignment (Streamlit ignores HTML nesting, so use columns)
    #     st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
    #     col1, col2, col3 = st.columns([1.9,1, 3])
    #     with col2:
    #         st.image(logo, width=300)
    #     st.markdown("</div>", unsafe_allow_html=True)

    # except FileNotFoundError:
    #     st.warning("⚠️ 'logo.JPG' not found. Put it in the same folder as this script.")

    # Continue your HTML below
    st.markdown("""
    <div class="splash-logo-outer">
        <div class="splash-sakhi">Sakhi</div>
        <div class="splash-tagline">Empowering Safety. Enabling Trust.</div>
    </div>
    """, unsafe_allow_html=True)



    st.markdown("<br><br>", unsafe_allow_html=True)

    if not st.session_state.show_login:
        # Only this button - fully functional and styled
        if st.button("🔒 Login as Authority"):
            st.session_state.show_login = True

    if st.session_state.show_login:
        st.subheader("Police/Authority Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in ["admin", "officer"] and (
                (username == "admin" and password == "password123")
                or (username == "officer" and password == "securepwd")
            ):
                st.success(f"Welcome {username.capitalize()}! Redirecting...")
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid login credentials")

    st.stop()



if "page" not in st.session_state:
    st.session_state.page = "home"
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "dashboard"
    
# pages = ["Home", "Dashboard", "Zone Prediction", "Zone Management", "Improvement Suggestions"]
# nav_cols = st.columns(len(pages))

# for i, p in enumerate(pages):
#     if nav_cols[i].button(p, key=f"nav_{i}"):
#         st.session_state.page = p

if st.session_state.page == "home":
    st.markdown(
        """
        <div class="hero" style="display:flex; flex-direction:column; align-items:flex-start; gap: 20px;">
            <h1 style="font-family:'Montserrat',sans-serif; font-weight:800; color:#0b3d91;">
                👮🏻‍♀️  Sakhi — Women Safety System
            </h1>
            <div style="
                background-color: #ffffff; 
                border-radius: 16px; 
                padding: 25px; 
                box-shadow: 0 8px 24px rgba(0,0,0,0.05); 
                font-family: 'Segoe UI', sans-serif; 
                font-size: 20px; 
                line-height: 1.7; 
                color: #0b1b3a; 
                text-align: justify;
                margin-bottom: 30px;
            ">
            Introducing a next-generation Women Safety App for police and government agencies—empowering authorities to predict risks, monitor safety in real-time, and take proactive measures to protect communities. With interactive maps, dynamic updates, and data-driven insights, the app helps make every area safer for women.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    

    st.markdown("<h3>📱 About the App</h3>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            background-color: #ffffff; 
            border-radius: 16px; 
            padding: 25px; 
            box-shadow: 0 8px 24px rgba(0,0,0,0.05); 
            font-family: 'Segoe UI', sans-serif; 
            font-size: 20px; 
            line-height: 1.7; 
            color: #0b1b3a; 
            text-align: justify;
            margin-bottom: 30px;
        ">
            Our Women Safety App equips authorities with data-driven tools to predict, monitor, and manage risk in real-time. 
            Using crime type, frequency, time, and location, the app’s risk prediction model classifies areas to highlight potential danger zones. 
            Interactive heatmaps provide quick insights, while dynamic updates allow authorities to mark areas as ‘Safe’ after preventive actions such as patrolling, installing streetlights, or deploying CCTV. 
            With this platform, police and government agencies can monitor and update area statuses, allocate resources proactively, and evaluate the effectiveness of safety measures, ensuring a safer environment for all.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📘 How to Use")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='card'><h4>1️⃣ Dashboard</h4><p>Explore comprehensive crime statistics through interactive charts and maps that highlight key trends, patterns, and evolving citywide hotspots in real time</p></div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("<div class='card'><h4>2️⃣ Zone Prediction</h4><p>Utilize advanced predictive algorithms to evaluate potential risk levels across different zones, ensuring timely decision-making and efficient deployment of resources.</p></div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'><h4>3️⃣ Zone Management</h4><p>Monitor, manage, and update safety statuses for all identified zones, enabling accurate classification into Safe, Unsafe, or Under Observation categories for coordinated action.</p></div>", unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='card'><h4>4️⃣ Suggestions</h4><p>Submit, review, and implement safety improvement ideas from on-ground officers, helping strengthen community trust and ensure continuous operational enhancement.</p></div>", unsafe_allow_html=True)

    st.write("")

    if st.button("▶️ Explore More"):
        st.session_state.page = "dashboard"

elif st.session_state.page == "dashboard":
    # You should load data outside the if nav_page block since metrics need it
    data = load_data()
    status_df = load_zone_status()
    model, ref_agg = load_model()

    nav_items = [
        ("🏙️ Dashboard", "dashboard"),
        ("🔮 Zone Prediction", "zone-pred"),
        ("🛡️ Zone Management", "zone-mgmt"),
        ("💬 Improvement Suggestions", "suggestions"),
    ]
    cols = st.columns(len(nav_items))
    for idx, (label, key) in enumerate(nav_items):
        if cols[idx].button(label):
            st.session_state.nav_page = key

    if st.session_state.nav_page == "dashboard":
        st.title("🏙️ Citywide Crime Map")
        m = folium.Map(location=[data["Lat"].mean(), data["Lon"].mean()], zoom_start=12)
        for _, row in data.iterrows():
            color = "red" if row["Severity"] == "High" else "orange" if row["Severity"]=="Medium" else "green"
            folium.CircleMarker(
                [row["Lat"], row["Lon"]],
                radius=6,
                color=color,
                fill=True,
                fill_opacity=0.7,
                popup=f"Crime: {row['Type_of_Crime']}<br>Date/Time: {row['Date']} {row['Time']}<br>Severity: {row['Severity']}"
            ).add_to(m)
        st.components.v1.html(m._repr_html_(), height=700)
        ## --- Graph 1: Monthly Trend ---
        data["Month"] = data["Date"].dt.to_period("M").astype(str)
        monthly_counts = data.groupby("Month").size().reset_index(name="Incidents")
        fig_monthly = px.bar(monthly_counts, x="Month", y="Incidents", 
                                    title="Incidents per Month",
                                    labels={"Month": "Month", "Incidents": "Number of Incidents"},
                                    color="Incidents", color_continuous_scale="teal")
        st.plotly_chart(fig_monthly, use_container_width=True)

                # --- Graph 2: Crime Type Distribution ---
        top_types = data["Type_of_Crime"].value_counts().nlargest(8)
        fig_types = px.pie(names=top_types.index, values=top_types.values, 
                                title="Top 8 Crime Types Distribution",
                                color_discrete_sequence=px.colors.sequential.Blues)
        st.plotly_chart(fig_types, use_container_width=True)

    elif st.session_state.nav_page == "zone-pred":
        st.title("🔮 Zone-wise Risk Prediction")
        area = st.selectbox("Area", sorted(data["Area"].unique()))
        min_age, max_age = int(data["Victim_Age"].min()), int(data["Victim_Age"].max())
        age_range = st.slider("Victim Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
        times_of_day = ["All","Morning (6-12)","Afternoon (12-17)","Evening (17-21)","Night (21-6)"]
        tod = st.selectbox("Time of Day", times_of_day)
        days = ["All"] + list(data["Day"].dropna().unique())
        weekday = st.selectbox("Day", days)

        filtered = data[data["Area"] == area].copy()
        filtered = filtered[filtered["Victim_Age"].between(*age_range)]
        if weekday != "All":
            filtered = filtered[filtered["Day"] == weekday]
        if tod != "All":
            hour = filtered["Time"].astype(str).str[:2].astype(int)
            if tod == "Morning (6-12)":
                filtered = filtered[(hour >= 6) & (hour < 12)]
            elif tod == "Afternoon (12-17)":
                filtered = filtered[(hour >= 12) & (hour < 17)]
            elif tod == "Evening (17-21)":
                filtered = filtered[(hour >= 17) & (hour < 21)]
            elif tod == "Night (21-6)":
                filtered = filtered[(hour >= 21) | (hour < 6)]

        m = folium.Map(location=[filtered["Lat"].mean(), filtered["Lon"].mean()], zoom_start=14)
        for _, row in filtered.iterrows():
            color = "red" if row["Severity"] == "High" else "orange" if row["Severity"] == "Medium" else "green"
            popup_html = f"""<b>ID:</b> {row['Incident_ID']}<br>
                             <b>Crime:</b> {row['Type_of_Crime']}<br>
                             <b>Date/Time:</b> {row['Date']} {row['Time']}<br>
                             <b>Day:</b> {row['Day']}<br>
                             <b>Victim Age:</b> {row['Victim_Age']}<br>
                             <b>Severity:</b> {row['Severity']}"""
            folium.CircleMarker([row["Lat"], row["Lon"]], radius=7, color=color,
                                fill=True, fill_opacity=0.7, popup=popup_html).add_to(m)
        st.components.v1.html(m._repr_html_(), height=600)

        if st.button("🔮 Predict Zone Severity"):
            total = len(filtered)
            high_ct = (filtered["Severity"] == "High").sum()
            reason = ""
            if total == 0:
                zone_risk = "No data"
                reason = "No matching incidents in this selection."
            elif high_ct >= 3:
                zone_risk = "🔴 High"
                reason = f"{high_ct} high severity incidents among {total} selected cases."
            elif high_ct == 2:
                zone_risk = "🟠 Medium"
                reason = "2 high severity incidents recently."
            else:
                zone_risk = "🟢 Low"
                reason = f"Only {high_ct} high severity incident(s)."

            st.success(f"Predicted Severity: {zone_risk}\n\nReason: {reason}")

            if total > 0:
                m2 = folium.Map(location=[filtered["Lat"].mean(), filtered["Lon"].mean()], zoom_start=14)
                for _, row in filtered.iterrows():
                    folium.CircleMarker([row["Lat"], row["Lon"]], radius=7, color="grey", fill=True, fill_opacity=0.3).add_to(m2)
                folium.Circle([filtered["Lat"].mean(), filtered["Lon"].mean()], radius=600,
                              color="red" if "🔴" in zone_risk else "orange" if "🟠" in zone_risk else "green",
                              fill=True, fill_opacity=0.2).add_to(m2)
                st.components.v1.html(m2._repr_html_(), height=600)

    elif st.session_state.nav_page == "zone-mgmt":
        st.title("🛡️ Zone Management")
        area = st.selectbox("Select Zone", sorted(data["Area"].unique()))
        status_options = ["⚠️ Unsafe", "🟡 Under Observation", "🟢 Safe"]
        sel_status = st.selectbox("Set Zone Status", status_options)
        if st.button("💾 Save Status"):
            now = str(datetime.datetime.now())
            status_df = status_df[status_df["Area"] != area]
            new_row = pd.DataFrame([{"Area": area, "Status": sel_status,
                                    "Officer": st.session_state.get("officer", ""),
                                    "Timestamp": now}])
            status_df = pd.concat([status_df, new_row], ignore_index=True)
            save_zone_status(status_df)
            st.success(f"Zone '{area}' status set to {sel_status}")
        st.markdown("### Zone Status Log")
        st.dataframe(status_df.sort_values("Timestamp", ascending=False))

    elif st.session_state.nav_page == "suggestions":
        st.title("💬 Improvement Suggestions & Notices")
        suggestion_file = "improvement_suggestions.csv"
        if "suggestions_df" not in st.session_state:
            try:
                st.session_state.suggestions_df = pd.read_csv(suggestion_file)
            except FileNotFoundError:
                st.session_state.suggestions_df = pd.DataFrame(columns=["User", "Message", "Timestamp"])
        user_msg = st.text_area("Enter message for colleagues/officers:")
        if st.button("Send Message"):
            if user_msg.strip():
                new_row = {"User": st.session_state.get("officer", "Unknown"),
                           "Message": user_msg.strip(),
                           "Timestamp": str(datetime.datetime.now())}
                st.session_state.suggestions_df = pd.concat([st.session_state.suggestions_df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.suggestions_df.to_csv(suggestion_file, index=False)
                st.success("Message sent!")
                st.experimental_rerun()
            else:
                st.warning("Please enter a message before sending.")
        st.markdown("### Past Messages")
        for _, row in st.session_state.suggestions_df.sort_values("Timestamp", ascending=False).iterrows():
            st.markdown(f"- **{row['User']}** ({row['Timestamp']}): {row['Message']}")

# Footer
from datetime import datetime
st.markdown(f"<div class='footer-note'>© {datetime.now().year} Sakhi. All rights reserved.</div>", unsafe_allow_html=True)
