# FastLanes Compression Demo

This repo demonstrates how to use the [FastLanes](https://github.com/cwida/fastlanes) Python bindings to compress and decode directories of CSV files, measure compression ratios, and manage the workflow using a Makefile and virtual environment.

### Run the Pipeline

To run the full pipeline on both datasets:

```bash
make run
````

This will:

* Create a virtual environment in `venv/`
* Install FastLanes Python bindings
* Run `main.py` on `kv_cache_original` and `data_diff`
* Generate `decoded.csv` for each dataset
* Report compression ratios