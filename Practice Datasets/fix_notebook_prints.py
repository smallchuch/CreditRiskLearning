"""
Patches a Jupyter notebook so bare `print(some_var)` calls can't dump a huge
DataFrame/Series repr into the output (which is what's been corrupting the
.ipynb on save/sync).

What it does:
  - Finds lines matching exactly `print(<identifier>)` (nothing else on the line).
  - Rewrites them to `print(<identifier>.head(10) if hasattr(<identifier>, "head") else <identifier>)`.
  - Leaves everything else untouched: print(df.head(5)) is already fine and is
    skipped, print("some string") is skipped, print(a, b) is skipped, etc.
  - Writes a timestamped backup before touching anything.

Usage:
    python fix_notebook_prints.py pandas_practice_notebook_v2.ipynb

Run this from a terminal in the same folder as the notebook (or pass a full path).
Uses only the standard library, no dependencies needed.
"""

import json
import re
import shutil
import sys
from datetime import datetime

PRINT_BARE_VAR = re.compile(r'^(\s*)print\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)\s*$')


def patch_source_line(line: str) -> str:
    m = PRINT_BARE_VAR.match(line.rstrip('\n'))
    if not m:
        return line
    indent, var = m.group(1), m.group(2)
    newline = '\n' if line.endswith('\n') else ''
    return f'{indent}print({var}.head(10) if hasattr({var}, "head") else {var}){newline}'


def patch_notebook(path: str) -> int:
    with open(path, encoding='utf-8') as f:
        nb = json.load(f)

    changed = 0
    for cell in nb.get('cells', []):
        if cell.get('cell_type') != 'code':
            continue
        new_source = []
        for line in cell.get('source', []):
            patched = patch_source_line(line)
            if patched != line:
                changed += 1
            new_source.append(patched)
        cell['source'] = new_source

    if changed:
        backup = f"{path}.bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(path, backup)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f"Patched {changed} print(...) call(s). Backup saved to: {backup}")
    else:
        print("No bare print(<var>) calls found — nothing to change.")

    return changed


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_notebook_prints.py <notebook.ipynb>")
        sys.exit(1)
    patch_notebook(sys.argv[1])
