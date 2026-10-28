-- boot from power-on, no input: prologue crawl captures every 150 frames (unique paths via smshot)
local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
SM_M=M; dofile("/workspace/song-master-en/tools/test/smshot.lua")
M.endAt=4800; M.shotEvery=150; M.shotDir="/tmp"
M.start()
