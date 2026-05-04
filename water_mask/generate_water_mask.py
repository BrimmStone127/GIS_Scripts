"""
generate_water_mask.py

Downloads OpenStreetMap water data for the St. Louis / Cahokia region via the
Overpass API and rasterizes it into a 3612x3612 grayscale PNG that aligns
pixel-for-pixel with the USGS_stlouis.tif terrain heightmap.

Output: water_mask.png  (white = water, black = land)

Usage:
    python3 generate_water_mask.py

    Optional: add --save-geojson to write the raw OSM response to water_data.json
"""

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import requests
from PIL import Image, ImageDraw

# -------------------------------------------------------------------
# Geotransform extracted from USGS_stlouis.tif
# -------------------------------------------------------------------
BOUNDS = {
    "left":   -91.00166666648283,
    "right":  -89.99833333311620,
    "top":     39.00166666718383,
    "bottom":  37.99833333291787,
}
IMG_WIDTH  = 3612
IMG_HEIGHT = 3612

# Degrees per pixel
DX = (BOUNDS["right"] - BOUNDS["left"])   / IMG_WIDTH
DY = (BOUNDS["top"]   - BOUNDS["bottom"]) / IMG_HEIGHT

OUTPUT_DIR = Path(__file__).parent


def lon_to_px(lon: float) -> float:
    return (lon - BOUNDS["left"]) / DX


def lat_to_py(lat: float) -> float:
    return (BOUNDS["top"] - lat) / DY


def build_overpass_query() -> str:
    """Build Overpass QL query for water features in the bounding box."""
    s = BOUNDS["bottom"]
    w = BOUNDS["left"]
    n = BOUNDS["top"]
    e = BOUNDS["right"]

    # bbox format for Overpass: south,west,north,east
    bbox = f"{s:.6f},{w:.6f},{n:.6f},{e:.6f}"

    return f"""
[out:json][timeout:120][bbox:{bbox}];
(
  way["natural"="water"];
  relation["natural"="water"];
  way["waterway"="river"];
  way["waterway"="riverbank"];
  way["waterway"="stream"];
  way["waterway"="canal"];
  way["landuse"="reservoir"];
);
out geom;
"""


def fetch_overpass(query: str) -> dict:
    url = "https://overpass-api.de/api/interpreter"
    headers = {
        "User-Agent": "PlanetGame-WaterMask/1.0 (game development tool)",
        "Accept": "application/json",
    }
    print("Querying Overpass API (this may take 30-60 seconds)...")
    t0 = time.time()
    resp = requests.post(url, data=query.encode("utf-8"),
                         headers=headers, timeout=180)
    if resp.status_code != 200:
        print(f"  HTTP {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()
    elapsed = time.time() - t0
    print(f"  Received {len(resp.content) / 1024:.0f} KB in {elapsed:.1f}s")
    return resp.json()


def geometry_to_pixel_ring(nodes: list[dict]) -> list[tuple[float, float]]:
    """Convert a list of OSM node dicts (with lat/lon) to pixel coords."""
    return [(lon_to_px(n["lon"]), lat_to_py(n["lat"])) for n in nodes]


def rasterize(data: dict) -> np.ndarray:
    """Rasterize OSM elements onto a black canvas, painting water white."""
    img = Image.new("L", (IMG_WIDTH, IMG_HEIGHT), color=0)
    draw = ImageDraw.Draw(img)

    rivers_drawn   = 0
    polygons_drawn = 0
    lines_drawn    = 0

    for element in data.get("elements", []):
        etype = element.get("type")
        tags  = element.get("tags", {})

        # ---- closed polygons (water bodies, riverbanks) ----
        if etype == "way":
            geom = element.get("geometry", [])
            if not geom:
                continue

            pixels = geometry_to_pixel_ring(geom)

            is_area = (
                tags.get("natural") == "water"
                or tags.get("waterway") == "riverbank"
                or tags.get("landuse") == "reservoir"
            )

            if is_area and len(pixels) >= 3:
                draw.polygon(pixels, fill=255)
                polygons_drawn += 1
            else:
                # River/stream centerline — draw as thick line
                waterway = tags.get("waterway", "")
                width_px = 10 if waterway == "river" else 4
                for i in range(len(pixels) - 1):
                    draw.line([pixels[i], pixels[i + 1]], fill=255, width=width_px)
                lines_drawn += 1

        # ---- relations (multi-polygon water bodies) ----
        elif etype == "relation":
            members = element.get("members", [])
            for member in members:
                if member.get("role") in ("outer", "inner", ""):
                    geom = member.get("geometry", [])
                    if not geom:
                        continue
                    pixels = geometry_to_pixel_ring(geom)
                    if member.get("role") == "inner":
                        # Holes — paint black to cut out
                        if len(pixels) >= 3:
                            draw.polygon(pixels, fill=0)
                    else:
                        if len(pixels) >= 3:
                            draw.polygon(pixels, fill=255)
                            rivers_drawn += 1

    print(f"  Painted: {polygons_drawn} polygons, {rivers_drawn} relation members, "
          f"{lines_drawn} centerlines")

    return np.array(img)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-geojson", action="store_true",
                        help="Save raw Overpass JSON response")
    parser.add_argument("--load-geojson", metavar="FILE",
                        help="Skip download, load from saved JSON file")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.load_geojson:
        print(f"Loading cached data from {args.load_geojson}...")
        with open(args.load_geojson) as f:
            data = json.load(f)
    else:
        query = build_overpass_query()
        data  = fetch_overpass(query)

        if args.save_geojson:
            cache_path = OUTPUT_DIR / "water_data.json"
            with open(cache_path, "w") as f:
                json.dump(data, f)
            print(f"  Saved raw data to {cache_path}")

    element_count = len(data.get("elements", []))
    print(f"Processing {element_count} OSM elements...")

    mask = rasterize(data)

    out_path = OUTPUT_DIR / "water_mask.png"
    Image.fromarray(mask, mode="L").save(out_path)

    water_px   = int(np.sum(mask > 0))
    total_px   = IMG_WIDTH * IMG_HEIGHT
    water_pct  = 100.0 * water_px / total_px

    print(f"Saved: {out_path}")
    print(f"  Water coverage: {water_px:,} / {total_px:,} pixels ({water_pct:.1f}%)")
    print()
    print("Next step: load water_mask.png alongside the terrain PNG in PNGTerrainSource")


if __name__ == "__main__":
    main()
