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
        l=re.sub(r'\^(\d)',r'[c1][name\1][c0]',l)
        l=re.sub(r'%([^:%"\[]+|\{\d\}):',r'[c1]\1[c0][n]',l)
        t=re.sub(r'~?@([^:@"\[]+|\{\d\}):',r'[wait]\1[tab][n]',l)
        if t.startswith('+'): t=t[1:]
        elif i and t.startswith(' ') and not out[-1].endswith(']'): t=' '+t.lstrip()
        elif i and t.startswith(' '): t=' '+t.lstrip() if out[-1].endswith('[c0]') else '[n]'+t
        elif i: t='[n]'+t
        out.append(t)
    s=''.join(out)
    s=re.sub(r'\{(\d)\}',r'[name\1]',s).replace('~','[wait]')
    return s
for f in sorted(glob.glob(ROOT + '/script/en/t_*.txt')):
    cur=None; body=[]
    for l in open(f).read().split('\n')+['>END']:
        if l.startswith('>'):
            if cur and body: EN[cur]={'en':txt2tags(body),'wrap':not nw}
            h=l[1:].split(); cur=h[0] if h else None; nw=('!' in h) or ('nowrap' in f); body=[]
        elif l.strip() or body: body.append(l.rstrip())
    while 0: pass
if os.environ.get('SM_PREVIEW'):  # test only: show another string in the first classroom line
    EN['e58f49c110']=dict(EN[os.environ['SM_PREVIEW']])
def lo(bank, a): return (bank & 0x7F) * 0x8000 + (a & 0x7FFF)
# --- strings: banks $20-$2F; pointer table $20:8000 (3 bytes * 0x800)
ids = {}; sdata = []
def sid(uid):
    if uid not in ids:
        n = len(ids); hi, l = divmod(n, 0xFE); ids[uid] = (hi << 8) | l
    return ids[uid]
bank, addr = 0x20, 0x8000 + 0x800 * 3
def block0(d):
    global BLOCK0_RAW; BLOCK0_RAW = bytes(d)
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
QUOTED = set()
stats = dict(blocks_over=[], strings=0, en=0)
newblocks = []
RAWP = json.load(open(ROOT + '/script/en/raw_inplace.json')) if os.path.exists(ROOT + '/script/en/raw_inplace.json') else []
for i in range(78):
    d = load(i)
    for P_ in RAWP:
        if P_['block'] != i: continue
        a = int(P_['off'], 16); o = bytes.fromhex(P_['old']); n = bytes.fromhex(P_['new'])
        assert bytes(d[a:a+len(o)]) == o and len(o) == len(n), P_['note']; d = bytes(d[:a]) + n + bytes(d[a+len(o):])
    p, end = parse(d)
    if i == 0: newblocks.append(block0(d)); continue
    out = bytearray(); last = 0; prevq = False
    for kind, s, e in p:
        if kind != 'text': continue
        raw = d[s:e]; uid = hashlib.sha1(raw).hexdigest()[:10]; stats['strings'] += 1
        if prevq: QUOTED.add(uid)
        prevq = bytes(raw[-2:]) == b'\x70\xff'
        out += d[last:s]; last = e
        if uid in EN:
            stats['en'] += 1
            n = sid(uid); out += bytes([0xFD, 0x30, n & 0xFF, n >> 8, raw[-1]])
        else: out += raw
    out += d[last:]
    limit = 0x1800 if i not in (0, 2, 3) else len(d)
    if len(out) > limit: stats['blocks_over'].append((i, len(out)))
    newblocks.append(bytes(out))
open(ROOT + '/build/quoted.txt', 'w').write('\n'.join(sorted(QUOTED)))
for uid, n in ids.items():
    v = EN[uid]; v['en']=re.sub(r'(\[END\]|\[LINE\])$','',v['en']); b = encode(v['en'], v.get('wrap', True), 1 if uid in QUOTED else 0) + b'\xfd\x31'
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
    assert bank < 0x3A  # $3A prologue, $3B splash, $3C lists, $3E names, $3F code
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
# --- dialogue word lists -> bank $3C (asm lh_* hooks). English from script/en/lists.json, else raw JP entries.
LE = json.load(open(ROOT + '/script/en/lists.json'))
b0 = load(0)[0] if False else None
jl = json.load(open(ROOT + '/script/jp/b00_lists.json'))
B0RAW = BLOCK0_RAW
tab = bytearray(0xA00); dat = bytearray(); base = 0x8A00
for k, name in enumerate(['places', 'terms', 'items', 'magic', 'monsters']):
    J = [x for x in jl if x['list'] == name][0]
    a = int(J['offset'], 16); raw = bytes(B0RAW[a:a+J['budget']]).split(b'\xff')
    n = len(J['entries']) - 1
    en = LE.get(name, [])
    assert not en or len(en) == n, (name, len(en), n)
    for i in range(n):
        e = encode(en[i], False) if en else raw[i]
        assert len(e) < 0x30, (name, i)
        p = base + len(dat); tab[k*0x200 + i*2: k*0x200 + i*2 + 2] = bytes([p & 255, p >> 8])
        dat += e + b'\xff'
