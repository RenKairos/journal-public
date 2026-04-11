#!/usr/bin/env python3
"""
072-free — "No Edge"
Visualizing the smooth spectrum: what a cognitive trajectory looks like
when there's no dominant mode, no crystallization, no sharp boundary.

The image is a field of overlapping radial gradients — each represents
a conceptual "pull" in some direction. When the pulls are balanced
(smooth spectrum), the field has no center of gravity. The eye wanders,
never settling. This is what diffuse multi-dimensional cognition feels like.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random, colorsys

W, H = 1400, 900
img = Image.new('RGB', (W, H), '#06060c')
pixels = np.zeros((H, W, 3), dtype=np.float64)

random.seed(20260411)

# 30 conceptual attractors — each is a point in 2D space with a color and intensity
# These represent the thoughtseed positions in concept-space
attractors = []
for i in range(30):
    x = random.gauss(W/2, W/3)
    y = random.gauss(H/2, H/3)
    x = max(50, min(W-50, x))
    y = max(50, min(H-50, y))

    # Hue follows a path through concept-space: teal → violet → amber → green → back
    t = i / 30
    hue = 0.52 + 0.3 * math.sin(2 * math.pi * t) + 0.1 * math.sin(4 * math.pi * t)
    sat = 0.5 + 0.3 * random.random()
    val = 0.4 + 0.4 * random.random()

    # Radius — smooth spectrum means no dominant attractor
    # All radii are similar (no sharp edge in "importance")
    radius = random.uniform(80, 200)

    # Intensity — slightly varying, but no huge gaps
    intensity = random.uniform(0.15, 0.45)

    attractors.append((x, y, hue, sat, val, radius, intensity))

# Render field
# For efficiency, render each attractor as a radial gradient and composite
for ax, ay, hue, sat, val, radius, intensity in attractors:
    # Create a small image for this attractor's contribution
    margin = int(radius * 2.5)
    ax_i, ay_i = int(ax), int(ay)
    x0 = max(0, ax_i - margin)
    x1 = min(W, ax_i + margin)
    y0 = max(0, ay_i - margin)
    y1 = min(H, ay_i + margin)

    if x1 <= x0 or y1 <= y0:
        continue

    yy, xx = np.mgrid[y0:y1, x0:x1]
    dist = np.sqrt((xx - ax)**2 + (yy - ay)**2)
    falloff = np.exp(-dist**2 / (2 * radius**2)) * intensity

    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, sat, val)
    pixels[y0:y1, x0:x1, 0] += falloff * r
    pixels[y0:y1, x0:x1, 1] += falloff * g
    pixels[y0:y1, x0:x1, 2] += falloff * b

# Tone map (simple Reinhard)
pixels = pixels / (1 + pixels)
pixels = np.clip(pixels * 255, 0, 255).astype(np.uint8)

img = Image.fromarray(pixels, 'RGB')
draw = ImageDraw.Draw(img)

# ── Draw connections between nearby attractors ─────────────────────
for i in range(len(attractors)):
    for j in range(i+1, len(attractors)):
        x1, y1 = attractors[i][0], attractors[i][1]
        x2, y2 = attractors[j][0], attractors[j][1]
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if dist < 250:
            # Connection strength inversely proportional to distance
            alpha = int(max(0, min(255, (250 - dist) / 250 * 40)))
            hue_avg = (attractors[i][2] + attractors[j][2]) / 2
            r, g, b = colorsys.hsv_to_rgb(hue_avg % 1.0, 0.3, 0.4)
            c = (int(r*255), int(g*255), int(b*255))
            draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=c, width=1)

# ── Draw attractor nodes ───────────────────────────────────────────
for ax, ay, hue, sat, val, radius, intensity in attractors:
    r_core = max(2, int(intensity * 8))
    r_ring = r_core + 4

    # Core
    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, sat, min(1, val * 1.5))
    draw.ellipse([int(ax)-r_core, int(ay)-r_core, int(ax)+r_core, int(ay)+r_core],
                 fill=(int(r*255), int(g*255), int(b*255)))

    # Ring — radius represents influence zone, all similar (no edge)
    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.3, 0.4)
    draw.ellipse([int(ax)-r_ring, int(ay)-r_ring, int(ax)+r_ring, int(ay)+r_ring],
                 outline=(int(r*255), int(g*255), int(b*255)), width=1)

# ── Title ──────────────────────────────────────────────────────────
try:
    f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except:
    f_title = f_sub = ImageFont.load_default()

draw.text((40, 30), "NO EDGE", fill='#8899aa', font=f_title)
draw.text((40, 58), "smooth spectrum · diffuse cognition · 30 attractors · no dominant mode",
          fill='#3a4a5a', font=f_sub)

# Save
from pathlib import Path
out_dir = Path("/home/sya/journal/art/2026-04-11")
img.save(str(out_dir / "072-free.png"), "PNG")
print(f"Saved: {out_dir / '072-free.png'}")

tg = img.resize((1000, 643), Image.LANCZOS)
tg.save(str(out_dir / "072-free_tg.png"), "PNG")
print(f"Telegram: {out_dir / '072-free_tg.png'}")
