# src/core/pso_refine.py — 5 LINES OF SWARM FURY
import numpy as np

def pso_refine_path(path_px, elev, transform, n=40, it=30):
    rows, cols = elev.shape
    pop = [_mutate(path_px, rows, cols) for _ in range(n)]
    g_best = min(pop, key=lambda p: _score(p, elev))
    for _ in range(it):
        pop = [_step(p, g_best, rows, cols) for p in pop]
        g_best = min(pop + [g_best], key=lambda p: _score(p, elev))
    return g_best

def _mutate(p, r, c): return p if len(p)<3 else p[:np.random.randint(1,len(p)-1)] + [(np.clip(p[i][0]+np.random.randint(-2,3),0,r-1), np.clip(p[i][1]+np.random.randint(-2,3),0,c-1)) for i in [np.random.randint(1,len(p)-1)]][0] + p[np.random.randint(1,len(p)-1):] if np.random.rand()<0.3 else p
def _step(p, g, r, c): return g if np.random.rand()<0.3 else p if np.random.rand()<0.5 else _mutate(p,r,c)
def _score(p, e): return sum(max(1, np.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]) + 100*max(0, abs(e[p[i+1]]-e[p[i]])/max(1,np.hypot(p[i+1][0]-p[i][0], p[i+1][1]-p[i][1]))-0.012)) for i in range(len(p)-1)) if len(p)>1 else 1e9
