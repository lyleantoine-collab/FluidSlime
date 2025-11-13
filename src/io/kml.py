# src/io/kml.py  ← REPLACE ENTIRE FILE
import simplekml

def path_to_kml(path_px, elev, transform, filename="spark_path.kml"):
    kml = simplekml.Kml()
    lin = kml.newlinestring(name="Shared Spark")
    coords = []
    for y, x in path_px:
        lon, lat = transform * (x, y)
        z = elev[int(y), int(x)] + 10  # float 10m above ground
        coords.append((lon, lat, z))
    lin.coords = coords
    lin.style.linestyle.color = simplekml.Color.lime
    lin.style.linestyle.width = 8
    lin.altitudemode = simplekml.AltitudeMode.relativetoground
    lin.extrude = 1
    kml.save(filename)
    print(f"KML saved: {filename}")
    return filename
