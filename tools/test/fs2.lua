local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
SM_M=M; dofile("/workspace/song-master-en/tools/test/smshot.lua")
local SEQ=dofile("/tmp/sm_seq.lua")
M.endAt=SEQ.endAt+5; M.shotEvery=0
local loaded=false
emu.addMemoryCallback(function() if PEND then M.savestate(PEND); PEND=nil end; if not loaded then loaded=true; M.loadstate(SEQ.state or "/workspace/smmenu/field.mss"); M.f=0 end end, emu.callbackType.exec, 0x00836E, 0x00836E)
for _,e in ipairs(SEQ.press) do M.press(e[1],e[2],e[3] or 4) end
local POKE=SEQ.poke or {}
local W=function(a) return emu.read(a,emu.memType.snesWorkRam) end
HITS={}

if SEQ.wrio then WL=io.open("/workspace/smmenu/wrio.txt","w"); emu.addMemoryCallback(function(ad,v) WL:write(string.format("%d %02x\n",M.f or 0,v)); WL:flush() end, emu.callbackType.write, 0x4201, 0x4201) end

for _,a in ipairs(SEQ.wtrace or {}) do emu.addMemoryCallback(function(ad,v) local st=emu.getState(); log2=log2 or io.open("/workspace/smmenu/wtrace.txt","w"); log2:write(string.format("%d w %04x=%02x pc=%02x:%04x\n",emu.getState()["ppu.frameCount"] or 0,ad,v,st["cpu.k"],st["cpu.pc"])); log2:flush() end, emu.callbackType.write, a, a, emu.cpuType.snes, emu.memType.snesWorkRam) end
for _,a in ipairs(SEQ.hits or {0x018091,0x0180a4,0x0180ae,0x0180b8,0x0181fb,0x018251,0x01829f,0x01833c}) do HITS[a]=0; emu.addMemoryCallback(function() HITS[a]=HITS[a]+1 end, emu.callbackType.exec, a, a) end
local RT={}
if SEQ.rtrace then emu.addMemoryCallback(function(a) if M.f>=SEQ.t0 and M.f<=SEQ.t1 then local st=emu.getState(); local k=string.format("%06x",st["cpu.k"]*65536+st["cpu.pc"]); RT[k]=(RT[k] or "")..string.format(" %x",a) end end, emu.callbackType.read, SEQ.rtrace[1], SEQ.rtrace[2], emu.cpuType.snes, emu.memType.snesWorkRam) end
local log=io.open("/workspace/smmenu/pos.txt","w")
M.onFrame=function(f)
 for _,p in ipairs(POKE) do local fr=p[3] or 5; local to=p[4] or fr; if f>=fr and f<=to then local v=p[2]; if p[5]=="or" then v=W(p[1])|p[2] end; emu.write(p[1],v,emu.memType.snesWorkRam) end end
 if SEQ.saveAt and f==SEQ.saveAt[1] then PEND=SEQ.saveAt[2] end
 if SEQ.logflag and f%100==0 then log:write(string.format("F0C14=%02x\n",W(0x0C14))) end
 if SEQ.enc and f>5 then local p=0xf000+W(0xf002)+256*W(0xf003); local n=W(p); if n<8 then for i=0,n-1 do local a=p+1+i*12+4; local v=W(a); if v%4~=3 then emu.write(a,v|3,emu.memType.snesWorkRam); emu.write(a+6,0,emu.memType.snesWorkRam); emu.write(a+7,0x0a,emu.memType.snesWorkRam) end end end end
 if f%25==0 then for a,c in pairs(HITS) do log:write(string.format("%06x:%d ",a,c)) end  log:write(string.format("%d x=%d y=%d map=%02x%02x e48=%02x e5c=%02x 5d=%d,%d\n",f,W(0xd88)+256*W(0xd89),W(0xd8a)+256*W(0xd8b),W(0xe44),W(0xe45),W(0xe48),W(0xe5c),W(0xe5d),W(0xe5e))); log:flush() end
 for _,s in ipairs(SEQ.shots) do if f==s then M.shot(string.format("/workspace/smmenu/out/f%05d.png",f))
  if SEQ.dump then local h=io.open(string.format("/workspace/smmenu/out/w%05d.bin",f),"wb"); local t={}
  for a=0,0x1FFFF do t[#t+1]=string.char(W(a)) end h:write(table.concat(t)); h:close() end end end end
local oe=M.onFrame
M.onFrame=function(f) oe(f); if f==SEQ.endAt then local h=io.open("/workspace/smmenu/rt.txt","w"); for k,v in pairs(RT) do h:write(k.." "..v:sub(1,200).."\n") end h:close() end end

local RI,HOLD=1,0
local function menuUp() return W(0x1AD4C)==66 and W(0x1AD4D)==41 end
local oe2=M.onFrame
M.onFrame=function(f) oe2(f)
 local R=SEQ.react; if not R or f<5 or f<HOLD then return end
 while RI<=#R do local s=R[RI]
  if s[1]=="menu" then if menuUp() then RI=RI+1 else return end
  elseif s[1]=="wait" then HOLD=f+s[2]; RI=RI+1; return
  elseif s[1]=="shot" then M.shot(string.format("/workspace/smmenu/out/r%02d_%05d.png",RI,f)); RI=RI+1
  else local l=s[2] or 6; M.press(f+1,s[1],l); HOLD=f+l+10; RI=RI+1; return end
 end end
for _,e in ipairs(SEQ.execpoke or {}) do emu.addMemoryCallback(function() emu.write(e[2],e[3],emu.memType.snesWorkRam) end, emu.callbackType.exec, e[1], e[1]) end
if SEQ.loghook then local LH=io.open("/workspace/smmenu/hook.txt","w")
 for _,a in ipairs({0x02803E,0x028050,0x028048}) do emu.addMemoryCallback(function() local st=emu.getState(); LH:write(string.format("%d %06x a=%04x x=%04x y=%04x d=%04x\n",M.f or 0,a,st["cpu.a"],st["cpu.x"],st["cpu.y"],st["cpu.d"])); LH:flush() end, emu.callbackType.exec, a, a) end end
if SEQ.force then emu.addMemoryCallback(function() if M.f>=SEQ.force[1] and not FORCED then local st=emu.getState(); st["cpu.a"]=(st["cpu.a"]&0xFF00)|SEQ.force[2]; emu.setState(st); FORCED=true end end, emu.callbackType.exec, 0x028050, 0x028050) end
for _,a in ipairs(SEQ.stk or {}) do emu.addMemoryCallback(function() local st=emu.getState(); local sp=st["cpu.sp"]; local t={}; for i=1,12 do t[#t+1]=string.format("%02x",emu.read(sp+i,emu.memType.snesWorkRam)) end; SL=SL or io.open("/workspace/smmenu/stk.txt","w"); SL:write(string.format("%d %06x a=%04x x=%04x y=%04x db=%02x sp=%04x %s\n",M.f or 0,a,st["cpu.a"],st["cpu.x"],st["cpu.y"],st["cpu.dbr"] or 0,sp,table.concat(t," "))); SL:flush() end, emu.callbackType.exec, a, a) end
if SEQ.dr then local oe3=M.onFrame; M.onFrame=function(f) oe3(f); if f>=SEQ.dr[1] and not DRD then DRD=1; local h=io.open("/workspace/smmenu/dr.bin","wb"); local t={}; for a=SEQ.dr[2],SEQ.dr[3]-1 do t[#t+1]=string.char(W(a)) end; h:write(table.concat(t)); h:close() end end end
M.start()
