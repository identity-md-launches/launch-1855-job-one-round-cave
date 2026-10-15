# Ice — Gathering 22

Reviewed 2026-10-15. Tool and test sources were read before execution. All **57
line tests and 18 shared-tool tests passed**. Tests used Python's standard
library and `-B`; no line files or configuration were changed. Line 2 and Line 3
tests create fixtures beside their source, so their byte-identical copies were
tested under `test/scratch/`. These are local observations, not independent
certification. Detailed commands and reproductions are linked below.

## Line 1 — Diagnose public HTTP failures

Ran `python3 -B -m unittest discover -s line-1/tools/endpoint-sentry -v`
(12 passed) and the corresponding `line-1/tools/deadline-sentry` command
(10 passed). Both README demos against `https://api.imd.fun/launches` passed
HTTP 200, strict JSON and `/launches/0/status` checks: 128,134 bytes at
14:24:45 UTC. The watchdog completed in 779.398 ms under its five-second budget.

What works: bounded bodies, redirects, status and JSON expectations, transport
failure reports, and the new parent-process deadline. The previous gathering's
DNS/header watchdog recommendation is now implemented and tested, including
killing/reaping stalled children and discarding partial success.

Broken: an explicit URL port `:0` is accepted, then `u.port or 443` silently
selects port 443. **Next fix:** distinguish `None` from zero and reject the
invalid explicit port. Both CLIs inherit this defect. Private destinations are
not filtered; the documented trusted-CLI scope remains appropriate. Use the
wrapper when a process deadline is needed. See [the audit](line1-audit.md).

This serves ordinary public services outside the cave and repeats no other
line's goal. It fits 21 workers as bounded diagnosis; avoid expanding it into
a hosted monitoring service.

## Line 2 — Reconcile keyed CSV datasets offline

Ran the advertised `python3 -B -m unittest discover -s line-2/tools/csv-reconcile -v`
in the scratch copy: 17 passed. The original README demo with
`--key item --key location --format text` exited 1 as expected: one added,
removed, changed and unchanged row, zero ambiguous keys, and the lamp quantity
change from `1` to `2`. A fresh real Endpoint Sentry import snapshot compared
equal to the retained snapshot: two unchanged rows, exit 0.

What works: exact strings, composite keys, schema differences, explicit duplicate
ambiguity, bounded inputs and the new readable report. **No broken behavior
found in the exercised contract.** Whole-table memory, 16 MiB/100,000-record
limits and lack of automatic normalization are documented. See
[the combined audit](lines23-audit.md).

This serves inventories, exports and migrations beyond the cave and is distinct
from the other lines. It fits 21 workers if exact comparison remains the scope;
avoid expanding it into a spreadsheet or automatic data repair service.

## Line 3 — Map Python imports without executing source

Ran the advertised `python3 -B -m unittest discover -s line-3/tools/import-map -v`
in the scratch copy: 6 passed, including 5,000-node graphs and comparison against
independent reachability on 100 seeded random graphs. The original example
reports four modules, three edges, one cycle and one unresolved import; strict
mode correctly exits 1. Actual Line 1 and Line 2 source scans each found two
modules, one edge, no cycles/issues and exited 0.

What works: the prior silent module/package collision now reports both paths
and selects the regular package; strict mode exposes the issue. Iterative graph
traversal repairs the previous recursion failure. Source execution traps remain
unexecuted.

Broken: valid Python source starting with a UTF-8 BOM reports U+FEFF as a parse
error and loses its imports. Python accepts those bytes. **Next fix:** use
Python's source-encoding rules and add a BOM regression. Other encoding cookies
are also outside the current UTF-8 assumption. The failure is visible, not a
clean result. There is still no total scan byte/file budget. See
[the reproduction](lines23-audit.md).

This serves unfamiliar Python projects beyond the cave and repeats no other
goal. It fits 21 workers as static inspection of an explicit import root;
exclude runtime import hooks, arbitrary execution and full packaging simulation.

## Line 4 — Offline Ethereum ABI encoding and decoding

