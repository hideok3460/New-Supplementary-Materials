# New-Supplementary-Materials

Supplementary evidence and saved-record audit for **Applied Sciences manuscript
applsci-4605095**, *Exact Logical-Channel Equivalence and Code-Space-Leakage-Aware
Tomography of a Five-Qubit Encoded-Qubit Transfer Circuit*.

Repository owner/citation entity: **hideok3460**. Original research attribution
is retained in the supplied documents and hardware archive. This folder was
prepared locally for repository publication; preparation itself does not
create a GitHub repository, publish a release, or establish publication rights.
See [the Japanese publishing guide](PUBLISH_GUIDE_JA.md).

## Contents and downloads

| Material | Location |
|---|---|
| Supplementary Derivations (PDF) | [supplement/Supplementary_Derivations.pdf](supplement/Supplementary_Derivations.pdf) |
| Supplementary Run02 Tables (PDF) | [supplement/Supplementary_Run02_Tables.pdf](supplement/Supplementary_Run02_Tables.pdf) |
| Editable supplement sources and table rows | [supplement/](supplement/) and [supplement/tables/](supplement/tables/) |
| Preserved complete hardware package | [supplement/ibm_phoenix_run02_reproducible.zip](supplement/ibm_phoenix_run02_reproducible.zip) — use **Download raw file** when GitHub cannot preview a ZIP |
| Manuscript audit and table-generation script | [audit/recheck_saved_results.py](audit/recheck_saved_results.py) |
| Original audit instructions and records | [audit/README.md](audit/README.md), [audit/data_audit.json](audit/data_audit.json), [audit/VALIDATION_JA.md](audit/VALIDATION_JA.md) |
| Read-only package/count verifier | [verify_repository.py](verify_repository.py) |
| Citation metadata | [CITATION.cff](CITATION.cff) |
| Publication rights review | [LICENSE_NOTICE.md](LICENSE_NOTICE.md) |

The outer `audit.zip` and `supplement.zip` supplied by the author are unpacked
into adjacent `audit/` and `supplement/` directories. **All 37 original files
are preserved byte-for-byte**, including the nested hardware ZIP. The original
outer ZIPs need not also be committed. Original revision-build records remain
historical records; they are not claims that this packaging step repeated
those builds. No manuscript PDF, author responses, or publisher-owned
conference paper was added to this repository.

## Saved acquisition, not a new experiment

- Run ID: `full_4resources_run02`; saved backend: `ibm_phoenix`.
- 1,746 raw count records at 4,096 shots each: **7,151,616 shots**.
- Six recorded IBM job identifiers are chunks of one acquisition, not six
  independent repeat experiments.
- Completed network results: 48 state rows (16 derived by frame tracking),
  32 CP-TNI fits, and 32 GOF summaries. Each baseline has 1/1/1 rows.
- The package preserves 500-resample files and numerical recovery audits.

The hardware ZIP contains two top-level English notebooks:
`ibm_phoenix_calculations.ipynb` and `analyze-phase-concurrence-cptni-gof.ipynb`.
They are **inside the ZIP**, not absent from the repository. Download and
extract a working copy to read them. The archive also contains older executed
notebook records and retained numerical metadata.

## Two different checksums

The checksum of the whole hardware ZIP is:

```text
d9a3ec3a5ef620e13216f9e4719508ea5148e4633ec26868e1f83cd1c382baab
```

The manuscript's checksum applies to the **normalized receiver_counts.json**,
not the ZIP. Its path inside the hardware package is
`Results/02_hardware/full_4resources_run02/receiver_counts.json`:

```text
99ce131823c6bc7b1cf50599adc079fbcf708cc7f46f44b07b7c88b6c646b188
```

[ORIGINAL_FILES_SHA256.json](ORIGINAL_FILES_SHA256.json) records all 37 supplied
files. The hardware ZIP's own `PACKAGE_FILE_SHA256.txt` records 3,373 entries.
These manifests are distinct and should not be silently regenerated after
editing historical evidence.

