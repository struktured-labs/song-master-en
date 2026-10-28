-- load field.mss then run SEQ inputs (relative frames), shots at SHOTS
local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
local SEQ=dofile("/workspace/smmenu/seq.lua")
M.endAt=SEQ.endAt+5; M.shotEvery=0
local loaded=false
emu.addMemoryCallback(function() if not loaded then loaded=true; M.loadstate("/workspace/smmenu/field.mss"); M.f=0 end end, emu.callbackType.exec, 0x00836E, 0x00836E)
for _,e in ipairs(SEQ.press) do M.press(e[1],e[2],e[3] or 4) end
local POKE=SEQ.poke or {}
M.onFrame=function(f) if f==5 then for _,p in ipairs(POKE) do emu.write(p[1],p[2],emu.memType.snesWorkRam) end end for _,s in ipairs(SEQ.shots) do if f==s then M.shot(string.format("/workspace/smmenu/out/f%05d.png",f)) end end end
M.start()
