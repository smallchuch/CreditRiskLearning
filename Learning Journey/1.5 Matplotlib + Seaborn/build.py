import json
from part_a import CELLS_A
from part_b import CELLS_B
from part_c import CELLS_C

cells = []
for i, (kind, text) in enumerate(CELLS_A + CELLS_B + CELLS_C):
    src = text.rstrip("\n").splitlines(keepends=True)
    cid = f"cell-{i:03d}"
    if kind == "md":
        cells.append({"cell_type": "markdown", "id": cid, "metadata": {}, "source": src})
    else:
        cells.append({"cell_type": "code", "id": cid, "metadata": {}, "execution_count": None,
                      "outputs": [], "source": src})

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = "matplotlib_seaborn_practice_home_credit.ipynb"
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

md = sum(1 for c in cells if c["cell_type"] == "markdown")
code = sum(1 for c in cells if c["cell_type"] == "code")
print(f"cells: {len(cells)} (md={md}, code={code})")
