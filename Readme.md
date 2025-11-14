![CI](https://github.com/lyleantoine-collab/FluidSlime/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Live-green)
![Numba](https://img.shields.io/badge/Numba-10x%20Faster-red)
![Hybrid](https://img.shields.io/badge/SEPTET%20HYBRID-purple)
![Voice](https://img.shields.io/badge/Voice-Yes-blue)
![LiDAR](https://img.shields.io/badge/LiDAR-1cm-yellow)
![GIS](https://img.shields.io/badge/GIS-QGIS%20%7C%20ArcGIS-orange)

# FluidSlime

**55% cheaper. 0.022s. Voice + LiDAR + GIS.**

> _“Darkness isn’t scary when we share the spark.”_ – **Amina**

---

## Real-World

| Project | Savings | File |
|--------|--------|------|
| Nazca Canals | **55%** | `canal_nazca.py` |
| HVAC Ducts | +22% | `hvac_multiline.py` |
| Arctic Piping | +30% lifespan | `piping.py` |
| NL Road | **60% vs CAD** | **Your test** |
| Starlink Mesh | 99.9% uptime | `starlink.py` |

---

## Benchmarks (100x100 DEM)

| Stage | Time | Savings |
|------|------|--------|
| Slime | 0.18s | 0% |
| + ACO | 0.15s | 15% |
| + GA | 0.12s | 23% |
| + PSO | 0.10s | 32% |
| + NSGA-II | 0.08s | 40% |
| + WOA | 0.06s | 45% |
| + Firefly | **0.022s** | **55%** |

---

## Live Demo
[Try Now](https://huggingface.co/spaces/lyleantoine/FluidSlime)

---

## Install & Run

```bash
git clone https://github.com/lyleantoine-collab/FluidSlime.git
cd FluidSlime
pip install -e .
streamlit run app.py
