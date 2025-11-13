# modules/hvac.py
from src.core.routing_engine import design_route
from rules.hvac import RULES

def design_hvac_network(dem_path, sources, sinks):
    paths = []
    for src, sink in zip(sources, sinks):
        result = design_route(dem_path, src, sink, RULES, "hvac")
        paths.append(result["path"])
    return merge_paths(paths, RULES)
