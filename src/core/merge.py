# src/core/merge.py
def merge_paths(paths, rules):
    merged = []
    for path in paths:
        if not any(np.array_equal(path[-1], m[0]) for m in merged):
            merged.append(path)
        else:
            for m in merged:
                if np.array_equal(path[-1], m[0]):
                    m.extend(path[1:])
    return merged
