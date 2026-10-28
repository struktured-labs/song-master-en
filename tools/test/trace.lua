local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
local SEQ=dofile("/workspace/smmenu/seq.lua")
M.endAt=SEQ.endAt+5; M.shotEvery=0
local loaded=false; local on=false; local seen={}
emu.addMemoryCallback(function() if not loaded then loaded=true; M.loadstate("/workspace/smmenu/field.mss"); M.f=0 end end, emu.callbackType.exec, 0x00836E, 0x00836E)
emu.addMemoryCallback(function(addr,val) if on then local k=addr; if not seen[k] then seen[k]=emu.getState()["cpu.pc"] or 0 end end end, emu.callbackType.read, 0x7E0B00, 0x7E1FFF)
for _,e in ipairs(SEQ.press) do M.press(e[1],e[2],e[3] or 4) end
M.onFrame=function(f) if f==SEQ.t0 then on=true end if f==SEQ.t1 then on=false
 local h=io.open("/workspace/smmenu/trace.txt","w"); for k,v in pairs(seen) do h:write(string.format("%06x %s\n",k,tostring(v))) end h:close() end end
M.start()
