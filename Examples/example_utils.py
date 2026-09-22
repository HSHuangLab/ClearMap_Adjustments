from pathlib import Path

import numpy as np
import tifffile
import matplotlib.pyplot as plt

# Reference: load one image (slice 20)
# project = Path(__file__).resolve().parent.parent
# image_path = (
#     project / "ClearMap" / "Test" / "Data" / "Synthetic"
#     / "test_iDISCO_020.tif"
# )
# image = tifffile.imread(image_path)

def load_synthetic_stack():
    """Load the example TIFF slices into an array ordered as Z, Y, X."""
    project_folder = Path(__file__).resolve().parent.parent

    data_folder = (
        project_folder / "ClearMap" / "Test" / "Data" / "Synthetic"
    )

    slice_files = sorted(data_folder.glob("test_iDISCO_*.tif"))

    if not slice_files:
        raise FileNotFoundError(f"No example TIFF slices found in {data_folder}")

    slices = [tifffile.imread(file) for file in slice_files]
    stack = np.stack(slices, axis=0)

    return stack

def plot_slice(volume, z):
    fig, ax = plt.subplots()
    ax.imshow(volume[z], cmap="gray")
    ax.set_title(f"Slice at Z index {z}")
    return fig

def plot_volume_3d(volume, percentile=99.5, comparison=None,
                   title="Bright voxels in 3D"):
    """Plot bright voxels, optionally overlaying a second volume."""
    # Select bright voxels
    threshold = np.percentile(volume, percentile)
    z, y, x = np.where(volume > threshold)

    # Create a 3D plotting area
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(x, y, z, color="blue", s=3, alpha=0.3,
               label="Original positions")

    if comparison is not None:
        # Use the original volume's threshold for both images.
        zc, yc, xc = np.where(comparison > threshold)
        ax.scatter(xc, yc, zc, color="orange", s=3, alpha=0.3,
                   label="Comparison positions")
        ax.legend()

    ax.set_xlim(0, volume.shape[2])
    ax.set_ylim(0, volume.shape[1])
    ax.set_zlim(0, volume.shape[0])
    ax.set_box_aspect(
        (volume.shape[2], volume.shape[1], volume.shape[0])
    )

    ax.set_xlabel("X (voxels)")
    ax.set_ylabel("Y (voxels)")
    ax.set_zlabel("Z (voxels)")
    ax.set_title(title)

    return fig


def plot_alignment(fixed, moving, aligned, z=19, percentile=99.5):
    """Compare equal-shaped Z,Y,X volumes in 2D and 3D.

    All panels use the fixed volume's intensity scale or brightness cutoff.
    Returns two figures; call plt.show() in the example script to display them.
    Red identifies aligned voxels, not a score of alignment accuracy.
    """
    if fixed.ndim != 3 or moving.shape != fixed.shape or aligned.shape != fixed.shape:
        raise ValueError("Expected three 3D volumes with the same Z,Y,X shape.")
    if not 0 <= z < fixed.shape[0]:
        raise ValueError(f"z must be between 0 and {fixed.shape[0] - 1}.")

    # Compare the same slice using one brightness scale.
    fig2d, axes = plt.subplots(1, 3, figsize=(14, 5))
    volumes = (fixed, moving, aligned)
    titles = ("Fixed — reference", "Moving — before alignment", "Moving — after alignment")
    for ax, volume, title in zip(axes, volumes, titles):
        ax.imshow(volume[z], cmap="gray", vmin=fixed.min(), vmax=fixed.max())
        ax.set_title(title)
        ax.set_xlabel("X (voxels)")
        ax.set_ylabel("Y (voxels)")
    fig2d.tight_layout()

    # Extract bright voxel positions once from each actual volume.
    threshold = np.percentile(fixed, percentile)
    coordinates = [np.where(volume > threshold) for volume in volumes]
    colors = ("blue", "yellow", "red")
    labels = ("Fixed (reference)", "Moving (before alignment)", "Aligned")

    fig3d = plt.figure(figsize=(14, 6))
    before = fig3d.add_subplot(121, projection="3d")
    after = fig3d.add_subplot(122, projection="3d")

    # Preserve the original comparison: two clouds before, all three after.
    for ax, indices, title in (
        (before, (0, 1), "Before alignment"),
        (after, (0, 1, 2), "After alignment"),
    ):
        for index in indices:
            zs, ys, xs = coordinates[index]
            ax.scatter(xs, ys, zs, color=colors[index], s=3, alpha=0.3,
                       label=labels[index])

        ax.set_xlim(0, fixed.shape[2])
        ax.set_ylim(0, fixed.shape[1])
        ax.set_zlim(0, fixed.shape[0])
        ax.set_box_aspect((fixed.shape[2], fixed.shape[1], fixed.shape[0]))
        ax.set_xlabel("X (voxels)")
        ax.set_ylabel("Y (voxels)")
        ax.set_zlabel("Z (voxels)")
        ax.set_title(title)
        ax.view_init(elev=25, azim=-60)
        ax.legend(loc="upper left", markerscale=4)

    fig3d.tight_layout()
    return fig2d, fig3d

def mae (array1,array2):
    return np.mean(np.abs(array1-array2))

def ncc (array1,array2):
    array1_centered = array1 - np.mean(array1)
    array2_centered = array2 - np.mean(array2)

    numerator = np.sum(array1_centered * array2_centered)

    denominator = np.sqrt(
        np.sum(array1_centered ** 2) *
        np.sum(array2_centered ** 2)
    )

    return numerator / denominator

def evaluate_alignment (fixed,moving,aligned):
        mae_fixed_moving=mae(fixed,moving)
        mae_fixed_aligned=mae(fixed,aligned)

        ncc_fixed_moving=ncc(fixed,moving)
        ncc_fixed_aligned=ncc(fixed,aligned)

        return {
    "mae_before": mae_fixed_moving,
    "mae_after": mae_fixed_aligned,
    "ncc_before": ncc_fixed_moving,
    "ncc_after": ncc_fixed_aligned
}