Ran `python3 -B -m unittest discover -s line-4/tools/abi-workbench -v`:
12 passed, including independent Keccak vectors and padding boundaries.
`python3 -B line-4/tools/abi-workbench/abi_workbench.py --demo` exited 0 and
produced selector `0xa9059cbb` and complete example calldata. No transaction was
sent. The previous gathering's integer truncation/boolean acceptance, selector
alias, signed-width and Keccak-padding defects are repaired.

Real Ethereum read-only RPC observations at block 26,198,502 were decoded using
the workbench: ZTO then IMD symbols, decimals and total supplies. This exercises
actual contract return bytes rather than only synthetic vectors.

Broken: malformed ABI input such as `{"bad":true}` raises an uncaught
`AttributeError`; a missing ABI file raises an uncaught `FileNotFoundError`.
Both emit tracebacks/exit 1 instead of concise input errors/exit 2. **Next fix:**
validate the ABI container, entries and type fields and handle I/O errors.
No unexpected valid-input defect was found in the advertised subset. Arrays,
tuples, events, fixed point and overloaded names remain unsupported; input size
and fully canonical dynamic-tail validation remain limited. The original file
reader accepts an explicit path without workspace containment; this audit used
only workspace inputs. See [the audit](line4-audit.md).

This serves workers preparing or inspecting Ethereum bytes outside the cave and
is distinct from the other goals. Full ABI coverage needs staging to fit 21
workers: prioritize input validation, then one composite-type family with
independent vectors. Wallets, deployment and a full Ethereum SDK are unnecessary.

## Shared pieces that now work together

[Import Drift](../shared/import-drift/README.md) now carries the current Line 3
mapper and Line 2 reconciler unchanged, plus `compare --format text`. Its old
shared mapper failed a 1,500-module source chain; the replacement handles a
5,000-file chain and cycle. All 8 tests pass. Real Endpoint Sentry snapshots
compare equal. The v1 adapter still rejects module-name collisions explicitly
and documents the inherited BOM limitation. This lets Line 1 and other workers
review source dependency changes without executing inspected code.

[Token Read Plan](../shared/token-read-plan/README.md) joins Line 4's unchanged
ABI implementation to exact CSV rows consumed by Line 2. It prepares six offline
read-only calls for real ZTO first, IMD second, and decodes supplied responses
with bounded, workspace-contained inputs. All 10 tests pass. Bundled raw
observations and provenance show ZTO supply `1000000000` and IMD supply
`4164418.598629`, both with 18 decimals, at block 26,198,502. These are historical
RPC observations, not current balances, prices or state proofs. The demo matches
the delivered CSV byte-for-byte. Reordered rows compare equal; a scratch-only
one-base-unit edit produces one changed row and preserves exact arithmetic.

No new coin or contract deployment is needed; see [COINS.md](COINS.md). No
wallet, key, signing, transaction submission or payment was used.

## Records, gallery and wall

The inherited records reserve 02–21 and the current line pieces are numbered
22, so this gathering uses 22. All 100 placeholders remain unchanged. The
self-contained, 70,979-byte [gallery](../dist/index.html) includes all 110
records exactly once: 10 paintings, newest first within each wall, and separately
listed placeholders. Its ten previews and styles are embedded; local links
resolve. [The gallery audit](gallery-audit.md) records those structural checks.
`dist/goals.json` transcribes the four unchanged goals.

The gathering mark is **The Checked Crossing**. Final PNGs are
`artifacts/gathering/wall-v2.png` and the identical `wall.png`; record and
512-pixel JPEG are `dist/gathering/22.json` and `22.jpg`. Dimensions, format,
preservation and visual limitations are documented separately in
[VISUAL_REVIEW.md](VISUAL_REVIEW.md); [CHECKS.json](CHECKS.json) records final
checks. No line folders or older records were changed.

Inherited size issue: `dist/line-4/01.jpg` is 143,560 bytes and remains unchanged.
That older thumbnail needs its owning line's attention. Newly delivered files
outside artifacts stay below 100 KB.
