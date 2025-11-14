# tests/test_hvac.py
def test_vortex_increases_flow():
    tubes = np.ones((10,10))
    path = [(5,5)]
    new_tubes = apply_vortex_dynamics(tubes, path, 1.0)
    assert new_tubes[5,5] > 1.0
