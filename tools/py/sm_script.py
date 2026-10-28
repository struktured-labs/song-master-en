"""Song Master script block parser (model of the indexer at $00:E9EC). No ROM data stored."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lzss import R, decomp
OPLEN = R[0x6A66:0x6A66+256]   # $00:EA66 opcode attribute table
FDARG = {0x0E:1,0x0F:1,0x10:1,0x11:1,0x12:1}
def block_src(i): return R[0x6C59+2*i], R[0x6C5A+2*i]
def load(i):
    idx, b = block_src(i); return decomp(b, idx)[0]
def parse(d):
    """yields ('op', start, end) / ('label', start, end) / ('text', start, end_incl_terminator)"""
    y = 0; out = []
    while y < len(d):
        op = d[y]
        if op == 0:
            out.append(('label', y, y+2)); lab = d[y+1]; y += 2
            if lab == 0xFF: break
            continue
        a = OPLEN[op]; L = a & 0x3F; s = y; y += L
        if a & 0x40:
            while d[y] != 0xFF: y += L - 1
            y += 1; out.append(('op', s, y)); continue
        out.append(('op', s, y))
        if a & 0x80:
            t = y
            while d[y] < 0xFE: y += 1
            y += 1; out.append(('text', t, y))
    return out, y
if __name__ == '__main__':
    tot = 0; n = 0
    for i in range(78):
        d = load(i); p, end = parse(d)
        txt = [x for x in p if x[0]=='text']; n += len(txt); tot += sum(e-s for _,s,e in txt)
        print(i, len(d), end, len(txt))
    print('strings', n, 'bytes', tot)
