import streamlit as st
from openai import OpenAI
import os
import json
import pandas as pd

# =====================
# API KEY
# =====================
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Missing OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key)

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(page_title="AI Health Analyzer", layout="centered")

st.title("🧠 AI Health Risk Analyzer")

# =====================
# INPUT
# =====================
disease_name = st.text_input("Enter a disease name:")

# =====================
# OPENAI CALL
# =====================
def get_disease_info(disease_name):

    prompt = f"""
Return ONLY valid JSON about the disease: {disease_name}

Include:
- name
- risk_level (Low, Medium, High)
- symptoms (list)
- statistics:
    - total_cases (number)
    - recovery_rate (percentage string like 85%)
    - mortality_rate (percentage string like 5%)
- prevention (list)
- recovery_options (dictionary)
- medication (dictionary with name, side_effects list, dosage)

IMPORTANT: Return ONLY JSON, no text.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a medical data assistant that outputs only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# =====================
# DISPLAY FUNCTION
# =====================
def display_info(data):

    try:
        info = json.loads(data)

        st.subheader(info["name"])

        # Risk level
        st.info(f"Risk Level: {info['risk_level']}")

        # Symptoms
        st.write("### Symptoms")
        st.write(", ".join(info["symptoms"]))

        # Stats
        st.write("### Statistics")

        total_cases = info["statistics"]["total_cases"]
        recovery = float(info["statistics"]["recovery_rate"].strip("%"))
        mortality = float(info["statistics"]["mortality_rate"].strip("%"))

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Cases", f"{total_cases:,}")
        col2.metric("Recovery Rate", f"{recovery}%")
        col3.metric("Mortality Rate", f"{mortality}%")

        chart_data = pd.DataFrame({
            "Rate": [recovery, mortality]
        }, index=["Recovery", "Mortality"])

        st.bar_chart(chart_data)

        chart_data = pd.DataFrame({
            "Rate": [recovery, mortality]
        }, index=["Recovery", "Mortality"])

        st.bar_chart(chart_data)

        # Prevention
        st.write("### Prevention Tips")
        for p in info["prevention"]:
            st.write("•", p)

        # Recovery
        st.write("### Recovery Options")
        for k, v in info["recovery_options"].items():
            st.write(f"**{k}:** {v}")

        # Medication
        st.write("### Medication")
        for i, (k, v) in enumerate(info["medication"].items(), 1):
            st.write(f"**{i}. {k}**")
            st.write(v)

    except Exception as e:
        st.error("Error parsing JSON response")
        st.code(str(e))


# =====================
# RUN APP
# =====================
if disease_name:

    with st.spinner("Analyzing disease..."):
        result = get_disease_info(disease_name)
        display_info(result)