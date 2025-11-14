# src/core/aco_refine.py — 10 lines of pure dominance
import numpy as np

def aco_refine_path(path_px, elev, transform, n_ants=50, steps=100, alpha=1.0, beta=2.0, evap=0.95):
    rows, cols = elev.shape
    pheromones = np.ones((rows, cols)) * 0.1
    best_path = path_px
    best_score = _score_path(path_px, elev)

    for _ in range(steps):
        for _ in range(n_ants):
            ant_path = [path_px[0]]
            pos = np.array(path_px[0])
            for _ in range(len(path_px)-1):
                neighbors = [p for p in _get_neighbors(pos, rows, cols) if p in path_px]
                if not neighbors: break
                probs = [(pheromones[y,x]**alpha) * ((1/_dist(elev, pos, n))**beta) for n in neighbors]
                probs = np.array(probs) / (sum(probs) + 1e-6)
                next_pos = neighbors[np.random.choice(len(neighbors), p=probs)]
                ant_path.append(tuple(next_pos))
                pos = next_pos
            score = _score_path(ant_path, elev)
            if score < best_score:
                best_path = ant_path
                best_score = score
                pheromones = pheromones * evap
                for y, x in ant_path: pheromones[y,x] += 1/best_score
    return best_path

def _get_neighbors(pos, rows, cols):
    y, x = pos
    return [(y+dy, x+dx) for dy in [-1,0,1] for dx in [-1,0,1] if 0 <= y+dy < rows and 0 <= x+dx < cols and (dy,dx) != (0,0)]

def _dist(elev, p1, p2):
    return max(1, np.hypot(p2[0]-p1[0], p2[1]-p1[1]) + abs(elev[p2] - elev[p1]))

def _score_path(path, elev):
    return sum(_dist(elev, path[i], path[i+1]) for i in range(len(path)-1))
