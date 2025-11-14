# src/core/routing_engine.py — FULL FILE (QUAD BEAST)
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost
import yaml

with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

# QUAD HYBRID IMPORTS
if cfg.get("use_hybrid", False):
    from src.core.aco_refine import aco_refine_path
    from src.core.ga_refine import ga_refine_path
    from src.core.pso_refine import pso_refine_path

def design_route(dem_path, start_latlon, end_latlon, rules, module="canal"):
    elev = start_px = end_px = transform = None
    if dem_path:
        elev, start_px, end_px, transform, _ = load_dem(dem_path, start_latlon, end_latlon)

    optimizer = get_optimizer()
    path_px, _ = optimizer(elev, start_px, end_px, transform)

    # QUAD HYBRID: SLIME → ACO → GA → PSO
    if cfg.get("use_hybrid", False) and elev is not None:
        path_px = aco_refine_path(path_px, elev, transform)
        path_px = ga_refine_path(path_px, elev, transform)
        path_px = pso_refine_path(path_px, elev, transform)

    cost = calculate_cost(path_px, elev, module) if elev else 0
    kml = path_to_kml(path_px, elev, transform, f"{module}.kml") if elev else None

    return {"path": path_px, "cost": cost, "kml": kml, "module": module}
