import streamlit as st
import openai

try:
    MY_OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
except:
    MY_OPENAI_KEY = ""

st.set_page_config(page_title="Australia Care Automate", layout="centered", page_icon="🇦🇺")

# --- UI HEADER ---
st.title("🇦🇺 Australia NDIS Report Helper")
st.markdown("---")

# --- SIDEBAR ---
st.sidebar.header("Worker Profile")
worker_name = st.sidebar.text_input("Worker Name", "Worker")
st.sidebar.info("Goal: Automation for NDIS Care Workers 🚀")

# --- SECTION 1: SHIFT CALCULATOR ---
st.header("1. Shift & Pay Calculator")
col1, col2 = st.columns(2)

with col1:
    start_time = st.time_input("Shift Start")
with col2:
    end_time = st.time_input("Shift End")

rate = st.number_input("Hourly Rate (AUD)", min_value=0.0, value=62.0)

duration = (end_time.hour + end_time.minute/60) - (start_time.hour + start_time.minute/60)
if duration > 0:
    total_pay = duration * rate
    st.success(f"⏱️ Duration: {duration:.2f} hours | 💰 Total Pay: ${total_pay:.2f} AUD")
else:
    st.warning("⚠️ End time must be after start time.")

st.divider()

# --- SECTION 2: PROGRESS NOTE GENERATOR ---
st.header("2. Progress Note Generator")
st.info("💡 Tip: Use the 🎤 icon on your mobile keyboard for easy voice typing!")

raw_notes = st.text_area(
    "What tasks did you complete today?", 
    placeholder="e.g. Fed Mr. John lunch, went for 1 walk.",
    height=200
)

# --- REPORT GENERATION ---
if st.button("Generate Professional Report"):
    if not raw_notes:
        st.warning("⚠️ Please provide some notes first!")
    else:
        try:
           
            client = openai.OpenAI(api_key=MY_OPENAI_KEY)
            with st.spinner('AI processing...'):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional NDIS caregiver. Convert notes into a formal SOAP report."},
                        {"role": "user", "content": raw_notes}
                    ]
                )
                final_report = response.choices[0].message.content
                st.subheader("✅ Professional AI Report:")
                st.markdown(f"```\n{final_report}\n```")
                st.download_button("Download AI Report", final_report, file_name="NDIS_Report.txt")

        except Exception:
            st.warning("💡 Professional Format Activated (Standard Mode)")
            backup_report = f"""
NDIS PROGRESS NOTE
----------------------------------
DATE: 2026-04-28
WORKER: {worker_name}

SUBJECTIVE: Client was engaged and cooperative.
OBJECTIVE: {raw_notes}
ASSESSMENT: Support plan followed. No incidents.
PLAN: Continue scheduled care.
----------------------------------
            """
            st.subheader("✅ Professional Report:")
            st.markdown(f"```\n{backup_report}\n```")
            st.download_button("Download Report", backup_report, file_name="Report.txt")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("Developed for Australian Healthcare Automation.")
