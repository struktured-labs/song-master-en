#!/bin/bash
# Song Master English: build the patch from source + your own ROM.
#   usage: tools/build.sh "/path/to/Song Master (Japan).sfc"   (or rom/..., or SONGMASTER_ROM)
# Output: build/songmaster_en.ips/.bps (+ build/songmaster_en.sfc for testing; never distribute it).
set -euo pipefail
cd "$(dirname "$0")/.."
ROM="${SONGMASTER_ROM:-rom/Song Master (Japan).sfc}"
if [ $# -gt 0 ] && [ -f "$1" ]; then ROM="$1"; shift; fi
[ -f "$ROM" ] || { echo "ROM not found: $ROM"; exit 1; }
export SONGMASTER_ROM="$(cd "$(dirname "$ROM")" && pwd)/$(basename "$ROM")"
python3 - "$SONGMASTER_ROM" <<'P'
import sys,zlib
d=open(sys.argv[1],'rb').read(); crc='%08X'%(zlib.crc32(d)&0xffffffff)
if len(d)==0x100200: sys.exit('ROM has a 512-byte copier header; remove it first.')
if crc!='4FA5FC25': sys.exit('Wrong ROM: crc32 %s (expected 4FA5FC25)'%crc)
print('ROM ok: Song Master (Japan), CRC32',crc)
P
ASAR="${ASAR:-tools/bin/asar}"; FLIPS="${FLIPS:-tools/bin/flips}"
if [ ! -x "$ASAR" ] || [ ! -x "$FLIPS" ]; then tools/get_tools.sh; fi
mkdir -p build
python3 tools/py/insert_sm.py "$SONGMASTER_ROM" build/songmaster_en.sfc
"$ASAR" --fix-checksum=on asm/main.asm build/songmaster_en.sfc
python3 - <<'P'
R=open('build/songmaster_en.sfc','rb').read()
assert len(R)==0x200000
c=sum(R)&0xFFFF; hc=R[0x7FDE]|R[0x7FDF]<<8; ic=R[0x7FDC]|R[0x7FDD]<<8
assert c==hc and (c^0xFFFF)==ic,(hex(c),hex(hc),hex(ic))
print('patched ROM ok: checksum %04X'%c)
P
rm -f build/songmaster_en.ips build/songmaster_en.bps
"$FLIPS" --create --ips "$SONGMASTER_ROM" build/songmaster_en.sfc build/songmaster_en.ips >/dev/null
"$FLIPS" --create --bps "$SONGMASTER_ROM" build/songmaster_en.sfc build/songmaster_en.bps >/dev/null
ls -l build/songmaster_en.ips build/songmaster_en.bps
