
from pathlib import Path
import numpy as np
import tifffile
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

# ==========================================
# A375 WT versus Cx43 — Spatial FLIM comparison
# ==========================================

root = Path(__file__).resolve().parent

wt = root / ".vscode" / "WT001"
cx = root / ".vscode" / "CX43_001"

output = root / "WT_CX43_Comparison"
output.mkdir(exist_ok=True)

def load_images(folder, prefix):
    raw = tifffile.imread(folder / f"{prefix}_FastFLIM.tif")
    intensity = tifffile.imread(
        folder / f"{prefix}_Intensity.tif"
    ).astype(np.float32)

    if raw.dtype == np.uint16:
        lifetime = raw.view(np.float16).astype(np.float32)
    else:
        lifetime = raw.astype(np.float32)

    if lifetime.shape != intensity.shape:
        raise ValueError(f"Image size mismatch for {prefix}")

    return lifetime, intensity

wt_tau, wt_int = load_images(wt, "A375_WT_001")
cx_tau, cx_int = load_images(cx, "A375_CX43_001")

# Same exploratory filters for both conditions
threshold = 35.0
lifetime_min = 2.0
lifetime_max = 7.0

def make_masked(tau, intensity):
    mask = (
        np.isfinite(tau)
        & np.isfinite(intensity)
        & (intensity >= threshold)
        & (tau >= lifetime_min)
        & (tau <= lifetime_max)
    )
    return np.where(mask, tau, np.nan), mask

wt_map, wt_mask = make_masked(wt_tau, wt_int)
cx_map, cx_mask = make_masked(cx_tau, cx_int)

# Identical colour scale
cmap = plt.get_cmap("turbo").copy()
cmap.set_bad("black")
norm = Normalize(vmin=3.0, vmax=5.5)

fig, axes = plt.subplots(1, 2, figsize=(13, 6))

im = axes[0].imshow(wt_map, cmap=cmap, norm=norm)
axes[0].set_title("A375 WT 001")
axes[0].axis("off")

axes[1].imshow(cx_map, cmap=cmap, norm=norm)
axes[1].set_title("A375 Cx43 001")
axes[1].axis("off")

cbar = fig.colorbar(
    im, ax=axes,
    fraction=0.025,
    pad=0.025
)
cbar.set_label("Candidate fluorescence lifetime (ns)")

fig.suptitle("Flipper-TM Spatial FLIM — WT versus Cx43", fontsize=15)
fig.subplots_adjust(
    left=0.03, right=0.90,
    bottom=0.05, top=0.88,
    wspace=0.05
)

for name, tau, mask in [
    ("WT", wt_tau, wt_mask),
    ("Cx43", cx_tau, cx_mask)
]:
    values = tau[mask]
    print(f"\n{name}")
    print("Selected pixels:", len(values))
    print("Mean candidate lifetime (ns):",
          round(float(np.mean(values)), 4))
    print("Median candidate lifetime (ns):",
          round(float(np.median(values)), 4))

fig.savefig(
    output / "A375_WT_vs_CX43_Spatial_FLIM.png",
    dpi=600, bbox_inches="tight"
)
fig.savefig(
    output / "A375_WT_vs_CX43_Spatial_FLIM.pdf",
    bbox_inches="tight"
)

print("\nSaved comparison in:", output)
plt.show()
