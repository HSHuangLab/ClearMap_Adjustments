import h5py as h5
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from Examples.example_utils import plot_slice
from ImarisRegistrationTool.ims_utils import load_ims


def read_text(attribute):
    text = b"".join(attribute).decode()
    return text


ims_path= Path(__file__).resolve().parent/"data"/"FINAL_L1-L10.ims"

volume, metadata = load_ims(ims_path,4)

physical_size_um = metadata["physical_size_um"]
physical_size_mm = tuple(
    size / 1000 for size in physical_size_um
)

plot_slice(volume, 40, physical_size_mm)
plt.show()
