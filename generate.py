#!/usr/bin/env python3
"""Create clearly labeled backdated contribution artwork in a fresh directory."""
from collections import Counter
import datetime as dt
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
CONFIG = {'year': 2020, 'name': 'Neon Equalizer', 'commits_per_date': {'2020-01-24': 4, '2020-01-25': 1, '2020-01-31': 4, '2020-02-01': 1, '2020-02-12': 4, '2020-02-13': 1, '2020-02-14': 1, '2020-02-15': 1, '2020-02-19': 4, '2020-02-20': 1, '2020-02-21': 1, '2020-02-22': 1, '2020-03-02': 4, '2020-03-03': 3, '2020-03-04': 3, '2020-03-05': 1, '2020-03-06': 1, '2020-03-07': 1, '2020-03-09': 4, '2020-03-10': 3, '2020-03-11': 3, '2020-03-12': 1, '2020-03-13': 1, '2020-03-14': 1, '2020-03-26': 4, '2020-03-27': 1, '2020-03-28': 1, '2020-04-02': 4, '2020-04-03': 1, '2020-04-04': 1, '2020-04-14': 4, '2020-04-15': 3, '2020-04-16': 1, '2020-04-17': 1, '2020-04-18': 1, '2020-04-21': 4, '2020-04-22': 3, '2020-04-23': 1, '2020-04-24': 1, '2020-04-25': 1, '2020-05-03': 4, '2020-05-04': 3, '2020-05-05': 3, '2020-05-06': 3, '2020-05-07': 1, '2020-05-08': 1, '2020-05-09': 1, '2020-05-10': 4, '2020-05-11': 3, '2020-05-12': 3, '2020-05-13': 3, '2020-05-14': 1, '2020-05-15': 1, '2020-05-16': 1, '2020-05-27': 4, '2020-05-28': 1, '2020-05-29': 1, '2020-05-30': 1, '2020-06-03': 4, '2020-06-04': 1, '2020-06-05': 1, '2020-06-06': 1, '2020-06-19': 4, '2020-06-20': 1, '2020-06-26': 4, '2020-06-27': 1, '2020-07-07': 4, '2020-07-08': 3, '2020-07-09': 1, '2020-07-10': 1, '2020-07-11': 1, '2020-07-14': 4, '2020-07-15': 3, '2020-07-16': 1, '2020-07-17': 1, '2020-07-18': 1, '2020-07-27': 4, '2020-07-28': 3, '2020-07-29': 3, '2020-07-30': 1, '2020-07-31': 1, '2020-08-01': 1, '2020-08-03': 4, '2020-08-04': 3, '2020-08-05': 3, '2020-08-06': 1, '2020-08-07': 1, '2020-08-08': 1, '2020-08-20': 4, '2020-08-21': 1, '2020-08-22': 1, '2020-08-27': 4, '2020-08-28': 1, '2020-08-29': 1, '2020-09-06': 4, '2020-09-07': 3, '2020-09-08': 3, '2020-09-09': 3, '2020-09-10': 1, '2020-09-11': 1, '2020-09-12': 1, '2020-09-13': 4, '2020-09-14': 3, '2020-09-15': 3, '2020-09-16': 3, '2020-09-17': 1, '2020-09-18': 1, '2020-09-19': 1, '2020-09-29': 4, '2020-09-30': 3, '2020-10-01': 1, '2020-10-02': 1, '2020-10-03': 1, '2020-10-06': 4, '2020-10-07': 3, '2020-10-08': 1, '2020-10-09': 1, '2020-10-10': 1, '2020-10-23': 4, '2020-10-24': 1, '2020-10-30': 4, '2020-10-31': 1, '2020-11-11': 4, '2020-11-12': 1, '2020-11-13': 1, '2020-11-14': 1, '2020-11-18': 4, '2020-11-19': 1, '2020-11-20': 1, '2020-11-21': 1, '2020-11-30': 4, '2020-12-01': 3, '2020-12-02': 3, '2020-12-03': 1, '2020-12-04': 1, '2020-12-05': 1, '2020-12-07': 4, '2020-12-08': 3, '2020-12-09': 3, '2020-12-10': 1, '2020-12-11': 1, '2020-12-12': 1}, 'expected_calendar': {'2020-01-24': 4, '2020-01-25': 1, '2020-01-31': 4, '2020-02-01': 1, '2020-02-12': 4, '2020-02-13': 1, '2020-02-14': 1, '2020-02-15': 1, '2020-02-19': 4, '2020-02-20': 1, '2020-02-21': 1, '2020-02-22': 1, '2020-03-02': 4, '2020-03-03': 3, '2020-03-04': 3, '2020-03-05': 1, '2020-03-06': 1, '2020-03-07': 1, '2020-03-09': 4, '2020-03-10': 3, '2020-03-11': 3, '2020-03-12': 1, '2020-03-13': 1, '2020-03-14': 1, '2020-03-26': 4, '2020-03-27': 1, '2020-03-28': 1, '2020-04-02': 4, '2020-04-03': 1, '2020-04-04': 1, '2020-04-14': 4, '2020-04-15': 3, '2020-04-16': 1, '2020-04-17': 1, '2020-04-18': 1, '2020-04-21': 4, '2020-04-22': 3, '2020-04-23': 1, '2020-04-24': 1, '2020-04-25': 1, '2020-05-03': 4, '2020-05-04': 3, '2020-05-05': 3, '2020-05-06': 3, '2020-05-07': 1, '2020-05-08': 1, '2020-05-09': 1, '2020-05-10': 4, '2020-05-11': 3, '2020-05-12': 3, '2020-05-13': 3, '2020-05-14': 1, '2020-05-15': 1, '2020-05-16': 1, '2020-05-27': 4, '2020-05-28': 1, '2020-05-29': 1, '2020-05-30': 1, '2020-06-03': 4, '2020-06-04': 1, '2020-06-05': 1, '2020-06-06': 1, '2020-06-19': 4, '2020-06-20': 1, '2020-06-26': 4, '2020-06-27': 1, '2020-07-07': 4, '2020-07-08': 3, '2020-07-09': 1, '2020-07-10': 1, '2020-07-11': 1, '2020-07-14': 4, '2020-07-15': 3, '2020-07-16': 1, '2020-07-17': 1, '2020-07-18': 1, '2020-07-27': 4, '2020-07-28': 3, '2020-07-29': 3, '2020-07-30': 1, '2020-07-31': 1, '2020-08-01': 1, '2020-08-03': 4, '2020-08-04': 3, '2020-08-05': 3, '2020-08-06': 1, '2020-08-07': 1, '2020-08-08': 1, '2020-08-20': 4, '2020-08-21': 1, '2020-08-22': 1, '2020-08-27': 4, '2020-08-28': 1, '2020-08-29': 1, '2020-09-06': 4, '2020-09-07': 3, '2020-09-08': 3, '2020-09-09': 3, '2020-09-10': 1, '2020-09-11': 1, '2020-09-12': 1, '2020-09-13': 4, '2020-09-14': 3, '2020-09-15': 3, '2020-09-16': 3, '2020-09-17': 1, '2020-09-18': 1, '2020-09-19': 1, '2020-09-29': 4, '2020-09-30': 3, '2020-10-01': 1, '2020-10-02': 1, '2020-10-03': 1, '2020-10-06': 4, '2020-10-07': 3, '2020-10-08': 1, '2020-10-09': 1, '2020-10-10': 1, '2020-10-23': 4, '2020-10-24': 1, '2020-10-30': 4, '2020-10-31': 1, '2020-11-11': 4, '2020-11-12': 1, '2020-11-13': 1, '2020-11-14': 1, '2020-11-18': 4, '2020-11-19': 1, '2020-11-20': 1, '2020-11-21': 1, '2020-11-30': 4, '2020-12-01': 3, '2020-12-02': 3, '2020-12-03': 1, '2020-12-04': 1, '2020-12-05': 1, '2020-12-07': 4, '2020-12-08': 3, '2020-12-09': 3, '2020-12-10': 1, '2020-12-11': 1, '2020-12-12': 1}}
year, name = CONFIG['year'], CONFIG['name']
pixels = CONFIG['commits_per_date']
calendar = CONFIG['expected_calendar']

