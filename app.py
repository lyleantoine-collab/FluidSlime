# app.py — run with: streamlit run app.py
import streamlit as st
import matplotlib.pyplot as plt
import rasterio
import numpy as np
from src.core.factory import get_optimizer
from src.io.kml import path_to_kml
from src.io.dem import load_dem

st.set_page_config(page_title="FluidSlime", layout="wide")
st.title("🦠 FluidSlime — Share the Spark")
st.markdown("**I aim to misbehave.** Darkness isn’t scary when we share the spark.")

col1, col2 = st.columns([1, 2])
with col1:
    st.header("Controls")
    module = st.selectbox("Design Mode", [
        "Gravity Canal", "Pump-Free Sewer", "HVAC Ducts",
        "Pipeline", "PCB Traces", "Ergonomic Walkway", "Nova Agora Starlink Mesh"
    ])
    uploaded_file = st.file_uploader("Drop GeoTIFF / HGT DEM", type=["tif", "hgt"])
    max_slope = st.slider("Max slope (%)", 0.1, 10.0, 1.2) / 100
    steps = st.slider("Iterations", 50, 1000, 400)
    optimizer_name = st.selectbox("Optimizer", ["hybrid", "nsga2", "pso", "ga", "classic"])

    if uploaded_file:
        with open("data/temp_dem.tif", "wb") as f:
            f.write(uploaded_file.getbuffer())
        dem_path = "data/temp_dem.tif"

        with rasterio.open(dem_path) as src:
            fig, ax = plt.subplots()
            src.plot.imshow(ax=ax, cmap='terrain')
            st.pyplot(fig)
            points = plt.ginput(2, timeout=0)
            plt.close()
            if len(points) == 2:
                start_lonlat = points[0][::-1]
                end_lonlat = points[1][::-1]
                st.write(f"Start: {start_lonlat}", f"End: {end_lonlat}")

                if st.button("🦠 RUN SLIME"):
                    with st.spinner("Slime is sharing the spark..."):
                        elev, start_px, end_px, transform, src = load_dem(dem_path, start_lonlat, end_lonlat)
                        run_optimizer = get_optimizer()
                        path_px, extra = run_optimizer(elev, start_px, end_px, transform)

                        fig, ax = plt.subplots(figsize=(10, 8))
                        src.plot.imshow(ax=ax, cmap='terrain', alpha=0.7)
                        ax.plot([transform * (x, y)[0] for y, x in path_px],
                                [transform * (x, y)[1] for y, x in path_px],
                                'lime', linewidth=6, label="Spark Path")
                        ax.legend()
                        st pyplot(fig)

                        kml_bytes = path_to_kml(path_px, elev, transform)
                        st.download_button("Download KML — Light up Google Earth", kml_bytes, "spark_path.kml")
                        st.success("Spark shared! 🌟")
