#!/usr/bin/env python3
"""Regenerate ATEKi Figure D.4 (Harsanyi dividends of the seven-database
game, measured-gap receiver) from the stored result file, without
recomputing it.

Data: ateki/results/harsanyi_dividends/expt_zhuo/harsanyi_dividends.json
Plot: write_plot() of ateki/experiments/09_harsanyi_dividends.py (pair
heat map with 7 pt cell text, symmetric colour range clipped at +-8 with
the one cell beyond it outlined and its value printed).
Output: ateki_tmlr/figures/harsanyi_dividends.png. ASCII only.
"""

import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SO = HERE.parents[2]
EXP = SO / "ateki" / "experiments" / "09_harsanyi_dividends.py"
ART = SO / "ateki" / "results" / "harsanyi_dividends" / "expt_zhuo" / "harsanyi_dividends.json"
OUT = HERE.parent / "ateki_tmlr" / "figures" / "harsanyi_dividends.png"


def main():
    spec = importlib.util.spec_from_file_location("harsanyi_exp", EXP)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    r = json.loads(ART.read_text(encoding="utf-8"))
    mod.write_plot(r, OUT)


if __name__ == "__main__":
    main()
