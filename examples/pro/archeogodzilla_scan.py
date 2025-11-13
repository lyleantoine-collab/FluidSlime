# 12-line ancient canal hunter
from src.modules.archeogodzilla import scan_ancient_canal

points = [(-14.74, -75.13), (-14.70, -75.11), (-14.68, -75.10)]
ghosts = scan_ancient_canal("data/nazca_dem.tif", points)

print(f"Found {len(ghosts)} ghost canals from 1500 years ago")
