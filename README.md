# GIS_Scripts

Tools for processing geographic data.

---

## Projects

### `elevation_tools/`

Converts USGS GeoTIFF elevation data to CSV for use in terrain system.

**Script:** `elevation_converter.py`

```bash
cd elevation_tools
python3 elevation_converter.py USGS_stlouis.tif
# Output: elevation_csvs/USGS_stlouis.csv
```

**Source data:** `elevation_tifs/USGS_stlouis.tif`
- Coverage: ~1° × 1° centered on St. Louis / Cahokia
- Bounds: W -91.0017, E -89.9983, N 39.0017, S 37.9983
- Size: 3612 × 3612 pixels
- Pixel scale: ~0.000278° per pixel (~30m resolution)
- CRS: WGS84 (EPSG:4326)

**Dependencies:** `rasterio`, `numpy`

---

### `water_mask/`

Downloads OSM hydrography for the St. Louis region and rasterizes it into a
3612 × 3612 grayscale PNG aligned pixel-for-pixel with `USGS_stlouis.tif`.

**Output:** `water_mask.png` — white = water, black = land

See [`water_mask/README.md`](water_mask/README.md) for full usage.

---

## Dependencies

```bash
pip install rasterio numpy requests Pillow
```

---

## Terrain Geographic Bounds

| Edge   | Value               |
|--------|---------------------|
| West   | -91.00166666648283  |
| East   | -89.99833333311620  |
| North  |  39.00166666718383  |
| South  |  37.99833333291787  |
| Width  | 3612 px             |
| Height | 3612 px             |
| dx/dy  | ~0.000278°/px (~30m)|

These bounds are embedded in `USGS_stlouis.tif` and are the reference for
aligning any additional data layers
