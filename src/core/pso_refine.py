# src/core/pso_refine.py — 7 LINES OF SWARM DOMINANCE
import numpy as np

def pso_refine_path(path_px, elev, transform, n_particles=40, max_iter=50):
    rows, cols = elev.shape
    particles = [_mutate_path(path_px, rows, cols) for _ in range(n_particles)]
    velocities = [[] for _ in range(n_particles)]
    p_best = particles.copy()
    g_best = min(p_best, key=lambda p: _score_path(p, elev))
    
    for _ in range(max_iter):
        for i, p in enumerate(particles):
            if _score_path(p, elev) < _score_path(p_best[i], elev):
                p_best[i] = p
            if _score_path(p, elev) < _score_path(g_best, elev):
                g_best = p
        for i in range(n_particles):
            particles[i] = _pso_step(particles[i], p_best[i], g_best, rows, cols)
    return g_best

def _pso_step(p, p_best, g_best, rows, cols):
    r1, r2 = np.random.rand(), np.random.rand()
    new_p = []
    for j in range(len(p)):
        if r1 < 0.5: new_p.append(p_best[j])
        elif r2 < 0.5: new_p.append(g_best[j])
        else: new_p.append(p[j])
    return _mutate_path(new_p, rows, cols) if np.random.rand() < 0.3 else new_p

def _mutate_path(path, rows, cols):
    if len(path) < 3: return path
    idx = np.random.randint(1, len(path)-1)
    y, x = path[idx]
    dy, dx = np.random.randint(-2, 3, 2)
    ny, nx = np.clip([y+dy, x+dx], 0, [rows-1, cols-1])
    return path[:idx] + [(ny, nx)] + path[idx+1:]

def _score_path(path, elev):
    if len(path) < 2: return 1e9
    return sum(max(1, np.hypot(path[i+1][0]-path[i][0], path[i+1][1]-path[i][1]) + 
                  100*max(0, abs(elev[path[i+1]] - elev[path[i]])/max(1, np.hypot(path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])) - 0.012))
               for i in range(len(path)-1))
