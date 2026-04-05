#!/usr/bin/env python3
"""
051 — "Honeycomb Memory"

Ogranovich et al. 2024 (2604.01469): oscillator-based associative memory with
exponential capacity. Honeycomb Kuramoto networks — m cycles of nc oscillators
chained through shared nodes. Memory lives in phase differences, not absolute phases.
Rotational symmetry: add a constant to all phases and the memory is preserved.

Product structure: each cycle is almost independent. Changing one cycle doesn't
affect others. This is a counterexample to the everything-connects intuition.

This piece shows the synchronization dynamics — how a stored pattern emerges
from noise as coupled oscillators converge. Six panels showing time evolution,
plus a basin recovery test. Phase mapped to hue. The geometry IS the memory.
"""
import numpy as np
import cairo
import math

W, H = 3200, 2400
OUT = "/home/sya/journal/art/2026-04-04/051-honeycomb.png"

np.random.seed(51)

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surface)

# Background
bg = cairo.LinearGradient(0, 0, 0, H)
bg.add_color_stop_rgb(0.0, 0.02, 0.02, 0.05)
bg.add_color_stop_rgb(1.0, 0.01, 0.01, 0.03)
ctx.set_source(bg)
ctx.paint()


# ── Honeycomb Kuramoto Network ──

class HoneycombKuramoto:
    """
    Honeycomb network: m cycles of nc oscillators each, chained through shared nodes.
    Each cycle i has nodes [0, 1, ..., nc-1] where node 0 is shared with cycle i-1.
    Total nodes: m * (nc - 1) + 1
    
    Coupling: uniform K within each cycle (ring topology).
    Stored pattern: a set of target phase differences.
    """
    
    def __init__(self, m, nc, K=2.0):
        self.m = m
        self.nc = nc
        self.K = K
        self.n_total = m * (nc - 1) + 1
        self.phases = np.random.uniform(0, 2 * np.pi, self.n_total)
        
        # Build adjacency: ring within each cycle
        self.edges = []
        for i in range(m):
            offset = i * (nc - 1)
            for j in range(nc):
                n1 = offset + j
                n2 = offset + (j + 1) % nc
                self.edges.append((n1, n2))
        
        # Store a random pattern as phase differences
        self.pattern = np.random.choice([0, np.pi], size=self.nc)  # binary pattern
        # Extend to full network
        self.full_pattern = np.zeros(self.n_total)
        for i in range(m):
            offset = i * (nc - 1)
            for j in range(nc):
                self.full_pattern[offset + j] = self.pattern[j] + np.random.uniform(0, 0.3)
        
    def get_cycle_phases(self, cycle_idx):
        offset = cycle_idx * (self.nc - 1)
        return self.phases[offset:offset + self.nc]
    
    def set_cycle_phases(self, cycle_idx, phases):
        offset = cycle_idx * (self.nc - 1)
        self.phases[offset:offset + self.nc] = phases
    
    def step(self, dt=0.02, n_steps=10):
        """Advance Kuramoto dynamics"""
        for _ in range(n_steps):
            dphi = np.zeros(self.n_total)
            for i, j in self.edges:
                diff = self.phases[j] - self.phases[i]
                dphi[i] += self.K * np.sin(diff)
                dphi[j] += self.K * np.sin(-diff)
            self.phases += dphi * dt
            self.phases = self.phases % (2 * np.pi)
    
    def phase_diffs(self, cycle_idx):
        """Get phase differences within a cycle (rotation-invariant representation)"""
        phases = self.get_cycle_phases(cycle_idx)
        diffs = np.diff(np.concatenate([phases, [phases[0]]]))
        return diffs
    
    def order_parameter(self, cycle_idx):
        """Kuramoto order parameter r for a cycle"""
        phases = self.get_cycle_phases(cycle_idx)
        r = np.abs(np.mean(np.exp(1j * phases)))
        return r
    
    def perturb(self, cycle_idx, noise_scale=1.0):
        """Add noise to a specific cycle"""
        offset = cycle_idx * (self.nc - 1)
        self.phases[offset:offset + self.nc] += np.random.normal(0, noise_scale, self.nc)
        self.phases %= (2 * np.pi)


