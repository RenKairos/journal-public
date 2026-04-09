#!/usr/bin/env python3
"""
065-free — "Avalanche Geometry"
Gradient avalanche dimensional crossover on a scale-free network.
Three panels: sub-diffusive (D<1), critical (D≈1), super-diffusive (D>1).

Uses stochastic cascade model on Barabási-Albert network.
Each node fires with probability sigmoid(stress - threshold) / temperature.
Temperature controls the sharpness of the firing threshold.
Low temperature = sharp threshold (sub-diffusive), 
High temperature = fuzzy threshold (super-diffusive).
Coupling α controls how much stress firing nodes transfer to neighbors.
"""

import numpy as np
import cairo
import random
import os
from math import exp

W, H = 2400, 800
PANEL_W = W // 3
N_NODES = 200
SEED = 65
np.random.seed(SEED)
random.seed(SEED)

def build_ba_network(n, m0=5, m=3):
    adj = {i: set() for i in range(m0)}
    for i in range(m0):
        for j in range(m0):
            if i != j:
                adj[i].add(j)
    degrees = [m0 - 1] * m0
    nodes = list(range(m0))
    for new_node in range(m0, n):
        total_deg = sum(degrees)
        probs = [d / total_deg for d in degrees]
        targets = set()
        while len(targets) != m:
            chosen = random.choices(nodes, weights=probs, k=1)[0]
            targets.add(chosen)
        adj[new_node] = set()
        for t in targets:
            adj[new_node].add(t)
            adj[t].add(new_node)
            degrees[t] += 1
        degrees.append(m)
        nodes.append(new_node)
    return adj

adj = build_ba_network(N_NODES)
mean_deg = sum(len(v) for v in adj.values()) / N_NODES
print(f"Network: {N_NODES} nodes, mean degree {mean_deg:.1f}")

# Precompute adjacency as numpy arrays for speed
adj_list = [list(adj[i]) for i in range(N_NODES)]
adj_array = np.zeros((N_NODES, N_NODES), dtype=np.float32)
for i in range(N_NODES):
    for j in adj[i]:
        adj_array[i, j] = 1.0
degree_arr = np.array([len(adj[i]) for i in range(N_NODES)], dtype=np.float32)

def layout_network(adj, width, height, iterations=500):
    n = len(adj)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    angles += np.random.normal(0, 0.15, n)
    pos = np.column_stack([
        width / 2 + (width * 0.38) * np.cos(angles),
        height / 2 + (height * 0.38) * np.sin(angles)
    ])
    for iteration in range(iterations):
        forces = np.zeros_like(pos)
        temp = 0.3 * (1 - iteration / iterations)
        for i in range(n):
            for j in adj[i]:
                if j > i:
                    diff = pos[j] - pos[i]
                    dist = np.linalg.norm(diff) + 1e-6
                    ideal = 25
                    force_mag = (dist - ideal) * 0.008
                    f = diff / dist * force_mag
                    forces[i] += f
                    forces[j] -= f
            for k in random.sample(range(n), min(12, n)):
                if k != i and k not in adj[i]:
                    diff = pos[k] - pos[i]
                    dist = np.linalg.norm(diff) + 1e-6
                    if dist < 45:
                        forces[i] -= diff / dist * 0.3 / (dist + 1)
        center = np.array([width / 2, height / 2])
        forces += (center - pos) * 0.002
        pos += forces * temp
        pos[:, 0] = np.clip(pos[:, 0], 35, width - 35)
        pos[:, 1] = np.clip(pos[:, 1], 35, height - 35)
    return pos

pos = layout_network(adj, PANEL_W - 20, H - 80)

def simulate_cascade(adj_list, degree_arr, n_nodes, alpha, temperature,
                      n_seed=3, seed_val=42, max_steps=60):
    """
    Stochastic cascade with temperature-controlled firing probability.
    
    alpha: how much stress a firing node transfers (per unit of degree)
    temperature: sharpness of threshold
      - low temp (0.1): very sharp, almost deterministic → sub-diffusive
      - medium temp (1.0): moderate stochasticity → critical  
      - high temp (5.0): very fuzzy, easy to fire → super-diffusive
    
    Each step:
    1. Compute firing probability for each node: σ((stress - threshold) / temperature)
    2. Stochastically determine which nodes fire
    3. Firing nodes transfer alpha/degree stress to each neighbor
    4. Firing nodes reset to 0
    """
    rng = np.random.RandomState(seed_val % (2**31))
    
    stress = rng.uniform(0.0, 0.5, n_nodes)
    threshold = 1.0
    history = []
    
    seeds = rng.choice(n_nodes, n_seed, replace=False)
    stress[seeds] = threshold + rng.uniform(0.5, 2.0, n_seed)
    
    for step in range(max_steps):
        # Firing probability
        excess = (stress - threshold) / temperature
        # Clip for numerical stability
        probs = 1.0 / (1.0 + np.exp(-np.clip(excess, -20, 20)))
        
        # Stochastic firing
        fires = rng.random(n_nodes) < probs
        firing = set(np.where(fires)[0])
        
        if not firing:
            break
        history.append(firing)
        
        # Stress transfer
        delta = np.zeros(n_nodes)
        for node in firing:
            deg = degree_arr[node]
            if deg == 0:
                continue
            transfer = alpha * stress[node] / deg
            for nb in adj_list[node]:
                delta[nb] += transfer
            stress[node] = 0.0
        
        stress += delta
        
        # Tiny decay to prevent runaway accumulation
        stress *= 0.995
    
    return history

