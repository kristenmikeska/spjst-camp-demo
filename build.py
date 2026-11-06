#!/usr/bin/env python3
"""Rebuild the GitHub demo from the WordPress snippets in ../camp-2027/.

Run from this folder:  python3 build.py
Then commit and push. The WordPress snippets stay the source of truth;
this only wraps them in a full page and swaps site links for demo links.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "camp-2027"

BAR = ('<div style="background:#FFF6D6;border-bottom:1px solid #E8D58A;color:#4A3B00;'
       'font:600 14px/1.4 system-ui,sans-serif;text-align:center;padding:10px 16px">'
       'Draft preview for review &mdash; not the live SPJST website. '
       '<span style="display:inline-block;margin-left:14px">{nav}</span></div>')

def page(title, nav, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<style>body{{margin:0;background:#fff}}</style>
</head>
<body>
{BAR.format(nav=nav)}
{body}
</body>
</html>
"""

camp = (SRC / "camp-2027.html").read_text()
raffle = (SRC / "camp-raffle-2027.html").read_text()

# Site links -> demo links (camp is the root page, raffle lives in camp-raffle/)
camp = camp.replace('href="/camp-raffle/"', 'href="camp-raffle/"')
raffle = (raffle.replace('href="/camp/#camp-fees"', 'href="../#camp-fees"')
                .replace('href="/camp/"', 'href="../"'))

for name, html in (("camp", camp), ("raffle", raffle)):
    left = [l for l in html.splitlines() if 'href="/' in l]
    assert not left, f"{name}: unconverted site link(s): {left}"

(HERE / "index.html").write_text(page(
    "SPJST Summer Camp 2027 — Draft",
    'Page 1 of 2: <strong>Summer Camp</strong> &middot; <a href="camp-raffle/" style="color:#24367C">View the Camp Raffle page</a>',
    camp))
(HERE / "camp-raffle").mkdir(exist_ok=True)
(HERE / "camp-raffle" / "index.html").write_text(page(
    "SPJST Summer Camp Raffle — Draft",
    'Page 2 of 2: <strong>Camp Raffle</strong> &middot; <a href="../" style="color:#24367C">Back to the Summer Camp page</a>',
    raffle))
print("Built index.html and camp-raffle/index.html")
