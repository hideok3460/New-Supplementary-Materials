# New-Supplementary-Materials

Supplementary evidence and saved-record audit for **Applied Sciences manuscript applsci-4605095**.
This repository revision is aligned to the author-supplied **17-page manuscript** in
`applsci-4605095frevised.zip`, revised **9 November 2026**:

> **Ideal Fixed-Code Channel Equivalence and Single-Session Hardware Diagnostics of a Five-Qubit Coherent State-Transfer Circuit**

Authors: Ami Ukai, Syunsuke Fujiwara, Takahiko Mori, and Hideaki Okazaki.
Repository citation entity: **hideok3460**. This is a manuscript-linked dataset,
not a declaration that the article has been accepted or published.

## Start here

| Material | Repository location |
|---|---|
| Supplementary Derivations (2 pages) | [PDF](supplement/Supplementary_Derivations.pdf), [LaTeX](supplement/Supplementary_Derivations.tex) |
| Supplementary Run02 Tables (11 pages) | [PDF](supplement/Supplementary_Run02_Tables.pdf), [LaTeX](supplement/Supplementary_Run02_Tables.tex), [table rows](supplement/tables/) |
| Complete, preserved experimental archive | [ibm_phoenix_run02_reproducible.zip](supplement/ibm_phoenix_run02_reproducible.zip) |
| Metric audit and table-generation script | [audit/recheck_saved_results.py](audit/recheck_saved_results.py), [instructions](audit/README.md) |
| Current supplied manuscript build/locator records | [BUILD_VALIDATION.json](audit/BUILD_VALIDATION.json), [current logs](audit/current_build_logs/), [locations.json](audit/locations.json) |
| Previous-round build records, not current evidence | [audit/previous_build_logs/](audit/previous_build_logs/) |
| Source alignment and verification | [FREVISED_ALIGNMENT.json](FREVISED_ALIGNMENT.json), [SOURCE_FILES_SHA256.json](SOURCE_FILES_SHA256.json), [verify_repository.py](verify_repository.py) |
| Update procedure and changes | [UPDATE_TO_FREVISED_JA.md](UPDATE_TO_FREVISED_JA.md), [alignment report](ALIGNMENT_REPORT_JA.md) |
| Citation and rights | [CITATION.cff](CITATION.cff), [LICENSE_NOTICE.md](LICENSE_NOTICE.md) |

The article and reviewer letters are **not** republished here. Paths beginning
`manuscript/` or `responses/` in preserved audit metadata refer to the submission
ZIP, not to missing public files. [MANUSCRIPT_ALIGNMENT.md](MANUSCRIPT_ALIGNMENT.md)
maps the current manuscript to the public evidence.

## What changed, and what did not

The two supplements now use the target article's exact title and 9 November 2026
revision date. Their table-row files and the hardware ZIP are unchanged. The
supplied build audit is for the **17-page** paper, not the earlier 15-page paper;
old build logs are explicitly historical. The new main-paper baseline figure
is Figure 5, the channel figure is Figure 6, the decision table is Table 7,
and the methods comparison is Table 8, according to the supplied locators.

**Important build limitation:** the supplied current log records **one 4.98134 pt
Overfull hbox** in the main manuscript. This repository update does not fix it,
does not rebuild the manuscript, and does not claim a warning-free new build.
The supplied supplemental logs record zero Overfull boxes. The local build PDF
and the author-supplied PDF are separately identified in the audit.

No new QPU job, numerical refit, remote IBM authentication, cross-backend test,
or independent repeated experiment is added by this repository alignment.
The historical numerical archive and saved-record audit keep their original
names, titles, timestamps, signatures and hashes. Those old labels are historical
provenance, not the current title or evidence of a second dataset.

## Preserved run02 evidence

- `full_4resources_run02`, recorded backend `ibm_phoenix`.
- **1746 circuits × 4096 shots = 7,151,616 shots**.
- Six stored IBM job IDs are chunks of **one acquisition**, not six independent repetitions.
- Network: 48 state rows (16 derived by software frame tracking), 32 CP-TNI fits,
  32 GOF summaries. Each of the two references contributes 1/1/1 rows.