def find_rep(adj_list, degree_arr, n_nodes, alpha, temperature,
             n_tries=500, pref_dur=None, pref_unique=None):
    best = None
    best_score = float('inf')
    for t in range(n_tries):
        sv = (SEED * 1000 + t * 137 + int(alpha * 1000) + int(temperature * 100)) % (2**31)
        ns = random.Random(sv).randint(1, 4)
        hist = simulate_cascade(adj_list, degree_arr, n_nodes, alpha, temperature,
                                 n_seed=ns, seed_val=sv)
        dur = len(hist)
        unique = len(set().union(*hist)) if hist else 0
        peak = max(len(s) for s in hist) if hist else 0
        
        if pref_dur and pref_unique:
            score = (abs(dur - pref_dur) / max(pref_dur, 1) * 2 +
                     abs(unique - pref_unique) / max(pref_unique, 1))
            if score < best_score:
                best_score = score
                best = (hist, dur, unique, peak)
        else:
            if best is None or unique > best[2]:
                best = (hist, dur, unique, peak)
    return best

print("Finding representative cascades...")
# (label, alpha, temperature, color, pref_duration, pref_unique_nodes)
regimes = [
    ("Sub-diffusive  D < 1",    0.3,  0.15, (1.0, 0.50, 0.10), 3,   6),
    ("Critical  D ≈ 1",         0.8,  0.6,  (0.95, 0.82, 0.30), 25,  80),
    ("Super-diffusive  D > 1",  1.0,  3.0,  (0.10, 0.82, 0.75), 50,  180),
]

cascade_data = []
for label, alpha, temp, color, td, tu in regimes:
    hist, dur, unique, peak = find_rep(adj_list, degree_arr, N_NODES, alpha, temp,
                                        1000, td, tu)
    print(f"  {label}: dur={dur}, unique={unique}/{N_NODES}, peak={peak}, α={alpha}, T={temp}")
    cascade_data.append((label, alpha, temp, color, hist, dur, unique, peak))

# ── Render ──────────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "065-free.png")
tg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "065-free_tg.png")

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)

bg = cairo.LinearGradient(0, 0, W, H)
bg.add_color_stop_rgb(0, 0.022, 0.022, 0.035)
bg.add_color_stop_rgb(0.5, 0.035, 0.030, 0.045)
bg.add_color_stop_rgb(1, 0.022, 0.028, 0.040)
ctx.set_source(bg)
ctx.rectangle(0, 0, W, H)
ctx.fill()

for x in [PANEL_W, 2 * PANEL_W]:
    sep = cairo.LinearGradient(x, 0, x, H)
    sep.add_color_stop_rgba(0, 0.2, 0.2, 0.25, 0)
    sep.add_color_stop_rgba(0.3, 0.2, 0.2, 0.25, 0.4)
    sep.add_color_stop_rgba(0.7, 0.2, 0.2, 0.25, 0.4)
    sep.add_color_stop_rgba(1, 0.2, 0.2, 0.25, 0)
    ctx.set_source(sep)
    ctx.set_line_width(1)
    ctx.move_to(x, 0)
    ctx.line_to(x, H)
    ctx.stroke()

