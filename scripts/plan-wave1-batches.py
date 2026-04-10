#!/usr/bin/env python3
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent.parent
clusters = json.load((ROOT/'data'/'wave1-clusters.json').open(encoding='utf-8'))['clusters']
# focus first on cleaner AT and major DE cities with high commercial value
priority_cities = ['wien','graz','linz','salzburg','innsbruck','klagenfurt','st-poelten','wiener-neustadt','berlin','hamburg','muenchen','koeln','frankfurt','stuttgart','hannover','duesseldorf']
selected = [c for c in clusters if c['city'] in priority_cities]
batches=[]
batch_size=20
for i in range(0, len(selected), batch_size):
    batches.append(selected[i:i+batch_size])
out = {'batch_count': len(batches), 'batch_size': batch_size, 'batches': batches}
json.dump(out, (ROOT/'data'/'wave1-batches.json').open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps({'batch_count': len(batches), 'first_batch': batches[0] if batches else []}, ensure_ascii=False, indent=2))
