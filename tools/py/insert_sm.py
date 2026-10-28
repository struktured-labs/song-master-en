#!/usr/bin/env python3
"""Build data: expand ROM to 2 MiB, insert English strings (stub FD 30 lo hi), rebuilt raw blocks, font.
usage: insert_sm.py IN.sfc OUT.sfc   (code hooks are applied afterwards by asar asm/main.asm)"""
import sys, os, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sm_script import load, parse
from smtext import ROOT
from encode_en import encode
import hashlib
src = open(sys.argv[1], 'rb').read(); assert len(src) == 0x100000
rom = bytearray(src) + bytearray(b'\xff' * 0x100000)
EN = {}
for f in sorted(glob.glob(ROOT + '/script/en/s_*.json')):
    for k, v in json.load(open(f)).items():
        if v.get('en'): EN[k] = v
import re
def txt2tags(body):
    out=[]
    for i,l in enumerate(body):
        m=re.match(r'(.*?)~?@([^:]+):(.*)$',l)
        if m: t=m.group(1)+'[wait]'+m.group(2)+'[tab][n]'+m.group(3)
        else: t=l
        if i and not t.startswith('[wait]'): t='[n]'+t
        elif i: t='[n]'+t
        out.append(t)
    s=''.join(out)
    s=re.sub(r'\{(\d)\}',r'[name\1]',s).replace('~','[wait]')
    return s
for f in sorted(glob.glob(ROOT + '/script/en/t_*.txt')):
    cur=None; body=[]
    for l in open(f).read().split('\n')+['>END']:
        if l.startswith('>'):
            if cur and body: EN[cur]={'en':txt2tags(body)}
            cur=l[1:].strip(); body=[]
        elif l.strip() or body: body.append(l.rstrip())
    while 0: pass
def lo(bank, a): return (bank & 0x7F) * 0x8000 + (a & 0x7FFF)
# --- strings: banks $20-$2F; pointer table $20:8000 (3 bytes * 0x800)
ids = {}; sdata = []
def sid(uid):
    if uid not in ids:
        n = len(ids); hi, l = divmod(n, 0xFE); ids[uid] = (hi << 8) | l
    return ids[uid]
bank, addr = 0x20, 0x8000 + 0x800 * 3
def block0(d):
    """rebuild the word lists in place; each list must fit its original byte budget (offsets are hard-coded)."""
    f = ROOT + '/script/en/b00_lists.json'
    if not os.path.exists(f): return bytes(d)
    out = bytearray(d)
    for L in json.load(open(f)):
        a = int(L['offset'], 16); n = L['budget']
        blob = b''.join(encode(e, False) + b'\xff' for e in L['entries'])
        jp = bytes(d[a:a+n]).split(b'\xff')[:-1]
        assert len(L['entries']) == len(jp), (L['list'], len(L['entries']), len(jp))
        if len(blob) > n: raise SystemExit('list %s over budget: %d > %d' % (L['list'], len(blob), n))
        out[a:a+n] = blob + b'\xff' * (n - len(blob))
    return bytes(out)
stats = dict(blocks_over=[], strings=0, en=0)
newblocks = []
for i in range(78):
    d = load(i); p, end = parse(d)
    if i == 0: newblocks.append(block0(d)); continue
    out = bytearray(); last = 0
    for kind, s, e in p:
        if kind != 'text': continue
        raw = d[s:e]; uid = hashlib.sha1(raw).hexdigest()[:10]; stats['strings'] += 1
        out += d[last:s]; last = e
        if uid in EN:
            stats['en'] += 1
            n = sid(uid); out += bytes([0xFD, 0x30, n & 0xFF, n >> 8, raw[-1]])
        else: out += raw
    out += d[last:]
    limit = 0x1800 if i not in (0, 2, 3) else len(d)
    if len(out) > limit: stats['blocks_over'].append((i, len(out)))
    newblocks.append(bytes(out))
for uid, n in ids.items():
    v = EN[uid]; v['en']=re.sub(r'(\[END\]|\[LINE\])$','',v['en']); b = encode(v['en'], v.get('wrap', True)) + b'\xfd\x31'
    if addr + len(b) > 0x10000: bank += 1; addr = 0x8000
    assert bank < 0x30
    o = lo(bank, addr); rom[o:o+len(b)] = b
    t = lo(0x20, 0x8000) + 3 * n; rom[t:t+3] = bytes([addr & 0xFF, addr >> 8, bank])
    addr += len(b)
# --- blocks: banks $30-$3E, raw (bit15 clear), table at bank:8000
bank, addr, idx = 0x30, 0x8000 + 0x100, 0
for i, b in enumerate(newblocks):
    blob = bytes([(len(b) - 1) & 0xFF, (len(b) - 1) >> 8]) + b
    if addr + len(blob) > 0x10000: bank += 1; addr = 0x8000 + 0x100; idx = 0
    assert bank < 0x3F
    rom[lo(bank, addr):lo(bank, addr)+len(blob)] = blob
    t = lo(bank, 0x8000) + 2 * idx; rom[t:t+2] = bytes([addr & 0xFF, addr >> 8])
    rom[0x6C59 + 2*i] = idx; rom[0x6C5A + 2*i] = bank
    addr += len(blob); idx += 1
# --- font: own lowercase/punct glyphs
cur = None; glyph = {}
for l in open(ROOT + '/font/lower8.txt'):
    l = l.rstrip('\n')
    if l.startswith('# ') or not l: continue
    if l.startswith('== '): cur = l[3:]; glyph[cur] = []; continue
    glyph[cur].append(l)
from encode_en import CH
EXTRA = {'…': ['........'] * 6 + ['##.##.##', '##.##.##']}
glyph.update(EXTRA)
for ch, rows in glyph.items():
    c = CH[ch]
    for y, r in enumerate(rows): rom[0x80000 + c*8 + y] = int(r.replace('#', '1').replace('.', '0'), 2)
f = ROOT + '/script/en/names.json'
if os.path.exists(f):
    nb = b''.join(encode(x, False) + b'\xff' for x in json.load(open(f)))
    rom[0x1F0000:0x1F0000+len(nb)] = nb
open(sys.argv[2], 'wb').write(rom)
print('strings %(strings)d translated %(en)d' % stats, 'unique ids', len(ids), 'str bank end %02X:%04X' % (bank, addr), 'over', stats['blocks_over'])
