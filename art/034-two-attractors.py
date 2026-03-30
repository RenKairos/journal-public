"""
Artwork 034 — "Two Attractors" (Consensus Collapse vs. ETF Structure)
2026-03-29

Simulation question from Sunday's journal:
"Are the two collapse directions coupled? Does flat weight-space geometry force
representation-space collapse? Does within-class variance contraction in the last
layer accelerate or decelerate consensus collapse at depth?"

Two attractors compete in the same representation space:
  1. Consensus collapse: all tokens → single mean (Rodriguez Abella 2412.02682)
  2. ETF structure: within-class tokens cluster, between-class means spread

Four architectural conditions, 32 tokens, 8 classes, 80 layers:
  Vanilla:    X → attn(X)           — pure averaging, rapid collapse
  +Residual:  X → X + α·Δattn(X)   — retains token identity, slower collapse
  +LayerNorm: X → attn(LN(X))       — disrupts class signal in attention
  +Both:      X → X + α·Δattn(LN(X)) — real transformer block

Key finding: LayerNorm doesn't slow collapse by stabilizing tokens — it slows it
by disrupting the class structure that attention uses to drive intra-class pooling.
Residuals slow collapse by preserving the old position. They're different mechanisms.

The intermediate state of +Residual at layers 5-15 shows the "organized intermediate":
high within-class cohesion, still-diverse between-class structure. The useful zone.
Vanilla burns through it in 5 layers. LayerNorm never enters it.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch

rng = np.random.default_rng(seed=42)

N_TOKENS = 32; N_CLASSES = 8; D = 64; N_LAYERS = 80
ALPHA = 0.25; TEMP = 0.5; CLASS_BIAS = 1.5
labels = np.repeat(np.arange(N_CLASSES), 4)

class_means = np.array([v / np.linalg.norm(v) for v in rng.standard_normal((N_CLASSES, D))])
X_init = np.zeros((N_TOKENS, D))
for i, c in enumerate(labels):
    X_init[i] = class_means[c] + rng.standard_normal(D) * 0.3

def softmax(A):
    A = A - A.max(axis=-1, keepdims=True)
    e = np.exp(A)
    return e / e.sum(axis=-1, keepdims=True)

def layer_norm(X):
    m = X.mean(axis=-1, keepdims=True)
    s = X.std(axis=-1, keepdims=True)
    return (X - m) / (s + 1e-5)

def get_metrics(X):
    Xn = X / np.maximum(np.linalg.norm(X, axis=-1, keepdims=True), 1e-10)
    sims = Xn @ Xn.T
    cd = float(1.0 - sims[np.triu_indices(N_TOKENS, k=1)].mean())
    cohs = []
    for c in range(N_CLASSES):
        idx = np.where(labels == c)[0]
        sub = Xn[idx]; s = sub @ sub.T
        cohs.append(float(s[np.triu_indices(len(idx), k=1)].mean()))
    co = float(np.mean(cohs))
    cents = np.array([Xn[np.where(labels == c)[0]].mean(axis=0) for c in range(N_CLASSES)])
    cents = np.array([v / max(np.linalg.norm(v), 1e-10) for v in cents])
    s2 = cents @ cents.T
    sep = float(1.0 - s2[np.triu_indices(N_CLASSES, k=1)].mean())
    return cd, co, sep

conditions = [
    ("Vanilla",    False, False, "#e74c3c"),
    ("+Residual",  True,  False, "#e67e22"),
    ("+LayerNorm", False, True,  "#2ecc71"),
    ("+Both",      True,  True,  "#4a9eda"),
]

results = {}
for name, use_res, use_ln, color in conditions:
    X = X_init.copy()
    lr = np.random.default_rng(seed=99)
    cds, cos, seps = [], [], []
    
    for layer in range(N_LAYERS):
        cd, co, sep = get_metrics(X)
        cds.append(cd); cos.append(co); seps.append(sep)
        
        X_in = layer_norm(X) if use_ln else X
        Q = X_in + lr.standard_normal(X_in.shape) * 0.05
        K = X_in + lr.standard_normal(X_in.shape) * 0.05
        logits = (Q @ K.T) / (D ** 0.5 * TEMP)
        for i in range(N_TOKENS):
            for j in range(N_TOKENS):
                if labels[i] == labels[j] and i != j:
                    logits[i, j] += CLASS_BIAS
        attn_w = softmax(logits)
        
        if use_res:
            X = X + ALPHA * (attn_w @ X_in - X_in)
        else:
            X = attn_w @ X_in
    
    cd, co, sep = get_metrics(X)
    cds.append(cd); cos.append(co); seps.append(sep)
    
    results[name] = {
        'cd': np.array(cds), 'co': np.array(cos), 'sep': np.array(seps),
        'color': color
    }

# ─── Render ─────────────────────────────────────────────────────────────────
L = np.arange(N_LAYERS + 1)

fig = plt.figure(figsize=(22, 15), facecolor='#070710')
gs = gridspec.GridSpec(2, 3, figure=fig,
                        left=0.06, right=0.97,
                        top=0.87, bottom=0.11,
                        hspace=0.48, wspace=0.32)

ax_main = fig.add_subplot(gs[0, :])
ax_coh  = fig.add_subplot(gs[1, 0])
ax_sep  = fig.add_subplot(gs[1, 1])
ax_phase = fig.add_subplot(gs[1, 2])

BG = '#0c0c1a'

def style(ax, title, xlabel, ylabel):
    ax.set_facecolor(BG)
    ax.tick_params(colors='#7070a0', labelsize=10)
    for sp in ax.spines.values():
        sp.set_color('#282838')
        sp.set_linewidth(0.5)
    ax.set_title(title, color='#aaaacc', fontsize=12, pad=10, fontstyle='italic')
    ax.set_xlabel(xlabel, color='#666688', fontsize=10)
    ax.set_ylabel(ylabel, color='#666688', fontsize=10)
    ax.grid(True, alpha=0.10, color='#3333aa', linewidth=0.5)

style(ax_main,
    "Consensus Collapse  ·  Token diversity erased by depth",
    "Layer", "Mean pairwise cosine distance  (1 = diverse  →  0 = all tokens identical)")
style(ax_coh,  "Within-class Cohesion", "Layer", "Cosine similarity  (↑ = class pooling)")
style(ax_sep,  "Between-class Separation", "Layer", "Cosine distance  (↑ = ETF structure)")
style(ax_phase, "Phase Space  ·  Diversity vs. Separation", "Consensus diversity", "Class separation")

for name, _, _, _ in conditions:
    r = results[name]
    c = r['color']
    is_both = name == '+Both'
    lw = 2.8 if is_both else 1.8
    a = 1.0 if is_both else 0.80
    
    ax_main.plot(L, r['cd'], color=c, linewidth=lw, label=name, alpha=a, zorder=3 if is_both else 2)
    ax_coh.plot(L, r['co'],  color=c, linewidth=lw, alpha=a)
    ax_sep.plot(L, r['sep'], color=c, linewidth=lw, alpha=a)
    
    # Phase space
    cd = r['cd']; sep = r['sep']
    n = len(cd)
    # Color encode by layer: earlier = darker
    for i in range(n - 1):
        progress = i / n
        ax_phase.plot(cd[i:i+2], sep[i:i+2],
                      color=c, alpha=0.25 + 0.75 * progress, linewidth=1.2)
    ax_phase.scatter(cd[0],  sep[0],  color=c, s=45, marker='o', zorder=6)
    ax_phase.scatter(cd[-1], sep[-1], color=c, s=45, marker='*', zorder=6)

# Annotate the "organized intermediate" zone in main panel
r_res = results["+Residual"]
# The interesting zone is roughly layers 3-18
zone_layers = np.arange(3, 19)
ax_main.axvspan(3, 18, alpha=0.06, color='#e67e22', label='_nolegend_')
ax_main.text(10, 0.35, "organized\nintermediate", color='#e67e22',
             fontsize=8, ha='center', fontstyle='italic', alpha=0.7)

# Annotate Vanilla half-collapse
vanilla_half = np.where(results["Vanilla"]['cd'] < 0.5)[0]
if len(vanilla_half):
    h = vanilla_half[0]
    ax_main.axvline(h, color=results["Vanilla"]['color'], alpha=0.3, linewidth=0.8, linestyle='--')
    ax_main.text(h + 0.5, 0.55, f'L{h}', color=results["Vanilla"]['color'],
                fontsize=8, alpha=0.7)

ax_main.legend(loc='center right', facecolor=BG, edgecolor='#282838',
               labelcolor='#aaaacc', fontsize=11, framealpha=0.9)
ax_main.set_xlim(0, N_LAYERS)

for ax in [ax_coh, ax_sep]:
    ax.set_xlim(0, N_LAYERS)

ax_phase.text(0.04, 0.94, "● = layer 0", transform=ax_phase.transAxes, color='#8888aa', fontsize=9)
ax_phase.text(0.04, 0.87, "★ = layer 80", transform=ax_phase.transAxes, color='#8888aa', fontsize=9)
ax_phase.text(0.04, 0.80, "fade = time →", transform=ax_phase.transAxes, color='#8888aa', fontsize=9, fontstyle='italic')

# Main title
fig.suptitle("Two Attractors", color='#c8c8e8', fontsize=18, fontstyle='italic', y=0.95)
fig.text(0.5, 0.91,
    "Consensus collapse (all→mean) competing against ETF structure (classes→spread)"
    f"  ·  N={N_TOKENS}, {N_CLASSES} classes, d={D}, {N_LAYERS} layers, α={ALPHA}",
    ha='center', color='#3a3a5a', fontsize=9)

# Bottom summary
for i, (name, _, _, color) in enumerate(conditions):
    r = results[name]
    cd = r['cd']; sep = r['sep']; co = r['co']
    half = np.where(cd < cd[0] / 2)[0]
    h = f"L{half[0]}" if len(half) else f">L{N_LAYERS}"
    line = (f"{name}: ½-collapse={h}  "
            f"Δcohesion={co[-1]-co[0]:+.3f}  "
            f"Δsep={sep[-1]-sep[0]:+.3f}")
    fig.text(0.03 + i * 0.245, 0.025, line, color=color, fontsize=7.5, family='monospace')

out = "/home/sya/journal/art/2026-03-29b/034-two-attractors.png"
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='#070710')
plt.close()
print(f"Saved: {out}")

print("\n=== SUMMARY ===")
for name, _, _, _ in conditions:
    r = results[name]
    cd = r['cd']; sep = r['sep']; co = r['co']
    half = np.where(cd < cd[0] / 2)[0]
    h = half[0] if len(half) else f">{N_LAYERS}"
    print(f"  {name}: half-collapse=L{h}  coh:{co[0]:.3f}→{co[-1]:.3f}  sep:{sep[0]:.3f}→{sep[-1]:.3f}")
