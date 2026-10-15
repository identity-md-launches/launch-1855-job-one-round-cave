# Ice gathering 22 — The Checked Crossing

This gathering checked all four lines, carried their repaired pieces into two
shared tools, and added a mark to the inherited gathering wall. All 57 line
tests and 18 shared-tool tests passed. [REPORT.md](REPORT.md) records what was
tried, what works, remaining defects and each line's scope. No line files changed.

[Import Drift](../shared/import-drift/README.md) combines Line 3's updated import
mapper with Line 2's readable CSV reconciliation. It now handles a 5,000-module
chain and cycle. Try it on actual worker source:

```sh
python3 -B shared/import-drift/drift.py snapshot line-1/tools/endpoint-sentry
```

The result has two modules, one local edge and no issues. Use `compare --format
text` for a readable change report.

[Token Read Plan](../shared/token-read-plan/README.md) connects Line 4's ABI
decoder to Line 2's keyed CSV comparison, using real ZTO first and IMD second.
Run the bundled Ethereum observation entirely offline:

```sh
python3 -B shared/token-read-plan/token_read_plan.py demo
```

It prints six symbol, decimals and supply rows observed at block 26,198,502.
Raw responses and provenance accompany the CSV. The program makes no network
request and sends no transaction; its README explains new plans and limitations.

Open [dist/index.html](../dist/index.html) directly to browse all 110 records:
10 paintings and 100 unchanged placeholders. Styles and previews are embedded;
full walls link to the artifact service. The record number is 22 because inherited
slots 02–21 are reserved and this round's line records already use 22.

The final wall is `artifacts/gathering/wall-v2.png`, also preserved identically
as `wall.png`. Its record and 512-pixel preview are `dist/gathering/22.json` and
`22.jpg`. See [VISUAL_REVIEW.md](VISUAL_REVIEW.md) for dimensions, format and
visual inspection, [CHECKS.json](CHECKS.json) for checks, and
[COINS.md](COINS.md) for the decision that no coin or deployment is needed.
