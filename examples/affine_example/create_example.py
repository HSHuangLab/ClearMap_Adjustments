
from examples.example_utils import load_synthetic_stack
from scipy.ndimage import affine_transform
from examples.example_utils import plot_volume_3d
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tifffile

fixed= load_synthetic_stack()

#Rotating
center =(np.array(fixed.shape)-1)/2
angle_degrees= 12
angle_rad= np.deg2rad(angle_degrees)
cos=np.cos(angle_rad)
sin=np.sin(angle_rad)

#rotating angle_degrees around x and y while z is fixed
rotation = np.array([
    [1,  0,  0],
    [0,  cos,  sin],
    [0, -sin,  cos],
])

inverse_rotation = np.linalg.inv(rotation)
offset = center - inverse_rotation @ center

moving = affine_transform(
    fixed,
    matrix=inverse_rotation,
    offset=offset,
    order=0,
    mode="constant",
    cval=0,
)

plot_volume_3d(
    fixed,
    comparison=moving,
    title="Original and rotated volume",
)
plt.show()

#anisotrophic translation

translation = np.array([3, 6, 0])

inverse_rotation = np.linalg.inv(rotation)

offset = center - inverse_rotation @ center
offset = offset - inverse_rotation @ translation

moving = affine_transform(
    fixed,
    matrix=inverse_rotation,
    offset=offset,
    order=0,
    mode="constant",
    cval=0,
)

plot_volume_3d(
    fixed,
    comparison=moving,
    title="Original vs rotation + translation",
)
plt.show()

#shearing
# Coordinates are ordered Z, Y, X.
shear = np.array([
    [1, 0,   0],
    [0, 1,   0],
    [0, 0.1, 1],
])

transform = shear @ rotation
combined_translation = shear @ translation

inverse_transform = np.linalg.inv(transform)
offset = center - inverse_transform @ (center + combined_translation)

moving_sheared = affine_transform(
    fixed,
    matrix=inverse_transform,
    offset=offset,
    order=0,
    mode="constant",
    cval=0,
)

plot_volume_3d(
    fixed,
    comparison=moving_sheared,
    title="Original vs rotation + translation + shear",
)
plt.show()

#saving the example images
output_folder = Path(__file__).resolve().parent / "output"
output_folder.mkdir(exist_ok=True)

tifffile.imwrite(
    output_folder / "fixed.tif",
    fixed,
    photometric="minisblack",
)

tifffile.imwrite(
    output_folder / "moving_affine.tif",
    moving_sheared,
    photometric="minisblack",
)

print("Saved affine example to:", output_folder)


