#!/usr/bin/env python3
"""Convert a transparent PNG's largest opaque region into an SDF polygon.

Based on OpenCV findContours and approxPolyDP:
https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html

Usage:
    python png_to_polygon.py "Hoover Tower.png"
    python png_to_polygon.py sprite.png --epsilon 0.005 --threshold 127

Output vertices are normalized relative to the entire source image:
    x = pixel_x / width - 0.5
    y = pixel_y / height - 0.5
They can be scaled by (2*bx, 2*by) and translated by the image center.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('png', type=Path, help='Transparent PNG image')
    parser.add_argument('--epsilon', type=float, default=0.005,
                        help='Polygon simplification tolerance as fraction of contour perimeter (default: 0.005)')
    parser.add_argument('--threshold', type=int, default=127,
                        help='Minimum alpha value treated as opaque (0..255; default: 127)')
    args = parser.parse_args()
    if not (0 <= args.threshold <= 255) or args.epsilon <= 0:
        parser.error('threshold must be between 0 and 255; epsilon must be positive')

    img = cv2.imread(str(args.png), cv2.IMREAD_UNCHANGED)
    if img is None:
        parser.error(f'Unable to open: {args.png}')
    if img.ndim != 3 or img.shape[2] != 4:
        parser.error('Input must be a PNG with an alpha channel (RGBA/BGRA).')

    height, width = img.shape[:2]
    mask = np.where(img[:, :, 3] > args.threshold, 255, 0).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        parser.error('No opaque pixels found at the selected threshold.')

    contour = max(contours, key=cv2.contourArea)
    tolerance = args.epsilon * cv2.arcLength(contour, True)
    polygon = cv2.approxPolyDP(contour, tolerance, True).reshape(-1, 2)
    if len(polygon) < 3:
        parser.error('Simplification left fewer than 3 vertices. Try a smaller --epsilon.')

    vertices = [[round(float(x) / width - 0.5, 6),
                 round(float(y) / height - 0.5, 6)] for x, y in polygon]
    json_path = args.png.with_name(args.png.stem + '_polygon.json')
    preview_path = args.png.with_name(args.png.stem + '_outline_preview.png')
    json_path.write_text(json.dumps({
        'source_image': args.png.name,
        'width': width,
        'height': height,
        'vertices': vertices
    }, indent=2), encoding='utf-8')

    preview = img.copy()
    cv2.polylines(preview, [polygon.reshape(-1, 1, 2)], True, (0, 0, 255, 255), 2)
    cv2.imwrite(str(preview_path), preview)
    print(f'{len(contours)} exterior contour(s) found; using largest ({len(polygon)} vertices).')
    print(f'Polygon: {json_path}')
    print(f'Preview: {preview_path}')
    if len(contours) > 1:
        print('WARNING: Other disconnected components were omitted.')
    print('NOTE: Internal transparent holes are not represented.')


if __name__ == '__main__':
    main()
