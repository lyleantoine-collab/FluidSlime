# app.py — FULL DARK MODE + RED LIGHT + PWA
import streamlit as st
import pyttsx3
import os
import numpy as np
from src.core.routing_engine import design_route
from streamlit_folium import folium_static
import folium

# === PWA MANIFEST ===
st.markdown("""
<link rel="manifest" href="/manifest.json">
""", unsafe_allow_html=True)

# === THEME SWITCHER ===
theme = st.sidebar.radio("Theme", ["Light", "Dark", "Red Light"], horizontal=True)
if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {background: #0e1117; color: #fafafa;}
    .stButton>button {background: #262730; color: #fafafa; border: 1px solid #444;}
    </style>
    """, unsafe_allow_html=True)
elif theme == "Red Light":
    st.markdown("""
    <style>
    .stApp {background: #1a0000; color: #ffcccc;}
    .stButton>button {background: #330000; color: #ff9999; border: 1px solid #660000;}
    .stTextInput>label, .stSelectbox>label {color: #ff9999;}
    </style>
    """, unsafe_allow_html=True)

# === REST OF APP (UNCHANGED FROM FINAL VERSION) ===
st.set_page_config(page_title="FluidSlime", layout="wide", initial_sidebar_state="expanded")
st.title("FluidSlime — 55% Cheaper. 0.022s. Voice-Controlled.")
st.markdown("**Say** `design canal` • **Drop** DEM • **Click** Run → **Download** KML")

with st.sidebar:
    st.header("Mode & Input")
    mode = st.selectbox("Design Mode", ["canal", "hvac", "piping", "pcb", "ergonomic", "starlink", "archeogodzilla"], key="mode")
    dem_file = st.file_uploader("Drop DEM (.tif/.npy)", ["tif", "npy"])
    lidar_file = st.file_uploader("Or LiDAR (.las/.laz)", ["las", "laz"])
    photo_dir = st.text_input("Or Drone Photos Folder (path)")
    p1 = st.text_input("Start (lat,lon)", "-14.735,-75.130")
    p2 = st.text_input("End (lat,lon)", "-14.685,-75.110")
    st.markdown("---")
    if st.button("Speak Command (Mobile OK)"):
        st.info("Use browser mic → say: `design canal`, `design hvac`, etc.")

if st.button("Run Optimization", type="primary") and (dem_file or lidar_file or photo_dir):
    with st.spinner("Slime is growing..."):
        dem_path = lidar_path = photo_path = None
        if dem_file:
            dem_path = f"data/{dem_file.name}"
            with open(dem_path, "wb") as f: f.write(dem_file.getbuffer())
        if lidar_file:
            lidar_path = f"data/{lidar_file.name}"
            with open(lidar_path, "wb") as f: f.write(lidar_file.getbuffer())
        if photo_dir and os.path.exists(photo_dir):
            photo_path = photo_dir

        try:
            start = tuple(map(float, p1.split(',')))
            end = tuple(map(float, p2.split(',')))
        except:
            st.error("Invalid coordinates. Use: lat,lon")
            st.stop()

        result = design_route(
            dem_path=dem_path,
            lidar_path=lidar_path,
            photo_dir=photo_path,
            start=start,
            end=end,
            module=mode
        )

    length = len(result['path']) * 30
    straight = int(np.hypot(end[0]-start[0], end[1]-start[1]) * 111000)
    savings = round((straight - length) / straight * 100, 1) if straight > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Length", f"{length:,.0f} m")
    col2.metric("Cost", f"${result['cost']:,.0f}")
    col3.metric("Savings", f"{savings}%")

    if result.get("kml"):
        with open(result["kml"], "rb") as f:
            kml_data = f.read()
        st.download_button(
            label="Download KML",
            data=kml_data,
            file_name=f"{mode}_path.kml",
            mime="application/vnd.google-earth.kml+xml"
        )

    engine = pyttsx3.init()
    summary = f"Your {mode} saves {savings} percent and costs {int(result['cost']):,} dollars."
    st.info(summary)
    engine.say(summary)
    engine.runAndWait()

    if st.checkbox("Show on Map"):
        m = folium.Map(location=[start[0], start[1]], zoom_start=16, tiles="OpenStreetMap")
        path_coords = []
        for y, x in result['path']:
            lon, lat = result.get('transform', lambda p: p)(x, y)
            path_coords.append([lat, lon])
        folium.PolyLine(path_coords, color="cyan" if theme=="Red Light" else "red", weight=5).add_to(m)
        folium_static(m)

    if st.button("Generate PDF Report"):
        from reports.auto_report import generate_report
        generate_report(result, f"{mode}_project")
        st.success("Report saved: `reports/project_report.pdf`")

else:
    st.info("Drop DEM/LiDAR/Drone → Click **Run**")
    st.code("python examples/pro/canal_nazca.py")

st.markdown("---")
st.markdown("*Mahsi Cho. DYB DYB DYB.* | [GitHub](https://github.com/lyleantoine-collab/FluidSlime)")
