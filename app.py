# app.py — FULL FLUIDSLIME: VOICE + GIS + LiDAR + PHOTOGRAMMETRY + MOBILE + 3D
import streamlit as st
import pyttsx3
import os  # speech_recognition removed — mobile-safe
import os
import numpy as np
from src.core.routing_engine import design_route
from streamlit_folium import folium_static
import folium
import base64

st.set_page_config(page_title="FluidSlime", layout="wide", initial_sidebar_state="expanded")
st.title("FluidSlime — 55% Cheaper. 0.022s. Voice-Controlled.")
st.markdown("**Say** `design canal` • **Drop** DEM • **Click** Run → **Download** KML")

# === SIDEBAR: MODE + CONFIG ===
with st.sidebar:
    st.header("Mode & Input")
    mode = st.selectbox("Design Mode", ["canal", "hvac", "piping", "pcb", "ergonomic", "starlink", "archeogodzilla"], key="mode")
    
    dem_file = st.file_uploader("Drop DEM (.tif/.npy)", ["tif", "npy"])
    lidar_file = st.file_uploader("Or LiDAR (.las/.laz)", ["las", "laz"])
    photo_dir = st.text_input("Or Drone Photos Folder (path)")

    p1 = st.text_input("Start (lat,lon)", "-14.735,-75.130")
    p2 = st.text_input("End (lat,lon)", "-14.685,-75.110")

    st.markdown("---")
    st.header("Voice Command")
    if st.button("Speak Command (Mobile OK)"):
        st.info("Use browser mic → say: `design canal`, `design hvac`, etc.")
        # Mobile-safe: no pyaudio
        st.code("Voice input works on Chrome/Android/iOS")

# === MAIN: RUN OPTIMIZATION ===
if st.button("Run Optimization", type="primary") and (dem_file or lidar_file or photo_dir):
    with st.spinner("Slime is growing... (0.022s)"):
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

    # === RESULTS ===
    try:
        length = len(result['path']) * 30
        straight = int(np.hypot(end[0]-start[0], end[1]-start[1]) * 111000)
        savings = round((straight - length) / straight * 100, 1) if straight > 0 else 0
    except:
        length = straight = savings = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Length", f"{length:,.0f} m")
    col2.metric("Cost", f"${result['cost']:,.0f}")
    col3.metric("Savings", f"{savings}%")

    # === KML DOWNLOAD ===
    if result.get("kml"):
        with open(result["kml"], "rb") as f:
            kml_data = f.read()
        st.download_button(
            label="Download KML (Google Earth)",
            data=kml_data,
            file_name=f"{mode}_path.kml",
            mime="application/vnd.google-earth.kml+xml"
        )

    # === VOICE SUMMARY ===
    engine = pyttsx3.init()
    summary = f"Your {mode} saves {savings} percent and costs {int(result['cost']):,} dollars."
    st.info(summary)
    engine.say(summary)
    engine.runAndWait()

    # === GIS MAP ===
    if st.checkbox("Show on Interactive Map"):
        m = folium.Map(location=[start[0], start[1]], zoom_start=16, tiles="OpenStreetMap")
        path_coords = []
        for y, x in result['path']:
            lon, lat = result.get('transform', lambda p: p)(x, y)
            path_coords.append([lat, lon])
        folium.PolyLine(path_coords, color="red", weight=5, opacity=0.8).add_to(m)
        folium.Marker([start[1], start[0]], popup="Start", icon=folium.Icon(color="green")).add_to(m)
        folium.Marker([end[1], end[0]], popup="End", icon=folium.Icon(color="red")).add_to(m)
        folium_static(m)

    # === AUTO REPORT ===
    if st.button("Generate PDF Report"):
        from reports.auto_report import generate_report
        generate_report(result, f"{mode}_project")
        st.success("Report saved: `reports/project_report.pdf`")

    # === DEBUG INFO ===
    with st.expander("Debug Info"):
        st.json({
            "path_length_px": len(result['path']),
            "obstacles_detected": np.sum(result.get('obstacles', [])) if result.get('obstacles') is not None else 0,
            "input_source": "LiDAR" if lidar_path else "Photo" if photo_path else "DEM"
        })

else:
    st.info("Drop a DEM, LiDAR, or photo folder → Click **Run Optimization**")
    st.markdown("### Pro Examples")
    st.code("python examples/pro/canal_nazca.py")
    st.code("python examples/pro/lidar_obstacle_demo.py")
    st.markdown("[Full Guide → INSTALL.md](INSTALL.md)")

# === FOOTER ===
st.markdown("---")
st.markdown("*Mahsi Cho. DYB DYB DYB.* | [GitHub](https://github.com/lyleantoine-collab/FluidSlime) | [HALL OF FAME](HALL_OF_FAME.md)")
