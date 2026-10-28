local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
M.endAt=3110
for f=400,4900,40 do M.press(f,"a",4) end
for f=600,4900,300 do M.press(f,"start",4) end
for f=2000,4900,200 do M.press(f,"up",30) M.press(f+100,"left",20) end
local L=io.open("/workspace/songmaster/work/t7.log","w")
emu.addMemoryCallback(function() local t={} for a=0x420,0x426 do t[#t+1]=string.format("%02X",emu.read(a,emu.memType.snesMemory)) end
 local s=emu.getState(); local sp=s["cpu.sp"]; local r={} for i=1,6 do r[#r+1]=string.format("%02X",emu.read(sp+i,emu.memType.snesMemory)) end
 L:write(string.format("f%d C1A4 dp420=%s stack=%s\n",M.f,table.concat(t," "),table.concat(r," "))) end, emu.callbackType.exec, 0x00C1A4,0x00C1A4)
M.onFrame=function(f) if f==3100 then L:close() end end
M.start()
