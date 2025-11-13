from src.core.routing_engine import design_route
from rules.canal import RULES
def design_gravity_canal(dem_path, start, end): return design_route(dem_path, start, end, RULES, "canal")
