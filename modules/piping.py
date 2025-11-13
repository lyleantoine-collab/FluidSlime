# modules/piping.py
from src.core.routing_engine import design_route
from rules.piping import RULES

def design_piping_network(dem_path, sources, sinks):
    paths = []
    for src, sink in zip(sources, sinks):
        result = design_route(dem_path, src, sink, RULES, "piping")
        paths.append(result["path"])
    return merge_paths(paths, RULES)
