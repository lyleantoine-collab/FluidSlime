# examples/pro/hvac_multiline.py
from src.modules.hvac import design_hvac_network
paths = design_hvac_network("data/sample_dem.tif", 
    sources=[(100,100), (200,150)], 
    sinks=[(300,300), (250,280)])
print(f"HVAC: {len(paths)} branches, vortex-optimized")
