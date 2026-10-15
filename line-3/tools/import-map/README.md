# Import Map

Import Map reads Python source with the standard library AST parser. It reports local import links, strongly connected import cycles, `if __name__ == "__main__"` entry points, unresolved local or relative imports, parse errors, and calls to `__import__` or `importlib.import_module`. It never imports or executes the inspected project.

Run the included example from the repository root:

```sh
python3 line-3/tools/import-map/import_map.py line-3/tools/import-map/examples
```

When tried locally, it found four modules, three local edges, the `pkg.engine`/`pkg.helper` cycle, `main` as an entry point, and the absent `pkg.missing` import. `--json` emits a deterministic machine-readable report; `--strict` exits 1 when a cycle or issue is found.

I also ran it on the existing `line-1/tools/endpoint-sentry` and `line-2/tools/csv-reconcile` source trees. Each scan found two modules and the test module's local import of its tool, with no cycles or unresolved imports. These scans read source only and did not run either tool.

The root is an import root, so a `src/` project should be scanned from `src/`. Absolute imports without a matching local top-level name are labeled external rather than missing, since source inspection cannot prove whether a third-party module is installed. `from module import name` may name an attribute rather than a submodule; the tool conservatively links to the known module. Dynamic import targets are flagged but not inferred.

## Step 22: collisions and deep graphs

A regular package (`pkg/__init__.py`) and a module (`pkg.py`) can share an
import name. The mapper now emits a `module_collision` issue containing both
paths and the selected path. It analyzes the regular package, following Python's
file-finder precedence, and explicitly identifies the shadowed source that was
not analyzed. `--strict` returns 1 for this issue. This is a static choice within
one import root, not a simulation of runtime path changes or custom import hooks.
The existing report shape and one-record-per-module convention are preserved.

Cycle detection now uses an iterative Tarjan traversal. It handles deep import
graphs without depending on the interpreter's recursion limit and computes the
cycle groups once per scan.

Run the reproducible checks from the repository root:

```sh
python3 -B -m unittest discover -s line-3/tools/import-map -v
```

Tried locally: all six tests passed. They reproduce top-level and nested
collisions, confirm package selection and strict failure, inspect execution-trap
source without running it, preserve the original four-module example, cover
parse errors and self-imports, traverse a 5,000-node chain and cycle, and compare
100 deterministic random graphs against an independent reachability algorithm.
The implementation and tests require only Python's standard library, offline.
Scanning remains whole-tree and unbounded in total bytes; AST parsing itself
still has Python's parser limits. No claim of general runtime import resolution
is made.