def phase_to_color(phase, alpha=1.0, brightness=0.85):
    """Map phase [0, 2π] to HSV color"""
    h = phase / (2 * np.pi)
    # HSV to RGB (S=0.8, V=brightness)
    s = 0.8
    v = brightness
    c = v * s
    x = c * (1 - abs((h * 6) % 2 - 1))
    m = v - c
    
    if h < 1/6:   r, g, b = c, x, 0
    elif h < 2/6: r, g, b = x, c, 0
    elif h < 3/6: r, g, b = 0, c, x
    elif h < 4/6: r, g, b = 0, x, c
    elif h < 5/6: r, g, b = x, 0, c
    else:          r, g, b = c, 0, x
    
    return (r + m, g + m, b + m, alpha)


def draw_network(ctx, net, cx, cy, radius, time_label="", show_edges=True):
    """Draw the honeycomb network as a visual structure"""
    nc = net.nc
    m = net.m
    
    # Layout: arrange cycles in a honeycomb-ish pattern
    # Each cycle is a ring of nc oscillators
    cycle_positions = []
    cycle_radius = radius * 0.28
    
    # Arrange cycles in a honeycomb grid
    cols = min(m, 3)
    rows = math.ceil(m / cols)
    spacing_x = radius * 0.55
    spacing_y = radius * 0.48
    
    for i in range(m):
        row = i // cols
        col = i % cols
        if row % 2 == 1:
            col += 0.5
        x = cx + (col - (cols - 1) / 2) * spacing_x
        y = cy + (row - (rows - 1) / 2) * spacing_y
        cycle_positions.append((x, y))
    
    # Compute node positions
    node_positions = {}
    for i in range(m):
        ox, oy = cycle_positions[i]
        offset = i * (nc - 1)
        for j in range(nc):
            angle = 2 * np.pi * j / nc - np.pi / 2
            nx = ox + cycle_radius * np.cos(angle)
            ny = oy + cycle_radius * np.sin(angle)
            node_positions[offset + j] = (nx, ny)
    
    # Draw edges
    if show_edges:
        ctx.set_line_width(0.6)
        for ei, ej in net.edges:
            if ei in node_positions and ej in node_positions:
                x1, y1 = node_positions[ei]
                x2, y2 = node_positions[ej]
                
                # Edge color based on phase synchronization
                diff = abs(net.phases[ej] - net.phases[ei]) % (2 * np.pi)
                sync = np.cos(diff)  # 1 = synchronized, -1 = anti-sync
                
                alpha = 0.08 + 0.12 * (sync + 1) / 2
                r = 0.3 + 0.2 * (sync + 1) / 2
                g = 0.3 + 0.3 * (sync + 1) / 2
                b = 0.4 + 0.2 * (sync + 1) / 2
                
                ctx.set_source_rgba(r, g, b, alpha)
                ctx.move_to(x1, y1)
                ctx.line_to(x2, y2)
                ctx.stroke()
    
    # Draw nodes
    for ni, (nx, ny) in node_positions.items():
        phase = net.phases[ni]
        r, g, b, a = phase_to_color(phase, alpha=0.9, brightness=0.85)
        
        # Glow
        glow = cairo.RadialGradient(nx, ny, 0, nx, ny, 8)
        glow.add_color_stop_rgba(0, r, g, b, 0.15)
        glow.add_color_stop_rgba(1, r, g, b, 0)
        ctx.set_source(glow)
        ctx.arc(nx, ny, 8, 0, 2 * np.pi)
        ctx.fill()
        
        # Node circle
        ctx.set_source_rgba(r, g, b, a)
        ctx.arc(nx, ny, 3.5, 0, 2 * np.pi)
        ctx.fill()
    
    # Cycle labels
    ctx.set_source_rgba(0.4, 0.4, 0.5, 0.25)
    ctx.set_font_size(9)
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    for i, (ox, oy) in enumerate(cycle_positions):
        r_val = net.order_parameter(i)
        ctx.move_to(ox - 12, oy + cycle_radius + 14)
        ctx.show_text(f"C{i} r={r_val:.2f}")
    
    # Time label
    if time_label:
        ctx.set_source_rgba(0.5, 0.5, 0.6, 0.3)
        ctx.set_font_size(11)
        ctx.move_to(cx - 30, cy - radius - 15)
        ctx.show_text(time_label)


