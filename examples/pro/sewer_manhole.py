# 14-line no-pump sewer
from src.modules.sewer import design_sewer

path = design_sewer("data/urban_dem.tif", (40.1, -75.2), (40.0, -75.1))
manholes = [path[i] for i in range(0, len(path), 80//30)]
print(f"{len(manholes)} manholes placed")
