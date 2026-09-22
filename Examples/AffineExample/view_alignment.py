from pathlib import Path

import matplotlib.pyplot as plt
import tifffile

from Examples.example_utils import plot_alignment, evaluate_alignment

# Locate this example's saved images.
output_folder = Path(__file__).resolve().parent / "output"

fixed = tifffile.imread(output_folder / "fixed.tif")
moving = tifffile.imread(output_folder / "moving_affine.tif")
aligned = tifffile.imread(
    output_folder / "alignment_rigid_affine" / "result.1.tif"
)

# Create the 2D and 3D comparisons.
plot_alignment(fixed, moving, aligned, z=19)

plt.show()

results = evaluate_alignment(fixed, moving, aligned)
print(results)