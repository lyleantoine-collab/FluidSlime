# src/io/kml.py
import simplekml

def path_to_kml(path_px, elev, transform, filename="fluidslime_canal.kml"):
    kml = simplekml.Kml()
    linestring = kml.newlinestring(name="Gravity Canal")
    coords = []
    for y, x in path_px:
        lon, lat = transform * (x, y)
        z = elev[int(y), int(x)] if elev is not None else 0
        coords.append((lon, lat, z))
    linestring.coords = coords
    linestring.style.linestyle.color = simplekml.Color.red
    linestring.style.linestyle.width = 4
    linestring.altitudemode = simplekml.AltitudeMode.relativetoground
    kml.save(filename)
    print(f"KML saved: {filename} — drop it in Google Earth!")
