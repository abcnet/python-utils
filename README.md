# python-utils

# PNG to SDF Polygon

A simple Python tool that converts the non-transparent region of a PNG image into simplified polygon vertices for Signed Distance Field (SDF) collision detection.

## Installation

```bash
pip install opencv-python numpy
```

## Usage

```bash
python png_to_polygon.py image.png
```

Optional parameters:

```bash
python png_to_polygon.py image.png --epsilon 0.003 --threshold 127
```

- `--epsilon`: Polygon simplification factor (default: `0.005`). Smaller values preserve more detail.
- `--threshold`: Alpha threshold (default: `127`).

## Output

- `image_polygon.json`: Polygon vertices normalized to image-centered coordinates.
- `image_outline_preview.png`: Preview of the extracted polygon outline.

The JSON vertices can be used with SDF polygon functions such as Inigo Quilez's `sdPolygon()`.

**Limitations:** Only the largest external contour is extracted. Internal holes and disconnected regions are not supported.

## References

- [OpenCV — Contours and Polygon Approximation](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html)
- [Inigo Quilez — 2D Distance Functions](https://iquilezles.org/articles/distfunctions2d/)

## License

MIT License.

## GLSL to JavaScript Conversion

Uses [glsl-transpiler](https://github.com/stackgl/glsl-transpiler) to convert GLSL code into JavaScript.

### Installation

Requires [Node.js](https://nodejs.org/).

```bash
npm install glsl-transpiler
```

### Usage

```bash
node convert.mjs [input.glsl|-] [output.js|-]
```

Both input and output default to `-` (stdin/stdout).

**Examples:**

```bash
# File to stdout
node convert.mjs shader.glsl

# File to file
node convert.mjs shader.glsl shader.js

# Stdin to stdout
node convert.mjs < shader.glsl

# Stdin to file
node convert.mjs < shader.glsl > shader.js

# File to file using redirection
node convert.mjs shader.glsl > shader.js
```

On Windows PowerShell:

```powershell
Get-Content shader.glsl -Raw | node convert.mjs
```

### Limitations

Generated JavaScript may require additional adjustments, particularly for GLSL arrays and vector types.

### References

- [stackgl/glsl-transpiler](https://github.com/stackgl/glsl-transpiler) — MIT License
- [Inigo Quilez — 2D Distance Functions](https://iquilezles.org/articles/distfunctions2d/)
