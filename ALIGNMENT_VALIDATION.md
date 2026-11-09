# Validation of the local frevised repository alignment

This is a repository/documentation alignment, not a new experiment or refit.
The source manuscript was inspected, not edited or recompiled in this step.

## Checks completed

- Both uploaded outer ZIPs were safely enumerated and extracted for comparison.
- All 101 entries in the target submission's PACKAGE_SHA256SUMS.txt matched.
- The 17-page author PDF and the two supplemental first pages were inspected;
  their title is the frevised title and the supplemental date is 9 November 2026.
- The main article's supplied build audit records one 4.98134 pt Overfull box.
  It was retained, not hidden or presented as repaired.
- Forty selected public source files are byte-identical to their target-submission
  counterparts. Source sizes and SHA-256 values are recorded separately.
- The two outer inputs contain the same hardware ZIP and all 17 supplementary
  table-row files. The original numerical audit/script/CSV values are unchanged.

## Verification scope

`verify_repository.py` is read-only and uses Python's standard library. It verifies
source files, titles/README links, current/historical log placement, the nested
hardware manifest and CRC, and saved-count/job consistency. It does not import
Qiskit, query IBM, run an optimizer, compile LaTeX or write results.

The public update omits the main manuscript, reviewer correspondence, permission
records and full-source editorial diffs. The selected audit logs retain upstream
paths and source names as provenance. This is not a privacy/rights certification.

Live GitHub contents were unavailable in this environment; the uploaded GitHub
snapshot was used. Fetch/review remote changes before applying the local update.
No GitHub files, commits, branches, tags or releases were created remotely.

## Executed checks in this preparation environment

- `verify_repository.py` completed successfully: 40 exact selected source files,
  current title/link/layout checks, 3373 nested hashes and ZIP CRC, 1746 raw counts,
  7,151,616 shots and six distinct stored job IDs with matching attribution.
- Twelve automated tests passed using the delivered verifier/checker code:
  original snapshot preflight (read-only), completed folder verification (read-only),
  copying the payload and removing only the three historical root logs, post-update
  rechecking, Windows-style CRLF-only recognition, rejection of unexplained local
  edits, hardware ZIP mismatch detection, stale-log detection, missing supplement
  detection, broken README-link detection, unchanged numerical tables/code/data,
  and unsafe-path rejection.
- The simulated update retained a `.git` sentinel and an unrelated local file;
  it did not operate on a real GitHub clone or send a remote request.
- Tests used a Linux Python process and a path containing spaces and Japanese text.
  A real Windows Explorer/GitHub Desktop UI session was not executed here.

No file-size/line-count result should be taken as scientific validation of the
inference, statistical interval coverage or independent hardware provenance.
All numerical audit results remain the author-provided saved results.