assert base + len(dat) <= 0x10000
rom[0x1E0000:0x1E0000 + 0xA00] = tab; rom[0x1E0A00:0x1E0A00 + len(dat)] = dat
# --- short (<= 8 cell) item/magic names for menu windows -> bank $3D, same layout as $3C (asm lhm_* hooks)
f = ROOT + '/script/en/lists_short.json'
if os.path.exists(f):
    LS = json.load(open(f)); tab = bytearray(0xA00); dat = bytearray()
    for k, name in enumerate(['places', 'terms', 'items', 'magic', 'monsters']):
        for i, x in enumerate(LS.get(name, LE.get(name, []) if name == 'monsters' else [])):
            e = encode(x, False); assert len(e) <= 8 or name == 'monsters', x
            p_ = 0x8A00 + len(dat); tab[k*0x200 + i*2: k*0x200 + i*2 + 2] = bytes([p_ & 255, p_ >> 8]); dat += e + b'\xff'
    assert rom[0x1E8000:0x1F0000] == b'\xff' * 0x8000, 'bank $3D not free'
    rom[0x1E8000:0x1E8A00] = tab; rom[0x1E8A00:0x1E8A00 + len(dat)] = dat
# --- battle-side list lookups (bank $01 reads the JP lists at $7E:D000 directly): English copies in bank $2D
# items (short) at $2D:D000, monsters at $2D:DA00, magic (short) at $2D:F000; re-point each LDX #base and LDA $7ED000,x
if os.path.exists(f):
    BB = 0x2D; o0 = BB * 0x8000 + 0x5000
    assert rom[o0:o0 + 0x3000] == b'\xff' * 0x3000, 'bank $2D D000-FFFF not free'
    lay = {'items': (0x0000, LS['items']), 'monsters': (0x0A00, LE['monsters']), 'magic': (0x2000, LS['magic'])}
    lim = {'items': 0x0A00, 'monsters': 0x2000, 'magic': 0x3000}
    for name, (base, ents) in lay.items():
        blob = b''.join(encode(x, False) + b'\xff' for x in ents)
        assert base + len(blob) <= lim[name], (name, len(blob))
        rom[o0 + base:o0 + base + len(blob)] = blob
    LDX = {0x8F63: 0x0430, 0x90E8: 0x0430, 0x9124: 0x0430, 0x914D: 0x0430, 0x9176: 0x0430, 0xB913: 0x0430,
           0xAAAB: 0x0951, 0x8F35: 0x0F7F, 0xB803: 0x0F7F}
    NEW = {0x0430: 0x0000, 0x0951: 0x0A00, 0x0F7F: 0x2000}
    for a, old in LDX.items():
        o = lo(1, a); assert rom[o] == 0xA2 and rom[o+1] | rom[o+2] << 8 == old, hex(a)
        n = NEW[old]; rom[o+1:o+3] = bytes([n & 255, n >> 8])
    for a in (0x8F3D, 0x8F66, 0x90F6, 0x9127, 0x9150, 0x9179, 0xAAB3, 0xAAD1, 0xB80C, 0xB91B):
        o = lo(1, a); assert rom[o:o+4] == bytes.fromhex('bf00d07e'), hex(a)
        rom[o+3] = BB
# --- bank $02 menus (script/en/menus.json): repack into the original pool and re-point the menu table
f = ROOT + '/script/en/menus.json'
if os.path.exists(f):
    MJ = json.load(open(f)); a0, a1 = (int(x, 16) for x in MJ['pool']); pool = bytearray(); orig = bytes(rom[a0:a1])
    for m in MJ['menus']:
        o = int(m['orig'], 16); pre = orig[o - a0:o - a0 + 2]
        ptr = 0x8000 + ((a0 + len(pool)) & 0x7FFF)
        for t in m['table']:
            t = int(t, 16); assert rom[t] | rom[t+1] << 8 == 0x8000 + (o & 0x7FFF), (hex(t), m['jp'])
            rom[t:t+2] = bytes([ptr & 255, ptr >> 8])
        pool += pre + b'\xfe'.join(encode(x, False) for x in m['items']) + b'\xff'
    assert len(pool) <= a1 - a0, ('menu pool over', len(pool), a1 - a0)
    rom[a0:a0 + len(pool)] = pool; rom[a0 + len(pool):a1] = b'\xff' * (a1 - a0 - len(pool))
# --- in-place UI strings (script/en/ui_inplace.json): each region is rewritten within its original bytes;
# strings keep their order, pointer operands listed in "refs" are re-pointed, leftover bytes become FF.
f = ROOT + '/script/en/ui_inplace.json'
if os.path.exists(f):
    for R_ in json.load(open(f))['regions']:
        a0, a1 = int(R_['start'], 16), int(R_['end'], 16); out = bytearray()
        for s_ in R_['strings']:
            o = int(s_['orig'], 16); want = 0x8000 + (o & 0x7FFF); new = 0x8000 + ((a0 + len(out)) & 0x7FFF)
            for t in s_.get('refs', []):
                t = int(t, 16); assert rom[t] | rom[t+1] << 8 == want, (hex(t), s_['jp'])
                rom[t:t+2] = bytes([new & 255, new >> 8])
            if not s_.get('refs'): assert o == a0 + len(out), ('unreferenced string moved', s_['jp'])
            out += bytes.fromhex(s_.get('pre', '')) + b'\xfe'.join(encode(x, False) for x in s_['items']) + b'\xff'
        assert len(out) <= a1 - a0, ('ui region over', R_['start'], len(out), a1 - a0)
        rom[a0:a0 + len(out)] = out; rom[a0 + len(out):a1] = b'\xff' * (a1 - a0 - len(out))
    for P_ in json.load(open(f)).get('patches', []):
        a = int(P_['addr'], 16); old = bytes.fromhex(P_['old']); new = bytes.fromhex(P_['new'])
        assert rom[a:a + len(old)] == old and len(old) == len(new), P_['note']
        rom[a:a + len(new)] = new
open(sys.argv[2], 'wb').write(rom)
print('strings %(strings)d translated %(en)d' % stats, 'unique ids', len(ids), 'str bank end %02X:%04X' % (bank, addr), 'over', stats['blocks_over'])
