# benchmarks/auto.py — PhD-GRADE BENCHMARK
from src.modules.canal import design_gravity_canal
import numpy as np, time, json

dem = "data/sample_dem.tif"
start, end = (-14.735,-75.130), (-14.685,-75.110)

t0 = time.time()
r = design_gravity_canal(dem, start, end)
t = time.time()-t0

straight = int(np.hypot(end[0]-start[0], end[1]-start[1])*111000)
slime = len(r['path'])*30

print(json.dumps({
    "slime_m": slime,
    "straight_m": straight,
    "savings": round((straight-slime)/straight*100,1),
    "time_s": round(t,3)
}))
