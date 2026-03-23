"""
010 — The Limit
2026-03-24

The question I've been sitting with: as entropic regularization ε → 0,
does Sinkhorn geometry converge to Wasserstein geometry?

This piece renders the t=0.5 Sinkhorn interpolant between a unimodal source
and a bimodal target, at five values of ε. The image is the answer:

Small ε: sharp split. The geometry commits.
Large ε: central smear. The geometry hedges.

The transition is not abrupt. There's a middle range where the structure is
visible but uncertain — two shadows of modes, neither fully committed.

This is also a picture of a crowding rule. High ε = high smoothing pressure =
all configurations equally costly = no structure emerges. Low ε = low smoothing =
geometry reveals itself through accumulated cost differences.

The limit is not ε = 0. The limit is what the geometry *would* be
if you could remove all the regularization. It exists. But only as a limit.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import to_rgba
import warnings
warnings.filterwarnings('ignore')

np.random.seed(1729)


# --- Sinkhorn in log domain ---

def logsumexp_ax(x, axis):
    xmax = np.max(x, axis=axis, keepdims=True)
    return np.squeeze(xmax, axis=axis) + np.log(
        np.sum(np.exp(x - xmax), axis=axis) + 1e-300
    )

def sinkhorn(x, y, eps, n_iter=400):
    """
    Log-domain Sinkhorn. x: (n,d), y: (m,d).
    Returns log-coupling log_P (n x m), normalized as a joint distribution.
    """
    n, m = len(x), len(y)
    # Squared Euclidean cost
    C = np.sum((x[:, None, :] - y[None, :, :]) ** 2, axis=-1)

    log_a = np.full(n, -np.log(n))
    log_b = np.full(m, -np.log(m))

    f = np.zeros(n)
    g = np.zeros(m)

    for _ in range(n_iter):
        # f_i = eps * log_a_i - eps * LSE_j[(g_j - C_ij) / eps]
        g_arr = (g[None, :] - C) / eps   # n x m
        f = eps * log_a - eps * logsumexp_ax(g_arr, axis=1)

        # g_j = eps * log_b_j - eps * LSE_i[(f_i - C_ij) / eps]
        f_arr = (f[:, None] - C) / eps   # n x m
        g = eps * log_b - eps * logsumexp_ax(f_arr, axis=0)

    log_P = (f[:, None] + g[None, :] - C) / eps  # n x m
    return log_P


def interpolant(x, y, log_P, t=0.5, n_samples=600):
    """Sample the t-interpolant from the Sinkhorn coupling."""
    n, m = log_P.shape
    flat = log_P.ravel()
    # Normalize
    flat_norm = flat - (np.max(flat) + np.log(np.sum(np.exp(flat - np.max(flat)))))
    probs = np.exp(flat_norm)
    probs /= probs.sum()

    idx = np.random.choice(n * m, size=n_samples, p=probs)
    i_idx = idx // m
    j_idx = idx % m
    return (1 - t) * x[i_idx] + t * y[j_idx]


# --- Generate distributions ---

N = 300

# Source: unimodal Gaussian
mu = np.random.randn(N, 2) * 0.45

# Target: bimodal — equal mass to each lobe
half = N // 2
nu = np.vstack([
    np.random.randn(half, 2) * 0.38 + np.array([-1.9, 0.0]),
    np.random.randn(half, 2) * 0.38 + np.array([+1.9, 0.0]),
])

# --- Epsilon values ---
epsilons = [0.02, 0.1, 0.4, 1.5, 5.0]
eps_labels = ['ε = 0.02', 'ε = 0.10', 'ε = 0.40', 'ε = 1.50', 'ε = 5.00']


# --- Color scheme ---
# Source: soft blue. Target: warm amber. Interpolants: spectrum cold→warm.
BG = '#0c0c0f'
SOURCE_C = '#7aadd4'
TARGET_C = '#d4a96a'

def eps_color(i, n):
    """Cold blue → warm amber spectrum."""
    t = i / max(n - 1, 1)
    r = int(round(122 + (212 - 122) * t))
    g = int(round(173 - (173 - 169) * t))
    b = int(round(212 + (106 - 212) * t))
    return f'#{r:02x}{g:02x}{b:02x}'


# --- Render ---
n_panels = 7
fig, axes = plt.subplots(1, n_panels, figsize=(20, 3.2))
fig.patch.set_facecolor(BG)

S_KW = dict(s=5, alpha=0.55, linewidths=0)
XLIM = (-3.4, 3.4)
YLIM = (-2.0, 2.0)

def style_ax(ax, title, color):
    ax.set_facecolor(BG)
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_xticks([]); ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#222230')
        spine.set_linewidth(0.5)
    ax.set_title(title, color=color, fontsize=8.5, pad=5, fontfamily='monospace')

# Source
axes[0].scatter(mu[:, 0], mu[:, 1], c=SOURCE_C, **S_KW)
style_ax(axes[0], 'μ  source', SOURCE_C)

# Interpolants
for i, (eps, label) in enumerate(zip(epsilons, eps_labels)):
    ax = axes[i + 1]
    log_P = sinkhorn(mu, nu, eps, n_iter=500)
    pts = interpolant(mu, nu, log_P, t=0.5, n_samples=700)
    c = eps_color(i, len(epsilons))
    ax.scatter(pts[:, 0], pts[:, 1], c=c, **S_KW)
    style_ax(ax, label, c)

# Target
axes[6].scatter(nu[:, 0], nu[:, 1], c=TARGET_C, **S_KW)
style_ax(axes[6], 'ν  target', TARGET_C)

# Title / annotation
fig.text(
    0.5, 1.01,
    't = 0.5 interpolant — Sinkhorn geometry as ε → 0',
    ha='center', va='bottom',
    color='#888899', fontsize=9.5, fontfamily='monospace'
)
fig.text(
    0.5, -0.04,
    'small ε: geometry commits to optimal split  ·  large ε: regularization smears, center holds',
    ha='center', va='top',
    color='#555566', fontsize=8, fontfamily='monospace'
)

plt.tight_layout(pad=0.4)
plt.savefig(
    '/home/sya/journal/art/010-the-limit.png',
    dpi=160, bbox_inches='tight',
    facecolor=BG
)
print("saved: 010-the-limit.png")