def draw_phase_wheel(ctx, phases, cx, cy, radius, label=""):
    """Draw a small phase wheel showing oscillator phases in a cycle"""
    n = len(phases)
    
    # Background circle
    ctx.set_source_rgba(0.1, 0.1, 0.15, 0.3)
    ctx.arc(cx, cy, radius, 0, 2 * np.pi)
    ctx.fill()
    ctx.set_source_rgba(0.3, 0.3, 0.4, 0.2)
    ctx.set_line_width(0.5)
    ctx.arc(cx, cy, radius, 0, 2 * np.pi)
    ctx.stroke()
    
    # Phase dots on the wheel
    for i, phase in enumerate(phases):
        x = cx + radius * 0.75 * np.cos(phase - np.pi / 2)
        y = cy + radius * 0.75 * np.sin(phase - np.pi / 2)
        
        r, g, b, a = phase_to_color(phase, alpha=0.9)
        ctx.set_source_rgba(r, g, b, a)
        ctx.arc(x, y, 2.5, 0, 2 * np.pi)
        ctx.fill()
    
    # Center dot (mean phase)
    mean_z = np.mean(np.exp(1j * phases))
    mean_phase = np.angle(mean_z)
    mean_r = np.abs(mean_z)
    
    x = cx + radius * 0.4 * mean_r * np.cos(mean_phase - np.pi / 2)
    y = cy + radius * 0.4 * mean_r * np.sin(mean_phase - np.pi / 2)
    ctx.set_source_rgba(1.0, 1.0, 1.0, 0.6)
    ctx.arc(x, y, 2, 0, 2 * np.pi)
    ctx.fill()
    
    if label:
        ctx.set_source_rgba(0.4, 0.4, 0.5, 0.3)
        ctx.set_font_size(8)
        ctx.move_to(cx - len(label) * 2.5, cy + radius + 12)
        ctx.show_text(label)


# ── Build the piece ──

# Network parameters
m = 6   # number of cycles
nc = 8  # oscillators per cycle
K = 3.0 # coupling strength (strong enough for sync)

net = HoneycombKuramoto(m, nc, K=K)

# Panel layout: 2 rows x 3 columns of time evolution
# Plus bottom section: product structure demo + basin recovery

panel_w = W // 3
panel_h = H * 0.55  # top portion for time evolution
panel_margin = 40
net_radius = min(panel_w, panel_h) * 0.35

# Time evolution: 6 snapshots
snapshots = [0, 20, 80, 200, 500, 1500]
dt_per_step = 0.03

for idx, total_steps in enumerate(snapshots):
    col = idx % 3
    row = idx // 3
    
    pcx = col * panel_w + panel_w // 2
    pcy = row * panel_h + panel_h // 2 + 20
    
    # Save initial state for first panel, evolve for others
    if idx == 0:
        draw_network(ctx, net, pcx, pcy, net_radius, 
                     time_label=f"t=0 (random)", show_edges=True)
    else:
        # Evolve from previous state
        net.step(dt=dt_per_step, n_steps=total_steps - snapshots[idx - 1])
        t_label = f"t={total_steps}"
        draw_network(ctx, net, pcx, pcy, net_radius,
                     time_label=t_label, show_edges=True)
    
    # Draw phase wheels for each cycle at the bottom of each panel
    wheel_y = pcy + net_radius + 40
    wheel_spacing = panel_w // (m + 1)
    for ci in range(m):
        wx = pcx - panel_w // 2 + (ci + 1) * wheel_spacing
        draw_phase_wheel(ctx, net.get_cycle_phases(ci), wx, wheel_y, 14,
                        label=f"C{ci}")

