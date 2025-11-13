import matplotlib.pyplot as plt
from src.core.slime import run_slime_optimizer
from src.io.dem import load_dem

def design_gravity_canal(dem_path, start_latlon, end_latlon,
                         max_slope=0.015, steps=200):
    elev, start_px, end_px = load_dem(dem_path, start_latlon, end_latlon)

    path_px, tubes = run_slime_optimizer(
        elev, start_px, end_px,
        max_slope=max_slope, steps=steps
    )

    plt.figure(figsize=(10,8))
    plt.imshow(tubes, cmap='viridis')
    plt.plot([p[1] for p in path_px], [p[0] for p in path_px], 'red', linewidth=3)
    plt.scatter([start_px[1], end_px[1]], [start_px[0], end_px[0]], c='cyan', s=100)
    plt.title('FluidSlime Gravity Canal')
    plt.colorbar(label='Flow strength')
    plt.show()

    return path_px, elev, tubes
# <<< ADD THESE LINES AT THE END OF design_gravity_canal >>>
    from src.io.kml import path_to_kml
    from rasterio.transform import from_origin  # temp fake transform if no DEM
    fake_transform = from_origin(-74.25, -13.15, 0.001, 0.001)  # rough Nazca area
    path_to_kml(path_px, elev, fake_transform)
    # <<<
    
    return path_px, elev, tubes
