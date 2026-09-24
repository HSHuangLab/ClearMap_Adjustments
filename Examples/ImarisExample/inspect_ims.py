import h5py as h5
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from Examples.example_utils import plot_slice
from Examples.ImarisExample.ims_utils import load_ims


def read_text(attribute):
    text = b"".join(attribute).decode()
    return text


ims_path= Path(__file__).resolve().parent/"data"/"FINAL_L1-L10.ims"

volume= load_ims(ims_path,4)

plot_slice(volume,40)
plt.show()
