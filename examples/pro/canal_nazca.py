# 15-line pro canal design
from src.modules.canal import design_gravity_canal
from src.io.dem import load_dem

dem = "data/nazca_dem.tif"
start = (-14.735, -75.130)
end   = (-14.685, -75.110)

result = design_gravity_canal(dem, start, end)
print(f"Cost: ${result['cost']:,.0f} | Length: {len(result['path'])*30}m")
