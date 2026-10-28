-- show the first classroom dialogue (string e58f49c110, replaced via SM_PREVIEW) and screenshot every 20 frames
local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
M.endAt=9000; M.shotEvery=20; M.shotDir="/tmp/smprev"
for f=400,2990,40 do M.press(f,"a",4) end
for f=3000,8900,90 do M.press(f,"a",4) end
for f=600,2900,300 do M.press(f,"start",4) end
for f=2000,2900,200 do M.press(f,"up",30) M.press(f+100,"left",20) end
M.start()
