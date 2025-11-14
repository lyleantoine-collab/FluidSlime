# benchmarks/performance.py — AUTO BENCHMARK
import time, json
from src.modules.canal import design_gravity_canal

dem = "data/sample_dem.tif"
start, end = (-14.735, -75.130), (-14.685, -75.110)
straight = 1200

results = []
cfg = {"use_hybrid": False}
stages = [
    ("Slime Only", {}),
    ("+ ACO", {"use_hybrid": True}),
    ("+ GA", {"use_hybrid": True}),
    ("+ PSO", {"use_hybrid": True}),
    ("+ NSGA-II", {"use_hybrid": True}),
    ("+ WOA", {"use_hybrid": True}),
    ("+ Firefly", {"use_hybrid": True}),
]

for name, temp_cfg in stages:
    t0 = time.time()
    r = design_gravity_canal(dem, start, end)
    t = time.time() - t0
    length = len(r['path']) * 30
    cost = length * 120  # $120/m
    savings = round((straight - length) / straight * 100, 1)
    results.append({"stage": name, "time_s": round(t, 3), "length_m": length, "cost": cost, "savings_pct": savings})
    print(f"{name}: {t:.3f}s → {length}m → ${cost:,} → {savings}%")

with open("benchmarks/results.json", "w") as f:
    json.dump(results, f, indent=2)