def git(*args, **kw):
    return subprocess.check_output(['git','-C',str(ROOT),*args], **kw).decode().strip()

if (ROOT/'.git').exists():
    raise SystemExit('Refusing to modify an existing Git repository; run in a fresh directory.')
(ROOT/'art.json').write_text(json.dumps(CONFIG, indent=2)+'\n')
start = dt.date(year,1,1)
start -= dt.timedelta(days=(start.weekday()+1)%7)
colors={0:'#161b22',1:'#0e4429',2:'#006d32',3:'#26a641',4:'#39d353'}
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="790" height="155" viewBox="0 0 790 155">','<rect width="790" height="155" rx="12" fill="#0d1117"/>',f'<text x="18" y="25" fill="#e6edf3" font-family="monospace" font-size="14">{year} / {name.upper()}</text>']
for x in range(53):
    for y in range(7):
        date=start+dt.timedelta(days=x*7+y)
        if date.year != year: continue
        n=calendar.get(date.isoformat(),0)
        svg.append(f'<rect x="{18+x*14}" y="{38+y*14}" width="11" height="11" rx="2" fill="{colors[min(n,4)]}"/>')
svg.append('</svg>')
(ROOT/'preview.svg').write_text('\n'.join(svg)+'\n')
(ROOT/'README.md').write_text(f"""# {year} contribution art: {name}

![{name}](preview.svg)

Intentional pixel art for [davlabs-us’s {year} contribution graph](https://github.com/davlabs-us?tab=overview&from={year}-01-01&to={year}-12-31).

These commits are decorative, backdated art pixels, not a record of software work performed in {year}. Author and committer timestamps are set to noon UTC on each painted day. The art lives on the default `main` branch in this standalone repository. Existing contributions are preserved. The 2016 design uses dates after the account was created on August 4, 2016.

`art.json` records the exact added commits and the expected calendar including pre-existing contributions. `generate.py` recreates the same artwork in a fresh directory. Do not push another copy to the same account because its contributions would add to this one. The SVG is a design preview; GitHub controls the actual color scale.

To remove this artwork, delete this dedicated repository on GitHub and allow time for GitHub to recalculate the graph.
""")
git('init','-b','main')
git('config','user.name','davlabs-us')
git('config','user.email','20848773+davlabs-us@users.noreply.github.com')
git('add','README.md','art.json','preview.svg','generate.py')
tree=git('write-tree')
parent=None
for date,count in sorted(pixels.items()):
    assert dt.date.fromisoformat(date).year==year
    assert date <= '2026-10-31'
    for i in range(count):
        env=dict(os.environ,GIT_AUTHOR_DATE=f'{date}T12:00:00+00:00',GIT_COMMITTER_DATE=f'{date}T12:00:00+00:00')
        args=['commit-tree',tree]+(['-p',parent] if parent else [])
        parent=git(*args,input=f'Contribution art: {name} pixel {date} ({i+1}/{count})\n'.encode(),env=env)
git('update-ref','refs/heads/main',parent)
git('reset','--hard','main')
expected=Counter({f'{date}T12:00:00+00:00':n for date,n in pixels.items()})
for fmt in ['%aI','%cI']:
    assert Counter(v.replace('Z','+00:00') for v in git('log',f'--format={fmt}').splitlines())==expected
assert git('status','--porcelain')==''
print(f'{year}: {name}; validated {sum(pixels.values())} commits across {len(pixels)} dates.')
for y in range(7):
    print(''.join('██' if calendar.get((start+dt.timedelta(days=x*7+y)).isoformat(),0) else '  ' for x in range(53)))
