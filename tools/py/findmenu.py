"""Find uncompressed menu strings: runs of table chars terminated by FE (line end) / FF (end).
usage: findmenu.py TBL [minlen]  (TBL = your local, Shift-JIS or UTF-8 .tbl; never committed)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__)); from paths import ROM
raw = open(sys.argv[1], 'rb').read()
try: txt = raw.decode('utf-8')
except UnicodeDecodeError: txt = raw.decode('shift_jis', 'replace')
t = {}
for l in txt.splitlines():
    k, _, v = l.partition('=')
    if len(k) == 2: t[int(k, 16)] = v
R = open(ROM, 'rb').read(); mn = int(sys.argv[2]) if len(sys.argv) > 2 else 4
i = 0
while i < len(R):
    j = i
    while j < len(R) and R[j] in t and R[j] < 0xB0 and R[j] not in (0xFE, 0xFF) and R[j] != 0: j += 1
    if j - i >= mn and j < len(R) and R[j] in (0xFE, 0xFF) and sum(1 for b in R[i:j] if b in (0x00, 0x6C)) == 0:
        s = ''.join(t[b] for b in R[i:j]); print('%06X %s' % (i, s))
    i = j + 1 if j > i else i + 1
