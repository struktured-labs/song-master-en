# Song Master — English translation (work in progress)

Goal: a complete English translation patch for **Song Master** (ソングマスター, Yanoman, 1992, Super Famicom).

**Status: playable draft.** 1738 of 2156 script strings are translated (about 81%); the rest are data junk, quote-only ops or untranslated ids (see TRANSLATION_NOTES.md). Checked in an emulator (Mesen2): main menus (Items, Magic, Equip, Status, Save, name entry), battle command window, battle Item list, spell/damage messages, the boot splash and the English prologue crawl. Shops and the shrine cure (ailment) menu have not been checked on screen yet.

### Extras
- **Boot splash**: struktured labs logo (`asm/splash.asm`, bank $3B); Start skips it.
- **Prologue crawl**: the intro text is a pre-drawn 1bpp bitmap; the English version is rendered by `tools/py/prologue.py` from `assets/prologue_en.txt` into `asm/prologue.bin` (bank $3A).
- **Rumble** (trinea/RCR rumble protocol on controller port 1): pulses scale with damage to the party, a long pulse on KO, a short tick on enemy hits. Hooks: joypad reader 00:E07A, damage applier 15:81A7, code at $3F:C000, RAM 7E:97F8-97FA. Verified in emulator only (packets logged), not yet on hardware. Pads without rumble ignore it.

### Test harness (not shipped; lives outside the repo)
Headless Mesen2 under Xvfb with Lua scripts: a field save state plus scripted presses, forced encounters, menu-aware waits (`react` steps wait until the battle command window is on screen), WRAM pokes, write traces (`wtrace`) and $4201 logging (`wrio`).

## Required ROM
No-Intro `Song Master (Japan).sfc`, headerless, LoROM, 1 MiB (8 Mbit)
- CRC32 `4FA5FC25`
- MD5 `568BD0C48ACBA2109C8097A23D4C1167`

This repository contains **no ROM data**. Supply your own legally obtained dump.

## Build
```
tools/build.sh "/path/to/Song Master (Japan).sfc"
```
Verifies the ROM hash, fetches/builds asar and Flips (tools/get_tools.sh), applies `asm/main.asm`, writes `build/songmaster_en.ips` and `build/songmaster_en.bps`.

## Layout
- `tools/build.sh`, `tools/get_tools.sh` — build pipeline (from Trinea DX)
- `tools/py/` — dump/insert templates, `dis65816.py`, `findscripts.py` research tools
- `docs/FINDINGS.md` — reverse-engineering notes

## License
Code: MIT (see LICENSE). Translation text/assets: license TBD.

## Credits
- struktured — hacking, tools
- Prior work by other community members will be credited here once permission is confirmed.
