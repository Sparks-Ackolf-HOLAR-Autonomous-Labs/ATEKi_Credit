"""Exploratory (not registered): per-campaign coordinator credit under both
rules and its rank correlation with the team score. Run from this folder."""
import json,sys,numpy as np
from pathlib import Path
src=open(Path(__file__).parent/'analyze_scale.py').read()
pre=src.split('pc = exp26.load_universe')[0]
__file__=str((Path(__file__).parent/'analyze_scale.py').resolve()); exec(pre)
for s in ['S1','S2','S3']:
  fs=sorted(Path(s,'campaigns').glob('orchestrated_s*.json'))
  rows=[]
  for f in fs:
    g=json.load(open(f)); P=sorted(g['agents'],key=lambda a:int(a[5:])); full=','.join(sorted(P))
    v=g['attribution']['v'][full]
    rows.append((f.stem, round(v,3), round(g['attribution']['hypergraph_myerson']['agent1']/abs(v),3), round(max_rule_shares(g)['agent1'],3)))
  print(s); [print(' ',r) for r in rows]
  b=[r[3] for r in rows]; print('  best-group mean %.3f, positive %d/%d'%(np.mean(b),sum(x>0 for x in b),len(b)))
from scipy.stats import spearmanr
T=[];B=[]
for s in ['S1','S2','S3']:
  for f in sorted(Path(s,'campaigns').glob('orchestrated_s*.json')):
    g=json.load(open(f)); P=sorted(g['agents'],key=lambda a:int(a[5:])); v=g['attribution']['v'][','.join(sorted(P))]
    T.append(v); B.append(max_rule_shares(g)['agent1'])
print('pooled n',len(T), spearmanr(T,B))
