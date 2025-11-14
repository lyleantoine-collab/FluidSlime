# src/io/geojson.py — QGIS / WEB EXPORT
import json

def path_to_geojson(path_px, transform, elev=None, filename="output.geojson"):
    coords = []
    for y, x in path_px:
        lon, lat = transform * (x, y)
        z = elev[y, x] if elev is not None else 0
        coords.append([lon, lat, z])
    
    geojson = {
        "type": "FeatureCollection",
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": coords
            },
            "properties": {
                "name": "FluidSlime Path",
                "length_m": len(path_px) * 30,
                "cost": len(path_px) * 30 * 120
            }
        }]
    }
    
    with open(filename, "w") as f:
        json.dump(geojson, f, indent=2)
    print(f"GEOJSON: {filename}")
