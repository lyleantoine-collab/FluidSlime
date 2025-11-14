# src/core/routing_engine.py — LiDAR + OBSTACLE AVOIDANCE + PHOTOGRAMMETRY
from src.core.factory import get_optimizer
from src.io.dem import load_dem
from src.io.kml import path_to_kml
from src.core.cost_engine import calculate_cost
from src.io.lidar import lidar_to_dem, detect_obstacles
from src.io.photogrammetry import photo_to_dem
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

def design_route(dem_path=None, lidar_path=None, photo_dir=None, start=None, end=None, module="canal"):
    elev = start_px = end_px = transform = obstacles = None

    # === INPUT: LiDAR, Photogrammetry, or DEM ===
    if lidar_path:
        dem_path, transform, elev = lidar_to_dem(lidar_path, resolution=cfg.get("lidar_resolution", 1.0))
        obstacles = detect_obstacles(lidar_path, height_threshold=cfg.get("obstacle_height", 2.0))
    elif photo_dir:
        dem_path, transform, elev = photo_to_dem(photo_dir, resolution=cfg.get("photo_resolution", 0.5))
    elif dem_path:
        elev, start_px, end_px, transform, _ = load_dem(dem_path, start, end)

    # === CONVERT START/END TO PIXEL ===
    if start and end and transform:
        start_px = [(
            int((transform * start)[0]),
            int((transform * start)[1])
        )]
        end_px = [(
            int((transform * end)[0]),
            int((transform * end)[1])
        )]

    # === RUN OPTIMIZER ===
    path_px, _ = get_optimizer()(elev, start_px, end_px, transform, obstacles=obstacles)

    # === HYBRID REFINEMENT ===
    if cfg.get("use_hybrid", False) and elev is not None:
        path_px = aco_refine_path(path_px, elev, transform, obstacles)
        path_px = ga_refine_path(path_px, elev, transform, obstacles)
        path_px = pso_refine_path(path_px, elev, transform, obstacles)
        path_px = nsga2_refine(path_px, elev, transform, obstacles)
        path_px = woa_refine_path(path_px, elev, transform, obstacles)
        path_px = firefly_refine_path(path_px, elev, transform, obstacles)

    # === OUTPUT ===
    cost = calculate_cost(path_px, elev, module, obstacles) if elev else 0
    kml = path_to_kml(path_px, elev, transform, f"{module}.kml") if elev else None

    return {"path": path_px, "cost": cost, "kml": kml, "module": module, "obstacles": obstacles}
