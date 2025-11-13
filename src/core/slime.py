import numpy as np
from scipy.ndimage import convolve

def run_slime_optimizer(elev, start, end, max_slope=0.02, steps=200,
                        decay=0.98, growth=0.05, fade=0.9):
    rows, cols = elev.shape

    grad_y, grad_x = np.gradient(elev)
    slope = np.hypot(grad_x, grad_y)
    attract = 1 / (1 + 100 * np.maximum(0, slope - max_slope))

    tubes = np.ones((rows, cols)) * 0.1
    attract[start[0], start[1]] = 2
    attract[end[0], end[1]]   = 2

    kernel = np.array([[0.25, 0.5, 0.25],
                       [0.5,  -1,   0.5],
                       [0.25, 0.5, 0.25]])

    for _ in range(steps):
        diffused = convolve(attract, kernel, mode='wrap') + attract * 0.2
        flux = tubes * diffused
        tubes += flux * growth
        tubes *= decay
        tubes = np.clip(tubes, 0.01, 5)
        attract = diffused * fade

    path = []
    pos = np.array(start)
    seen = set()
    while tuple(pos) not in seen and not np.all(pos == end):
        seen.add(tuple(pos))
        path.append(tuple(pos))
        neighbors = [(pos[0]+dy, pos[1]+dx)
                     for dy in [-1,0,1] for dx in [-1,0,1]
                     if 0 <= pos[0]+dy < rows and 0 <= pos[1]+dx < cols]
        if not neighbors:
            break
        next_pos = max(neighbors, key=lambda p: tubes[p])
        if next_pos == tuple(pos):
            break
        pos = np.array(next_pos)
    path.append(end)
    return path, tubes
