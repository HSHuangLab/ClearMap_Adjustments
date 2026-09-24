from pathlib import Path
import numpy as np

import matplotlib.pyplot as plt
import tifffile

from Examples.example_utils import plot_alignment,evaluate_alignment,inspect_volume

# File paths belong to this experiment; plotting lives in the shared utility.
output_folder = Path(__file__).resolve().parent / "output"

fixed = tifffile.imread(output_folder / "fixed.tif")
moving = tifffile.imread(output_folder / "moving_shifted.tif")
aligned = tifffile.imread(
    output_folder / "alignment_translation" / "result.0.tif"
)

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

fixed_inner = fixed[:, :, 10:-10]
moving_inner=moving[:,:,10:-10]
aligned_inner = aligned[:, :, 10:-10]

results = evaluate_alignment(fixed_inner, moving_inner, aligned_inner)
print(results)
