import json, requests, streamlit as st

st.set_page_config(page_title="Darukaa Earth AI Environmental Scientist")
st.title("🌱 Darukaa.Earth — Biodiversity Intelligence")

api = st.sidebar.text_input("FastAPI URL", "http://localhost:8000")
session_id = st.sidebar.text_input("Session ID", "demo")

with st.form("metrics"):
    st.subheader("Structured environmental input")
    soc = st.number_input("Soil organic carbon (%)", min_value=0.0, value=0.3)
    ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, value=7.0)
    moisture = st.text_input("Soil moisture", "unknown")
    rainfall = st.selectbox("Rainfall", ["low","medium","high"])
    temperature = st.number_input("Temperature (°C)", value=25.0)
    land = st.text_input("Land use type", "monoculture")
    crop = st.text_input("Crop", "wheat")
    region = st.text_input("Region", "semi-arid")
    pollution = st.text_input("Pollution", "")
    deforestation = st.text_input("Deforestation", "")
    question = st.text_input("Question", "How can I improve biodiversity?")
    submitted = st.form_submit_button("Analyze")

if submitted:
    payload = {
        "session_id":session_id,
        "message":question,
        "metrics":{
            "soil_organic_carbon":soc, "soil_ph":ph,
            "soil_moisture":moisture, "rainfall":rainfall,
            "temperature":temperature, "land_use_type":land,
            "crop":crop, "region":region,
            "pollution":pollution or None, "deforestation":deforestation or None
        }
    }
    try:
        r = requests.post(api.rstrip("/") + "/chat", json=payload, timeout=180)
        r.raise_for_status()
        st.json(r.json())
    except Exception as e:
        st.error(str(e))

st.divider()
st.subheader("Raw JSON input")
raw = st.text_area("Paste ChatRequest JSON", height=180)
if st.button("Send JSON") and raw:
    try:
        r = requests.post(api.rstrip("/") + "/chat", json=json.loads(raw), timeout=180)
        st.json(r.json())
    except Exception as e:
        st.error(str(e))
