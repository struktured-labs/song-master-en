#!/bin/bash
# wk.sh 'lua body' -> /tmp/wk/*.png, /tmp/wk_log.txt
echo "return {$1}" > /tmp/wk.lua; rm -rf /tmp/wk; mkdir -p /tmp/wk
cd /workspace/song-master-en && timeout 400 bash tools/test/mesen_run_sm.sh $PWD/build/songmaster_en.sfc $PWD/tools/test/walk.lua 380 >/dev/null 2>&1
python3 - <<'P'
import glob
from PIL import Image
fs=sorted(glob.glob('/tmp/wk/f*.png'));W=8;R=(len(fs)+W-1)//W
S=Image.new('RGB',(128*W,112*max(R,1)))
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((128,112)),((i%W)*128,(i//W)*112))
S.save('/workspace/wk.png'); print(len(fs))
P
