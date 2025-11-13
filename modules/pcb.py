from src.core.routing_engine import design_route
from rules.pcb import RULES
def design_pcb(grid, start, end): return design_route(None, start, end, RULES, "pcb")
