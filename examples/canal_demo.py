# Quick test — works with fake data until you drop a real DEM
import numpy as np
from src.modules.canal import design_gravity_canal

# Fake terrain for instant testing
elev_dummy = np.random.rand(200, 200) * 50
np.save("data/demo_elev.npy", elev_dummy)  # fake DEM replacement

# Pretend coords (Nazca region style)
start = (-13.162, -74.200)
end   = (-13.180, -74.180)

# Run it
path, elev, tubes = design_gravity_canal("data/demo_elev.npy", start, end)
print(f"FluidSlime found a {len(path)}-segment canal!")
