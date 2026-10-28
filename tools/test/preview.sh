#!/bin/bash
# usage: tools/test/preview.sh UID OUT.png  -- build with SM_PREVIEW=UID, run headless, contact sheet of stable text frames
set -e; cd "$(dirname "$0")/../.."
SM_PREVIEW=$1 bash tools/build.sh >/dev/null
rm -rf /tmp/smprev; mkdir -p /tmp/smprev
for try in 1 2 3; do rm -rf /tmp/smprev; mkdir -p /tmp/smprev; DONEFILE=/tmp/smprev/s08980.png timeout 700 bash tools/test/mesen_run_sm.sh "$PWD/build/songmaster_en.sfc" "$PWD/tools/test/preview.lua" 650 || true; [ -f /tmp/smprev/s08980.png ] && break; done
python3 - "$2" <<'P'
import sys,glob,hashlib
from PIL import Image
fs=sorted(glob.glob('/tmp/smprev/s0[3-8]*.png'));cs=[Image.open(f).convert('RGB').crop((0,136,256,224)) for f in fs]
hs=[hashlib.md5(c.tobytes()).hexdigest() for c in cs];out=[];seen=set()
for i in range(len(cs)-1):
    if hs[i]==hs[i+1] and hs[i] not in seen: seen.add(hs[i]);out.append(cs[i])
W=3;rows=max(1,(len(out)+W-1)//W);S=Image.new('RGB',(256*W,88*rows))
for i,c in enumerate(out): S.paste(c,((i%W)*256,(i//W)*88))
S.save(sys.argv[1]);print(len(out),'frames')
P
