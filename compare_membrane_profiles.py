
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent

wt_path = root / ".vscode/WT001/Lifetime_Analysis/WT001_Membrane_Width3_Profile.csv"
cx_path = root / ".vscode/CX43_001/Lifetime_Analysis/CX43_001_Membrane_Width3_Profile.csv"

output = root / "WT_CX43_Comparison"
output.mkdir(exist_ok=True)

wt = np.genfromtxt(wt_path, delimiter=",", names=True)
cx = np.genfromtxt(cx_path, delimiter=",", names=True)

wt_x = wt["distance_px"]
wt_y = wt["candidate_lifetime_ns"]

cx_x = cx["distance_px"]
cx_y = cx["candidate_lifetime_ns"]

wt_mean = float(np.nanmean(wt_y))
cx_mean = float(np.nanmean(cx_y))

# Three balanced panels
fig, axes = plt.subplots(
    1, 3,
    figsize=(15, 4.6),
    gridspec_kw={"width_ratios": [1.3, 1.3, 0.8]}
)

colors = ["#1678a2", "#d17725"]

# WT profile
axes[0].plot(wt_x, wt_y, color=colors[0], lw=1.4)
axes[0].axhline(wt_mean, color=colors[0], ls="--", lw=1)
axes[0].set_title("A. A375 WT 001")
axes[0].set_xlabel("Membrane distance (pixels)")
axes[0].set_ylabel("Candidate lifetime (ns)")
axes[0].set_ylim(3.0, 5.2)
axes[0].set_xlim(0, max(wt_x))
axes[0].grid(alpha=0.2)

# Cx43 profile
axes[1].plot(cx_x, cx_y, color=colors[1], lw=1.4)
axes[1].axhline(cx_mean, color=colors[1], ls="--", lw=1)
axes[1].set_title("B. A375 Cx43 001")
axes[1].set_xlabel("Membrane distance (pixels)")
axes[1].set_ylim(3.0, 5.2)
axes[1].set_xlim(0, max(cx_x))
axes[1].grid(alpha=0.2)

# Means displayed as descriptive points
axes[2].scatter(
    [0, 1],
    [wt_mean, cx_mean],
    s=110,
    c=colors,
    zorder=3
)

axes[2].set_xticks([0, 1], ["WT", "Cx43"])
axes[2].set_xlim(-0.5, 1.5)
axes[2].set_ylim(4.1, 4.65)
axes[2].set_title("C. Selected segment means")
axes[2].set_ylabel("Candidate lifetime (ns)")
axes[2].grid(axis="y", alpha=0.2)

for i, value in enumerate([wt_mean, cx_mean]):
    axes[2].annotate(
        f"{value:.4f}",
        (i, value),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

fig.suptitle(
    "A375 WT versus Cx43 — Flipper-TM Membrane Lifetime",
    fontsize=14
)

fig.text(
    0.5, 0.01,
    "Exploratory: one manually selected membrane segment per condition",
    ha="center",
    fontsize=9
)

fig.tight_layout(rect=[0, 0.05, 1, 0.94])

for ext in ("png", "pdf", "svg"):
    path = output / f"WT_vs_CX43_Membrane_Comparison_REVISED.{ext}"
    fig.savefig(
        path,
        dpi=600 if ext == "png" else None,
        bbox_inches="tight"
    )
    print("Saved:", path)

print("\nWT mean:", round(wt_mean, 4))
print("Cx43 mean:", round(cx_mean, 4))
print("Difference:", round(cx_mean - wt_mean, 4), "ns")

plt.show()
