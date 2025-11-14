# tests/test_hybrid.py — FULL HYBRID TESTS
import numpy as np
from src.core.routing_engine import design_route

def test_septet_hybrid():
    # Mock DEM
    elev = np.full((50, 50), 100.0)
    transform = type('obj', (), {'__mul__': lambda s, p: p})()
    
    result = design_route(
        dem_path=None,
        lidar_path=None,
        start=(0, 0),
        end=(49, 49),
        module="canal"
    )
    
    path = result['path']
    assert len(path) > 10, "Path too short"
    assert len(path) < 100, "Path too long"
    assert result['cost'] > 0, "Cost zero"
    print("SEPTET TEST PASSED")
