# src/core/ga_refine.py — FULL FILE (12 LINES OF EVOLUTION)
import numpy as np

def ga_refine_path(path_px, elev, transform, pop_size=50, generations=30, mutation_rate=0.2):
    rows, cols = elev.shape
    population = [_mutate_path(path_px, rows, cols) for _ in range(pop_size)]
    for _ in range(generations):
        scores = [_score_path(p, elev) for p in population]
        best_idx = np.argmin(scores)
        if scores[best_idx] < _score_path(path_px, elev):
            path_px = population[best_idx]
        # Breed top 10%
        elite = [population[i] for i in np.argsort(scores)[:pop_size//10]]
        population = elite[:]
        while len(population) < pop_size:
            parent1, parent2 = np.random.choice(elite, 2, replace=False)
            child = _crossover(parent1, parent2)
            if np.random.rand() < mutation_rate:
                child = _mutate_path(child, rows, cols)
            population.append(child)
    return path_px

def _crossover(p1, p2):
    split = len(p1)//2
    return p1[:split] + [p for p in p2[split:] if p not in p1[:split]]

def _mutate_path(path, rows, cols):
    if len(path) < 3: return path
    idx = np.random.randint(1, len(path)-1)
    y, x = path[idx]
    dy, dx = np.random.randint(-2, 3, 2)
    new_y, new_x = np.clip([y+dy, x+dx], 0, [rows-1, cols-1])
    return path[:idx] + [(new_y, new_x)] + path[idx+1:]

def _score_path(path, elev):
    if len(path) < 2: return 1e6
    score = 0
    for i in range(len(path)-1):
        y1, x1 = path[i]; y2, x2 = path[i+1]
        dz = abs(elev[y2,x2] - elev[y1,x1])
        dist = max(1, np.hypot(y2-y1, x2-x1))
        score += dist + 100 * max(0, dz/dist - 0.012)
    return score
