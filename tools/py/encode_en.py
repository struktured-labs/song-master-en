"""English text -> Song Master bytes. Tags as in smtext.decode. Word-wraps dialogue to the window width."""
import re
from smtext import TAG, ARG
LOWER = {chr(97+i): 0x01+i for i in range(26)}
CH = {' ':0x00, "'":0x1B, '"':0x1C, '…':0x1D, '.':0xA0, ',':0xB0, '!':0x74, '?':0x75, ':':0x9B, '=':0x9C,
      '-':0x9E, '/':0x9F, '(':0xAA, ')':0xAB, '[':0xA4, ']':0xA5, '<':0xA8, '>':0xA9, '*':0x6C, '♥':0xAD, '©':0xA1,
      '_':0x9A, '・':0x9D, '◆':0xAC, '×':0x6D, '▶':0x71, '▼':0x72, '▲':0x73, '「':0x70}
for i in range(10): CH[str(i)] = 0x76+i
for i in range(26): CH[chr(65+i)] = 0x80+i
CH.update(LOWER)
RTAG = {v: k for k, v in TAG.items()}
TOK = re.compile(r'\[([A-Za-z0-9:]+)\]|(.)', re.S)
NAMEW = 6   # display width assumed for [nameN]
WIDTH = 24
def tokens(s):
    for m in TOK.finditer(s):
        if m.group(1) is not None: yield ('tag', m.group(1))
        else: yield ('ch', m.group(2))
def tagbytes(t):
    if re.match(r'x[0-9A-F]{2}$', t): return bytes([int(t[1:], 16)])  # raw byte (menu option ids)
    if t == 'LINE': return b'\xfe'
    if t == 'END': return b'\xff'
    m = re.match(r'FD([0-9A-F]{2})(?::([0-9A-F]{2}))?$', t)
    if m:
        b = bytes([0xFD, int(m.group(1), 16)])
        return b + (bytes([int(m.group(2), 16)]) if m.group(2) else b'')
    return bytes([0xFD, RTAG[t]])
TERMW = {}  # display width of list words (script/en/lists.json)
def _termw():
    import json, os
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../script/en/lists.json')
    if not os.path.exists(f): return
    for code, name in (('FD0E', 'places'), ('FD0F', 'terms'), ('FD10', 'items'), ('FD11', 'magic'), ('FD12', 'monsters')):
        for i, e in enumerate(json.load(open(f)).get(name, [])): TERMW['%s:%02X' % (code, i + 1)] = len(e)
_termw()
def wrap(s, width=WIDTH, col0=0):
    """re-flow text between [n] tags: words never split; continuation lines indented by one space."""
    out = []; col = 0
    toks = list(tokens(s)); i = 0
    def width_of(tk):
        if tk[0] == 'ch': return 1
        if tk[1].startswith('name'): return NAMEW
        if tk[1] == 'tab': return 5
        if tk[1][:5] in ('FD0E:', 'FD0F:', 'FD10:', 'FD11:', 'FD12:'): return TERMW.get(tk[1], 8)
        return 0
    # group into words
    words = []; cur = []
    for tk in toks:
        if tk == ('ch', ' ') or (tk[0] == 'tag' and tk[1] in ('n', '0C', 'wait', 'LINE', 'END', 'FD31')):
            if cur: words.append(('w', cur)); cur = []
            words.append(('sep', tk))
        else: cur.append(tk)
    if cur: words.append(('w', cur))
    res = []; col = col0; pending_space = False
    for kind, x in words:
        if kind == 'sep':
            if x == ('ch', ' '):
                pending_space = col > 0
                continue
            res.append(x)
            if x[1] in ('n', '0C'): col = 0
            pending_space = False
            continue
        w = sum(width_of(t) for t in x)
        need = w + (1 if pending_space else 0)
        if col > 0 and col + need > width:
            res.append(('tag', 'n')); res.append(('ch', ' ')); col = 1; pending_space = False
        if pending_space: res.append(('ch', ' ')); col += 1
        res.extend(x); col += w; pending_space = False
    return res
def paginate(toks, maxlines=3):
    """insert [wait] so no more than maxlines text lines appear between waits (window scrolls)."""
    out = []; lines = 0
    for t in toks:
        if t == ('tag', 'wait'): lines = -1 if False else 0
        if t == ('tag', 'n'):
            lines += 1
            if lines > maxlines:
                out.append(('tag', 'wait')); lines = 1
        out.append(t)
    return out
def encode(s, dowrap=True, col0=0):
    toks = wrap(s, col0=col0) if dowrap else list(tokens(s))
    if dowrap: toks = paginate(toks)
    # A space byte straight after a list term (FD0E-FD12) is rendered as a line break by the
    # game (seen: "the thief / Guild.", "an old man / named"). Re-emit the current colour tag
    # between the term and the space so the space is not the first byte after the term.
    fixed = []; colr = 'c0'
    for i, t in enumerate(toks):
        if t[0] == 'tag' and t[1] in ('c0', 'c1', 'c2', 'c3'): colr = t[1]
        fixed.append(t)
        if t[0] == 'tag' and t[1][:5] in ('FD0E:', 'FD0F:', 'FD10:', 'FD11:', 'FD12:') \
                and i + 1 < len(toks) and toks[i + 1] == ('ch', ' '):
            fixed.append(('tag', colr))
    toks = fixed
    b = bytearray()
    for k, v in toks:
        if k == 'tag': b += tagbytes(v)
        else:
            if v not in CH: raise ValueError('unencodable %r in %r' % (v, s))
            b.append(CH[v])
    return bytes(b)
