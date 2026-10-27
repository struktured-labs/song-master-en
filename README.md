# Song Master — English translation (work in progress)

Goal: a complete English translation patch for **Song Master** (ソングマスター, Yanoman, 1992, Super Famicom).

**Status: research.** Script format, dialogue compression and font are being reverse-engineered. No playable patch yet.

## Required ROM
No-Intro `Song Master (Japan).sfc`, headerless, LoROM, 1 MiB (8 Mbit)
- CRC32 `4FA5FC25`
- MD5 `568BD0C48ACBA2109C8097A23D4C1167`

This repository contains **no ROM data**. Supply your own legally obtained dump.

## Build
```
tools/build.sh "/path/to/Song Master (Japan).sfc"
```
Verifies the ROM hash, fetches/builds asar and Flips (tools/get_tools.sh), applies `asm/main.asm`, writes `build/songmaster_en.ips`.

## Layout
- `tools/build.sh`, `tools/get_tools.sh` — build pipeline (from Trinea DX)
- `tools/py/` — dump/insert templates, `dis65816.py`, `findscripts.py` research tools
- `docs/FINDINGS.md` — reverse-engineering notes

## License
Code: MIT (see LICENSE). Translation text/assets: license TBD.

## Credits
- struktured — hacking, tools
- Prior work by other community members will be credited here once permission is confirmed.
