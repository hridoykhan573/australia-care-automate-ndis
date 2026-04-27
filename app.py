import streamlit as st
import openai

# 1. Page Configuration (Mobile Friendly)
st.set_page_config(
    page_title="NDIS Care Automate",
    page_icon="🤖",
    layout="centered"
)

# 2. Custom CSS for Mobile App Look
st.markdown("""
    <style>
    /* Full width buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    /* Input box styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 1px solid #ddd;
    }
    /* Header styling */
    .main-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure API Key Loading (From Streamlit Secrets)
# Make sure to add OPENAI_API_KEY in your Streamlit Dashboard Secrets!
api_key = st.secrets.get("OPENAI_API_KEY")

# 4. App Header
st.markdown('<p class="main-header">🤖 NDIS AI Report Assistant</p>', unsafe_allow_html=True)
st.write("---")

# 5. Shift Pay Calculator Section
with st.expander("💰 Shift Pay Calculator", expanded=False):
    rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=35.0)
    hours = st.number_input("Total Hours Worked", min_value=0.0, value=8.0)
    total_pay = rate * hours
    st.success(f"Estimated Pay: ${total_pay:,.2f}")

# 6. AI Progress Note Section
st.subheader("📝 Daily Progress Notes")

# Mic Instruction for Mobile Users
st.info("💡 **Tip:** Tap the 🎤 icon on your mobile keyboard to speak your notes!")

raw_notes = st.text_area(
    "What tasks did you complete today?", 
    placeholder="Example: Fed client breakfast, went for a 20 min walk, administered morning meds at 10 AM...",
    height=250
)

if st.button("Generate Professional Report"):
    if not api_key:
        st.error("API Key not found! Please add it to Streamlit Secrets.")
    elif not raw_notes.strip():
        st.warning("Please enter some notes first.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            
            with st.spinner("AI is writing your report..."):
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional NDIS care worker assistant. Convert raw notes into a formal, clinical SOAP report (Subjective, Objective, Assessment, Plan) using professional English."},
                        {"role": "user", "content": raw_notes}
                    ]
                )
                
                report = response.choices[0].message.content
                st.subheader("✅ Professional Report")
                st.markdown(f"```\n{report}\n```")
                
                # Download Button
                st.download_button(
                    label="📥 Download Report as TXT",
                    data=report,
                    file_name="NDIS_Progress_Note.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")

# 7. Footer
st.markdown("---")
st.caption("Developed by Hridoy Khan | Secure & Private")
