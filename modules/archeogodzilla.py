from src.core.routing_engine import design_route
from rules.canal import RULES
def scan_ancient_canal(dem_path, known_points):
    # Use slime to trace ghost canals
    paths = []
    for i in range(len(known_points)-1):
        path = design_route(dem_path, known_points[i], known_points[i+1], RULES, "canal")
        paths.append(path)
    return paths
