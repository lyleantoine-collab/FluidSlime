# src/core/slime.py — FULL FILE (NUMBA + CONCISE BEAST)
import numpy as np
from numba import jit

@jit(nopython=True)
def _slime_step(tubes: np.ndarray, diffused: np.ndarray, flow_factor: float = 0.05) -> np.ndarray:
    return tubes * diffused * flow_factor

@jit(nopython=True)
def _diffuse(elev: np.ndarray, source_y: int, source_x: int, decay: float = 0.9) -> np.ndarray:
    rows, cols = elev.shape
    diffused = np.zeros((rows, cols), dtype=np.float32)
    diffused[source_y, source_x] = 1.0
    for _ in range(20):
        new_diff = np.zeros_like(diffused)
        for y in range(rows):
            for x in range(cols):
                if diffused[y, x] > 0:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < rows and 0 <= nx < cols and (dy != 0 or dx != 0):
                                cost = 1.0 / (1.0 + abs(elev[ny, nx] - elev[y, x]))
                                new_diff[ny, nx] += diffused[y, x] * cost * decay
        diffused = new_diff
    return diffused

def run_slime_optimizer(elev: np.ndarray, start: tuple, end: tuple, transform, steps: int = 400) -> tuple:
    rows, cols = elev.shape
    start_y, start_x = start
    end_y, end_x = end

    tubes = np.zeros((rows, cols), dtype=np.float32)
    tubes[start_y, start_x] = 1.0
    tubes[end_y, end_x] = 1.0

    for _ in range(steps):
        diffused = _diffuse(elev, start_y, start_x)
        diffused += _diffuse(elev, end_y, end_x)
        tubes = _slime_step(tubes, diffused)

    # Extract path
    path = []
    pos = (start_y, start_x)
    path.append(pos)
    visited = set([pos])
    for _ in range(rows * cols):
        y, x = pos
        neighbors = [(y+dy, x+dx) for dy in [-1,0,1] for dx in [-1,0,1] 
                    if 0 <= y+dy < rows and 0 <= x+dx < cols and (dy,dx) != (0,0)]
        next_pos = max(neighbors, key=lambda p: tubes[p[0], p[1]], default=None)
        if next_pos is None or next_pos in visited or tubes[next_pos[0], next_pos[1]] < 0.01:
            break
        path.append(next_pos)
        pos = next_pos
        visited.add(pos)
        if pos == (end_y, end_x):
            break

    return path, {"tubes": tubes}
