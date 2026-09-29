from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ELASTIX_PATH = PROJECT_ROOT / "tools" / "elastix" / "bin" / "elastix"

def run_elastix(fixed_path, moving_path, parameter_path, output_path):
    if not ELASTIX_PATH.is_file():
        raise FileNotFoundError(
            f"Elastix executable not found: {ELASTIX_PATH}"
        )

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    command = [
        str(ELASTIX_PATH),
        "-f", str(fixed_path),
        "-m", str(moving_path),
        "-p", str(parameter_path),
        "-out", str(output_path)
    ]

    subprocess.run(command, check=True)

