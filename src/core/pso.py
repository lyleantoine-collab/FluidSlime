# src/core/pso.py  ← REPLACE ENTIRE FILE
import numpy as np
import yaml
with open("config/default.yaml") as f:
    cfg = yaml.safe_load(f)["slime"]

def run_pso_optimizer(elev, start, end, transform):
    rows, cols = elev.shape
    n_particles = 40
    max_steps = cfg["steps"] // 3

    # Initialize particles
    particles = []
    velocities = []
    p_best = []
    p_best_scores = []

    for _ in range(n_particles):
        path = _random_path(start, end, rows, cols)
        particles.append(path)
        velocities.append([np.random.uniform(-1, 1, 2) for _ in range(len(path))])
        score = _path_score(path, elev, cfg["max_slope"])
        p_best.append(path)
        p_best_scores.append(score)

    g_best = p_best[np.argmin(p_best_scores)]
    g_best_score = min(p_best_scores)

    for _ in range(max_steps):
        for i in range(n_particles):
            path = particles[i]
            for j in range(len(path)-1):
                r1, r2 = np.random.rand(), np.random.rand()
                v = (0.7 * np.array(velocities[i][j]) +
                     1.5 * r1 * (np.array(p_best[i][j]) - np.array(path[j])) +
                     1.5 * r2 * (np.array(g_best[j]) - np.array(path[j])))
                velocities[i][j] = list(np.clip(v, -3, 3))

            # Rebuild path
            new_path = [start]
            pos = np.array(start)
            for v in velocities[i][:len(path)-1]:
                pos = np.clip(pos + v.astype(int), 0, [rows-1, cols-1])
                new_path.append(tuple(pos))
                if tuple(pos) == end: break
            particles[i] = new_path

            score = _path_score(new_path, elev, cfg["max_slope"])
            if score < p_best_scores[i]:
                p_best[i] = new_path
                p_best_scores[i] = score
                if score < g_best_score:
                    g_best = new_path
                    g_best_score = score

    return g_best, g_best_score

def _random_path(start, end, rows, cols):
    path = [start]
    pos = np.array(start)
    while tuple(pos) != end and len(path) < rows + cols:
        move = np.random.randint(-1, 2, 2)
        pos = np.clip(pos + move, 0, [rows-1, cols-1])
        path.append(tuple(pos))
    return path

def _path_score(path, elev, max_slope):
    if len(path) < 2: return 1e6
    total = len(path)
    for i in range(len(path)-1):
        y1, x1 = path[i]
        y2, x2 = path[i+1]
        dz = abs(elev[y2, x2] - elev[y1, x1])
        dist = max(1, np.hypot(y2-y1, x2-x1))
        if dz / dist > max_slope: total += 100
    return total
