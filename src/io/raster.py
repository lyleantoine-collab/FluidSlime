# src/io/raster.py — COST HEATMAP
import rasterio
import numpy as np

def cost_heatmap(elev, path_px, transform, filename="cost_heatmap.tif"):
    cost = np.zeros(elev.shape, dtype=np.float32)
    for i in range(len(path_px)-1):
        y1, x1 = path_px[i]
        y2, x2 = path_px[i+1]
        dist = max(1, np.hypot(y2-y1, x2-x1))
        slope = abs(elev[y2,x2] - elev[y1,x1]) / dist
        cost[y1,x2] = dist * 120 + 1000 * max(0, slope - 0.012)
    
    with rasterio.open(
        filename, 'w', driver='GTiff',
        height=cost.shape[0], width=cost.shape[1],
        count=1, dtype=cost.dtype, crs='EPSG:4326',
        transform=transform
    ) as dst:
        dst.write(cost, 1)
    print(f"HEATMAP: {filename}")
