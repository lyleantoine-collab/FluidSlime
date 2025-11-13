# src/core/pso.py — 12 lines of pure power
from sko.PSO import PSO
import numpy as np

def run_pso_optimizer(elev, start, end, transform):
    rows, cols = elev.shape
    def objective(xy):
        path = _raster_to_path(xy, start, end, rows, cols)
        return _path_score(path, elev, 0.012)  # max_slope

    pso = PSO(func=objective, n_dim=2, pop=40, max_iter=100, lb=[0,0], ub=[rows-1, cols-1])
    pso.run()
    best_xy = pso.gbest_x
    path = _raster_to_path(best_xy, start, end, rows, cols)
    return path, pso.gbest_y
