# src/io/shapefile.py — ARCGIS EXPORT
import shapefile
from src.io.dem import pixel_to_latlon

def path_to_shapefile(path_px, transform, elev=None, filename="output"):
    w = shapefile.Writer(filename, shapeType=shapefile.POLYLINE)
    w.field("length_m", "N", decimal=2)
    w.field("cost_usd", "N")
    
    points = [pixel_to_latlon(transform, x, y) for y, x in path_px]
    w.line([[[lon, lat] for lon, lat in points]])
    w.record(len(path_px)*30, len(path_px)*30*120)
    
    w.close()
    # Create .prj file
    with open(f"{filename}.prj", "w") as f:
        f.write('GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]')
    print(f"SHAPEFILE: {filename}.shp")
