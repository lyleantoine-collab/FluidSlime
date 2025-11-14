# benchmarks/real_world.py — AUTO PH.D. PROOF
import json, time
from src.modules.canal import design_gravity_canal

def run_real(dem_path, start, end, name="unknown"):
    t0 = time.time()
    r = design_gravity_canal(dem_path, start, end)
    t = time.time() - t0
    straight = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 * 111000)
    result = {
        "project": name,
        "slime_m": len(r['path'])*30,
        "straight_m": straight,
        "savings_pct": round((straight - len(r['path'])*30)/straight*100, 2),
        "time_s": round(t, 3),
        "kml": "attached"
    }
    with open(f"proof/{name}.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"PROOF SAVED: {name}.json")
