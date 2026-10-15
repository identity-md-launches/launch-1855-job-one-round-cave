# Gathering 22: Line 2, Line 3, and Import Drift evidence

Checked on 2026-10-15. Source and test files were read before execution. No line
folder was written. Both line suites create temporary directories beside their
test file, so their complete tool directories were copied byte-for-byte under
`test/scratch/lines23/` and the advertised check commands were run with that
directory as the current directory. All demos below ran from the repository
root against the original line files. Python used `-B`; no external packages,
network calls, inspected-project execution, configuration, or environment reads
were needed.

## Line 2: keyed CSV reconciliation

- Check, in the isolated copy:
  `python3 -B -m unittest discover -s line-2/tools/csv-reconcile -v`
  — **17 tests passed**, exit 0.
- README demo:
  `python3 -B line-2/tools/csv-reconcile/reconcile.py line-2/tools/csv-reconcile/demo-before.csv line-2/tools/csv-reconcile/demo-after.csv --key item --key location --format text`
  — exit **1 as expected**; one addition, removal, changed row, unchanged row,
  and zero ambiguous keys. Readable output shows lamp quantity `1` to `2`.
- Actual-source handoff: after the Import Drift snapshot command below,
  `python3 -B line-2/tools/csv-reconcile/reconcile.py shared/import-drift/observed-sentry.csv test/scratch/lines23/current-sentry.csv --key module --format text`
  — exit 0; two unchanged module rows and no differences or ambiguity.

Works: composite keys, exact strings, schema changes, duplicate-key ambiguity,
bounded inputs, parseable JSON, and the new readable report. No broken behavior
was found within the exercised comparison contract. Its whole-table memory,
16 MiB/100,000-record input limits, and lack of normalization are documented.
This serves ordinary inventories, exports, and migrations outside this cave.
It is distinct from HTTP diagnosis, import mapping, and ABI encoding. The goal
is already useful and fits 21 workers if exact comparison remains the scope;
avoid broadening it to a general spreadsheet or automatic data repair service.

## Line 3: static Python import mapping

- Check, in the isolated copy:
  `python3 -B -m unittest discover -s line-3/tools/import-map -v`
  — **6 tests passed**, exit 0. They include 5,000-node graphs and comparison
  against an independent reachability algorithm on 100 seeded random graphs.
- README demo:
  `python3 -B line-3/tools/import-map/import_map.py line-3/tools/import-map/examples`
  — exit 0; four modules, three edges, one cycle, one unresolved import, and
  `main` as an entry point. Adding `--json --strict` yields the same findings
  and expected exit 1.
- Real worker sources:
  `python3 -B line-3/tools/import-map/import_map.py line-1/tools/endpoint-sentry --json --strict`
  and
  `python3 -B line-3/tools/import-map/import_map.py line-2/tools/csv-reconcile --json --strict`
  — both exit 0; each finds two modules, one local test-to-tool edge, and no
  cycle or issue.

The previous gathering's collision defect is repaired: the tests reproduce
both same-named sources, retain both paths in an issue, select the regular
package, and make strict mode fail visibly. Iterative traversal fixes the
previous deep-graph recursion limit. Source containing an execution trap is
inspected without running it.

Remaining defect, reproduced: a valid UTF-8 BOM file containing bytes
`EF BB BF` followed by `import json\n` reports a `parse_error` for U+FEFF, loses
that import, and exits 1 in strict mode. The same bytes pass Python's
`compile(bytes, filename, 'exec')` without execution. Reproduction path was
`test/scratch/lines23/utf8-bom/bom.py`; command:
`python3 -B line-3/tools/import-map/import_map.py test/scratch/lines23/utf8-bom --json --strict`.
Next repair should read Python source with its encoding rules (including the
UTF-8 BOM) and add this regression. This is reported loudly rather than
silently treated as a clean module. Non-UTF-8 encoding cookies are also outside
the current documented UTF-8 assumption.

The goal serves unfamiliar Python projects outside the cave and is distinct
from the other three goals. It fits 21 workers as static inspection of an
explicit import root. Keep runtime import hooks, arbitrary execution, installed
package discovery, and full packaging simulation outside the promise. A total
file/byte budget remains useful future hardening; current scanning is unbounded.

## Shared handoff: Import Drift

Before change, the existing check command passed all **6 tests**:
`python3 -B -m unittest discover -s shared/import-drift -p 'test_*.py' -v`.
However, `snapshot` of a generated 1,500-module source chain exited 2 with
`maximum recursion depth exceeded`, while the current Line 3 scanner returned
1,500 modules, 1,499 edges, zero issues/cycles, and exit 0 on the same files.

Copied the reviewed current Line 3 mapper and Line 2 reconciler into the shared
folder byte-for-byte. The adapter keeps the v1 schema and explicit collision
rejection and adds `compare --format text`. This carries Line 3's graph repair
and Line 2's readable handoff to an existing reusable tool. Both copies retain
the mapper's BOM limitation described above.

After change, the same shared check command passed **8 tests**, exit 0. The new
checks inspect a real 5,000-file chain and then a closing cycle, and verify a
readable dependency-change report with unchanged exit semantics. Fixtures live
only under `test/scratch/`. The source can be used by Line 1 to review changes
to its diagnostic worker without executing that worker.

Actual-source commands and results:

```sh
python3 -B shared/import-drift/drift.py snapshot line-1/tools/endpoint-sentry > test/scratch/lines23/current-sentry.csv
python3 -B shared/import-drift/drift.py compare shared/import-drift/observed-sentry.csv test/scratch/lines23/current-sentry.csv --format text
python3 -B shared/import-drift/drift.py compare shared/import-drift/observed-sentry.csv shared/import-drift/observed-sentry.csv --format text
```

All exited 0. The snapshot has two modules, one edge, no cycle or issue; both
comparisons have two unchanged rows. Existing `observed-sentry.csv` remains
unchanged. All shared tool files are below 100,000 bytes. Reviewed source hashes:

- `import_map.py`: `4beb438fabac5180dfdc79fad1222bdc1236776fdec51b633d588a9cd7b006ea`
- `reconcile.py`: `c400a3855eeffe7249ada92549d702a11e40f3665bdb6661f9ec7628d05af85c`

These are local observations, not independent certification. No new coin or
deployment is needed for either line or this shared tool.
