# src/io/lidar.py — LiDAR → DEM + OBSTACLE MASK
import numpy as np
import laspy
import rasterio
from scipy.spatial import KDTree
from scipy.ndimage import distance_transform_edt

def lidar_to_dem(las_file, resolution=1.0, output_tif="lidar_dem.tif"):
    las = laspy.read(las_file)
    x, y, z = las.x, las.y, las.z
    points = np.vstack((x, y, z)).T

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    width = int((xmax - xmin) / resolution) + 1
    height = int((ymax - ymin) / resolution) + 1

    dem = np.full((height, width), np.nan, dtype=np.float32)
    tree = KDTree(points[:, :2])
    for i in range(height):
        for j in range(width):
            cy = ymin + i * resolution + resolution/2
            cx = xmin + j * resolution + resolution/2
            _, idx = tree.query([cx, cy], k=10)
            dem[i, j] = np.mean(points[idx, 2])

    # Fill NaN
    mask = ~np.isnan(dem)
    if mask.any():
        dist = distance_transform_edt(~mask)
        dem[~mask] = np.interp(dist[~mask], dist[mask], dem[mask])

    transform = rasterio.transform.from_origin(xmin, ymax, resolution, resolution)
    with rasterio.open(output_tif, 'w', driver='GTiff', height=height, width=width,
                       count=1, dtype='float32', crs='EPSG:4326', transform=transform) as dst:
        dst.write(dem, 1)
    print(f"LiDAR → DEM: {output_tif}")
    return output_tif, transform, dem

def detect_obstacles(las_file, height_threshold=2.0, resolution=1.0):
    las = laspy.read(las_file)
    x, y, z = las.x, las.y, las.z
    ground_z = np.percentile(z, 5)  # Assume 5th percentile is ground
    obstacle_mask = z > ground_z + height_threshold

    if not np.any(obstacle_mask):
        return None

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    width = int((xmax - xmin) / resolution) + 1
    height = int((ymax - ymin) / resolution) + 1

    grid = np.zeros((height, width), dtype=bool)
    obs_x, obs_y = x[obstacle_mask], y[obstacle_mask]
    j_idx = ((obs_x - xmin) / resolution).astype(int)
    i_idx = ((obs_y - ymin) / resolution).astype(int)
    valid = (i_idx >= 0) & (i_idx < height) & (j_idx >= 0) & (j_idx < width)
    grid[i_idx[valid], j_idx[valid]] = True

    print(f"OBSTACLES: {np.sum(grid)} cells blocked")
    return grid
