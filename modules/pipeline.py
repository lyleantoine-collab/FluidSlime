from src.core.routing_engine import design_route
from rules.pipeline import RULES
def design_pipeline(dem_path, start, end): return design_route(dem_path, start, end, RULES, "pipeline")
