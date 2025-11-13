import rasterio

def load_dem(dem_path, start_latlon, end_latlon):
    with rasterio.open(dem_path) as src:
        elev = src.read(1).astype(float)
        transform = src.transform
        start_y, start_x = ~transform * start_latlon
        end_y, end_x     = ~transform * end_latlon
        return elev, (int(start_y), int(start_x)), (int(end_y), int(end_x))
