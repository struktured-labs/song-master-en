local M=dofile("/workspace/trinea/tools/mesen_lib.lua")
local S=dofile("/tmp/wk.lua")
M.endAt=S.endAt or 6000; M.shotEvery=0
local W=function(a) return emu.read(a,emu.memType.snesWorkRam) end
local loaded=false
emu.addMemoryCallback(function() if not loaded then loaded=true; M.loadstate(S.state); M.f=0 end
 if S.save and M.f==S.save[1] then M.savestate(S.save[2]) end end, emu.callbackType.exec, 0x00836E, 0x00836E)
local log=io.open("/tmp/wk_log.txt","w")
local i,busy,t0=1,0,0
M.onFrame=function(f)
 local x=W(0xd88)+256*W(0xd89); local y=W(0xd8a)+256*W(0xd8b)
 if f%20==0 then log:write(string.format("%d step=%d x=%d y=%d map=%02x%02x\n",f,i,x,y,W(0xe44),W(0xe45))); log:flush() end
 if f%120==0 then local t={} for k=1,12 do local e=0xd84+12*k; if W(e+1)+W(e+2)+W(e+3)>0 then t[#t+1]=string.format("%d:%d,%d",k,W(e+4)+256*W(e+5),W(e+6)+256*W(e+7)) end end log:write(f.." npcs "..table.concat(t," ").."\n") end
 if f%(S.every or 30)==0 then M.shot(string.format("/tmp/wk/f%05d.png",f)) end
 if S.dump and f==S.dump[1] then local o=io.open(S.dump[2],"wb"); for a=0,0x1fff do o:write(string.char(W(a))) end o:close() end
 if f<(S.start or 60) or f<busy then return end
 local s=S.steps[i]; if not s then return end
 if t0==0 then t0=f end
 local k=s[1]; local done=false
 if k=='talk' then local e=0xd84+12*s[2]; local nx=W(e+4)+256*W(e+5); local ny=W(e+6)+256*W(e+7)
  local side=s[4] or 'below'; local tx,ty,face=nx,ny+16,'up'
  if side=='above' then ty=ny-16; face='down' elseif side=='left' then tx=nx-16;ty=ny;face='right' elseif side=='right' then tx=nx+16;ty=ny;face='left' end
  local dx,dy=tx-x,ty-y
  if s.lx and math.abs(s.lx-x)<=1 and math.abs(s.ly-y)<=1 then s.stuck=(s.stuck or 0)+1 else s.stuck=0 end; s.lx,s.ly=x,y
  if (s.stuck or 0)>=2 and math.abs(dx)<=4 then dy=0 elseif (s.stuck or 0)>=2 then s.stuck=0; s.alt=not s.alt end
  if s.alt and math.abs(dx)>4 then M.press(f+1,dx>0 and 'right' or 'left',8); busy=f+10; if math.abs(dy)<=4 then s.alt=false end return end
  if f-t0>(s[3] or 600) then done=true; log:write(f.." talk timeout\n")
  elseif math.abs(dx)>4 and (side=='left' or side=='right' or math.abs(dy)<=4 or s.phase=='x') then M.press(f+1,dx>0 and 'right' or 'left',math.min(8,math.max(1,math.abs(dx)//2))); busy=f+10
  elseif math.abs(dy)>4 then M.press(f+1,dy>0 and 'down' or 'up',math.min(8,math.max(1,math.abs(dy)//2))); busy=f+10
  elseif math.abs(dx)>4 then M.press(f+1,dx>0 and 'right' or 'left',math.min(8,math.max(1,math.abs(dx)//2))); busy=f+10
  else M.press(f+1,face,2); M.press(f+6,'a',4); busy=f+40; done=true; log:write(string.format("%d talked npc %d at %d,%d\n",f,s[2],nx,ny)) end
 end
 if k=='A' or k=='B' or k=='start' then M.press(f+1,string.lower(k),4); busy=f+(s[3] or 30); s[2]=(s[2] or 1)-1; done=s[2]<=0
 elseif k=='wait' then busy=f+s[2]; done=true
 elseif k~='talk' then local d={L='left',R='right',U='up',D='down'}
  local cur=(k=='L' or k=='R') and x or y
  if (k=='L' and cur<=s[2]) or (k=='R' and cur>=s[2]) or (k=='U' and cur<=s[2]) or (k=='D' and cur>=s[2]) or f-t0>(s[3] or 400) then done=true
  else M.press(f+1,d[k],8); busy=f+9 end end
 if done then log:write(string.format("%d done step %d %s x=%d y=%d\n",f,i,k,x,y)); i=i+1; t0=0 end
end
M.start()
