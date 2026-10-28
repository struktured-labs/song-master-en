"""Song Master text codec (own table derived from ROM font)."""
import os, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
T = {}
for l in open(ROOT + '/tables/sm_jp.tbl', encoding='utf-8'):
    a, b = l.rstrip('\n').split('=', 1); T[int(a, 16)] = b
TAG = {0x0A:'wait',0x0B:'tab',0x0C:'0C',0x0D:'n',0x1B:'pause',0x1F:'c0',0x20:'c1',0x21:'c2',0x22:'c3'}
for i in range(10): TAG[i] = 'name%d' % i
ARG = {0x0E,0x0F,0x10,0x11,0x12}
def decode(b):
    s = ''; j = 0; mark = None
    while j < len(b):
        c = b[j]
        if c == 0xFD:
            x = b[j+1]
            if x in ARG: s += '[FD%02X:%02X]' % (x, b[j+2]); j += 3
            else: s += '[%s]' % TAG.get(x, 'FD%02X' % x); j += 2
            continue
        if c == 0xFE: s += '[LINE]'; j += 1; continue
        if c == 0xFF: s += '[END]'; j += 1; continue
        if c in (0x6E, 0x6F) and j+1 < len(b) and b[j+1] < 0x6E:
            base = T[b[j+1]]
            comp = unicodedata.normalize('NFC', base + ('\u3099' if c == 0x6E else '\u309A'))
            if len(comp) == 1: s += comp; j += 2; continue
        s += T.get(c, '{%02X}' % c); j += 1
    return s
def jpchars(b):
    n = 0; j = 0
    while j < len(b):
        c = b[j]
        if c == 0xFD: j += 3 if b[j+1] in ARG else 2; continue
        if c < 0xFE and c not in (0x6E, 0x6F): n += 1
        j += 1
    return n
