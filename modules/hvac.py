from src.core.routing_engine import design_route
from rules.hvac import RULES
def design_hvac(dem_path, start, end): return design_route(dem_path, start, end, RULES, "hvac")
