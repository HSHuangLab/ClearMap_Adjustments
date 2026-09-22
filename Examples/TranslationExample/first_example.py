from pathlib import Path
import matplotlib.pyplot as plt
import tifffile
import numpy as np

from Examples.example_utils import load_synthetic_stack, plot_volume_3d

#all 40 slice images
stack= load_synthetic_stack()

print("3D stack shape:", stack.shape)

#shift 10 voxels
fixed=stack
moving= np.zeros_like(fixed)
moving[:,:,10:]=fixed[:,:,:-10]

output_folder = Path(__file__).resolve().parent / "output"
output_folder.mkdir(exist_ok=True)

fixed_path = output_folder / "fixed.tif"
moving_path = output_folder / "moving_shifted.tif"

tifffile.imwrite(fixed_path, fixed, photometric="minisblack")
tifffile.imwrite(moving_path, moving, photometric="minisblack")

print("Saved fixed image:", fixed_path)
print("Saved moving image:", moving_path)

plot_volume_3d(
    fixed,
    comparison=moving,
    title="Our artificial shift: 10 voxels along X",
)

plt.show()
