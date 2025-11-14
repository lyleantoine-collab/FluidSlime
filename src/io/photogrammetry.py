# src/io/photogrammetry.py — DRONE PHOTOS → DEM
import numpy as np
import rasterio
from pathlib import Path
import subprocess
import os

def photo_to_dem(photo_dir, resolution=0.5, output_tif="photo_dem.tif"):
    photo_dir = Path(photo_dir)
    if not photo_dir.exists():
        raise FileNotFoundError(f"Photo directory not found: {photo_dir}")

    # Use OpenDroneMap (ODM) via Docker
    cmd = [
        "docker", "run", "-v", f"{photo_dir}:/dataset",
        "opendronemap/odm", "--dsm", "--dem-resolution", str(resolution),
        "--output-dir", "/dataset/output"
    ]
    print("Running OpenDroneMap... (this may take 5–30 mins)")
    subprocess.run(cmd, check=True)

    dsm_path = photo_dir / "output" / "dsm.tif"
    if not dsm_path.exists():
        raise FileNotFoundError("DSM not generated")

    # Copy and return
    import shutil
    shutil.copy(dsm_path, output_tif)
    with rasterio.open(output_tif) as src:
        dem = src.read(1)
        transform = src.transform
    print(f"PHOTOGRAMMETRY → DEM: {output_tif}")
    return output_tif, transform, dem
