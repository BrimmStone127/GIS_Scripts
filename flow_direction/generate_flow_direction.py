"""
generate_flow_direction.py

Computes D8 flow direction for every water tile in the St. Louis / Cahokia
terrain and writes a flow_direction.png aligned pixel-for-pixel with
full_map_8bit.png and water_mask.png.

D8 algorithm: each water pixel drains to whichever of its 8 neighbours has
the steepest downhill slope.  Diagonal neighbours use distance sqrt(2).
Pixels with no downhill neighbour (flat basins, true lakes) are marked LAKE.

Output pixel values
-------------------
  0  E   (+x,  0)
  1  SE  (+x, +y)
  2  S   ( 0, +y)
  3  SW  (-x, +y)
  4  W   (-x,  0)
  5  NW  (-x, -y)
  6  N   ( 0, -y)
  7  NE  (+x, -y)
  8  LAKE  (closed basin / no outlet)
255  NOT_WATER (land tile — ignored by game)

Usage
-----
    python3 generate_flow_direction.py

Options
-------
    --heightmap PATH   Path to full_map_8bit.png  (default: auto-detect)
    --watermask PATH   Path to water_mask.png      (default: auto-detect)
    --output PATH      Output PNG path             (default: flow_direction.png)
    --water-threshold  Brightness cutoff for water mask (default: 0.5)
"""

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Constants — match PlanetGame encoding
# ---------------------------------------------------------------------------
DIR_E   = 0
DIR_SE  = 1
DIR_S   = 2
DIR_SW  = 3
DIR_W   = 4
DIR_NW  = 5
DIR_N   = 6
DIR_NE  = 7
DIR_LAKE      = 8    # closed basin / no outlet
DIR_NOT_WATER = 255  # land tile

# (dx, dy, distance) for each direction index
_DIRS = [
    ( 1,  0, 1.0),        # 0 E
    ( 1,  1, 1.4142135),  # 1 SE
    ( 0,  1, 1.0),        # 2 S
    (-1,  1, 1.4142135),  # 3 SW
    (-1,  0, 1.0),        # 4 W
    (-1, -1, 1.4142135),  # 5 NW
    ( 0, -1, 1.0),        # 6 N
    ( 1, -1, 1.4142135),  # 7 NE
]


def _find_assets() -> tuple[Path, Path]:
    """Walk up from script location to find the PlanetGame asset folder."""
    candidates = [
        Path(__file__).parents[3] / "PlanetGame/assets/terrain/reference",
        Path.home() / "projects/PlanetGame/assets/terrain/reference",
    ]
    for c in candidates:
        if (c / "full_map_8bit.png").exists():
            return c / "full_map_8bit.png", c / "water_mask.png"
    return Path("full_map_8bit.png"), Path("water_mask.png")


def compute_flow_direction(
    heightmap: np.ndarray,
    water_mask: np.ndarray,
    water_threshold: float = 0.5,
) -> np.ndarray:
    """
    Parameters
    ----------
    heightmap   : float32 array (H, W), values 0-1
    water_mask  : float32 array (H, W), values 0-1  (>threshold = water)
    water_threshold : float

    Returns
    -------
    uint8 array (H, W) with direction values 0-8 for water pixels,
    DIR_NOT_WATER (255) for land.
    """
    H, W = heightmap.shape
    is_water = water_mask > water_threshold

    out = np.full((H, W), DIR_NOT_WATER, dtype=np.uint8)

    # Pad heightmap with edge values so neighbour lookups don't go out-of-bounds
    padded = np.pad(heightmap, 1, mode="edge")

    # Process all water pixels in one vectorised pass
    ys, xs = np.where(is_water)
    if len(ys) == 0:
        print("WARNING: no water pixels found — check water_threshold or mask path")
        return out

    print(f"  Processing {len(ys):,} water pixels …")

    # Centre elevations for all water pixels
    center_elev = heightmap[ys, xs]

    # Compute slope toward each of the 8 neighbours
    # Using padded array: padded[y+1, x+1] == heightmap[y, x]
    best_dir = np.full(len(ys), DIR_LAKE, dtype=np.uint8)
    best_slope = np.zeros(len(ys), dtype=np.float32)  # must beat 0 to count

    for d_idx, (dx, dy, dist) in enumerate(_DIRS):
        ny = ys + dy
        nx = xs + dx
        # Clamp to valid range for direct lookup (padded handles the edge pixels)
        neighbor_elev = padded[ys + dy + 1, xs + dx + 1]  # +1 for pad offset
        slope = (center_elev - neighbor_elev) / dist       # positive = downhill
        improved = slope > best_slope
        best_slope = np.where(improved, slope, best_slope)
        best_dir   = np.where(improved, d_idx, best_dir).astype(np.uint8)

    out[ys, xs] = best_dir
    return out


def main():
    default_hm, default_wm = _find_assets()
    script_dir = Path(__file__).parent

    parser = argparse.ArgumentParser(description="Generate D8 flow direction PNG")
    parser.add_argument("--heightmap",       default=str(default_hm))
    parser.add_argument("--watermask",       default=str(default_wm))
    parser.add_argument("--output",          default=str(script_dir / "flow_direction.png"))
    parser.add_argument("--water-threshold", type=float, default=0.5)
    args = parser.parse_args()

    hm_path = Path(args.heightmap)
    wm_path = Path(args.watermask)
    out_path = Path(args.output)

    # --- Load heightmap ---
    if not hm_path.exists():
        sys.exit(f"ERROR: heightmap not found: {hm_path}")
    print(f"Loading heightmap: {hm_path}")
    hm_img = Image.open(hm_path).convert("L")
    heightmap = np.array(hm_img, dtype=np.float32) / 255.0
    print(f"  Size: {heightmap.shape[1]}x{heightmap.shape[0]}")

    # --- Load water mask ---
    if not wm_path.exists():
        sys.exit(f"ERROR: water mask not found: {wm_path}")
    print(f"Loading water mask: {wm_path}")
    wm_img = Image.open(wm_path).convert("L")
    water_mask = np.array(wm_img, dtype=np.float32) / 255.0

    if heightmap.shape != water_mask.shape:
        sys.exit(
            f"ERROR: heightmap ({heightmap.shape}) and water mask ({water_mask.shape}) "
            "must be the same size"
        )

    # --- Compute ---
    print("Computing D8 flow directions …")
    flow = compute_flow_direction(heightmap, water_mask, args.water_threshold)

    # --- Stats ---
    water_count = int(np.sum(water_mask > args.water_threshold))
    lake_count  = int(np.sum(flow == DIR_LAKE))
    river_count = water_count - lake_count
    print(f"  Water pixels : {water_count:,}")
    print(f"  River pixels : {river_count:,}  (have a downhill neighbour)")
    print(f"  Lake pixels  : {lake_count:,}   (closed basin / no outlet)")
    for d_idx, label in enumerate(["E","SE","S","SW","W","NW","N","NE"]):
        count = int(np.sum(flow == d_idx))
        print(f"    {label:2s}: {count:,}")

    # --- Save ---
    out_img = Image.fromarray(flow, mode="L")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_img.save(out_path)
    print(f"\nSaved: {out_path}")
    print("Copy flow_direction.png to assets/terrain/reference/ in PlanetGame.")


if __name__ == "__main__":
    main()
