# app.py — FULL FILE (VOICE + QUAD HYBRID)
import streamlit as st
import speech_recognition as sr
from src.modules.canal import design_gravity_canal
from src.modules.hvac import design_hvac_network

st.title("FluidSlime — Voice-Controlled Bio-Engineer")

# VOICE INPUT
if st.button("Speak Command"):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        st.write("Listening...")
        audio = r.listen(src)
    try:
        cmd = r.recognize_google(audio).lower()
        st.write(f"You said: {cmd}")
        if "canal" in cmd:
            st.session_state.mode = "canal"
        elif "hvac" in cmd:
            st.session_state.mode = "hvac"
    except: st.error("Voice not recognized")

mode = st.selectbox("Mode", ["canal", "hvac"], key="mode")
dem = st.file_uploader("Drop DEM", ["tif","npy"])

if dem and st.button("Run"):
    with st.spinner("Slime is growing..."):
        if mode == "canal":
            p1 = st.text_input("Start (lat,lon)", "-14.735,-75.130")
            p2 = st.text_input("End (lat,lon)", "-14.685,-75.110")
            r = design_gravity_canal(dem.name, tuple(map(float,p1.split(','))), tuple(map(float,p2.split(','))))
        else:
            src = st.text_input("Sources", "(-14.7,-75.1),(-14.75,-75.12)")
            snk = st.text_input("Sinks", "(-14.68,-75.11),(-14.69,-75.105)")
            r = design_hvac_network(dem.name, [tuple(map(float,s.split(','))) for s in src.split('),(')], [tuple(map(float,s.split(','))) for s in snk.split('),(')])
        st.success(f"Cost: ${r['cost']:,.0f} | Length: {len(r['path'])*30}m")
        st.download_button("KML", r["kml"], "path.kml")
# After result
import pyttsx3
engine = pyttsx3.init()
engine.say(f"Your design saves {int((1200 - len(r['path'])*30)/1200*100)} percent and costs {int(r['cost']):,} dollars.")
engine.runAndWait()
# Add to app.py
import folium

if st.checkbox("Show on Map"):
    m = folium.Map(location=[start[0], start[1]], zoom_start=15, tiles="OpenStreetMap")
    folium.PolyLine(
        [(transform * (x, y))[1], (transform * (x, y))[0]] for y, x in result['path']
    ).add_to(m)
    folium_static(m)
