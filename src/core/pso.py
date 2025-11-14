from sko.PSO import PSO
import numpy as np

def run_pso_optimizer(elev, start, end, transform):
    rows, cols = elev.shape
    def objective(xy):
        path = _xy_to_path(xy, start, end, rows, cols)
        return len(path) + _slope_penalty(path, elev, 0.012)
    pso = PSO(func=objective, n_dim=2*len(elev.flatten()), pop=40, max_iter=100, lb=[0]*200, ub=[rows-1]*200)
    pso.run()
    best_xy = pso.gbest_x
    path = _xy_to_path(best_xy, start, end, rows, cols)
    return path, pso.gbest_y

def _xy_to_path(xy, start, end, rows, cols):
    # Decode xy to path (simplified)
    path = [start]
    pos = np.array(start)
    for i in range(50):
        pos += np.random.randint(-1,2,2)
        pos = np.clip(pos, 0, [rows-1, cols-1])
        path.append(tuple(pos))
        if tuple(pos) == end: break
    return path

def _slope_penalty(path, elev, max_slope):
    penalty = 0
    for i in range(len(path)-1):
        y1, x1 = path[i]; y2, x2 = path[i+1]
        dz = abs(elev[y2,x2] - elev[y1,x1])
        dist = max(1, np.hypot(y2-y1, x2-x1))
        if dz/dist > max_slope: penalty += 100
    return penalty
