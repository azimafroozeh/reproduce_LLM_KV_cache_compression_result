import pyfastlanes
import os

# Static list of datasets to process
DATASETS = ["kv_cache_original", "diff_data"]


def size_of_file(path):
    return os.path.getsize(path) if os.path.exists(path) else 0


def process_dataset(csv_dir):
    fls_file = "data.fls"
    decoded_csv_path = os.path.join(csv_dir, "decoded.csv")

    print(f"-- FastLanes version: {pyfastlanes.get_version()}")
    print(f"-- Processing dataset in: '{csv_dir}'")

    # Check input files exist
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
    if not csv_files:
        print(f"-- Error: No CSV files found in '{csv_dir}'")
        return

    # Clean up any previous output
    for path in [fls_file, decoded_csv_path]:
        if os.path.exists(path):
            os.remove(path)

    # Encode and decode
    conn = pyfastlanes.connect()
    conn.inline_footer().read_csv(csv_dir).to_fls(fls_file)
    reader = conn.read_fls(fls_file)
    reader.to_csv(decoded_csv_path)

    # Compression statistics (static uncompressed size)
    compressed_size = size_of_file(fls_file)
    if compressed_size > 0:
        uncompressed_size = 1024 * 1024  # Static 1 MiB
        ratio = uncompressed_size / compressed_size
        compressed_kb = compressed_size / 1024
        print(f"-- Compression ratio: (1 MiB / {compressed_kb:.2f} KB) = {ratio:.2f}x")
    else:
        print("-- Error: Compressed file not found or size is 0")


def main():
    for dataset in DATASETS:
        process_dataset(dataset)


if __name__ == "__main__":
    main()
