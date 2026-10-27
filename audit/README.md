# Independent recheck of the preserved run02 results

The reported audit reruns the released tomography functions on raw counts and independently compares their outputs to saved matrices/CSV values. It rechecks metrics, table/interval arithmetic, 500-sample array lengths, and GOF p-values. It does **not** repeat CVXPY/SCS optimization for all bootstrap fits, authenticate IBM records remotely, or establish statistical coverage. No synthetic validation output is counted as hardware evidence.

1. Extract `../supplement/ibm_phoenix_run02_reproducible.zip` into a separate working directory. Keep that extracted archive unchanged.
2. Use Python with NumPy, pandas and SciPy installed. The scientific archive includes its own environment records and requirements for full numerical reproduction.
3. Run from this directory, for example:

```sh
python recheck_saved_results.py --hardware-root /path/to/ibm_phoenix_run02_reproducible --output-root /path/to/new_audit_recheck
```

Use quoted paths on Windows. The hardware-root directory must directly contain `PACKAGE_FILE_SHA256.txt`, `quantum_core.py`, and `Results/`. The audit makes no SDK connection. Output consists of `audit/data_audit.json`, CSV extracts and generated row-only TeX tables in a **separate** output folder. Do not modify the preserved archive to satisfy an assertion.

The main article and supplement use the saved table values rounded for display, not replacements obtained by refitting. All 3373 manifest entries, 1746 count records, 50 reported state rows, 34 channel rows and 34 GOF rows were checked. The source archive hash is recorded in `BUILD_VALIDATION.json`.

Full numeric solver re-execution, additional hardware experiments, repeated-session variability and a confidence-interval coverage study were not performed in the manuscript revision environment.
