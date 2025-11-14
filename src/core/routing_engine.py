# src/core/routing_engine.py — SLIME → ANT → GA → PSO → NSGA-II → WOA → FIREFLY
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost
import yaml

with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

if cfg.get("use_hybrid", False):
    from src.core.aco_refine import aco_refine_path
    from src.core.ga_refine import ga_refine_path
    from src.core.pso_refine import pso_refine_path
    from src.core.nsga2 import nsga2_refine
    from src.core.woa_refine import woa_refine_path
    from src.core.firefly_refine import firefly_refine_path

def design_route(dem_path, start, end, rules, module="canal"):
    elev = start_px = end_px = transform = None
    if dem_path:
        elev, start_px, end_px, transform, _ = load_dem(dem_path, start, end)

    path_px, _ = get_optimizer()(elev, start_px, end_px, transform)

    if cfg.get("use_hybrid", False) and elev is not None:
        path_px = aco_refine_path(path_px, elev, transform)
        path_px = ga_refine_path(path_px, elev, transform)
        path_px = pso_refine_path(path_px, elev, transform)
        path_px = nsga2_refine(path_px, elev, transform)
        path_px = woa_refine_path(path_px, elev, transform)
        path_px = firefly_refine_path(path_px, elev, transform)

    cost = calculate_cost(path_px, elev, module) if elev else 0
    kml = path_to_kml(path_px, elev, transform, f"{module}.kml") if elev else None

    return {"path": path_px, "cost": cost, "kml": kml, "module": module}
from src.io.dxf import path_to_dxf
path_to_dxf(path_px, f"{module}.dxf")
# Add at end of design_route()
from src.io.geojson import path_to_geojson
from src.io.shapefile import path_to_shapefile
from src.io.raster import cost_heatmap

if elev is not None:
    path_to_geojson(path_px, transform, elev, f"{module}.geojson")
    path_to_shapefile(path_px, transform, elev, module)
    cost_heatmap(elev, path_px, transform, f"{module}_cost.tif")
