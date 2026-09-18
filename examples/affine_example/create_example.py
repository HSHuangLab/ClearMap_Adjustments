
from examples.example_utils import load_synthetic_stack
from scipy.ndimage import affine_transform
from examples.example_utils import plot_volume_3d

import matplotlib.pyplot as plt
import numpy as np

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

print(rotation)




