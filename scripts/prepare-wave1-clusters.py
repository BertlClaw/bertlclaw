#!/usr/bin/env python3
from pathlib import Path
import csv, json, re, collections
ROOT = Path(__file__).resolve().parent.parent
src = ROOT / 'data' / 'wave1-priority-pages.csv'
rows = list(csv.DictReader(src.open(encoding='utf-8')))
city_groups = collections.defaultdict(list)
for r in rows:
    slug = r['path'].removeprefix('/landingpage-').removesuffix('.html')
    parts = slug.split('-')
    city = '-'.join(parts[:-1]) if len(parts) > 1 else slug
    profession = parts[-1] if len(parts) > 1 else 'base'
    city_groups[city].append({**r, 'profession': profession, 'slug': slug})
out = []
for city, items in sorted(city_groups.items()):
    markets = sorted(set(i['market'] for i in items))
    out.append({
        'city': city,
        'market': markets[0] if markets else 'unknown',
        'count': len(items),
        'professions': sorted(i['profession'] for i in items),
        'paths': [i['path'] for i in items],
    })
out_json = ROOT / 'data' / 'wave1-clusters.json'
json.dump({'count': len(out), 'clusters': out}, out_json.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(json.dumps({'cluster_count': len(out), 'sample': out[:12]}, ensure_ascii=False, indent=2))
