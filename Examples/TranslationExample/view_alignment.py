from pathlib import Path

import matplotlib.pyplot as plt
import tifffile

from Examples.example_utils import plot_alignment,evaluate_alignment

# File paths belong to this experiment; plotting lives in the shared utility.
output_folder = Path(__file__).resolve().parent / "output"

fixed = tifffile.imread(output_folder / "fixed.tif")
moving = tifffile.imread(output_folder / "moving_shifted.tif")
aligned = tifffile.imread(
    output_folder / "alignment_translation" / "result.0.tif"
)

plot_alignment(fixed, moving, aligned, z=19)
plt.show()

results = evaluate_alignment(fixed, moving, aligned)
print(results)
