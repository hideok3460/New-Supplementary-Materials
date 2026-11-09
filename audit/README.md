# Audit records aligned to the 9 November 2026 manuscript

Current article: **Ideal Fixed-Code Channel Equivalence and Single-Session Hardware Diagnostics of a Five-Qubit Coherent State-Transfer Circuit** (applsci-4605095).
The authoritative submission is `applsci-4605095frevised.zip`; its main source is
`manuscript/template3revised.tex` and its author PDF is
`manuscript/Manuscriptrevised2.pdf` (**17 pages**).
Those manuscript files and the reviewer letters are not published in this
supplementary-data repository. They are referenced only to identify the supplied
build records. See [the manuscript map](../MANUSCRIPT_ALIGNMENT.md).

## Current versus historical build evidence

- [BUILD_VALIDATION.json](BUILD_VALIDATION.json) and [current_build_logs/](current_build_logs/)
  are copied from the target submission. They are **not** a new compile performed
  during this repository update. They report successful builds and resolved
  references, but **one 4.98134 pt Overfull hbox** in the main manuscript (source
  lines 209--210). Do not relabel this as a warning-free build.
- [locations.json](locations.json) contains supplied 17-page `.aux` locators.
- [VALIDATION_JA.md](VALIDATION_JA.md) is the supplied revision-validation note.
- [previous_build_logs/](previous_build_logs/) preserves the older logs and audit
  with 15-page counts. They are historical, not current build evidence.
- [input_archives.json](input_archives.json) retains the upstream filenames and
  hashes recorded by the author package. Additional outer-source identity is in
  [FREVISED_ALIGNMENT.json](../FREVISED_ALIGNMENT.json). Earlier upstream ZIPs
  were not independently obtained/revalidated during this alignment.

The editorial reviewer-action logs, full old manuscript TeX, manuscript diffs
and reviewer replies are intentionally left in the private submission package;
they are not necessary for checking the saved quantum data.

## Numeric evidence is unchanged

`data_audit.json`, the state/calibration CSVs, `recheck_saved_results.py`,
`requirements-audit.txt`, and the 17 supplementary table-row files are unchanged
from both uploaded inputs. The hardware archive is also byte-identical.
The 50 state/34 channel/34 GOF checks recorded in the saved audit are not a new
QPU acquisition or a repeat of every optimizer fit.

For read-only integrity checking, run `python ../verify_repository.py`.
For the existing metric/table audit:

1. Extract `../supplement/ibm_phoenix_run02_reproducible.zip` into a separate work folder.
2. Install the packages in `requirements-audit.txt` in your chosen Python environment.
3. Run, using quoted actual paths (one line on Windows):

```text
python recheck_saved_results.py --hardware-root "/path/to/ibm_phoenix_run02_reproducible" --output-root "/path/to/new_audit_recheck"
```

The hardware-root folder must directly contain `PACKAGE_FILE_SHA256.txt`,
`quantum_core.py`, and `Results/`. Use a new output directory outside the
preserved repository and hardware archive. Do not run this into the published
`audit/` directory. Generated table rows can be compared against the published
rows, but should not automatically replace them.

No IBM credentials are needed for these saved-record checks. Full numerical
refits use the archived software/environment and are a different operation.
