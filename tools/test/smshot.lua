-- Unique capture paths: every screenshot goes to /tmp/smrun/<RUN>/<RUN>_<basename>; a path is never reused.
-- RUN is created per run by mesen_run_sm.sh (written to /tmp/sm_run.lua).
local M=SM_M
local R=dofile("/tmp/sm_run.lua")
local raw=M.shot
M.shot=function(name)
  local b=name:match("([^/]+)$")
  local p=R.dir.."/"..R.id.."_"..b
  local h=io.open(p,"r"); if h then h:close(); error("capture path reused: "..p) end
  raw(p)
end
M.RUN=R
return R
