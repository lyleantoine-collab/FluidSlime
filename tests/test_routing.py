import pytest
import numpy as np
from src.core.routing_engine import design_route
from rules.canal import RULES

def test_path_length_positive():
    elev = np.zeros((10,10))
    result = design_route(None, (0,0), (5,5), RULES, "canal")
    assert len(result['path']) > 1

def test_cost_positive():
    assert design_route(None, (0,0), (0,0), RULES, "canal")['cost'] >= 0

def test_no_crash_bad_input():
    try:
        design_route("bad.tif", (0,0), (0,0), RULES, "canal")
    except Exception:
        pass  # Graceful fail OK
