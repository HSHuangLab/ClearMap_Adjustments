import numpy as np

def mae (array1,array2):
    return np.mean(np.abs(array1.astype(float)-array2.astype(float)))

def mse (array1,array2):
    return np.mean((array1.astype(float)-array2.astype(float))**2)


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

        mse_fixed_moving = mse(fixed, moving)
        mse_fixed_aligned = mse(fixed, aligned)

        ncc_fixed_moving=ncc(fixed,moving)
        ncc_fixed_aligned=ncc(fixed,aligned)

        return {
    "mae_before": mae_fixed_moving,
    "mae_after": mae_fixed_aligned,
    "mse_before": mse_fixed_moving,
    "mse_after": mse_fixed_aligned,
    "ncc_before": ncc_fixed_moving,
    "ncc_after": ncc_fixed_aligned
}
