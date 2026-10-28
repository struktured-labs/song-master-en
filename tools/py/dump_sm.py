#!/usr/bin/env python3
"""Dump all 78 script blocks -> script/jp/bNN.json and deduplicated script/jp/strings.json"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sm_script import load, parse, block_src
from smtext import decode, jpchars, ROOT
uniq = {}; order = []
os.makedirs(ROOT + '/script/jp', exist_ok=True)
for i in range(1, 78):
    d = load(i); p, end = parse(d); msgs = []
    idx, bank = block_src(i)
    for k, (kind, s, e) in enumerate([x for x in p if x[0] == 'text']):
        raw = bytes(d[s:e]); h = hashlib.sha1(raw).hexdigest()[:10]
        if h not in uniq:
            uniq[h] = dict(uid=h, first='b%02d_%03d' % (i, k), raw=raw.hex(' '), text=decode(raw), chars=jpchars(raw), uses=0); order.append(h)
        uniq[h]['uses'] += 1
        msgs.append(dict(id='b%02d_%03d' % (i, k), off='0x%04X' % s, op='%02X' % d[s-1] if s else '', uid=h, text=decode(raw)))
    json.dump(dict(info=dict(block=i, src='bank %02X idx %d' % (bank, idx), size=len(d), strings=len(msgs)), messages=msgs),
              open(ROOT + '/script/jp/b%02d.json' % i, 'w'), ensure_ascii=False, indent=1)
json.dump([uniq[h] for h in order], open(ROOT + '/script/jp/strings.json', 'w'), ensure_ascii=False, indent=1)
print(len(order), sum(uniq[h]['chars'] for h in order))

# block 0 = five FF-separated word lists at fixed offsets (FD 0E..12 / bank 01 menus use them by offset)
LISTS = [('places', 0x000, 0x20F, '0E'), ('terms', 0x20F, 0x430, '0F'), ('items', 0x430, 0x951, '10'), ('monsters', 0x951, 0xF7F, '12'), ('magic', 0xF7F, None, '11')]
d = load(0); L = []
for name, a, b, fd in LISTS:
    b = b or len(d); it = bytes(d[a:b]).split(b'\xff')[:-1]
    L.append(dict(list=name, offset='0x%03X' % a, budget=b - a, fd=fd, entries=[decode(x) for x in it]))
json.dump(L, open(ROOT + '/script/jp/b00_lists.json', 'w'), ensure_ascii=False, indent=1)
from lzss import R
nm = R[0x3C5F:0x3C5F+49].split(b'\xff')[:10]
json.dump([decode(x) for x in nm], open(ROOT + '/script/jp/default_names.json', 'w'), ensure_ascii=False, indent=1)
