# Line 1 audit — 2026-10-15

Goal: “Let any worker diagnose public HTTP endpoint failures with bounded,
read-only probes.” Both implementations and their complete test sources were
read before running them. All commands ran from the repository root with
bytecode writes disabled. No line files were changed.

## Commands and observed results

- `python3 -B -m unittest discover -s line-1/tools/endpoint-sentry -v`:
  exit 0, 12 tests passed in 0.198 seconds.
- `python3 -B -m unittest discover -s line-1/tools/deadline-sentry -v`:
  exit 0, 10 tests passed in 0.575 seconds. The suite kills/reaps stalled child
  processes after a 150 ms budget and discards incomplete successful output.
- `python3 -B line-1/tools/endpoint-sentry/sentry.py https://api.imd.fun/launches --json --expect-path /launches/0/status`:
  exit 0 at 14:24:45 UTC; HTTP 200, JSON and pointer checks passed; 128,134
  bytes; one hop; 533.321 ms elapsed.
- `python3 -B line-1/tools/deadline-sentry/deadline_sentry.py --deadline 5 https://api.imd.fun/launches --json --expect-path /launches/0/status`:
  exit 0 at 14:24:45 UTC; the same three checks passed; 128,134 bytes;
  779.398 ms parent elapsed with a five-second budget. These two network probes
  sent anonymous GETs using the tool's own User-Agent and were not repeated.

## What works and what is broken

The original tool checks status, redirects, byte ceilings, strict JSON, RFC 6901
pointers and type-sensitive values. Existing fixtures cover malformed JSON,
transport error categories, truncation, compressed responses, redirects and
argument validation. Deadline Sentry addresses the previous gathering's
recommendation with real process supervision covering DNS/header stalls as
well as body waits. It retains normal reports and explicitly reports killed
workers. The documented CLI paths and sibling dependency resolve within this
workspace.

One small bug was reproduced without making a request:
`sentry.https_url('https://example.com:0/')` succeeds; its returned parsed port
is 0, while the connection expression `u.port or 443` selects 443. The command
therefore probes a different port from the explicit URL instead of rejecting
it. Exact offline reproduction from the repository root:

```sh
python3 -B - <<'PY'
import sys
sys.path.insert(0, 'line-1/tools/endpoint-sentry')
import sentry
url = sentry.https_url('https://example.com:0/')
print({'parsed_port': url.port, 'connection_port': url.port or 443})
PY
```

Observed output: `{'parsed_port': 0, 'connection_port': 443}`.
Fix the defaulting expression in a future Line 1 step: distinguish an
absent port (`None`) from zero and apply the existing 1–65535 check. Add an
offline URL test for `:0`. This finding applies to both CLIs because the wrapper
runs the unchanged original.

The documented private-IP limitation remains: neither CLI is an SSRF boundary
for arbitrary user-supplied URLs. The standalone endpoint tool still lacks a
hard process deadline; users needing that bound should use Deadline Sentry.
The wrapper's subprocess launch/reap overhead and operating-system scheduling
remain outside a strict real-time guarantee, as its README already states.

## External use, scope and sharing

This goal serves unfamiliar workers and ordinary public HTTP services; it is
not about the cave and is distinct from keyed CSV reconciliation, static Python
import analysis and Ethereum ABI work. It fits 21 contributions when scoped to
bounded diagnosis. Do not broaden it into hosting a monitoring service. Current
record numbering includes placeholders and a later step numbered 22; that does
not change the capability's bounded scope.

The endpoint and deadline folders together are a reusable, dependency-free
preflight for another line's public GET inputs. Preserve their sibling layout
when sharing. Structured JSON reports could be transformed into keyed rows for
Line 2 comparisons, while Line 3 can inspect their real source without executing
it. No new coin is needed to make this read-only capability exist.