- The same saved 500-resample arrays, baseline numerical-recovery audit,
  calibration records, and compiled circuit metadata remain available.

The current article treats these data as single-session diagnostics. It does not
claim exact noisy-device equivalence or a fidelity advantage over the direct
preparation and SWAP references. Counting intervals are not guarantees of
coverage, SPAM removal, or repeated-session uncertainty.

The two English notebooks `ibm_phoenix_calculations.ipynb` and
`analyze-phase-concurrence-cptni-gof.ipynb` are **inside the preserved hardware ZIP**.
Download it and extract a separate working copy to inspect them. The acquisition
notebook should remain in saved-record `reuse` mode for review. The analysis
notebook may permit numerical recovery if verification fails; do not confuse
executing that option with the read-only checks below.

## Two different SHA-256 values

Whole hardware ZIP:

```text
d9a3ec3a5ef620e13216f9e4719508ea5148e4633ec26868e1f83cd1c382baab
```

Normalized `Results/02_hardware/full_4resources_run02/receiver_counts.json` inside it:

```text
99ce131823c6bc7b1cf50599adc079fbcf708cc7f46f44b07b7c88b6c646b188
```

The latter, not the ZIP hash, is the value cited in the manuscript.
The inner `PACKAGE_FILE_SHA256.txt` covers 3373 entries. Do not rename files or
rewrite historical JSON inside that ZIP merely to replace an old article title.

## Read-only verification

From this repository root, using Python 3.9 or newer:

```text
python verify_repository.py
```

Only the Python standard library is used. It checks the selected byte-exact
submission artifacts, current-title metadata, obsolete-root-log absence,
internal README links, hardware CRC/3373 hashes, raw/normalized count agreement,
shots and job attribution. It makes no network call, writes no file and fits no
numerical model. The expected final line is:

```text
FREVISED_REPOSITORY_ALIGNMENT_VERIFIED_OFFLINE
```

This verifies stored file consistency, not license compliance, remote provenance,
statistical coverage or acceptance of the article. See [ALIGNMENT_VALIDATION.md](ALIGNMENT_VALIDATION.md).

## Saved-result metric audit

Extract the hardware ZIP to a **separate working folder outside this repository**.
Install `audit/requirements-audit.txt` in a chosen Python environment, then run:

```text
python audit/recheck_saved_results.py --hardware-root "/path/to/ibm_phoenix_run02_reproducible" --output-root "/path/to/new_audit_recheck"
```

`--hardware-root` must directly contain `PACKAGE_FILE_SHA256.txt`, `quantum_core.py`
and `Results/`. Use a new output folder. The preserved script rechecks states,
channel metrics, percentile arithmetic and GOF p-values from saved results;
it does **not** redo all 500 constrained optimizations. Its historic
`input_archive = applsci-fixed4.zip` string records the original audit input and
is not a required path for the current command. Do not edit it as an apparent
compatibility fix.

## Version and citation

Repository: https://github.com/hideok3460/New-Supplementary-Materials

Suggested citation: hideok3460. *New-Supplementary-Materials*. GitHub, 2026.
Record the actual access date and the actual release tag/commit used.
[RELEASE_NOTES_frevised.md](RELEASE_NOTES_frevised.md) proposes a new snapshot
(e.g. `applsci-4605095-frevised-20261109`); it does not assert that the tag exists.
Do not silently replace a previously cited release. No DOI, publication date,
license grant or journal acceptance is created by this update.

## Rights and privacy

[LICENSE_NOTICE.md](LICENSE_NOTICE.md) is a review notice, not a license grant.
Do not add credentials, `.qiskit`, `.venv`, editorial correspondence, permission
billing details or the full submitted manuscript without separate review.
Historical data/logs retain job IDs and some local paths. Review their disclosure
before publishing; `.gitignore` cannot inspect the contents of a nested ZIP.
