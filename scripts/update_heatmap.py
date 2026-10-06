"""Fetch GitHub's public contribution calendar and render a self-contained SVG."""
from pathlib import Path
from datetime import date, timedelta
from html import escape
import json
import re
import requests
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
USERNAME = 'ziaabdullah00'
response = requests.get(f'https://github.com/users/{USERNAME}/contributions', timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
tips = {t.get('for'): t.get_text(' ', strip=True) for t in soup.select('tool-tip[for]')}
days = []
for cell in soup.select('[data-date][data-level]'):
    label = tips.get(cell.get('id'), cell.get('aria-label', ''))
    match = re.search(r'([\d,]+) contributions?', label)
    if match:
        count = int(match.group(1).replace(',', ''))
    elif 'No contributions' in label:
        count = 0
    else:
        raise ValueError(f'Cannot parse contribution count for {cell.get("data-date")}: {label!r}')
    days.append({'date':cell['data-date'], 'level':int(cell['data-level']), 'count':count})
if len(days) < 350 or len({d['date'] for d in days}) != len(days):
    raise ValueError(f'Unexpected calendar: {len(days)} days; preserving existing output')
days.sort(key=lambda d:d['date'])
total = sum(d['count'] for d in days)
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data/contributions.json').write_text(json.dumps({'username':USERNAME,'total':total,'days':days},indent=2)+'\n')
start = date.fromisoformat(days[0]['date'])
start -= timedelta(days=(start.weekday()+1)%7)
palette = ['#161b22','#0e4429','#006d32','#26a641','#39d353']
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="860" height="220" viewBox="0 0 860 220" role="img">', f'<title>{USERNAME}: {total:,} contributions in the last year</title>', '<rect width="860" height="220" rx="14" fill="#0d1117"/>', '<style>@keyframes reveal{from{opacity:0;transform:translateY(-5px)}to{opacity:1;transform:translateY(0)}}.day{animation:reveal .4s both}@media(prefers-reduced-motion:reduce){.day{animation:none}}</style>', '<g font-family="monospace" fill="#8b949e" font-size="10">']
for row,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
    s.append(f'<text x="16" y="{63+row*18}">{label}</text>')
seen=set()
for d in days:
    dt=date.fromisoformat(d['date']); offset=(dt-start).days; col,row=divmod(offset,7)
    x,y=51+col*14.8,51+row*18
    if dt.month not in seen and dt.day<=7:
        seen.add(dt.month); s.append(f'<text x="{x:.1f}" y="35">{dt.strftime("%b")}</text>')
    s.append(f'<rect class="day" x="{x:.1f}" y="{y}" width="11.8" height="14" rx="3" fill="{palette[d["level"]]}" style="animation-delay:{(col+row)*.018:.3f}s"><title>{escape(d["date"])}: {d["count"]} contributions</title></rect>')
s.append(f'<text x="24" y="198" fill="#c9d1d9" font-size="12">{total:,} contributions in the last year</text><text x="680" y="198">Less</text>')
for i,color in enumerate(palette):
    s.append(f'<rect x="{714+i*17}" y="187" width="12" height="12" rx="2" fill="{color}"/>')
s.append('<text x="805" y="198">More</text></g></svg>')
(ROOT/'contrib-heatmap.svg').write_text('\n'.join(s)+'\n')
print(f'Rendered {len(days)} days, {total:,} contributions')