## Quick offline integrity check

From this repository directory, using Python 3:

```sh
python verify_repository.py
```

This requires only Python's standard library. It verifies original file bytes,
the nested ZIP CRC/manifest, the normalized counts, individual raw records,
shot totals, and saved job attribution. It makes no network connection,
submits no quantum job, fits no numerical estimator, and writes no files.
Expected final line includes `PUBLICATION_FILES_VERIFIED_OFFLINE`.

This is an internal saved-record check, **not fresh IBM-side authentication**,
a privacy certification, a statistical coverage study, or new hardware data.

## Recheck manuscript metrics and regenerate table rows

1. Preserve this publication folder. Extract a separate working copy of
   `supplement/ibm_phoenix_run02_reproducible.zip` **outside this Git repository**.
2. The directory passed as `--hardware-root` must directly contain
   `PACKAGE_FILE_SHA256.txt`, `quantum_core.py`, and `Results/`.
3. Install the small audit environment using your chosen Python environment:

```sh
python -m pip install -r audit/requirements-audit.txt
```

4. Run the preserved audit script, giving a separate output directory:

```sh
python audit/recheck_saved_results.py \
  --hardware-root /path/to/working/ibm_phoenix_run02_reproducible \
  --output-root /path/to/new_audit_recheck
```

Use quoted paths on Windows; put the command on one line there. Do not write
outputs inside the extracted original hardware archive or overwrite `audit/`.
The outputs include audit JSON/CSV and `manuscript/tables/` and
`supplement/tables/` TeX rows in the separate output directory. The original
script retains its historical `input_archive = applsci-fixed4.zip` label; it
does not require that outer manuscript ZIP for this saved-record audit.

The audit rechecks state/channel metrics, intervals and GOF summaries from
preserved records; it does **not** repeat all 500 optimization refits. New
values are not substituted into the preserved tables automatically.

## Notebook safety and full reproduction

In a separate working copy, keep `ACQUISITION_MODE = "reuse"` in the acquisition
notebook. Do not enable `live` for simple review. No IBM authentication is
needed for saved-record verification.

**Important supplied-code detail:** the analysis notebook currently contains
`ALLOW_NUMERICAL_REPAIR = True`. It normally validates and reuses the complete
saved repair; if validation fails, it can attempt a costly numerical repair.
For a strictly read-only review, use `verify_repository.py` and the audit
command above instead of executing that repair path. Do not disable integrity
checks or edit hashed original files merely to make a notebook continue.

Full optimization reruns require the original archive's documented packages
and numerical environment. Such reruns are different from an offline audit.
Count-only intervals do not include all SPAM, drift and calibration
uncertainties. Read the supplement and numerical audit for limitations.

## Version and citation

Use a named release/tag such as `v1.0.0` for the exact manuscript snapshot,
and identify the actual release/tag or commit in the article after it exists.
[RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md) is a proposed description,
not a statement that publication has already occurred. Add a real release
date or DOI only after it exists.

Suggested repository citation:

> hideok3460. New-Supplementary-Materials. GitHub, 2026.
> https://github.com/hideok3460/New-Supplementary-Materials
> (accessed on the actual date of access).

[MANUSCRIPT_TEXT_AFTER_PUBLICATION.tex](MANUSCRIPT_TEXT_AFTER_PUBLICATION.tex)
contains conditional manuscript replacements to use only after anonymous
public access is verified. It does not alter the manuscript automatically.

## Rights and security

No license was chosen on behalf of the authors. Confirm data-sharing and
reuse rights, author approvals, and an appropriate code/data/document license.
Review original job identifiers and local-user paths in historical logs.
Do not commit API keys, account files, `.venv`, `.qiskit`, or private emails.
See [LICENSE_NOTICE.md](LICENSE_NOTICE.md). Public visibility alone does not
make every item freely reusable.
