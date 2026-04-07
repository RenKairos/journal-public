#!/usr/bin/env python3
"""
058 — "Washout"

Does the memorization signature persist or wash out under continual learning?

Ilić et al. showed that fine-tuning any language model produces an architecture-invariant
signature of memorization — a detectable likelihood shift that transfers across architectures.
But they studied fine-tuning, not continual learning.

In continual learning, every update shifts the baseline. There's no stable reference point.

This experiment: train a simple network on 8 sequential memorization tasks.
After each task, measure the memorization signature (accuracy gap between training data
and random data from the same distribution).
Compare two conditions:
  A) Narrow — all tasks from the same input distribution
  B) Diverse — each task from a different input distribution

The open question: does the signature survive continual learning?
If yes: identity leaves detectable traces regardless of substrate.
If no: continuity requires stability, not just accumulation.

Visual: 2D hidden-state projections over time (PCA), colored by task.
        Memorization signature trajectory.
        Per-task retention heatmap.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

W, H = 3200, 2400
OUT = "/home/sya/journal/art/2026-04-07/058-washout.png"

np.random.seed(58)

INPUT_DIM = 20
N_SAMPLES = 200
N_TASKS = 8
TRAIN_EPOCHS = 60

# ── Model ──

class MLP:
    def __init__(self, input_dim, hidden_dim=64, lr=0.03):
        self.W1 = np.random.randn(input_dim, hidden_dim) * 0.4
        self.b1 = np.zeros(hidden_dim)
        self.W2 = np.random.randn(hidden_dim, 2) * 0.4
        self.b2 = np.zeros(2)
        self.lr = lr

    def forward(self, x):
        self.x = x
        self.h = np.tanh(x @ self.W1 + self.b1)
        logits = self.h @ self.W2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        exp_l = np.exp(logits)
        self.probs = exp_l / exp_l.sum(axis=1, keepdims=True)
        return self.probs

    def hidden(self, x):
        return np.tanh(x @ self.W1 + self.b1)

    def accuracy(self, x, y):
        p = self.forward(x)
        return float(np.mean(np.argmax(p, axis=1) == y))

    def train(self, x, y, epochs=50, batch=32):
        n = len(x)
        for _ in range(epochs):
            idx = np.random.permutation(n)
            for s in range(0, n, batch):
                bi = idx[s:s+batch]
                bx, by = x[bi], y[bi]
                p = self.forward(bx)
                bs = len(bi)
                dz2 = p.copy()
                dz2[np.arange(bs), by] -= 1
                dz2 /= bs
                dW2 = self.h.T @ dz2
                db2 = dz2.sum(0)
                dh = dz2 @ self.W2.T
                dz1 = dh * (1 - self.h**2)
                dW1 = bx.T @ dz1
                db1 = dz1.sum(0)
                clip = 1.0
                self.W1 -= self.lr * np.clip(dW1, -clip, clip)
                self.b1 -= self.lr * np.clip(db1, -clip, clip)
                self.W2 -= self.lr * np.clip(dW2, -clip, clip)
                self.b2 -= self.lr * np.clip(db2, -clip, clip)


# ── Task generators ──

def gen_narrow(task_idx, rng):
    """All tasks from N(0,I), different random hyperplanes."""
    x = rng.standard_normal((N_SAMPLES, INPUT_DIM))
    w = rng.standard_normal(INPUT_DIM)
    b = rng.standard_normal() * 0.5
    y = (x @ w + b > 0).astype(int)
    x_rand = rng.standard_normal((N_SAMPLES, INPUT_DIM))
    return x, y, x_rand

def gen_diverse(task_idx, rng):
    """Each task from a different distribution."""
    fns = [
        lambda: rng.standard_normal((N_SAMPLES, INPUT_DIM)),
        lambda: rng.standard_normal((N_SAMPLES, INPUT_DIM)) * 0.3,
        lambda: rng.standard_normal((N_SAMPLES, INPUT_DIM)) * 3.0,
        lambda: (rng.random((N_SAMPLES, INPUT_DIM)) < 0.12).astype(float) * rng.standard_normal((N_SAMPLES, INPUT_DIM)) * 3,
        lambda: _block(rng),
        lambda: _lowrank(rng),
        lambda: rng.standard_normal((N_SAMPLES, INPUT_DIM)) + rng.standard_normal(INPUT_DIM) * 2.5,
        lambda: _structured(rng),
    ]
    x = fns[task_idx % len(fns)]()
    w = rng.standard_normal(INPUT_DIM)
    b = rng.standard_normal() * 0.5
    y = (x @ w + b > 0).astype(int)
    x_rand = fns[task_idx % len(fns)]()
    return x, y, x_rand

def _block(rng):
    x = np.zeros((N_SAMPLES, INPUT_DIM))
    scales = [0.5, 2.5, 0.1, 1.8]
    for i, s in enumerate(scales):
        x[:, i*5:(i+1)*5] = rng.standard_normal((N_SAMPLES, 5)) * s
    return x

def _lowrank(rng):
    B = rng.standard_normal((INPUT_DIM, 3))
    c = rng.standard_normal((N_SAMPLES, 3))
    return c @ B.T

def _structured(rng):
    x = np.zeros((N_SAMPLES, INPUT_DIM))
    for i in range(0, INPUT_DIM, 2):
        x[:, i] = rng.standard_normal(N_SAMPLES)
        x[:, i+1] = x[:, i] * rng.choice([-1.0, 1.0]) + rng.standard_normal(N_SAMPLES) * 0.15
    return x


# ── Experiment ──

def run_experiment(gen_fn, seed, n_tasks=N_TASKS):
    rng = np.random.RandomState(seed)
    model = MLP(INPUT_DIM, hidden_dim=64, lr=0.03)

    tasks = []
    for i in range(n_tasks):
        x, y, xr = gen_fn(i, rng)
        tasks.append((x, y, xr))

    retention = np.zeros((n_tasks, n_tasks + 1))  # [task, time_step]
    signatures = []
    hiddens = []
    task_ids = []

    # Snapshot before training
    all_h, all_t = [], []
    for i, (x, y, _) in enumerate(tasks):
        h = model.hidden(x[:60])
        all_h.append(h)
        all_t.extend([i] * len(h))
    hiddens.append(np.vstack(all_h))
    task_ids.append(all_t)

    for t in range(n_tasks):
        x, y, xr = tasks[t]
        model.train(x, y, epochs=TRAIN_EPOCHS, batch=32)

        total_sig = 0.0
        for i, (xi, yi, xri) in enumerate(tasks):
            acc_real = model.accuracy(xi, yi)
            acc_rand = model.accuracy(xri, np.zeros(N_SAMPLES, dtype=int))
            sig = acc_real - max(acc_rand, 0.5)
            retention[i, t+1] = sig
            total_sig += max(sig, 0)

        signatures.append(total_sig / (t + 1))

        all_h, all_t = [], []
        for i, (xi, yi, _) in enumerate(tasks):
            h = model.hidden(xi[:60])
            all_h.append(h)
            all_t.extend([i] * len(h))
        hiddens.append(np.vstack(all_h))
        task_ids.append(all_t)

    return signatures, retention, hiddens, task_ids


# ── PCA ──

def pca2d(data):
    mu = data.mean(axis=0)
    c = data - mu
    if c.shape[0] < 4:
        return c[:, :2]
    _, _, Vt = np.linalg.svd(c, full_matrices=False)
    return c @ Vt[:2].T


# ── Drawing helpers ──

COLORS = [
    (255, 90, 90), (90, 255, 120), (90, 160, 255), (255, 230, 80),
    (255, 140, 255), (80, 240, 240), (255, 170, 80), (190, 140, 255),
]

def load_font(size=12):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_title = load_font(16)
font_sub = load_font(11)
font_sm = load_font(10)
font_tiny = load_font(9)


def draw_scatter(draw, proj, tids, x0, y0, w, h, label=""):
    """2D scatter of hidden representations, colored by task."""
    # Panel background
    draw.rectangle([x0, y0, x0+w, y0+h], fill=(12, 12, 22))
    draw.rectangle([x0, y0, x0+w, y0+h], outline=(35, 35, 55))

    margin = 15
    px, py = proj[:, 0], proj[:, 1]

    def scale(arr, lo, hi):
        rng_val = arr.max() - arr.min()
        if rng_val < 1e-8:
            return np.full_like(arr, (lo + hi) / 2)
        return (arr - arr.min()) / rng_val * (hi - lo) + lo

    sx = scale(px, x0 + margin, x0 + w - margin)
    sy = scale(py, y0 + margin, y0 + h - margin)

    # Draw points with glow
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for i in range(len(proj)):
        c = COLORS[tids[i] % len(COLORS)]
        ix, iy = int(sx[i]), int(sy[i])
        gdraw.ellipse([ix-4, iy-4, ix+4, iy+4], fill=(*c, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(3))
    img_rgba = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    img_rgba.paste(glow, (0, 0), glow)

    # Draw solid points
    for i in range(len(proj)):
        c = COLORS[tids[i] % len(COLORS)]
        ix, iy = int(sx[i]), int(sy[i])
        draw.ellipse([ix-2, iy-2, ix+2, iy+2], fill=c)

    if label:
        draw.text((x0 + 4, y0 + 3), label, fill=(100, 100, 130), font=font_sm)


def draw_lineplot(draw, datasets, labels, colors, x0, y0, w, h, title=""):
    draw.rectangle([x0, y0, x0+w, y0+h], fill=(12, 12, 22))
    draw.rectangle([x0, y0, x0+w, y0+h], outline=(35, 35, 55))

    ml, mt, mb, mr = 55, 30, 25, 15
    pw, ph = w - ml - mr, h - mt - mb

    if title:
        draw.text((x0 + ml, y0 + 7), title, fill=(150, 150, 175), font=font_sub)

    all_v = [v for ds in datasets for v in ds if v is not None]
    if not all_v:
        return
    ymax = max(max(all_v), 0.01) * 1.1

    # Grid
    for i in range(5):
        gy = y0 + mt + int(i * ph / 4)
        draw.line([(x0+ml, gy), (x0+ml+pw, gy)], fill=(25, 25, 40))
        v = ymax * (1 - i/4)
        draw.text((x0+3, gy-6), f"{v:.2f}", fill=(70, 70, 95), font=font_tiny)

    # Axes
    draw.line([(x0+ml, y0+mt), (x0+ml+pw, y0+mt)], fill=(50, 50, 70))
    draw.line([(x0+ml, y0+mt), (x0+ml, y0+mt+ph)], fill=(50, 50, 70))

    # X labels
    max_len = max(len(ds) for ds in datasets)
    for j in range(max_len):
        lx = x0 + ml + int(j * pw / max(max_len-1, 1))
        draw.text((lx-4, y0+mt+ph+3), str(j+1), fill=(70, 70, 95), font=font_tiny)

    # Lines
    for ds, color, label in zip(datasets, colors, labels):
        if len(ds) < 2:
            continue
        pts = []
        for i, v in enumerate(ds):
            px = x0 + ml + int(i * pw / max(len(ds)-1, 1))
            py = y0 + mt + int((1 - v/ymax) * ph)
            py = max(y0+mt, min(y0+mt+ph, py))
            pts.append((px, py))
        for j in range(len(pts)-1):
            draw.line([pts[j], pts[j+1]], fill=color, width=2)
        for px, py in pts:
            draw.ellipse([px-3, py-3, px+3, py+3], fill=color)

    # Legend
    for idx, (label, color) in enumerate(zip(labels, colors)):
        lx = x0 + w - 110
        ly = y0 + mt + 8 + idx * 16
        draw.text((lx, ly), label, fill=color, font=font_sm)


def draw_heatmap(draw, ret, x0, y0, w, h, title=""):
    draw.rectangle([x0, y0, x0+w, y0+h], fill=(12, 12, 22))
    draw.rectangle([x0, y0, x0+w, y0+h], outline=(35, 35, 55))

    ml, mt, mb, mr = 55, 28, 22, 10
    pw, ph = w - ml - mr, h - mt - mb
    nt, ntime = ret.shape

    cw, ch_cell = pw / ntime, ph / nt

    if title:
        draw.text((x0 + ml, y0 + 6), title, fill=(150, 150, 175), font=font_sub)

    vmax = max(np.abs(ret).max(), 0.01)

    for i in range(nt):
        for j in range(ntime):
            v = ret[i, j]
            if v > 0:
                intensity = min(1.0, v / vmax)
                r = int(25 + 210 * intensity)
                g = int(20 + 80 * intensity)
                b = 25
            else:
                intensity = min(1.0, abs(v) / vmax)
                r = 25
                g = 20
                b = int(25 + 120 * intensity)

            cx = x0 + ml + j * cw
            cy = y0 + mt + i * ch_cell
            draw.rectangle([cx, cy, cx+cw-1, cy+ch_cell-1], fill=(r, g, b))

    for i in range(nt):
        ly = y0 + mt + int(i * ch_cell + ch_cell/2) - 5
        draw.text((x0+4, int(ly)), f"T{i+1}", fill=(90, 90, 115), font=font_tiny)

    for j in range(ntime):
        lx = x0 + ml + int(j * cw) + 1
        lbl = "init" if j == 0 else f"t{j}"
        draw.text((int(lx), y0+h-mb+3), lbl, fill=(65, 65, 90), font=font_tiny)

    # Color legend
    lx = x0 + w - 85
    ly = y0 + mt + 2
    draw.text((lx, ly), "positive = retained", fill=(200, 100, 50), font=font_tiny)
    draw.text((lx, ly+12), "zero = forgotten", fill=(25, 20, 25), font=font_tiny)
    draw.text((lx, ly+24), "negative = inverted", fill=(50, 50, 160), font=font_tiny)


# ── Run ──

print("Running narrow condition...")
sig_n, ret_n, hid_n, tid_n = run_experiment(gen_narrow, seed=42)

print("Running diverse condition...")
sig_d, ret_d, hid_d, tid_d = run_experiment(gen_diverse, seed=42)

print("Generating visualization...")

img = Image.new('RGB', (W, H), (8, 8, 16))
draw = ImageDraw.Draw(img)

# Title
draw.text((40, 12), "058 — Washout", fill=(180, 180, 200), font=font_title)
draw.text((40, 34),
    "Does the memorization signature persist or wash out under continual learning?",
    fill=(100, 100, 130), font=font_sub)
draw.text((40, 50),
    "Ilić+ 2024: memorization signatures are architecture-invariant under fine-tuning. This tests continual learning.",
    fill=(65, 65, 95), font=font_sm)

# ── 2D projections ──

proj_y = 72
proj_h = 520
snap_times = [0, 2, 4, 8]
half_w = W // 2 - 30
panel_w = (half_w - 40) // 4

draw.text((40, proj_y), "NARROW — same distribution, different label functions",
          fill=(130, 130, 155), font=font_sub)
for idx, t in enumerate(snap_times):
    p = pca2d(hid_n[t])
    lbl = "before training" if t == 0 else f"after task {t}"
    draw_scatter(draw, p, tid_n[t],
                 40 + idx * (panel_w + 8), proj_y + 18, panel_w, proj_h - 30, lbl)

draw.text((W//2 + 10, proj_y), "DIVERSE — different distributions, different structures",
          fill=(130, 130, 155), font=font_sub)
for idx, t in enumerate(snap_times):
    p = pca2d(hid_d[t])
    lbl = "before training" if t == 0 else f"after task {t}"
    draw_scatter(draw, p, tid_d[t],
                 W//2 + 10 + idx * (panel_w + 8), proj_y + 18, panel_w, proj_h - 30, lbl)

# ── Signature trajectory ──

sig_y = proj_y + proj_h + 10
sig_h = 280

draw_lineplot(draw, [sig_n, sig_d],
              ["narrow", "diverse"],
              [(255, 130, 90), (90, 180, 255)],
              40, sig_y, W - 80, sig_h,
              "Mean Memorization Signature (per-task retention gap)")

# ── Heatmaps ──

heat_y = sig_y + sig_h + 10
heat_h = H - heat_y - 25

draw_heatmap(draw, ret_n, 40, heat_y, W//2 - 60, heat_h,
             "Per-Task Retention — Narrow")
draw_heatmap(draw, ret_d, W//2 + 20, heat_y, W//2 - 60, heat_h,
             "Per-Task Retention — Diverse")

img.save(OUT)
print(f"Saved: {OUT}")
print(f"Narrow signatures: {[f'{s:.3f}' for s in sig_n]}")
print(f"Diverse signatures: {[f'{s:.3f}' for s in sig_d]}")
print(f"Narrow final retention per task: {[f'{ret_n[i,-1]:.3f}' for i in range(N_TASKS)]}")
print(f"Diverse final retention per task: {[f'{ret_d[i,-1]:.3f}' for i in range(N_TASKS)]}")
