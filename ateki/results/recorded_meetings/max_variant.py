"""Hypergraph/star Myerson with max-of-components aggregation (the team
reports one ranking, so a split team is worth its best component), next to
the sum-of-components rule of exp 11. Uses the cached coalition values in
each campaign log. ASCII only."""
import itertools, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from analysis.shapley import ShapleyEngine
HERE = Path(__file__).resolve().parent
P = ["agent1", "agent2", "agent3", "agent4", "agent5"]
def comps(S, H):
    par = {p: p for p in S}
    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for e in H:
        if set(e) <= S:
            r = f(e[0])
            for x in e[1:]:
                par[f(x)] = r
    out = {}
    for p in S:
        out.setdefault(f(p), set()).add(p)
    return [frozenset(c) for c in out.values()]
res = {}
for path in sorted((HERE / "campaigns").glob("*.json")):
    g = json.load(open(path, encoding="utf-8"))
    V = {frozenset(k.split(",")) if k != "-" else frozenset(): v
         for k, v in g["attribution"]["v"].items()}
    H = g["attribution"]["hyperedges"]
    vmax = lambda S: max([V[c] for c in comps(set(S), H)], default=0.0)
    sc = ShapleyEngine(P, vmax).exact().scores
    tot = V[frozenset(P)]
    res[path.stem] = {a: sc[a] / abs(tot) for a in P}
arms = {}
for arm in ["flat", "orchestrated"]:
    rows = [v for k, v in res.items() if k.startswith(arm)]
    arms[arm] = {a: float(np.mean([r[a] for r in rows])) for a in P}
json.dump({"per_campaign": res, "mean_share": arms},
          open(HERE / "max_variant.json", "w", encoding="utf-8"), indent=1)
print(json.dumps(arms, indent=1))
