#!/bin/bash
# robust headless runner: own persistent Xvfb :78, waits for /tmp/mesen_done or Mesen exit
pgrep -x Mesen >/dev/null && kill -9 $(pgrep -x Mesen); sleep 0.5
rm -f ~/.config/Mesen2/mesen.lock /tmp/mesen_done
RUN=$(date +%Y%m%d-%H%M%S)-$$-$RANDOM; RUNDIR=/tmp/smrun/$RUN; mkdir -p "$RUNDIR"
printf 'return {id="%s",dir="%s"}\n' "$RUN" "$RUNDIR" > /tmp/sm_run.lua; echo "$RUNDIR" > /tmp/sm_last_run; echo "RUN_DIR=$RUNDIR"
if ! pgrep -f 'Xvfb :78' >/dev/null; then setsid nohup Xvfb :78 -screen 0 1280x800x24 >/dev/null 2>&1 < /dev/null & sleep 1.5; fi
DISPLAY=:78 /workspace/trinea/tools/mesen/Mesen "$1" "$2" > /tmp/mesen_gui.out 2>&1 &
P=$!; T=${3:-120}
for i in $(seq 1 $((T*4))); do [ -f "${DONEFILE:-/tmp/mesen_done}" ] && break; kill -0 $P 2>/dev/null || { echo "MESEN EXITED early"; break; }; sleep 0.25; done
[ -f "${DONEFILE:-/tmp/mesen_done}" ] && echo "done in ~$((i/4))s"
kill -9 $P 2>/dev/null; true
