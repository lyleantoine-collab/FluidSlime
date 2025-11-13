# src/core/cost_engine.py
def calculate_cost(path_px, elev, module="canal"):
    length_m = len(path_px) * 30
    if module == "canal":
        return length_m * 380  # $/m
    elif module == "sewer":
        return length_m * 520 + (length_m//80)*8000
    # add more…
    return length_m * 400
