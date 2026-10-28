"""Song Master LZSS decompressor (Python model of $00:C1A4). Reads the ROM from paths.ROM; never stores ROM data.
usage: lzss.py BANK(hex) INDEX(hex) [outfile]
Block = pointer table at BANK:8000 + 2*INDEX -> BANK:ptr.
Header word: bit15=1 compressed (bit15=0 is handled by the raw-copy path at $00:C27D, not modelled here); size = (w & 0x7FFF)+1.
Then repeat: flag byte, 8 flags LSB first. 1 = literal byte. 0 = 16-bit LE ref w: src = w & 0x0FFF (absolute position
in a 4 KiB ring at $7F:F000), len = 2*(w>>12)+3. Ring write pointer starts at 0; the ring is NOT cleared."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from paths import ROM
R = open(ROM, 'rb').read()
def lo(bank, a): return (bank & 0x7F) * 0x8000 + (a & 0x7FFF)
def decomp(bank, idx, ring=None):
    p = lo(bank, R[lo(bank, 0x8000 + 2*idx)] | R[lo(bank, 0x8000 + 2*idx) + 1] << 8)
    w = R[p] | R[p+1] << 8; p += 2
    assert w & 0x8000, 'raw block'
    n = (w & 0x7FFF) + 1
    ring = bytearray(ring or 0x1000); wp = 0; out = bytearray()
    while True:
        fl = R[p]; p += 1
        for _ in range(8):
            if fl & 1:
                b = R[p]; p += 1; out.append(b); ring[wp] = b; wp = (wp+1) & 0xFFF; n -= 1
                if n == 0: return bytes(out), p
            else:
                r = R[p] | R[p+1] << 8; p += 2; s = r & 0xFFF; L = 2*(r >> 12) + 3
                for _ in range(L):
                    b = ring[s]; s = (s+1) & 0xFFF; out.append(b); ring[wp] = b; wp = (wp+1) & 0xFFF; n -= 1
                    if n == 0: return bytes(out), p
            fl >>= 1
if __name__ == '__main__':
    o, end = decomp(int(sys.argv[1], 16), int(sys.argv[2], 16))
    print('decompressed %d bytes, source ends at file 0x%X' % (len(o), end))
    if len(sys.argv) > 3: open(sys.argv[3], 'wb').write(o)
