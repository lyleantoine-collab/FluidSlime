# src/core/routing_engine.py
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost

def design_route(dem_path, start_latlon, end_latlon, rules, module="canal"):
    if dem_path:
        elev, start_px, end_px, transform, src = load_dem(dem_path, start_latlon, end_latlon)
    else:
        elev, start_px, end_px, transform = None, start_latlon, end_latlon, None

    optimizer = get_optimizer()
    path_px, extra = optimizer(elev, start_px, end_px, transform)

    cost = calculate_cost(path_px, elev, module) if elev is not None else 0
    kml_file = path_to_kml(path_px, elev, transform) if elev is not None else None

    return {
        "path": path_px,
        "cost": cost,
        "kml": kml_file,
        "module": module,
        "spark": "shared"
    }
# In routing_engine.py
from src.core.vortex_termite import apply_termite_decay, apply_vortex_dynamics

def design_route(...):
    # After slime run
    tubes = apply_termite_decay(tubes, rules.get("termite_decay", 0.95))
    tubes = apply_vortex_dynamics(tubes, path_px, rules.get("vortex_strength", 0.3))