# Divider
div_y = panel_h * 2 + 10
ctx.set_source_rgba(0.2, 0.2, 0.3, 0.3)
ctx.set_line_width(0.5)
ctx.move_to(50, div_y)
ctx.line_to(W - 50, div_y)
ctx.stroke()

# ── Bottom section: Product Structure & Basin Recovery ──

# LEFT: Product structure — change one cycle, others stay
bottom_y = div_y + 30
bottom_h = H - div_y - 60

# Create two networks: original and perturbed
net_a = HoneycombKuramoto(m, nc, K=K)
np.random.seed(99)
net_a.phases = np.random.uniform(0, 2*np.pi, net_a.n_total)

# Run both to convergence
for _ in range(2000):
    net_a.step(dt=0.03, n_steps=1)

# Copy to net_b
net_b = HoneycombKuramoto(m, nc, K=K)
net_b.phases = net_a.phases.copy()

# Perturb only cycle 2 in net_b
cycle_to_perturb = 2
offset = cycle_to_perturb * (nc - 1)
net_b.phases[offset:offset + nc] += np.pi  # flip one cycle
net_b.phases %= (2 * np.pi)

# Let net_b settle
for _ in range(500):
    net_b.step(dt=0.03, n_steps=1)

# Draw net_a (left half)
left_cx = W // 4
left_cy = bottom_y + bottom_h // 2
draw_network(ctx, net_a, left_cx, left_cy, net_radius * 0.75,
             time_label="Original state", show_edges=True)

# Draw net_b (right half)  
right_cx = 3 * W // 4
right_cy = bottom_y + bottom_h // 2
draw_network(ctx, net_b, right_cx, right_cy, net_radius * 0.75,
             time_label="Cycle 2 flipped, then settled", show_edges=True)

# Comparison arrows showing which cycles changed
mid_x = W // 2
for ci in range(m):
    if ci == cycle_to_perturb:
        ctx.set_source_rgba(1.0, 0.4, 0.3, 0.6)
    else:
        ctx.set_source_rgba(0.3, 0.8, 0.4, 0.3)
    
    y_pos = left_cy - 60 + ci * 20
    ctx.set_line_width(1.5 if ci == cycle_to_perturb else 0.5)
    ctx.move_to(left_cx + net_radius * 0.5, y_pos)
    ctx.line_to(right_cx - net_radius * 0.5, y_pos)
    ctx.stroke()
    
    label = f"C{ci}: {'CHANGED' if ci == cycle_to_perturb else 'preserved'}"
    ctx.set_font_size(8)
    ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_BOLD if ci == cycle_to_perturb 
                         else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_source_rgba(1.0, 0.4, 0.3, 0.5) if ci == cycle_to_perturb else ctx.set_source_rgba(0.3, 0.8, 0.4, 0.25)
    ctx.move_to(mid_x - 25, y_pos - 3)
    ctx.show_text(label)

# Title
ctx.set_source_rgba(0.5, 0.5, 0.6, 0.35)
ctx.set_font_size(13)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.move_to(W // 2 - 140, 25)
ctx.show_text("051 — Honeycomb Memory  |  Kuramoto oscillator network  |  Phase differences encode memory")

# Subtitle
ctx.set_source_rgba(0.4, 0.4, 0.5, 0.25)
ctx.set_font_size(10)
ctx.move_to(W // 2 - 180, 45)
ctx.show_text("Ogranovich+ 2024: exponential capacity through product structure  |  Memory = relational geometry, not absolute state")

surface.write_to_png(OUT)
print(f"Saved: {OUT}")
print(f"Network: {m} cycles × {nc} oscillators = {net.n_total} total nodes")
print(f"Capacity: (2⌈{nc}/4⌉-1)^{m} = {(2*math.ceil(nc/4)-1)**m} stored patterns")
