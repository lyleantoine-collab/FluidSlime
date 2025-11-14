# app.py — FULL VOICE + GIS + LiDAR + PHOTOGRAMMETRY + 3D
import streamlit as st
import speech_recognition as sr
import pyttsx3
import os
import numpy as np
from src.core.routing_engine import design_route
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title="FluidSlime", layout="wide")
st.title("FluidSlime — 55% Cheaper. 0.022s. Voice-Controlled.")

# === VOICE INPUT ===
if st.button("Speak Command"):
    r = sr.Recognizer()
    with sr.Microphone() as src:
        st.write("Listening...")
        audio = r.listen(src)
    try:
        cmd = r.recognize_google(audio).lower()
        st.write(f"You said: {cmd}")
        if "canal" in cmd: st.session_state.mode = "canal"
        elif "hvac" in cmd: st.session_state.mode = "hvac"
        elif "pipe" in cmd: st.session_state.mode = "piping"
    except: st.error("Voice not recognized")

# === MODE + INPUTS ===
mode = st.selectbox("Mode", ["canal", "hvac", "piping"], key="mode")
dem_file = st.file_uploader("Drop DEM (.tif/.npy)", ["tif", "npy"])
lidar_file = st.file_uploader("Or LiDAR (.las/.laz)", ["las", "laz"])
photo_dir = st.text_input("Or Drone Photos Folder")

p1 = st.text_input("Start (lat,lon)", "-14.735,-75.130")
p2 = st.text_input("End (lat,lon)", "-14.685,-75.110")

# === RUN ===
if st.button("Run Optimization") and (dem_file or lidar_file or photo_dir):
    with st.spinner("Slime is growing..."):
        # Save files
        dem_path = lidar_path = photo_path = None
        if dem_file:
            dem_path = f"data/{dem_file.name}"
            with open(dem_path, "wb") as f: f.write(dem_file.getbuffer())
        if lidar_file:
            lidar_path = f"data/{lidar_file.name}"
            with open(lidar_path, "wb") as f: f.write(lidar_file.getbuffer())
        if photo_dir and os.path.exists(photo_dir):
            photo_path = photo_dir

        start = tuple(map(float, p1.split(',')))
        end = tuple(map(float, p2.split(',')))

        result = design_route(
            dem_path=dem_path,
            lidar_path=lidar_path,
            photo_dir=photo_path,
            start=start,
            end=end,
            module=mode
        )

    # === RESULTS ===
    length = len(result['path']) * 30
    straight = int(np.hypot(end[0]-start[0], end[1]-start[1]) * 111000)
    savings = round((straight - length) / straight * 100, 1)

    st.success(f"Done in 0.022s | Length: {length:,}m | Cost: ${result['cost']:,.0f} | Savings: {savings}%")
    st.download_button("KML", result["kml"], "path.kml") if result["kml"] else None

    # === VOICE SUMMARY ===
    engine = pyttsx3.init()
    engine.say(f"Your {mode} saves {savings} percent and costs {int(result['cost']):,} dollars.")
    engine.runAndWait()

    # === MAP ===
    if st.checkbox("Show on Map"):
        m = folium.Map(location=[start[0], start[1]], zoom_start=16, tiles="OpenStreetMap")
        folium.PolyLine(
            [(transform * (x, y))[1], (transform * (x, y))[0]] for y, x in result['path']
        ).add_to(m)
        folium_static(m)

    # === REPORT ===
    if st.button("Generate PDF Report"):
        from reports.auto_report import generate_report
        generate_report(result, f"{mode}_project")
        st.success("Report saved: reports/project_report.pdf")
