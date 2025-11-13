from src.core.routing_engine import design_route
from rules.ergonomic import RULES
def design_ergonomic_path(dem_path, start, end): return design_route(dem_path, start, end, RULES, "ergonomic")
