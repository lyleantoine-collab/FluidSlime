# examples/pro/piping_multiline.py
from src.modules.piping import design_piping_network
paths = design_piping_network("data/sample_dem.tif", 
    sources=[(50,50), (150,80)], 
    sinks=[(400,400), (380,390)])
print(f"Piping: {len(paths)} lines, termite-decay stable")
