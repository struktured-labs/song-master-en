#!/bin/bash
# usage: tools/test/preview.sh UID NAME.png  (sheet saved as /tmp/smrun/<RUN>/<RUN>_NAME.png, path printed)  -- build with SM_PREVIEW=UID, run headless, contact sheet of stable text frames
set -e; cd "$(dirname "$0")/../.."
SM_PREVIEW=$1 bash tools/build.sh >/dev/null
for try in 1 2 3; do timeout 700 bash tools/test/mesen_run_sm.sh "$PWD/build/songmaster_en.sfc" "$PWD/tools/test/preview.lua" 650 || true; D=$(cat /tmp/sm_last_run); ls $D/*s08980.png >/dev/null 2>&1 && break; done
python3 - "$D" "$2" <<'P'
import sys,glob,hashlib,os
d=sys.argv[1];r=os.path.basename(d)
from PIL import Image
fs=sorted(glob.glob(d+'/'+r+'_s0[3-8]*.png'));cs=[Image.open(f).convert('RGB').crop((0,136,256,224)) for f in fs]
hs=[hashlib.md5(c.tobytes()).hexdigest() for c in cs];out=[];seen=set()
for i in range(len(cs)-1):
    if hs[i]==hs[i+1] and hs[i] not in seen: seen.add(hs[i]);out.append(cs[i])
W=3;rows=max(1,(len(out)+W-1)//W);S=Image.new('RGB',(256*W,88*rows))
for i,c in enumerate(out): S.paste(c,((i%W)*256,(i//W)*88))
o=d+'/'+r+'_'+os.path.basename(sys.argv[2]);S.save(o);print(o,len(out),'frames')
P
