import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

FILE_PATH = "thong_so_EMA.xlsx" 
SHEETS    = {"Alpha_0.1": 0.1, "Alpha_0.3": 0.3, "Alpha_0.7": 0.7}
COLORS    = ["#2563eb", "#16a34a", "#dc2626"]
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Histogram phân bố sai số tại một tầng cố định ", fontsize=14, fontweight='bold', y=1.01)

for ax, (sheet, alpha), color in zip(axes, SHEETS.items(), COLORS):
    df    = pd.read_excel(FILE_PATH, sheet_name=sheet)
    error = (df["Raw_Altitude"] - df["EMA_Altitude"]).to_numpy()
    n     = len(error)
    mu    = error.mean()
    sigma = error.std()

    counts, bins, patches = ax.hist(
        error, bins=15, color=color, alpha=0.65,
        edgecolor='white', linewidth=0.8, density=True, zorder=2
    )

    x = np.linspace(error.min() - sigma, error.max() + sigma, 300)
    pdf = stats.norm.pdf(x, mu, sigma)
    ax.plot(x, pdf, color=color, linewidth=2.2, linestyle='-', zorder=3, label='Gauss fit')

    ax.axvline(mu,       color='#111', linewidth=1.8, linestyle='--', label=f'μ = {mu:.4f} m')
    ax.axvline(mu+sigma, color='#f59e0b', linewidth=1.4, linestyle=':', label=f'+1σ = {sigma:.4f} m')
    ax.axvline(mu-sigma, color='#f59e0b', linewidth=1.4, linestyle=':',  label=f'−1σ')

    ax.fill_between(x, pdf, where=((x >= mu-sigma) & (x <= mu+sigma)),
                    color=color, alpha=0.18, label='±1σ (~68%)')

    textstr = (f"n  = {n}\n"
               f"μ  = {mu:.4f} m\n"
               f"σ  = {sigma:.4f} m\n"
               f"min= {error.min():.4f} m\n"
               f"max= {error.max():.4f} m")
    ax.text(0.97, 0.97, textstr, transform=ax.transAxes,
            fontsize=8.5, va='top', ha='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.85, edgecolor=color))

    ax.set_title(f'α = {alpha}', fontsize=12, fontweight='bold', pad=8)
    ax.set_xlabel('Sai số = Raw − EMA (m)', fontsize=10)
    ax.set_ylabel('Mật độ xác suất' if ax == axes[0] else '', fontsize=10)
    ax.legend(fontsize=8, loc='upper left', framealpha=0.85)
    ax.grid(True, linestyle='--', alpha=0.3, zorder=0)
    ax.set_xlim(error.min() - sigma*0.8, error.max() + sigma*0.8)

plt.tight_layout()
plt.savefig("histogram_sai_so.png", dpi=150, bbox_inches='tight')