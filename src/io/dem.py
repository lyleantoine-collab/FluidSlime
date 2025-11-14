import rasterio
from rasterio.errors import RasterioIOError

def load_dem(dem_path, start_latlon, end_latlon):
    try:
        with rasterio.open(dem_path) as src:
            if src.crs is None:
                raise ValueError("DEM missing CRS - add EPSG:4326")
            elev = src.read(1).astype(float)
            transform = src.transform
            start_y, start_x = ~transform * start_latlon
            end_y, end_x = ~transform * end_latlon
            return elev, (int(start_y), int(start_x)), (int(end_y), int(end_x)), transform, src
    except RasterioIOError:
        raise ValueError(f"Invalid DEM: {dem_path}. Try a GeoTIFF.")
    except Exception as e:
        raise ValueError(f"DEM load failed: {e}")
