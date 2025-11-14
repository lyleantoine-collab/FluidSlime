# src/core/factory.py
import yaml
from src.core.slime import run_slime_optimizer as classic
from src.core.hybrid_slime import run_hybrid_optimizer as hybrid
from src.core.ga_nsga2 import run_nsga2_optimizer as nsga2
from src.core.genetic import run_ga_optimizer as ga
from src.core.pso import run_pso_optimizer as pso

with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

def get_optimizer():
    mode = cfg.get("optimizer", "hybrid")
    return {"classic": classic, "hybrid": hybrid, "nsga2": nsga2, "ga": ga, "pso": pso}.get(mode, hybrid)
# factory.py — add vortex/termite toggle
cfg["use_vortex"] = True
cfg["use_termite"] = True
