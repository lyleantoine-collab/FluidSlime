# app.py — RUN WITH: streamlit run app.py
import streamlit as st
import matplotlib.pyplot as plt
import rasterio
import numpy as np
import simplekml
import yaml
import os

# Import our engines
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost
from src.modules.archeogodzilla import scan_ancient_canal

# Page config
st.set_page_config(page_title="FluidSlime", layout="wide", initial_sidebar_state="expanded")
st.title("FluidSlime — Share the Spark")
st.markdown("""
**I aim to misbehave.**  
*“Darkness isn’t scary when we share the spark.”* – Amina, Kenya
""")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    module = st.selectbox("Design Mode", [
        "Gravity Canal", "Pump-Free Sewer", "HVAC Ducts",
        "Pipeline", "PCB Traces", "Ergonomic Walkway",
        "Nova Agora Starlink Mesh", "ArcheoGodzilla"
    ])
    uploaded_file = st.file_uploader("Drop DEM (GeoTIFF/HGT)", type=["tif", "hgt"])
    max_slope = st.slider("Max Slope (%)", 0.1, 10.0, 1.2) / 100
    steps = st.slider("Iterations", 50, 1000, 400)
    optimizer_name = st.selectbox("Optimizer", ["hybrid", "nsga2", "pso", "ga", "classic"])

    # Update config on the fly
    cfg_path = "config/default.yaml"
    if os.path.exists(cfg_path):
        with open(cfg_path, "r") as f:
            cfg = yaml.safe_load(f)
        cfg["slime"]["max_slope"] = max_slope
        cfg["slime"]["steps"] = steps
        cfg["optimizer"] = optimizer_name
        with open(cfg_path, "w") as f:
            yaml.dump(cfg, f)

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input")
    if uploaded_file:
        dem_path = "data/temp_dem.tif"
        with open(dem_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("DEM loaded!")

        with rasterio.open(dem_path) as src:
            fig, ax = plt.subplots(figsize=(6, 5))
            src.plot.imshow(ax=ax, cmap='terrain')
            ax.set_title("Click Start → End")
            st.pyplot(fig)

            # Let user click points
            points = plt.ginput(2, timeout=0)
            plt.close()
            if len(points) == 2:
                start_lonlat = points[0][::-1]  # (y,x) → (lat,lon)
                end_lonlat = points[1][::-1]
                st.write(f"**Start:** {start_lonlat}")
                st.write(f"**End:** {end_lonlat}")

                if st.button("RUN SLIME", type="primary"):
                    with st.spinner("Slime is hunting..."):
                        elev, start_px, end_px, transform, src = load_dem(dem_path, start_lonlat, end_lonlat)
                        run_optimizer = get_optimizer()
                        path_px, extra = run_optimizer(elev, start_px, end_px, transform)

                        # Cost
                        cost = calculate_cost(path_px, elev, module.lower().replace(" ", "_"))

                        # KML
                        kml_file = path_to_kml(path_px, elev, transform, f"{module.lower()}_path.kml")

                        st.session_state.result = {
                            "path": path_px,
                            "elev": elev,
                            "transform": transform,
                            "cost": cost,
                            "kml": kml_file,
                            "module": module
                        }

with col2:
    st.subheader("Output")
    if 'result' in st.session_state:
        result = st.session_state.result
        fig, ax = plt.subplots(figsize=(10, 8))
        with rasterio.open(dem_path) as src:
            src.plot.imshow(ax=ax, cmap='terrain', alpha=0.7)
        ax.plot([result["transform"] * (x, y)[0] for y, x in result["path"]],
                [result["transform"] * (x, y)[1] for y, x in result["path"]],
                'lime', linewidth=6, label="Spark Path")
        ax.scatter([result["transform"] * result["path"][0][1]][0],
                   [result["transform"] * result["path"][0][0]][1], c='cyan', s=200, zorder=5)
        ax.scatter([result["transform"] * result["path"][-1][1]][0],
                   [result["transform"] * result["path"][-1][0]][1], c='magenta', s=200, zorder=5)
        ax.legend()
        ax.set_title(f"{result['module']} — Cost: ${result['cost']:,.0f}")
        st.pyplot(fig)

        with open(result["kml"], "rb") as f:
            st.download_button(
                "Download KML — Open in Google Earth",
                f.read(),
                result["kml"],
                "application/vnd.google-earth.kml+xml"
            )

        st.success("SPARK SHARED!")
        st.balloons()

    elif module == "ArcheoGodzilla" and uploaded_file:
        if st.button("SCAN ANCIENT CANALS"):
            with st.spinner("ArcheoGodzilla awakening..."):
                known_points = [(-14.735, -75.130), (-14.685, -75.110)]  # Example Nazca points
                ancient_paths = scan_ancient_canal("data/temp_dem.tif", known_points)
                st.write(f"Found {len(ancient_paths)} ghost canals!")
                # Future: overlay all paths
# In app.py, add to module selector
elif module == "HVAC Multi-Line":
    sources = [(-14.7, -75.1), (-14.75, -75.12)]
    sinks = [(-14.68, -75.11), (-14.69, -75.105)]
    paths = design_hvac_network("data/temp_dem.tif", sources, sinks)
