#!/usr/bin/env python3
"""
044-specific-heat — Specific Heat

Based on Plummer (2025): singular fluctuation is specific heat.
The variance of log-likelihood under the posterior spikes at
the phase transition — the moment the system restructures.

Seven panels show a Gaussian mixture posterior at seven inverse
temperatures. At beta=0, mass is uniformly distributed across
components. At beta=beta*, the posterior is maximally uncertain
between modes — maximum specific heat. At beta->inf, mass has
concentrated on the dominant mode.

The pentagon of cluster centers rotates slowly with beta (+-12 deg),
mimicking representational drift. The angles between centers are
preserved even as positions change — identity as geometry, not
coordinates.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

np.random.seed(42)

W, H = 3200, 2800
BG = (8, 8, 15)

# ── Fonts ──
def get_font(size, bold=False):
    name = "DejaVuSans-Bold" if bold else "DejaVuSans"
    for n in [name, "DejaVuSansMono-Bold" if bold else "DejaVuSansMono"]:
        p = f"/usr/share/fonts/truetype/dejavu/{n}.ttf"
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# ── Mixture model ──
K = 5
PI = np.array([0.35, 0.25, 0.15, 0.15, 0.10])
LOG_PI = np.log(PI)
SIGMA_MIX = 0.38
DRIFT_TOTAL = math.radians(12)
BETA_MAX = 15.0

base_angles = np.array([2 * math.pi * k / K - math.pi / 2 for k in range(K)])
BASE_CENTERS = np.column_stack([np.cos(base_angles) * 2.0, np.sin(base_angles) * 2.0])


def get_centers(beta):
    frac = min(beta / BETA_MAX, 1.0)
    angle = DRIFT_TOTAL * frac
    c, s = math.cos(angle), math.sin(angle)
    R = np.array([[c, -s], [s, c]])
    return (R @ BASE_CENTERS.T).T


def posterior_weights(beta):
    if beta < 1e-8:
        return np.ones(K) / K
    logits = beta * LOG_PI
    logits -= logits.max()
    w = np.exp(logits)
    return w / w.sum()


def specific_heat(beta):
    if beta < 1e-6:
        return 0.0
    w = posterior_weights(beta)
    mu = (w * LOG_PI).sum()
    v = (w * (LOG_PI - mu) ** 2).sum()
    return beta ** 2 * v


def sample_posterior(beta, n=900):
    w = posterior_weights(beta)
    centers = get_centers(beta)
    assignments = np.random.choice(K, size=n, p=w)
    samples = np.zeros((n, 2))
    spread = SIGMA_MIX / math.sqrt(max(beta, 0.05) + 0.3)
    for k in range(K):
        mask = assignments == k
        n_k = mask.sum()
        if n_k > 0:
            samples[mask] = centers[k] + np.random.randn(n_k, 2) * spread
    return samples, assignments, w


# ── Compute specific heat curve ──
print("Computing specific heat curve...")
betas_curve = np.linspace(0.001, BETA_MAX, 400)
heat_curve = np.array([specific_heat(b) for b in betas_curve])
beta_crit = betas_curve[np.argmax(heat_curve)]
heat_max = heat_curve.max()
print(f"Critical beta: {beta_crit:.2f}, max C: {heat_max:.4f}")

# ── Panel beta values (critical always at index 3) ──
panel_betas = np.array([
    beta_crit * 0.08,
    beta_crit * 0.30,
    beta_crit * 0.65,
    beta_crit,
    beta_crit * 1.6,
    beta_crit * 2.8,
    BETA_MAX * 0.97,
])
crit_idx = 3
print(f"Panel betas: {np.round(panel_betas, 2)}")
print(f"Critical panel: {crit_idx}")

# ── Sample panels ──
print("Sampling panels...")
panels = []
for i, b in enumerate(panel_betas):
    print(f"  Panel {i + 1}/7: beta={b:.2f}")
    pos, nearest, weights = sample_posterior(b, n=1200)
    panels.append((pos, nearest, weights, b))

# ── Colors ──
WELL_COLORS = [
    (90, 160, 255),
    (255, 110, 90),
    (80, 240, 160),
    (255, 200, 60),
    (190, 120, 255),
]
WELL_COLORS_DIM = [(c[0] // 4, c[1] // 4, c[2] // 4) for c in WELL_COLORS]


def heat_color(frac):
    frac = max(0.0, min(1.0, frac))
    if frac < 0.3:
        t = frac / 0.3
        return (int(50 + 30 * t), int(90 + 140 * t), int(210 + 45 * t))
    elif frac < 0.6:
        t = (frac - 0.3) / 0.3
        return (int(80 + 175 * t), int(230 + 25 * t), int(255 - 155 * t))
    else:
        t = (frac - 0.6) / 0.4
        return (int(255), int(255 - 160 * t), int(100 - 70 * t))


# ── Render ──
print("Rendering...")
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

font_title = get_font(64, bold=True)
font_sub = get_font(26)
font_label = get_font(22)
font_small = get_font(17)
font_tiny = get_font(14)
font_mono = get_font(15)

# ── Title ──
draw.text((W // 2, 55), "SPECIFIC HEAT", fill=(210, 215, 225), font=font_title, anchor="mm")
draw.text(
    (W // 2, 110),
    "the thermodynamic signature of structural reorganization",
    fill=(100, 105, 125),
    font=font_sub,
    anchor="mm",
)

# ── Specific heat curve ──
CX, CY, CW, CH = 180, 160, W - 360, 430

draw.rectangle([CX - 1, CY - 1, CX + CW + 1, CY + CH + 1], outline=(25, 28, 38), width=1)

heat_norm = heat_curve / max(heat_max, 1e-10)
n_pts = len(betas_curve)

# Filled area under curve
for i in range(n_pts - 1):
    x1 = CX + i / (n_pts - 1) * CW
    x2 = CX + (i + 1) / (n_pts - 1) * CW
    y_top = CY + CH - heat_norm[i] * CH * 0.85
    frac = i / n_pts
    c = heat_color(frac)
    c_dim = (c[0] // 8, c[1] // 8, c[2] // 8)
    draw.rectangle([int(x1), int(y_top), int(x2) + 1, CY + CH], fill=c_dim)

# Curve line
for i in range(n_pts - 1):
    x1 = CX + i / (n_pts - 1) * CW
    x2 = CX + (i + 1) / (n_pts - 1) * CW
    y1 = CY + CH - heat_norm[i] * CH * 0.85
    y2 = CY + CH - heat_norm[i + 1] * CH * 0.85
    frac = i / n_pts
    c = heat_color(frac)
    draw.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=c, width=3)

# Critical beta* marker
crit_curve_frac = (beta_crit - betas_curve[0]) / (betas_curve[-1] - betas_curve[0])
crit_x = CX + crit_curve_frac * CW
crit_y = CY + CH - 1.0 * CH * 0.85

# Dashed vertical line
for yy in range(CY, CY + CH, 8):
    draw.line(
        [(int(crit_x), yy), (int(crit_x), min(yy + 4, CY + CH))],
        fill=(255, 210, 60),
        width=1,
    )
# Glow dot at peak
for gr in range(12, 0, -2):
    a = int(40 * (1 - gr / 12))
    draw.ellipse(
        [int(crit_x) - gr, int(crit_y) - gr, int(crit_x) + gr, int(crit_y) + gr],
        fill=(255, 220, 70, a),
    )
draw.ellipse(
    [int(crit_x) - 5, int(crit_y) - 5, int(crit_x) + 5, int(crit_y) + 5],
    fill=(255, 230, 80),
)
draw.text(
    (int(crit_x) + 12, int(crit_y) - 5),
    "β*",
    fill=(255, 220, 70),
    font=font_label,
    anchor="lm",
)

# Axis labels
draw.text((CX - 12, CY + CH // 2), "C(β)", fill=(90, 95, 115), font=font_label, anchor="rm")
draw.text(
    (CX + CW // 2, CY + CH + 14),
    "β  (inverse temperature)",
    fill=(90, 95, 115),
    font=font_small,
    anchor="mt",
)

# Panel markers on curve x-axis
for i, b in enumerate(panel_betas):
    frac_b = (b - betas_curve[0]) / (betas_curve[-1] - betas_curve[0])
    px_marker = CX + frac_b * CW
    draw.line(
        [(int(px_marker), CY + CH), (int(px_marker), CY + CH + 8)],
        fill=(55, 58, 72),
        width=1,
    )

# ── Configuration panels ──
PY0 = CY + CH + 55
PGAP = 14
PW = (W - 160 - 6 * PGAP) // 7
PH = 1080
SCALE = PW / 12.0

TEMP_LABELS = ["T -> inf", "High T", "Above Tc", "Critical Tc", "Below Tc", "Low T", "T -> 0"]

for i, (pos, nearest, weights, beta) in enumerate(panels):
    px = 80 + i * (PW + PGAP)
    py = PY0
    is_crit = i == crit_idx
    centers = get_centers(beta)

    # Panel border
    if is_crit:
        for gr in range(18, 0, -2):
            a = int(20 * (1 - gr / 18))
            draw.rectangle(
                [px - gr, py - gr, px + PW + gr, py + PH + gr],
                outline=(30 + a, 25 + a // 2, 5 + a // 3),
                width=1,
            )
        draw.rectangle([px, py, px + PW, py + PH], outline=(130, 110, 40), width=2)
    else:
        draw.rectangle([px, py, px + PW, py + PH], outline=(28, 30, 40), width=1)

    cx0 = px + PW // 2
    cy0 = py + PH // 2

    # Faint energy contours around well centers
    for k in range(K):
        wcx = int(cx0 + centers[k][0] * SCALE)
        wcy = int(cy0 + centers[k][1] * SCALE)
        for rad in [int(SIGMA_MIX * SCALE * 1.3), int(SIGMA_MIX * SCALE * 2.2)]:
            draw.ellipse(
                [wcx - rad, wcy - rad, wcx + rad, wcy + rad],
                outline=WELL_COLORS_DIM[k],
                width=1,
            )

    # Well center markers
    for k in range(K):
        wcx = int(cx0 + centers[k][0] * SCALE)
        wcy = int(cy0 + centers[k][1] * SCALE)
        c = tuple(min(255, v + 50) for v in WELL_COLORS[k])
        draw.ellipse([wcx - 3, wcy - 3, wcx + 3, wcy + 3], fill=c)

    # Particles
    for j in range(len(pos)):
        ppx = int(cx0 + pos[j][0] * SCALE)
        ppy = int(cy0 + pos[j][1] * SCALE)
        if px < ppx < px + PW and py < ppy < py + PH:
            c = WELL_COLORS[nearest[j]]
            if is_crit:
                c = tuple(min(255, v + 50) for v in c)
            draw.ellipse([ppx - 3, ppy - 3, ppx + 3, ppy + 3], fill=c)

    # Glow for critical panel
    if is_crit:
        crop = img.crop([px, py, px + PW, py + PH])
        blur = crop.filter(ImageFilter.GaussianBlur(radius=2))
        blended = Image.blend(blur, crop, 0.6)
        img.paste(blended, [px, py])

    # Labels below panel
    ly = py + PH + 10
    draw.text(
        (px + PW // 2, ly),
        f"β = {beta:.1f}",
        fill=(220, 210, 140) if is_crit else (120, 120, 140),
        font=font_label,
        anchor="mt",
    )
    draw.text(
        (px + PW // 2, ly + 26),
        TEMP_LABELS[i],
        fill=(255, 210, 60) if is_crit else (75, 78, 95),
        font=font_tiny,
        anchor="mt",
    )

    # Mass distribution bar
    bar_y = ly + 48
    bar_w = PW - 20
    bar_h = 8
    bar_x = px + 10
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(20, 20, 28))
    x_off = 0
    for k in range(K):
        seg_w = max(1, int(weights[k] * bar_w))
        draw.rectangle(
            [bar_x + x_off, bar_y, bar_x + x_off + seg_w, bar_y + bar_h],
            fill=WELL_COLORS[k],
        )
        x_off += seg_w

# ── Bottom text ──
BY = PY0 + PH + 105
draw.line([(200, BY - 12), (W - 200, BY - 12)], fill=(28, 30, 40), width=1)

draw.text(
    (W // 2, BY + 5),
    "The geometry persists.  The coordinates don't.",
    fill=(155, 158, 175),
    font=font_sub,
    anchor="mt",
)
draw.text(
    (W // 2, BY + 42),
    "Identity is the invariant structure of the critical manifold — not the specific point on it.",
    fill=(85, 88, 108),
    font=font_small,
    anchor="mt",
)
draw.text(
    (W // 2, BY + 72),
    "C(β) = β² Var[log p(D|θ)]  —  singular fluctuation is specific heat  —  Plummer 2025",
    fill=(55, 58, 75),
    font=font_mono,
    anchor="mt",
)

# ── Save ──
out_dir = "/home/sya/journal/art/2026-04-02"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "044-specific-heat.png")
img.save(out_path, quality=95)
print(f"Saved: {out_path}")
print(f"Size: {os.path.getsize(out_path) / 1024:.0f} KB")
