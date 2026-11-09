#!/usr/bin/env python3
"""Read-only byte/count checks for this packaged manuscript repository.

Uses only Python's standard library. No network, no IBM SDK, no fits and no
writes. Checks the selected exact copies from frevised plus the nested archive manifest.
"""
from __future__ import annotations
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
HARDWARE_REL = 'supplement/ibm_phoenix_run02_reproducible.zip'
PREFIX = 'ibm_phoenix_run02_reproducible/'
COUNTS_REL = 'Results/02_hardware/full_4resources_run02/receiver_counts.json'
EXPECTED_COUNTS_SHA256 = '99ce131823c6bc7b1cf50599adc079fbcf708cc7f46f44b07b7c88b6c646b188'
EXPECTED_ZIP_SHA256 = 'd9a3ec3a5ef620e13216f9e4719508ea5148e4633ec26868e1f83cd1c382baab'

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def digest_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def safe_relative(name: str) -> str:
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and '\\' not in name and ':' not in name,
            'Unsafe manifest path; do not extract or bypass this check.')
    return p.as_posix()

def main() -> None:
    manifest = json.loads((ROOT / 'SOURCE_FILES_SHA256.json').read_text(encoding='utf-8'))
    require(manifest['schema_version'] == 2, 'Unexpected source-file manifest version.')
    originals = manifest['files']
    for entry in originals:
        rel = safe_relative(entry['path'])
        path = ROOT / rel
        require(path.is_file(), 'Missing source file: ' + rel)
        require(path.stat().st_size == entry['bytes'], 'Size mismatch: ' + rel)
        require(digest_file(path) == entry['sha256'], 'SHA-256 mismatch: ' + rel)
    print(f'FREVISED_SOURCE_FILES_VERIFIED: {len(originals)}/{len(originals)}')
    meta = json.loads((ROOT / 'FREVISED_ALIGNMENT.json').read_text(encoding='utf-8'))
    title = meta['article']['title']
    for name in ['README.md', 'CITATION.cff', 'supplement/Supplementary_Derivations.tex',
                 'supplement/Supplementary_Run02_Tables.tex']:
        require(title in (ROOT / name).read_text(encoding='utf-8'), 'Current title absent: ' + name)
    for old in meta['obsolete_root_logs_removed_after_preserving_history']:
        require(not (ROOT / safe_relative(old)).exists(),
                'Obsolete root log still present; follow the move instructions: ' + old)
    import re
    for name in ['README.md', 'audit/README.md', 'MANUSCRIPT_ALIGNMENT.md']:
        page = ROOT / name
        for target in re.findall(r'\]\(([^)]+)\)', page.read_text(encoding='utf-8')):
            if '://' not in target and not target.startswith('#'):
                require((page.parent / target.split('#')[0]).exists(),
                        'Broken local link in ' + name + ': ' + target)
    b = json.loads((ROOT / 'audit/BUILD_VALIDATION.json').read_text(encoding='utf-8'))
    require(b['builds']['template3revised']['compiled_pages'] == 17, 'Not the 17-page build record.')
    require(b['builds']['template3revised']['overfull_hbox_count'] == 1, 'Build-warning record changed.')
    print('CURRENT_TITLE_AND_LINKS_VERIFIED; supplied 17-page build warning retained')

    hardware = ROOT / HARDWARE_REL
    require(digest_file(hardware) == EXPECTED_ZIP_SHA256, 'Hardware ZIP hash mismatch.')
    with zipfile.ZipFile(hardware) as archive:
        names = archive.namelist()
        require(len(set(names)) == len(names), 'Duplicate ZIP entry names.')
        for name in names:
            safe_relative(name)
        require(archive.testzip() is None, 'Hardware ZIP CRC check failed.')
        lines = archive.read(PREFIX + 'PACKAGE_FILE_SHA256.txt').decode('utf-8').splitlines()
        require(len(lines) == 3373, 'Unexpected hardware-manifest count.')
        for line in lines:
            h, rel = line.split('  ', 1)
            rel = safe_relative(rel)
            require(hashlib.sha256(archive.read(PREFIX + rel)).hexdigest() == h,
                    'Inner archive hash mismatch: ' + rel)
        print('HARDWARE_MANIFEST_VERIFIED: 3373/3373; ZIP CRC passed')
        blob = archive.read(PREFIX + COUNTS_REL)
        require(hashlib.sha256(blob).hexdigest() == EXPECTED_COUNTS_SHA256,
                'Normalized receiver-count hash mismatch.')
        saved = json.loads(blob)
        records = saved['records']
        raw = sorted(n for n in names if n.startswith(PREFIX +
                     'Results/02_hardware/full_4resources_run02/raw_counts/')
                     and n.endswith('.json'))
        require(saved['data_kind'] == 'HARDWARE' and saved['backend'] == 'ibm_phoenix',
                'Unexpected saved acquisition labels.')
        require(len(records) == 1746 and len(raw) == 1746, 'Unexpected circuit count.')
        indexed = {int(record['acquisition_index']): record for record in records}
        require(set(indexed) == set(range(1746)), 'Acquisition indices are incomplete or duplicated.')
        shots = 0
        for member in raw:
            record = json.loads(archive.read(member))
            require(record == indexed[int(record['acquisition_index'])],
                    'Raw/normalized record mismatch: ' + member)
            require(record['shots'] == 4096, 'Unexpected shots: ' + member)
            values = list(record['counts'].values())
            require(all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in values),
                    'Invalid count values: ' + member)
            require(sum(values) == 4096, 'Counts do not sum to shots: ' + member)
            shots += sum(values)
        jobs = json.loads(archive.read(PREFIX +
                         'Results/02_hardware/full_4resources_run02/submitted_jobs.json'))
        ids = {job['job_id'] for job in jobs}
        require(len(jobs) == 6 and len(ids) == 6, 'Unexpected saved job count.')
        require({r['hardware_job_id'] for r in records} == ids == set(saved['job_ids']),
                'Job attribution mismatch.')
        require(shots == 7151616, 'Unexpected total shot count.')
        print('SAVED_COUNTS_VERIFIED: 1746 circuits; 7151616 shots; 6 stored job IDs')
    print('NORMALIZED_COUNTS_SHA256:', EXPECTED_COUNTS_SHA256)
    print('FREVISED_REPOSITORY_ALIGNMENT_VERIFIED_OFFLINE')
    print('Scope: saved bytes and count consistency only; no remote IBM authentication,')
    print('new QPU acquisition, numerical refits, or privacy/license certification.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, UnicodeError) as exc:
        print('VERIFICATION_FAILED: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
