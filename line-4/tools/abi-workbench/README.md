# ABI Workbench

A Python standard-library CLI that computes Ethereum selectors with Keccak-256,
encodes unsigned function calldata, and decodes supplied return bytes offline.
It never connects to RPC, signs, sends, pays, or reads keys or environment values.
ABI paths are explicit inputs; keep them inside your workspace.

## Run it

From the repository root:

```sh
python3 -B -m unittest discover -s line-4/tools/abi-workbench -v
```

This runs 12 regression tests, including the gathering's four defect reports,
all 32 integer widths, malformed output checks, and eight Keccak vectors
independently obtained using `cast keccak` (Cast is not needed to run the tests).
All 12 passed locally. The original demo also passed:

```sh
python3 -B line-4/tools/abi-workbench/abi_workbench.py --demo
```

The demo's transfer **argument** is the real ZTO address; it is only a formatting
example, not a destination envelope or an executed token transfer. Its amount is
illustrative, not a balance or price. It prints `0xa9059cbb` and complete calldata.

An included ABI exercises canonical alias handling:

```sh
python3 -B line-4/tools/abi-workbench/abi_workbench.py encode --abi line-4/tools/abi-workbench/alias-example.json --function transfer --args '["0xd782bdea4ef02a0bd391eb9089470c8080f0a68e",12]'
```

For your ABI use `encode --abi PATH --function NAME --args '[...]'`, or
`decode --abi PATH --function NAME --data 0x...`. ABI files are JSON arrays of
function entries. Integer inputs must be exact JSON integers or decimal strings
(e.g. `"1000000000000000000"`); floats, booleans, exponent strings and whitespace
are rejected. JSON numeric exponents parse as floats and are rejected too.

## Supported scope and repairs

Supports `address`, `bool`, `int`/`uint` (canonicalized to 256 bits), widths
8 through 256 in steps of 8, `bytes1` through `bytes32`, `string`, and `bytes`.
The new repair combines Keccak's padding bits at the 135-byte boundary, avoids
lossy integer conversion, canonicalizes aliases before selector hashing, and
rejects signed words with invalid sign extension. Additional checks reject
nonzero address/bytes padding, dynamic offsets into the head, missing tail
padding, and nonzero dynamic padding. Direct `encode_value` calls now use the
same type validation as the CLI.

Tuples, arrays, events, fixed point and ambiguous overloaded names are explicitly
unsupported. The decoder does not enforce a unique ordering of dynamic tails,
reject shared tails, or reject every surplus word; it is not a full strict-mode
ABI validator. Inputs are held in memory without a total size budget. This is a
local byte interpreter, not proof of an on-chain value or transaction success.
The tests are regressions, not an independent audit or full ABI conformance suite.
