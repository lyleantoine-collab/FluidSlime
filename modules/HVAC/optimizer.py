# modules/HVAC/optimizer.py
from core.vascular_engine import VascularSlime
import json

def optimize_ductwork(cad_file):
    with open("constraints/ASHRAE_limits.json") as f:
        limits = json.load(f)
    
    slime = VascularSlime(grid_size=(800,800))
    # stub: parse IFC/Revit → sources/sinks
    slime.place_food(sources=air_intakes, sinks=returns)
    trail = slime.run()
    return convert_to_duct_path(trail, max_pressure_drop=limits["max_in_wc_per_100ft"])
