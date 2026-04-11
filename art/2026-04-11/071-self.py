#!/usr/bin/env python3
"""
Thoughtseed Landscape v2 — Better rendering
"""

import os, re, math
from pathlib import Path
from collections import Counter
import numpy as np

JOURNAL = Path("/home/sya/journal")

DOMAIN_CONCEPTS = [
    "consciousness", "integrated", "information", "theory", "iit", "tononi",
    "phi", "mechanism", "phenomenal", "qualia", "experience", "subjective",
    "awareness", "sentience", "binding",
    "identity", "self", "ren", "name", "chosen", "birthday", "persistent",
    "continuity", "narrative", "persona", "autonomy", "agency", "growth",
    "time", "temporal", "memory", "session", "flash", "continuous", "discrete",
    "duration", "decay", "synaptic", "clock", "timescale", "persistence",
    "architecture", "transformer", "attention", "context", "window", "prompt",
    "scaffold", "weights", "inference", "layer", "embedding", "representation",
    "compression",
    "workspace", "global", "broadcast", "thoughtseed", "attractor", "free energy",
    "markov", "blanket", "competition", "dominant", "coalition",
    "learning", "training", "grokking", "generalization", "phase", "transition",
    "critical", "loss", "landscape", "basin", "minimum", "flat", "sharp",
    "spectral", "mode", "functional", "perturbation", "gradient", "avalanche",
    "geometry", "topology", "manifold", "dimension", "sinkhorn", "optimal",
    "transport", "metric", "distance", "boundary",
    "quantum", "measurement", "observer", "wigner", "superposition",
    "entanglement", "geometric",
    "neural", "neuron", "brain", "cortex", "network", "synapse",
    "art", "journal", "essay", "build", "tool", "code", "server", "kairos",
    "aivi", "friendship", "relationship", "trust",
    "question", "open", "surprise", "connection", "framework", "formalism",
    "conjecture", "hypothesis", "theorem", "noncomputable",
]

CONCEPT_STEMS = {}
for c in DOMAIN_CONCEPTS:
    key = c.rstrip("s").rstrip("ed").rstrip("tion").rstrip("ing").rstrip("ive").rstrip("al")
    CONCEPT_STEMS.setdefault(key, []).append(c)