for panel_idx, (label, alpha, temp, color, hist, dur, unique, peak) in enumerate(cascade_data):
    ctx.save()
    ctx.translate(panel_idx * PANEL_W + 10, 10)
    
    r, g, b = color
    n_steps = len(hist)
    
    activity = np.zeros(N_NODES)
    edge_activity = {}
    
    for step_idx, firing_set in enumerate(hist):
        t_weight = np.exp(1.5 * step_idx / max(n_steps - 1, 1)) / np.e**1.5
        for node in firing_set:
            activity[node] += t_weight
        for node in firing_set:
            for nb in adj[node]:
                if nb in firing_set:
                    edge = (min(node, nb), max(node, nb))
                    edge_activity[edge] = edge_activity.get(edge, 0) + t_weight
    
    max_act = max(activity.max(), 1)
    max_edge = max(edge_activity.values()) if edge_activity else 1
    
    # Ghost network
    ctx.set_source_rgba(0.07, 0.07, 0.09, 0.08)
    ctx.set_line_width(0.2)
    for i in range(N_NODES):
        for j in adj[i]:
            if j > i:
                ctx.move_to(pos[i][0], pos[i][1])
                ctx.line_to(pos[j][0], pos[j][1])
                ctx.stroke()
    
    # Cascade edges
    for (i, j), count in edge_activity.items():
        intensity = count / max_edge
        av = intensity ** 0.45 * 0.75
        lw = 0.3 + intensity * 5.0
        ctx.set_source_rgba(r, g, b, av)
        ctx.set_line_width(lw)
        ctx.move_to(pos[i][0], pos[i][1])
        ctx.line_to(pos[j][0], pos[j][1])
        ctx.stroke()
    
    # Nodes
    for i in range(N_NODES):
        act = activity[i] / max_act
        if act > 0.01:
            gr = 3 + act * 18
            glow = cairo.RadialGradient(pos[i][0], pos[i][1], 0,
                                         pos[i][0], pos[i][1], gr)
            glow.add_color_stop_rgba(0, r, g, b, act * 0.6)
            glow.add_color_stop_rgba(0.3, r, g, b, act * 0.3)
            glow.add_color_stop_rgba(1, r, g, b, 0)
            ctx.set_source(glow)
            ctx.arc(pos[i][0], pos[i][1], gr, 0, 2 * np.pi)
            ctx.fill()
        
        nr = 0.8 + act * 4.5
        ctx.set_source_rgba(r, g, b, 0.1 + act * 0.9)
        ctx.arc(pos[i][0], pos[i][1], nr, 0, 2 * np.pi)
        ctx.fill()
        
        if act > 0.25:
            ctx.set_source_rgba(min(r+0.45, 1), min(g+0.45, 1), min(b+0.45, 1), act * 0.8)
            ctx.arc(pos[i][0], pos[i][1], nr * 0.3, 0, 2 * np.pi)
            ctx.fill()
    
    # Timeline
    sizes = [len(s) for s in hist]
    if sizes:
        sw = PANEL_W - 40
        sh = 40
        sx = 15
        sy = H - 65
        
        ctx.set_source_rgba(0.03, 0.03, 0.05, 0.7)
        ctx.rectangle(sx, sy, sw, sh)
        ctx.fill()
        
        mx = max(sizes)
        nb = len(sizes)
        bw = max(sw / max(nb, 1), 1.5)
        
        for idx, sz in enumerate(sizes):
            bh = (sz / mx) * (sh - 6)
            t = idx / max(nb - 1, 1)
            a = 0.1 + t * 0.7
            ctx.set_source_rgba(r, g, b, a)
            ctx.rectangle(sx + idx * bw, sy + sh - bh - 3, max(bw - 0.5, 0.5), bh)
            ctx.fill()
        
        peak_idx = sizes.index(mx)
        px = sx + peak_idx * bw + bw/2
        ctx.set_source_rgba(1, 1, 1, 0.25)
        ctx.set_line_width(0.5)
        ctx.move_to(px, sy + 1)
        ctx.line_to(px, sy + sh - 1)
        ctx.stroke()
        
        ctx.set_source_rgba(0.35, 0.35, 0.4, 0.5)
        ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(7)
        ctx.move_to(sx, sy - 2)
        ctx.show_text(f"cascade: duration={nb}  peak={mx}@t{peak_idx}")
    
    # Labels
    ctx.set_source_rgb(0.50, 0.50, 0.55)
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(11)
    ctx.move_to(15, H - 18)
    ctx.show_text(label)
    
    ctx.set_source_rgba(0.30, 0.30, 0.35, 0.6)
    ctx.set_font_size(8)
    ctx.move_to(15, 22)
    ctx.show_text(f"nodes: {unique}/{N_NODES}  |  steps: {dur}  |  peak: {peak}  |  α={alpha}  T={temp}")
    
    ctx.restore()

# Title + arrow
ctx.set_source_rgb(0.50, 0.50, 0.55)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(9)
ctx.move_to(10, 12)
ctx.show_text("065 — Avalanche Geometry")

ay = 12
ax0 = PANEL_W + 25
ax1 = 2 * PANEL_W - 25
ctx.set_source_rgba(0.25, 0.25, 0.3, 0.35)
ctx.set_line_width(0.5)
ctx.move_to(ax0, ay)
ctx.line_to(ax1, ay)
ctx.stroke()
ctx.move_to(ax1, ay)
ctx.line_to(ax1 - 5, ay - 2.5)
ctx.line_to(ax1 - 5, ay + 2.5)
ctx.close_path()
ctx.fill()
ctx.set_font_size(7)
ctx.set_source_rgba(0.3, 0.3, 0.35, 0.35)
ctx.move_to((ax0 + ax1) / 2 - 45, ay - 2)
ctx.show_text("dimensional crossover  D →")

surface.write_to_png(output_path)
print(f"\nWritten: {output_path}")

from PIL import Image
img = Image.open(output_path)
max_dim = 1280
ratio = min(max_dim / img.width, max_dim / img.height)
if ratio < 1:
    tg_img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
else:
    tg_img = img.copy()
tg_img.save(tg_path)
print(f"Telegram: {tg_path} ({tg_img.size[0]}x{tg_img.size[1]})")
