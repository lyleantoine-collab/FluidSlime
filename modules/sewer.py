from src.core.routing_engine import design_route
from rules.sewer import RULES
def design_sewer(dem_path, start, end): return design_route(dem_path, start, end, RULES, "sewer")
