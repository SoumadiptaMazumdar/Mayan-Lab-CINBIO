
from pathlib import Path
import numpy as np
import tifffile

# ========================================
# LEICA FLIM PHASOR DATA INSPECTION
# Sample: A375 WT Flipper-TM 001
# ========================================

# Folder containing the Leica TIFF exports
folder = Path(__file__).resolve().parent / ".vscode" / "WT001"

if not folder.exists():
    raise FileNotFoundError(
        f"Cannot find folder: {folder}"
    )

# Find all TIFF images automatically
tiff_files = sorted(
    list(folder.glob("*.tif")) +
    list(folder.glob("*.tiff"))
)

if not tiff_files:
    raise FileNotFoundError(
        f"No TIFF files found in {folder}"
    )

print("\n===================================")
print("A375 WT 001 — LEICA PHASOR ANALYSIS")
print("===================================")
print(f"Folder: {folder}")
print(f"Number of TIFF files: {len(tiff_files)}")

# Identify Leica channels
def identify_channel(filename):
    name = filename.lower().replace("_", " ")

    if "imaginary" in name:
        return "Phasor Imaginary (S)"

    if "real" in name:
        return "Phasor Real (G)"

    if "intensity" in name:
        return "Phasor Intensity"

    if "plot" in name:
        return "Phasor Plot"

    return "Other Leica image"


# Inspect original numerical values
for path in tiff_files:

    image = tifffile.imread(path)
    channel = identify_channel(path.name)

    print("\n-----------------------------------")
    print(f"FILE: {path.name}")
    print(f"CHANNEL: {channel}")
    print("-----------------------------------")

    print(f"Shape: {image.shape}")
    print(f"Data type: {image.dtype}")

    print(f"Minimum: {np.min(image)}")
    print(f"Maximum: {np.max(image)}")
    print(f"Mean: {np.mean(image):.3f}")
    print(f"Median: {np.median(image):.3f}")
    print(f"Standard deviation: {np.std(image):.3f}")
    print(f"Unique values: {len(np.unique(image))}")

    # Inspect raw pixel values without modifying data
    print("First 10 pixel values:")
    print(image.ravel()[:10])

print("\n===================================")
print("INSPECTION COMPLETE")
print("No image data were modified.")
print("Phasor scaling is not yet validated.")
print("===================================")
