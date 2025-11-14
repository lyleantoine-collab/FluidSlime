import numpy as np

def merge_paths(paths, rules):
    merged = []
    for path in paths:
        attached = False
        for m in merged:
            if np.array_equal(path[-1], m[0]):
                m.extend(path[1:])
                attached = True
                break
        if not attached:
            merged.append(path)
    return merged
