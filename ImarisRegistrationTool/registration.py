from pathlib import Path
import subprocess
import tifffile
from datetime import datetime
import numpy as np
import platform,sys

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent[1]

if platform.system() == "Windows":
    ELASTIX_PATH = PROJECT_ROOT / "tools" / "elastix" / "windows" / "elastix.exe"
else:
    ELASTIX_PATH = PROJECT_ROOT / "tools" / "elastix" / "bin" / "elastix"

PARAMETERS_DIR= PROJECT_ROOT/ "ImarisRegistrationTool"/ "Parameters"

PARAMETERS_FILES = {
    "Translation": PARAMETERS_DIR / "translation.txt",
    "Rigid": PARAMETERS_DIR / "rigid.txt",
    "Affine": PARAMETERS_DIR / "affine.txt"
}

def read_transform_parameters(file_path):
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("(TransformParameters"):
                values = line.strip("()\n").split()[1:]
                return np.array(values, dtype=float)

    raise ValueError("TransformParameters not found")


def run_elastix(fixed_vol, moving_vol, parameter_paths, output_parent):
    if not ELASTIX_PATH.is_file():
        raise FileNotFoundError(
            f"Elastix executable not found: {ELASTIX_PATH}"
        )

    if not parameter_paths:
        raise ValueError("At least one parameter file is required.")

    for par_path in parameter_paths:
        if not Path(par_path).is_file():
            raise FileNotFoundError(
                f"Parameter file not found: {par_path}"
            )

    time = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path= Path(output_parent)/f"output{time}"
    output_path.mkdir(parents=True, exist_ok=True)

    fixed_path= output_path/"Fixed.tif"
    moving_path= output_path/"Moving.tif"

    tifffile.imwrite(fixed_path, fixed_vol, photometric="minisblack")
    tifffile.imwrite(moving_path, moving_vol, photometric="minisblack")

    command = [
            str(ELASTIX_PATH),
            "-f", str(fixed_path),
            "-m", str(moving_path),   
        ]

    for par_path in parameter_paths:

        command= command + ["-p", str(par_path)]

    command= command + ["-out", str(output_path)]

    subprocess.run(command, check=True)

    aligned_vol = tifffile.imread(output_path / f"result.{len(parameter_paths)-1}.tif")
    return aligned_vol,output_path


# fixed = tifffile.imread(PROJECT_ROOT/"Examples"/"TranslationExample"/"output"/"fixed.tif")
# moving = tifffile.imread(PROJECT_ROOT/"Examples"/"TranslationExample"/"output"/"moving_shifted.tif")
# parameter_path= PROJECT_ROOT/"Examples"/"TranslationExample"/"translation.txt"
# output_path= PROJECT_ROOT/"Examples"/"TranslationExample"/"output_test_for_app"
# aligned = run_elastix(
#     fixed,
#     moving,
#     [parameter_path],
#     output_path
# )

# print(aligned.shape)