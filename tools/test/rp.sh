#!/bin/bash
# rp.sh NAME 'lua table body'  -> battle/field harness (fs2.lua). Captures in fresh /tmp/smrun/<RUN>/; sheet <RUN>_NAME.png (path printed)
echo "return {$2}" > /tmp/sm_seq.lua
cd /workspace/song-master-en && timeout 300 bash tools/test/mesen_run_sm.sh ${ROM:-$PWD/build/songmaster_en.sfc} $PWD/tools/test/fs2.lua 280 >/dev/null 2>&1
D=$(cat /tmp/sm_last_run); cp /workspace/smmenu/pos.txt "$D/$(basename $D)_pos.txt" 2>/dev/null
python3 - "$D" "$1" <<'P'
import sys,glob,os
from PIL import Image
d,n=sys.argv[1],sys.argv[2];r=os.path.basename(d)
fs=sorted(glob.glob(d+'/'+r+'_[fr]*.png'));W=4;R=(len(fs)+W-1)//W
S=Image.new('RGB',(256*W,224*max(R,1)))
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((256,224)),((i%W)*256,(i//W)*224))
o=d+'/'+r+'_'+n+'.png'; S.save(o); print(o,len(fs))
P
