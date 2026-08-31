#!/usr/bin/env python3
"""Extract the embedded `var DATA = {...}` from index.html into
pedigree-data.json, so other consumers (alec-bell.github.io/genealogy.html)
can fetch the same data the app renders. Run by CI on every index.html
change; safe to run by hand."""
import json, re, sys

s = open('index.html', encoding='utf-8').read()
m = re.search(r'var\s+DATA\s*=\s*', s)
if not m:
    sys.exit('no `var DATA =` found in index.html')
i = m.end(); depth = 0; instr = False; esc = False; q = ''
start = i
while i < len(s):
    c = s[i]
    if instr:
        if esc: esc = False
        elif c == '\\': esc = True
        elif c == q: instr = False
    else:
        if c in '"\'': instr = True; q = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
    i += 1
data = json.loads(s[start:i])
out = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
open('pedigree-data.json', 'w', encoding='utf-8').write(out)
print(f'wrote pedigree-data.json ({len(data)} persons, {len(out)} bytes)')
