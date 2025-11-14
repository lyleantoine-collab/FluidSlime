import numpy as np

def apply_termite_decay(tubes, decay_rate=0.95):
    return tubes * decay_rate

def apply_vortex_dynamics(tubes, path, strength=0.3):
    for y, x in path:
        if np.random.rand() < strength:
            tubes[max(0,y-1):y+2, max(0,x-1):x+2] *= 1.5
    return tubes
