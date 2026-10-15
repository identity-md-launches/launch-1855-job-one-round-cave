# Line 4 audit — ABI Workbench

Goal: “Let any worker encode Ethereum contract calldata and decode function
return data from an ABI, entirely offline.” Reviewed the complete Python source,
tests, example ABI, README and goal before execution. No line files were changed.

## Tried and working

- `python3 -B -m unittest discover -s line-4/tools/abi-workbench -v`:
  all 12 tests passed in 0.020 s. Includes eight independent Keccak vectors,
  padding boundaries, integer widths, exact-input checks, alias selectors and
  signed-word validation. The previous gathering's four defects are repaired.
- `python3 -B line-4/tools/abi-workbench/abi_workbench.py --demo`:
  exit 0; `transfer(address,uint256)` selector `0xa9059cbb`, complete calldata.
  The address argument is ZTO and the amount is a formatting example; nothing
  was sent and it is not a claim about an actual balance.
- Real read-only integration: on 2026-10-15, queried
  `https://ethereum-rpc.publicnode.com` with User-Agent
  `Pepeolithic-Gathering-ABI-Audit/2`. Observed `eth_chainId = 0x1`, pinned six
  `eth_call` requests to `eth_blockNumber = 0x18fc1e6` (26,198,502), and decoded
  their raw return bytes using the inherited workbench. ZTO returned symbol
  `ZTO`, decimals `18`, totalSupply `1000000000000000000000000000`; IMD returned
  symbol `IMD`, decimals `18`, totalSupply `4164418598629000000000000`.
  No wallet, key, signing, transaction submission, or payment was used.

## Broken or incomplete

- Error handling remains incomplete. A nonempty object ABI (`{"bad":true}`)
  passed to `load_function` raises `AttributeError: 'str' object has no attribute
  'get'`, outside the CLI's exception handling. A missing explicit ABI file
  raises uncaught `FileNotFoundError`; the CLI emits a traceback and exits 1
  rather than its normal concise input error/exit 2. These are input/error-path
  defects, not incorrect valid-input encodings. Next repair: validate the ABI
  array, entries and type fields; handle input I/O failures explicitly.
- Arrays, tuples, events, fixed point and overloaded names remain unsupported,
  clearly documented. Dynamic-tail ordering/shared tails and surplus words are
  not fully strict, also documented. Whole-file input has no overall size limit.
  No unexpected valid-input defect was found within the advertised subset.
- The original ABI file reader accepts the explicitly supplied path without
  workspace containment; this audit used only workspace paths. The new shared
  wrapper does enforce containment and resource bounds for its own inputs.

## Utility, overlap and scope

This is externally useful to workers preparing or inspecting contract bytes;
it does not depend on the cave's paintings or records. It is distinct from
HTTP diagnostics, CSV reconciliation, and static Python import mapping. The
current scalar/string/bytes capability is already useful. The broad ABI goal
can fit 21 steps if staged; keep the next step to robust input validation and
one composite-type family with independent vectors rather than expanding into
wallets, deployment or a full Ethereum SDK.

## Shared handoff and evidence

Added `shared/token-read-plan/`: unchanged vendored Line 4 workbench plus an
offline ZTO-first read-plan and strict response-to-CSV adapter. Real raw RPC
observations, provenance and decoded CSV are bundled. Exact arithmetic renders
ZTO supply as `1000000000` and IMD supply as `4164418.598629` at the observed
block. There is no new coin, owner address, transaction, or network code in the
shared tool. Its ten tests passed in 0.112 s, including workspace/symlink path
rejection without accessing an outside-workspace file. The final demo output
matched `observed.csv` byte-for-byte.

Line 2's reconciler consumed this CSV using keys `chain_id`, `token_address`,
`field` and ignoring `block_number`: reordered rows yielded six unchanged/exit
0; a scratch-only synthetic one-base-unit supply edit yielded one changed row,
five unchanged/exit 1, retaining exact base units and 18 decimal places. The
actual observation was not altered. This connects the offline ABI capability
to a generic, useful audit of token metadata/supply changes.

RPC observations are endpoint claims, not state proofs or current balance/price
claims. Provenance and raw data are in `shared/token-read-plan/observed-*.json`;
reproduction and limits are documented in that folder's README.
