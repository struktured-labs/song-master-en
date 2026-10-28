#!/bin/bash
# wk.sh 'lua body' -> captures in a fresh /tmp/smrun/<RUN>/ ; sheet at <RUNDIR>/<RUN>_sheet.png (path printed)
echo "return {$1}" > /tmp/wk.lua
cd /workspace/song-master-en && timeout 400 bash tools/test/mesen_run_sm.sh $PWD/build/songmaster_en.sfc $PWD/tools/test/walk.lua 380 >/dev/null 2>&1
D=$(cat /tmp/sm_last_run); cp /tmp/wk_log.txt "$D/$(basename $D)_log.txt"
python3 - "$D" <<'P'
import glob,sys,os
from PIL import Image
d=sys.argv[1];r=os.path.basename(d)
fs=sorted(glob.glob(d+'/'+r+'_f*.png'));W=8;R=(len(fs)+W-1)//W
S=Image.new('RGB',(128*W,112*max(R,1)))
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((128,112)),((i%W)*128,(i//W)*112))
o=d+'/'+r+'_sheet.png'; S.save(o); print(o, len(fs))
P
