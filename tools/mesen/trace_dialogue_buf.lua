local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
M.endAt=3110
for f=400,4900,40 do M.press(f,"a",4) end
for f=600,4900,300 do M.press(f,"start",4) end
for f=2000,4900,200 do M.press(f,"up",30) M.press(f+100,"left",20) end
local L=io.open("/workspace/songmaster/work/t6.log","w"); local seen={}
emu.addMemoryCallback(function(a,v) local s=emu.getState(); local k=string.format("%02X%04X",s["cpu.k"],s["cpu.pc"])
  local e=seen[k]; if not e then L:write(string.format("f%d W %s %06X=%02X\n",M.f,k,a,v)); seen[k]={M.f,a} end end, emu.callbackType.write, 0x7ED200,0x7ED5FF)
emu.addMemoryCallback(function(a,v) local s=emu.getState(); local k="b"..string.format("%02X%04X",s["cpu.k"],s["cpu.pc"])
  if not seen[k] then L:write(string.format("f%d W %s %06X=%02X\n",M.f,k,a,v)); seen[k]=1 end end, emu.callbackType.write, 0x7E7960,0x7E79A0)
M.onFrame=function(f) if f==3100 then local t={}
  for a=0x7ED200,0x7ED40F do t[#t+1]=string.format("%02X",emu.read(a,emu.memType.snesMemory)) end
  L:write("D200 "..table.concat(t," ").."\n"); t={}
  for a=0x7E7960,0x7E799F do t[#t+1]=string.format("%02X",emu.read(a,emu.memType.snesMemory)) end
  L:write("7960 "..table.concat(t," ").."\n"); M.shot("/workspace/songmaster/work/f3100.png"); L:close() end end
M.start()
