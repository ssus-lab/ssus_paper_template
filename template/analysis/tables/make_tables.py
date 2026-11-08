"""Run every table formatter in this folder: `pixi run tables`.

A formatter is a script beside this one. It reads raw outputs from
results/, formats the numbers, and writes one table for the paper with
ssus_papers.Table (paper/_tbl_<name>.md, included in the paper with
{{< include _tbl_<name>.md >}}). It never computes a result. The paper's
renders run this first, so a table cannot go stale. Files whose names start
with an underscore are skipped, as helpers.
"""

import runpy
from pathlib import Path

here = Path(__file__).resolve().parent
for script in sorted(here.glob("*.py")):
    if script.name == Path(__file__).name or script.name.startswith("_"):
        continue
    print(f"tables: {script.name}")
    runpy.run_path(str(script), run_name="__main__")
