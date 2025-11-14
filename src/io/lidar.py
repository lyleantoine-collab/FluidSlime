# src/io/lidar.py — LiDAR → DEM + 3D PATH
import numpy as np
import laspy
import rasterio
from scipy.spatial import KDTree
from src.io.dem import pixel_to_latlon

def lidar_to_dem(las_file, resolution=1.0, output_tif="lidar_dem.tif"):
    las = laspy.read(las_file)
    x, y, z = las.x, las.y, las.z
    points = np.vstack((x, y, z)).T

    # Grid bounds
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    width = int((xmax - xmin) / resolution) + 1
    height = int((ymax - ymin) / resolution) + 1

    # Rasterize
    dem = np.full((height, width), np.nan, dtype=np.float32)
    tree = KDTree(points[:, :2])
    for i in range(height):
        for j in range(width):
            cy = ymin + i * resolution
            cx = xmin + j * resolution
            _, idx = tree.query([cx, cy], k=5)
            dem[i, j] = np.mean(points[idx, 2])

    # Fill gaps
    from scipy.ndimage import distance_transform_edt
    mask = ~np.isnan(dem)
    dist = distance_transform_edt(~mask)
    dem[~mask] = np.interp(dist[~mask], dist[mask], dem[mask])

    # Save
    transform = rasterio.transform.from_origin(xmin, ymax, resolution, resolution)
    with rasterio.open(
        output_tif, 'w', driver='GTiff',
        height=height, width=width, count=1,
        dtype='float32', crs='EPSG:4326', transform=transform
    ) as dst:
        dst.write(dem, 1)
    print(f"LiDAR → DEM: {output_tif} ({width}x{height})")
    return output_tif, transform, dem