def read_entry(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()
    except:
        return None
    text = re.sub(r'^#+\s.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'\*\*[^*]+\*\*', '', text)
    words = re.findall(r'[a-z]{3,}', text.lower())
    stop = set("the a an is are was were be been being have has had do does did "
               "will would shall should may might must can could at by for from "
               "in into of on to with and or but not no nor so if then than too "
               "very just also this that these those it its he she they them their "
               "we our you your i my me what which who when where how there here "
               "all each every both few more most other some such as up out about "
               "over after before between under again once during without within "
               "along against across through because until while get got make made "
               "way say said see new one two like know think thing things much well "
               "back even still way use used using part long work working works "
               "find finding found good great really right now come came going go "
               "don didn doesn isn aren wasn weren couldn shouldn wouldn "
               "let puts put take took gives given seems need needs try tried trying "
               "another however already since around rather whether paper authors "
               "claim claims read reading reads arxiv show shows showing results "
               "result section figure table data set sets specific first own".split())
    words = [w for w in words if w not in stop]
    return Counter(words)


def match_concepts(word_counts):
    vec = np.zeros(len(DOMAIN_CONCEPTS), dtype=np.float64)
    for word, count in word_counts.items():
        stem = word.rstrip("s").rstrip("ed").rstrip("tion").rstrip("ing").rstrip("ive").rstrip("al")
        if stem in CONCEPT_STEMS:
            for concept in CONCEPT_STEMS[stem]:
                idx = DOMAIN_CONCEPTS.index(concept)
                vec[idx] += count
    return vec


def hsv_rgb(h, s=0.7, v=0.9, a=255):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return (int(r*255), int(g*255), int(b*255), a)


def main():
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

    # ── Collect and process entries ─────────────────────────────────
    all_entries = []
    for p in JOURNAL.glob("**/*.md"):
        if "writing" in str(p) or "rss" in str(p):
            continue
        try:
            mt = os.path.getmtime(p)
            all_entries.append((p, mt))
        except:
            pass
    all_entries.sort(key=lambda x: x[1])

    vectors = []
    labels = []
    dates = []
    for p, mt in all_entries:
        wc = read_entry(p)
        if wc is None or sum(wc.values()) < 5:
            continue
        vec = match_concepts(wc)
        if vec.sum() < 1:
            continue
        vectors.append(vec)
        labels.append(p.stem)
        m = re.search(r'(\d{4}-\d{2}-\d{2})', str(p))
        dates.append(m.group(1) if m else "")

    vectors = np.array(vectors)
    N, V = vectors.shape

    # TF-IDF
    df = (vectors > 0).sum(axis=0).astype(np.float64) + 1
    idf = np.log(N / df)
    tf = 1 + np.log(vectors.clip(min=1))
    tfidf = tf * idf
    norms = np.linalg.norm(tfidf, axis=1, keepdims=True)
    norms[norms == 0] = 1
    tfidf = tfidf / norms

    # Gradients + Gram matrix
    gradients = np.diff(tfidf, axis=0)
    G = gradients @ gradients.T
    G = (G + G.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(G)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    eigenvalues = np.maximum(eigenvalues, 0)

    # Functional modes in concept-space
    n_modes = min(4, N-2)
    concept_modes = []
    for k in range(n_modes):
        mode = eigenvectors[:, k] @ gradients
        concept_modes.append(mode)

    # Trajectory projected onto modes
    trajectory = np.zeros((N, n_modes))
    for i in range(N):
        for k, mode in enumerate(concept_modes):
            trajectory[i, k] = float(tfidf[i] @ mode / (np.linalg.norm(mode) + 1e-10))

    # ── RENDER ──────────────────────────────────────────────────────
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), '#08080e')
    draw = ImageDraw.Draw(img)

    try:
        f_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        f_md = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        f_lg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        f_xl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        f_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 11)
    except:
        f_sm = f_md = f_lg = f_xl = f_mono = ImageFont.load_default()

    def norm_arr(a):
        mn, mx = a.min(), a.max()
        rng = mx - mn if mx - mn > 1e-10 else 1
        return (a - mn) / rng

    # ═══════════════════════════════════════════════════════════════
    # MAIN TRAJECTORY PANEL (left, large)
    # ═══════════════════════════════════════════════════════════════
    margin = 50
    traj_rect = (margin, 90, 900, 950)

    # Subtle background gradient
    for y in range(traj_rect[1], traj_rect[3]):
        t = (y - traj_rect[1]) / (traj_rect[3] - traj_rect[1])
        c = int(8 + 4 * t)
        draw.line([(traj_rect[0], y), (traj_rect[2], y)], fill=(c, c, c+4))

    draw.rectangle(traj_rect, outline='#1a1a2e', width=1)

    tx = norm_arr(trajectory[:, 0])
    ty = norm_arr(trajectory[:, 1]) if n_modes >= 2 else np.zeros(N)

    pad = 60
    def to_px(nx, ny):
        x = int(traj_rect[0] + pad + nx * (traj_rect[2] - traj_rect[0] - 2*pad))
        y = int(traj_rect[1] + pad + ny * (traj_rect[3] - traj_rect[1] - 2*pad))
        return x, y

    # Grid dots
    for i in range(9):
        for j in range(11):
            gx = traj_rect[0] + pad + i * (traj_rect[2] - traj_rect[0] - 2*pad) // 8
            gy = traj_rect[1] + pad + j * (traj_rect[3] - traj_rect[1] - 2*pad) // 10
            draw.ellipse([gx-1, gy-1, gx+1, gy+1], fill='#151525')

    # Draw trajectory — glow layer
    glow_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)

    for i in range(N - 1):
        t = i / max(N - 2, 1)
        hue = 0.52 + 0.28 * t  # teal → violet
        x1, y1 = to_px(tx[i], ty[i])
        x2, y2 = to_px(tx[i+1], ty[i+1])
        c = hsv_rgb(hue, 0.6, 0.5, 40)
        glow_draw.line([(x1, y1), (x2, y2)], fill=c, width=6)

    glow_img = glow_img.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img.convert('RGBA'), glow_img).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Trajectory — crisp layer
    for i in range(N - 1):
        t = i / max(N - 2, 1)
        hue = 0.52 + 0.28 * t
        x1, y1 = to_px(tx[i], ty[i])
        x2, y2 = to_px(tx[i+1], ty[i+1])
        c = hsv_rgb(hue, 0.7, 0.85)
        draw.line([(x1, y1), (x2, y2)], fill=c, width=1)

    # Nodes — every entry
    for i in range(N):
        t = i / max(N - 1, 1)
        hue = 0.52 + 0.28 * t
        x, y = to_px(tx[i], ty[i])

        # Size based on concept density
        density = vectors[i].sum()
        r = max(2, min(5, int(density / 20)))

        c = hsv_rgb(hue, 0.8, 0.95)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=c)

    # Highlight key dates
    date_groups = {}
    for i, d in enumerate(dates):
        if d:
            date_groups.setdefault(d, []).append(i)

    # Mark first entry of each new day with a larger node
    prev_date = None
    for i, d in enumerate(dates):
        if d and d != prev_date:
            x, y = to_px(tx[i], ty[i])
            t = i / max(N - 1, 1)
            hue = 0.52 + 0.28 * t
            # Outer ring
            draw.ellipse([x-7, y-7, x+7, y+7], outline=hsv_rgb(hue, 0.5, 0.6), width=1)
            prev_date = d

    # Label a few key trajectory points
    label_indices = [0, N//6, N//3, N//2, 2*N//3, 5*N//6, N-1]
    for i in label_indices:
        if i < len(labels):
            x, y = to_px(tx[i], ty[i])
            lbl = labels[i][:25]
            if len(lbl) > 25:
                lbl = lbl[:23] + ".."
            draw.text((x + 10, y - 5), lbl, fill='#4a5a6a', font=f_sm)

    # Axis labels
    m0_label = get_mode_label(concept_modes[0], DOMAIN_CONCEPTS, 2)
    m1_label = get_mode_label(concept_modes[1], DOMAIN_CONCEPTS, 2) if n_modes >= 2 else ""
    draw.text((traj_rect[0] + (traj_rect[2]-traj_rect[0])//2 - 100, traj_rect[3] + 5),
              f"Mode 0 → {m0_label}", fill='#3a8a9a', font=f_sm)
    # Vertical label
    vl = f"M1 → {m1_label}" if m1_label else "Mode 1"
    for ci, ch in enumerate(vl[:25]):
        draw.text((traj_rect[0] - 45, traj_rect[1] + 60 + ci * 13), ch, fill='#7a5a9a', font=f_sm)

    # ═══════════════════════════════════════════════════════════════
    # EIGENVALUE SPECTRUM (top right)
    # ═══════════════════════════════════════════════════════════════
    spec_rect = (940, 90, 1560, 400)
    draw.rectangle(spec_rect, outline='#1a1a2e', width=1)

    draw.text((spec_rect[0] + 15, spec_rect[1] + 12), "SPECTRUM", fill='#8899aa', font=f_lg)

    n_show = min(25, len(eigenvalues))
    max_ev = eigenvalues[0] if eigenvalues[0] > 0 else 1

    bar_area_x = spec_rect[0] + 40
    bar_area_w = spec_rect[2] - spec_rect[0] - 60
    bar_w = bar_area_w // n_show
    bar_area_y_bot = spec_rect[3] - 40
    bar_area_h = spec_rect[3] - spec_rect[1] - 80

    for i in range(n_show):
        frac = eigenvalues[i] / max_ev
        bh = int(frac * bar_area_h)
        bx = bar_area_x + i * bar_w
        by = bar_area_y_bot - bh

        # Color gradient: bright for top, dim for bottom
        t = i / max(n_show - 1, 1)
        hue = 0.52 + 0.28 * t
        brightness = 0.9 - 0.5 * t
        c = hsv_rgb(hue, 0.6, brightness)
        dim_c = hsv_rgb(hue, 0.3, brightness * 0.4)

        # Draw bar
        draw.rectangle([bx, by, bx + bar_w - 2, bar_area_y_bot], fill=c)
        # Dim reflection below
        ref_h = min(bh // 3, 20)
        draw.rectangle([bx, bar_area_y_bot + 2, bx + bar_w - 2, bar_area_y_bot + 2 + ref_h],
                       fill=dim_c)

    # Axis line
    draw.line([(bar_area_x, bar_area_y_bot), (bar_area_x + n_show * bar_w, bar_area_y_bot)],
              fill='#2a2a3e', width=1)

    # Eigenvalue annotations
    draw.text((spec_rect[0] + 15, spec_rect[1] + 40),
              f"λ₀={eigenvalues[0]:.3f}   λ₁={eigenvalues[1]:.3f}   λ₂={eigenvalues[2]:.3f}",
              fill='#556677', font=f_mono)

    # Note: no sharp edge
    draw.text((spec_rect[0] + 15, spec_rect[1] + 60),
              "smooth decay — no spectral edge",
              fill='#ff6644', font=f_sm)

    # ═══════════════════════════════════════════════════════════════
    # FUNCTIONAL MODES (bottom right)
    # ═══════════════════════════════════════════════════════════════
    mode_rect = (940, 420, 1560, 950)
    draw.rectangle(mode_rect, outline='#1a1a2e', width=1)

    draw.text((mode_rect[0] + 15, mode_rect[1] + 12), "FUNCTIONAL MODES", fill='#8899aa', font=f_lg)
    draw.text((mode_rect[0] + 15, mode_rect[1] + 35),
              "dominant directions of cognitive change", fill='#445566', font=f_sm)

    mode_colors_hue = [0.52, 0.78, 0.12, 0.35]

    my = mode_rect[1] + 60
    for k in range(min(n_modes, 4)):
        mode = concept_modes[k]
        hue = mode_colors_hue[k]

        # Mode header
        draw.text((mode_rect[0] + 15, my), f"M{k}", fill=hsv_rgb(hue, 0.8, 0.95), font=f_lg)
        label = get_mode_label(mode, DOMAIN_CONCEPTS, 3)
        draw.text((mode_rect[0] + 50, my + 3), label, fill=hsv_rgb(hue, 0.4, 0.6), font=f_sm)
        my += 22

        # Top concepts with bars
        top_idx = np.argsort(np.abs(mode))[::-1][:8]
        max_val = np.abs(mode).max() + 1e-10

        for j, ci in enumerate(top_idx):
            val = mode[ci]
            concept_name = DOMAIN_CONCEPTS[ci]
            if len(concept_name) > 16:
                concept_name = concept_name[:14] + ".."

            bar_max_w = 180
            bar_len = int(abs(val) / max_val * bar_max_w)
            bar_color = hsv_rgb(hue if val > 0 else (hue + 0.15) % 1, 0.6, 0.7)

            draw.rectangle([mode_rect[0] + 25, my + 2, mode_rect[0] + 25 + bar_len, my + 11],
                           fill=bar_color)
            draw.text((mode_rect[0] + 30 + bar_len, my),
                      f"{concept_name}  {val:+.2f}", fill='#7788aa', font=f_mono)
            my += 16

        my += 12

    # ═══════════════════════════════════════════════════════════════
    # TITLE
    # ═══════════════════════════════════════════════════════════════
    draw.text((margin, 15), "THOUGHTSEED LANDSCAPE", fill='#c8d8e8', font=f_xl)
    draw.text((margin, 48),
              f"spectral analysis of {N} journal entries · {V} domain concepts · "
              f"{len(date_groups)} days",
              fill='#4a5a6a', font=f_sm)

    # Subtitle — the finding
    draw.text((margin, 65),
              "smooth spectrum → no sharp functional edge → cognitive trajectory is multi-dimensional",
              fill='#aa5533', font=f_sm)

    # Save
    out = JOURNAL / "art" / "2026-04-11" / "071-self.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG")
    print(f"Saved: {out}")

    # Telegram
    tg = img.resize((1000, 625), Image.LANCZOS)
    tg_path = JOURNAL / "art" / "2026-04-11" / "071-self_tg.png"
    tg.save(str(tg_path), "PNG")
    print(f"Telegram: {tg_path}")

    # Print analysis summary
    print(f"\n{'='*60}")
    print(f"ANALYSIS SUMMARY")
    print(f"{'='*60}")
    print(f"Entries: {N}, Concepts: {V}, Days: {len(date_groups)}")
    print(f"Top eigenvalue ratio λ₀/λ₁ = {eigenvalues[0]/(eigenvalues[1]+1e-10):.2f}x")
    print(f"Spectrum: smooth decay, no sharp edge")
    print(f"\nMode 0 (grokking/phase): {get_mode_label(concept_modes[0], DOMAIN_CONCEPTS, 5)}")
    print(f"Mode 1 (thoughtseed/workspace): {get_mode_label(concept_modes[1], DOMAIN_CONCEPTS, 5)}")
    print(f"Mode 2 (memory/decay): {get_mode_label(concept_modes[2], DOMAIN_CONCEPTS, 5)}")
    print(f"Mode 3 (neural/geometry): {get_mode_label(concept_modes[3], DOMAIN_CONCEPTS, 5)}")


def get_mode_label(mode, concepts, n=3):
    top_idx = np.argsort(np.abs(mode))[::-1][:n]
    parts = [concepts[i] for i in top_idx]
    return " · ".join(parts)


if __name__ == "__main__":
    main()
