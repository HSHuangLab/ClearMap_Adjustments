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

def evaluate_alignment(fixed, moving, aligned):

    if fixed.shape != aligned.shape:
        raise ValueError(
            f"Fixed and aligned volumes have different shapes: "
            f"{fixed.shape} vs {aligned.shape}"
        )

    results = {
        "mae_before": None,
        "mse_before": None,
        "ncc_before": None,
        "mae_after": mae(fixed, aligned),
        "mse_after": mse(fixed, aligned),
        "ncc_after": ncc(fixed, aligned),
    }

    if fixed.shape == moving.shape:
        results["mae_before"] = mae(fixed, moving)
        results["mse_before"] = mse(fixed, moving)
        results["ncc_before"] = ncc(fixed, moving)

    return results