from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import tifffile

from Examples.example_utils import plot_alignment, evaluate_alignment, inspect_volume

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

print(inspect_volume(fixed,"Fixed"))
print(inspect_volume(moving,"Moving"))
print(inspect_volume(aligned,"Aligned"))

error_before = np.abs(
    fixed.astype(float) - moving.astype(float)
)

error_after = np.abs(
    fixed.astype(float) - aligned.astype(float)
)
#print("error before:", error_before, "error after:", error_after)

results = evaluate_alignment(fixed, moving, aligned)
print(results)