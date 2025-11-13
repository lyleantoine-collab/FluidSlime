# modules/archeogodzilla.py — 18 lines of ancient magic
import numpy as np
from src.core.routing_engine import design_route
from rules.canal import RULES

def scan_ancient_canal(dem_path, known_points, threshold=0.8):
    """
    Hunts for 'ghost canals' in DEM using known anchor points.
    Returns list of slime-reconstructed ancient paths.
    """
    from src.io.dem import load_dem
    elev, _, _, transform, _ = load_dem(dem_path, known_points[0], known_points[-1])
    
    ghosts = []
    for i in range(len(known_points)-1):
        start_px = ~transform * known_points[i]
        end_px   = ~transform * known_points[i+1]
        
        # Run slime with ancient bias
        result = design_route(dem_path, known_points[i], known_points[i+1], RULES, "canal")
        path = result["path"]
        
        # Validate: must follow low-gradient "valley"
        if _ancient_score(path, elev) > threshold:
            ghosts.append(path)
    
    return ghosts

def _ancient_score(path, elev):
    slopes = []
    for i in range(len(path)-1):
        y1, x1 = path[i]; y2, x2 = path[i+1]
        dz = abs(elev[y2,x2] - elev[y1,x1])
        dist = max(1, np.hypot(y2-y1, x2-x1))
        slopes.append(dz/dist)
    return 1 / (1 + np.std(slopes))  # low variance = ancient
