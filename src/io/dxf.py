# src/io/dxf.py — CAD EXPORT
def path_to_dxf(path_px, filename="output.dxf"):
    with open(filename, "w") as f:
        f.write("0\nSECTION\n2\nENTITIES\n")
        for i in range(len(path_px)-1):
            y1, x1 = path_px[i]
            y2, x2 = path_px[i+1]
            f.write(f"0\nLINE\n8\n0\n10\n{x1*30}\n20\n{y1*30}\n11\n{x2*30}\n21\n{y2*30}\n")
        f.write("0\nENDSEC\n0\nEOF\n")
    print(f"DXF: {filename}")
