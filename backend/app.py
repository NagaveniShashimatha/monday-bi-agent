import streamlit as st
from monday_client import fetch_board_items
from data_cleaner import run_step_3
from bi_engine import generate_pipeline_insight

# -------------------------------
# App Title
# -------------------------------
st.set_page_config(page_title="Monday BI Agent", layout="centered")
st.title("📊 Monday.com Business Intelligence Agent")

# -------------------------------
# Session state (for follow-ups)
# -------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "quarter" not in st.session_state:
    st.session_state.quarter = None

# -------------------------------
# Fetch REAL data from monday.com
# -------------------------------
DEALS_BOARD_ID = 5026563827  # your real Deals board ID

raw_items = fetch_board_items(DEALS_BOARD_ID)

# Clean data (STEP 3)
result = run_step_3(raw_items)
cleaned_deals = result["cleaned_data"]
warnings = result["data_quality_notes"]

# -------------------------------
# User input
# -------------------------------
user_question = st.text_input("Ask a business question:")

# -------------------------------
# Simple intent handling
# -------------------------------
def handle_question(question):
    question = question.lower()

    if "pipeline" in question and "energy" in question:
        if st.session_state.quarter is None:
            return "Do you want the current quarter or next quarter?"

        return generate_pipeline_insight(cleaned_deals, warnings)

    if "leadership" in question:
        return (
            "📊 Leadership Update\n"
            "• Pipeline health is stable\n"
            "• Energy sector is dominant\n"
            "• Some data quality risks exist"
        )

    return "I can help with pipeline, sector performance, and leadership updates."

# -------------------------------
# Handle response
# -------------------------------
if user_question:
    st.session_state.conversation.append(("User", user_question))

    if user_question.lower() in ["current quarter", "this quarter"]:
        st.session_state.quarter = "current"
        response = generate_pipeline_insight(cleaned_deals, warnings)

    elif user_question.lower() in ["next quarter"]:
        st.session_state.quarter = "next"
        response = generate_pipeline_insight(cleaned_deals, warnings)

    else:
        response = handle_question(user_question)

    st.session_state.conversation.append(("Agent", response))

# -------------------------------
# Display conversation
# -------------------------------
for speaker, message in st.session_state.conversation:
    if speaker == "User":
        st.markdown(f"**🧑 User:** {message}")
    else:
        st.markdown(f"**🤖 Agent:** {message}")
