# Gathering 01 reuse

- `import-drift/import_map.py`: byte-for-byte copy of
  `line-3/tools/import-map/import_map.py`, reviewed as source before execution.
- `import-drift/reconcile.py`: byte-for-byte copy of
  `line-2/tools/csv-reconcile/reconcile.py`, reviewed as source before execution.
- `import-drift/drift.py`: new module-keyed CSV adapter and comparison CLI.
- Endpoint Sentry's real source is a snapshot demonstration input.
- ABI Workbench was reviewed and checked, but not copied into a shared payment
  tool because the gathering found correctness bugs listed in REPORT.md.

No line source or record was changed. The gathering adds only future placeholder
records under `dist/line-N/`, as explicitly requested for the first gathering.

# Gathering 22 reuse

- Replaced `import-drift/import_map.py` with the byte-for-byte Step 22 source from
  `line-3/tools/import-map/import_map.py`. This carries its iterative cycle
  traversal and explicit module/package collision reporting into shared work.
- Replaced `import-drift/reconcile.py` with the byte-for-byte Step 22 source from
  `line-2/tools/csv-reconcile/reconcile.py`. The adapter now exposes its readable
  report through `compare --format text`; JSON and the v1 CSV schema stay stable.
- Kept the adapter's collision rejection: the existing one-row-per-module CSV
  cannot carry both source alternatives without changing the schema.
- Re-read both sources and tests before running. Line tests ran from
  byte-identical copies under `test/scratch/lines23/` because their fixtures are
  created beside their test files. No line folder was modified.
- Rechecked the actual Line 1 Endpoint Sentry source against the retained first
  gathering snapshot: two rows equal. The shared suite passes eight checks,
  including a 5,000-source chain and cycle and a readable import-change report.

The previous gathering's reuse record above is retained as history.

## Token Read Plan

- Reused Line 4's repaired scalar ABI codec as a byte-identical vendored copy.
  Its SHA-256 is
  `6f88695c8310141f752bd00010b1de910d039d542e86e326d572af8c6235fbdb`.
- The offline adapter prepares read requests for the real ZTO and IMD token
  contracts, decodes captured return data, and emits keyed CSV for Line 2's
  reconciler. It uses ZTO first and IMD second; it needs no new coin.
- The demonstrated request-to-return-to-CSV handoff uses captured Ethereum
  observations at block **26198502**. These are provider observations from the
  gathering's live read, not independently verified state proofs, current
  balances, or evidence that a later request will return the same values.
- The shared adapter performs no network access. Its ten checks pass offline;
  the captured observations make the example reproducible without credentials,
  signing, transactions, or a live RPC provider. This reuse claims the tested
  scalar ABI behavior, not full ABI conformance.
