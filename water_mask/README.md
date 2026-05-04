# water_mask — River & Water Body Generator

Generates a binary water mask PNG for the PlanetGame St. Louis / Cahokia terrain.
The output aligns pixel-for-pixel with `elevation_tools/elevation_tifs/USGS_stlouis.tif`
and `PlanetGame/assets/terrain/reference/full_map_8bit.png`.

---

## Quick Start

```bash
cd /home/clay/projects/GIS_Scripts/water_mask

# Download OSM water data and generate mask (saves water_data.json for reuse)
python3 generate_water_mask.py --save-geojson

# Regenerate from cached data (no network request)
python3 generate_water_mask.py --load-geojson water_data.json
```

Output: `water_mask.png` (3612 × 3612, grayscale, white = water)

**Dependencies:** `requests`, `Pillow`, `numpy`

---

## What It Does

1. Queries the [Overpass API](https://overpass-api.de/) for OSM features in the terrain bounding box:
   - `natural=water` (lakes, ponds, oxbow lakes)
   - `waterway=river` / `riverbank` / `stream` / `canal`
   - `landuse=reservoir`
2. Rasterizes polygons (filled white) and centerlines (thick white lines) onto a black canvas
3. Saves a grayscale PNG matching the terrain dimensions exactly

---

## Geographic Alignment

The script uses the exact bounds extracted from `USGS_stlouis.tif`:

| Parameter | Value |
|-----------|-------|
| West      | -91.00166666648283 |
| East      | -89.99833333311620 |
| North     |  39.00166666718383 |
| South     |  37.99833333291787 |
| Output    | 3612 × 3612 px     |

Pixel → geographic conversion:
- `lon = left + (px / width) * (right - left)`
- `lat = top  - (py / height) * (top - bottom)`

---

## Known Data Quality Issues

OSM data for this region includes modern features that did not exist in the
Mississippian period. You may want to remove or adjust these in GIMP:

- **Boxy shapes** — likely quarry lakes (limestone/gravel extraction) or
  broken OSM relation geometry where a partial polygon ring gets closed incorrectly
- **Reservoirs** — modern flood control impoundments
- **Canals** — Chain of Rocks Canal and other 20th-century engineering works

**To fix in GIMP:**
1. Open `water_mask.png`
2. Paint black over unwanted water areas (use a hard brush)
3. Paint white to add missing water areas
4. Save as PNG (overwrite)
5. Copy to PlanetGame: `cp water_mask.png ~/projects/PlanetGame/assets/terrain/reference/water_mask.png`
6. Run `./tools/reimport_assets.sh` in PlanetGame before launching

**To regenerate from scratch:** re-run the script. Your GIMP edits will be overwritten,
so keep a backup or use `--load-geojson water_data.json` and re-apply edits to the fresh output.

---

## Investigating Problem Areas

The raw OSM data is saved in `water_data.json`. To inspect the largest polygons
and identify which OSM features are causing issues:

```python
import json
data = json.load(open("water_data.json"))
for el in data["elements"]:
    tags = el.get("tags", {})
    geom = el.get("geometry", [])
    print(el["type"], el["id"], len(geom), tags)
```

Use the OSM ID to look up the feature at `https://www.openstreetmap.org/<type>/<id>`.

---

## Files

| File | Description |
|------|-------------|
| `generate_water_mask.py` | Main script |
| `water_mask.png` | Generated output (copy to PlanetGame assets) |
| `water_data.json` | Cached Overpass API response (optional, for reuse) |
