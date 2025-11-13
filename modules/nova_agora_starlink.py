from src.core.routing_engine import design_route
from rules.starlink_mesh import RULES
def design_starlink_mesh(positions):
    return design_route(None, None, None, RULES, "starlink")
