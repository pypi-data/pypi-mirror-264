"""
helper tools to produce the original solutions for a specific problem

to be used interactively under ipython
"""

from pathlib import Path

from exact_cover_samples import problems, summary

import xcover

DATA = Path("../src/exact_cover_samples/data/")

if not DATA.exists():
    print(f"WARNING: data directory {DATA} not found")

def solve(name):
    problem = problems[name]()
    data = problem["data"]
    name = problem["name"]
    solutions = xcover.covers_bool(data)
    with (DATA / f"{name}-solutions.csv").open('w') as f:
        for s in solutions:
            print(",".join(str(i) for i in s), file=f)
