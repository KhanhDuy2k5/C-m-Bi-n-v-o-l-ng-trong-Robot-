import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D


FILE_PATH  = "thong_so_EMA.xlsx"
SHEETS     = {
    "Alpha_0.1": 0.1,
    "Alpha_0.3": 0.3,
    "Alpha_0.7": 0.7,
}
DT = 20.0 

def calc_trise(t, y_ema, y_init, y_final):
    delta = y_final - y_init
    y_10 = y_init + 0.1 * delta
    y_90 = y_init + 0.9 * delta
    if delta > 0:
        i10 = np.where(y_ema >= y_10)[0]
        i90 = np.where(y_ema >= y_90)[0]
    else:
        i10 = np.where(y_ema <= y_10)[0]
        i90 = np.where(y_ema <= y_90)[0]
    if len(i10) == 0 or len(i90) == 0:
        return None, None, None, None, None
    t10 = t[i10[0]];  t90 = t[i90[0]]
    return t90 - t10, t10, t90, y_10, y_90


fig, axes = plt.subplots(3, 1, figsize=(12, 13), sharex=False)
fig.suptitle("Đồ thị thời gian: Áp suất (thô và lọc) theo thời gian — T_rise và T_settle", fontsize=15, fontweight='bold', y=0.98)

for ax, (sheet, alpha) in zip(axes, SHEETS.items()):
    df     = pd.read_excel(FILE_PATH, sheet_name=sheet)
    t      = df["Time_ms"].to_numpy()
    raw    = df["Raw_Altitude"].to_numpy()
    ema    = df["EMA_Altitude"].to_numpy()

    y_init  = np.mean(ema[:5])
    y_final = np.mean(ema[-20:])
    T_settle = DT / alpha

    trise, t10, t90, y_10, y_90 = calc_trise(t, ema, y_init, y_final)

    ax.plot(t, raw, color='#aaaaaa', linewidth=1.2, alpha=0.7, label='Raw Altitude', zorder=1)
    ax.plot(t, ema, color='#2563eb', linewidth=2.2, label='EMA Altitude', zorder=2)

    ax.axhline(y_final, color='#9333ea', linewidth=1.2, linestyle='--', alpha=0.8, label=f'y_final = {y_final:.4f} m')

    if trise is not None:
        ax.axhline(y_10, color='#f97316', linewidth=1.1, linestyle=':', label=f'y₁₀ = {y_10:.4f} m (10%)')
        ax.axhline(y_90, color='#ea580c', linewidth=1.1, linestyle=':', label=f'y₉₀ = {y_90:.4f} m (90%)')

        ymin, ymax = ax.get_ylim()
        ax.axvline(t10, color='#f97316', linewidth=1.5, linestyle='--', alpha=0.9)
        ax.axvline(t90, color='#ea580c', linewidth=1.5, linestyle='--', alpha=0.9)

        y_arrow = y_final + (raw.max() - raw.min()) * 0.35
        ax.annotate('', xy=(t90, y_arrow), xytext=(t10, y_arrow),
                    arrowprops=dict(arrowstyle='<->', color='#e05b2e', lw=1.8))
        ax.text((t10 + t90) / 2, y_arrow + (raw.max()-raw.min())*0.04,
                f'T_rise = {trise:.0f} ms', ha='center', va='bottom',
                color='#e05b2e', fontsize=9.5, fontweight='bold')

    t_settle_x = t[0] + T_settle
    ax.axvline(t_settle_x, color='#16a34a', linewidth=2, linestyle='--',
               label=f'T_settle = {T_settle:.2f} ms (= Δt/α)')
    ax.text(t_settle_x + 20, y_final - (raw.max()-raw.min())*0.15,
            f'T_settle\n{T_settle:.2f} ms', color='#16a34a',
            fontsize=8.5, va='top', fontweight='bold')
    
    ax.set_title(f'α = {alpha}  |  T_rise = {trise} ms  |  T_settle = {T_settle:.2f} ms',
                 fontsize=11, fontweight='bold', pad=6)
    ax.set_xlabel('Thời gian (ms)', fontsize=10)
    ax.set_ylabel('Altitude (m)', fontsize=10)
    ax.set_xlim(t[0] - 20, t[-1] + 20)
    ax.grid(True, linestyle='--', alpha=0.35)
    ax.legend(fontsize=8, loc='upper right', ncol=2, framealpha=0.85)

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("do_thi_EMA.png", dpi=150, bbox_inches='tight')
plt.show()