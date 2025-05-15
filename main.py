import pyfastlanes
import os
import pandas as pd
import numpy as np

# Static list of datasets to process
DATASETS = ["kv_cache_original", "diff_data"]


def size_of_file(path):
    return os.path.getsize(path) if os.path.exists(path) else 0


def validate_csvs(csv_dir):
    """
    Compares data.csv vs decoded.csv in csv_dir, treating both as float32
    and allowing tiny rounding differences.
    """
    orig_path = os.path.join(csv_dir, "data.csv")
    dec_path = os.path.join(csv_dir, "decoded.csv")

    if not os.path.exists(orig_path) or not os.path.exists(dec_path):
        print(f"-- Validation skipped: missing data.csv or decoded.csv in '{csv_dir}'")
        return False

    # Load both as float32
    orig = pd.read_csv(orig_path, dtype="float32")
    dec = pd.read_csv(dec_path, dtype="float32")

    # Check shape
    if orig.shape != dec.shape:
        print(f"-- Validation FAILED: shape mismatch "
              f"(data.csv {orig.shape}, decoded.csv {dec.shape})")
        return False

    # Check content with tolerance
    # (rtol/atol can be adjusted if needed)
    mask = ~np.isclose(orig.values, dec.values, rtol=1e-05, atol=1e-08)
    if mask.any():
        # first mismatch
        i, j = np.argwhere(mask)[0]
        col = orig.columns[j]
        print(f"-- Validation FAILED at row {i}, column '{col}': "
              f"{orig.iat[i, j]!r} != {dec.iat[i, j]!r}")
        return False

    print("-- Validation PASSED: data.csv matches decoded.csv within float32 tolerances.")
    return True


def process_dataset(csv_dir):
    fls_file = os.path.join(csv_dir, "data.fls")
    decoded_csv = os.path.join(csv_dir, "decoded.csv")

    print(f"-- FastLanes version: {pyfastlanes.get_version()}")
    print(f"-- Processing dataset in: '{csv_dir}'")

    # Ensure data.csv exists
    data_csv = os.path.join(csv_dir, "data.csv")
    if not os.path.exists(data_csv):
        print(f"-- Error: 'data.csv' not found in '{csv_dir}'")
        return

    # Clean up old outputs
    for f in (fls_file, decoded_csv):
        if os.path.exists(f):
            os.remove(f)

    # Encode & decode
    conn = pyfastlanes.connect()
    conn.inline_footer().read_csv(csv_dir).to_fls(fls_file)
    conn.read_fls(fls_file).to_csv(decoded_csv)

    # Compression stats
    comp_size = size_of_file(fls_file)
    if comp_size > 0:
        uncomp = 1024 * 1024  # 1 MiB
        ratio = uncomp / comp_size
        print(f"-- Compression ratio: (1 MiB / {comp_size / 1024:.2f} KB) = {ratio:.2f}x")
    else:
        print("-- Error: compressed file missing or zero size")

    # Validation (float32-aware)
    validate_csvs(csv_dir)


def main():
    for ds in DATASETS:
        process_dataset(ds)


if __name__ == "__main__":
    main()
