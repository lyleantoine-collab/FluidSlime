# app.py — MOBILE VOICE (WebRTC)
import streamlit as st
import pyttsx3
import os
import numpy as np
from src.core.routing_engine import design_route
from streamlit_folium import folium_static
import folium

# === MOBILE VOICE ===
if st.button("Speak (Mobile OK)"):
    st.write("Use browser mic → say 'design canal'")
    # WebRTC fallback
    import js
    try:
        cmd = js.speech_to_text()
        st.write(f"You said: {cmd}")
    except:
        st.write("Voice not supported on this device")

# === REST UNCHANGED ===
# [Keep all previous code from FULL app.py]
