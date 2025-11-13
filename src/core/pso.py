# src/core/pso.py
import numpy as np
import yaml
with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)

def run_pso_optimizer(elev, start, end, transform):
    rows, cols = elev.shape
    n_particles = 50
    particles = [generate_random_path(start, end, rows, cols) for _ in range(n_particles)]
    velocities = [np.random.uniform(-1, 1, len(p)) for p in particles]
    p_best = particles[:]
    p_best_score = [path_length(p, elev) for p in particles]
    g_best = p_best[np.argmin(p_best_score)]

    for _ in range(cfg["slime"]["steps"]//2):
        for i in range(n_particles):
            # velocity update, path rebuild, etc. (full code from earlier message)
            pass  # shortened for space — full version in previous message
    return g_best, None

def generate_random_path(start, end, rows, cols):
    path = [start]
    pos = np.array(start)
    while tuple(pos) != end:
        move = np.random.randint(-1, 2, 2)
        pos = np.clip(pos + move, 0, [rows-1, cols-1])
        path.append(tuple(pos))
    return path

def path_length(path, elev):
    return len(path)
