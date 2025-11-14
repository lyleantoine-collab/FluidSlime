# examples/pro/lidar_obstacle_demo.py
from src.core.routing_engine import design_route

result = design_route(
    lidar_path="data/sample_with_buildings.las",
    start=(-47.5, -52.7),
    end=(-47.6, -52.8)
)
print(f"OBSTACLE-AVOIDING PATH: {len(result['path'])}m — Avoided {np.sum(result['obstacles'])} cells")
