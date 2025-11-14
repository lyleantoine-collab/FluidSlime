# src/core/routing_engine.py — FULL FILE (TRIPLE HYBRID)
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost
import yaml

# Load config
with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

# HYBRID IMPORTS
if cfg.get("use_hybrid", False):
    from src.core.aco_refine import aco_refine_path
    from src.core.ga_refine import ga_refine_path

def design_route(dem_path, start_latlon, end_latlon, rules, module="canal"):
    if dem_path:
        elev, start_px, end_px, transform, src = load_dem(dem_path, start_latlon, end_latlon)
    else:
        elev, start_px, end_px, transform = None, start_latlon, end_latlon, None

    optimizer = get_optimizer()
    path_px, extra = optimizer(elev, start_px, end_px, transform)

    # TRIPLE HYBRID
    if cfg.get("use_hybrid", False) and elev is not None:
        path_px = aco_refine_path(path_px, elev, transform)
        path_px = ga_refine_path(path_px, elev, transform)

    cost = calculate_cost(path_px, elev, module) if elev is not None else 0
    kml_file = path_to_kml(path_px, elev, transform, f"{module}_path.kml") if elev is not None else None

    return {
        "path": path_px,
        "cost": cost,
        "kml": kml_file,
        "module": module,
        "spark": "shared"
    }
