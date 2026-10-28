# Findings — Song Master (Japan)

ROM: 1,048,576 bytes, no copier header. CRC32 4FA5FC25, MD5 568BD0C48ACBA2109C8097A23D4C1167 (checked locally; the ROM is not in this repo).

## Internal header (file 0x7FC0, LoROM)
| field | value |
|---|---|
| title (0x7FC0) | `SONG MASTER` (padded to 21 bytes) |
| map mode (0x7FD5) | 0x20, LoROM / SlowROM |
| cart type (0x7FD6) | 0x02, ROM + RAM + battery |
| ROM size (0x7FD7) | 0x0A, 1 MiB (8 Mbit) |
| SRAM size (0x7FD8) | 0x03, 8 KiB |
| region (0x7FD9) | 0x00, Japan |
| maker (0x7FDA) | 0x1A |
| version (0x7FDB) | 0x00 |
| checksum complement / checksum | 0x00CD / 0xFF32 (matches the computed sum 0xFF32, so the ROM is valid) |
| vectors | emulation RESET $8000; native NMI $836E; every other vector points to $FFBF |

## Text encoding
- One byte per character. Hiragana 01-34, katakana 35-6B, 6E = dakuten (゛) and 6F = handakuten (゜), both placed **before** the base kana, Latin A-Z 80-99, punctuation and a few kanji from 9A up.
- 70 = 『 (opening quote), FE = line end, FF = end of string. FD xx is a control code (speaker or name, window, wait, etc.; full list not decoded yet).
- A community .tbl (MrRichard999, Shift-JIS) was used locally only. It is not redistributed.

## Uncompressed menu text
- Battle command menu: plain bytes around file 0xAE90-0xAFFF (bank $01), repeated for each party layout.
  The commands are たたかう / マジック / アイテム / いどう / ぼうぎょ / にげる, separated by FE and ending with FF.
- `tools/py/findmenu.py TBL` lists FE/FF-terminated runs of table characters (many false positives; filter by region).
  `findscripts.py` (inherited) is Trinea-specific and is not applicable here.

## Dialogue: LZSS-compressed, decompressed to WRAM
Traced headless with Mesen2 under Xvfb (`tools/mesen/*.lua`, via trinea `mesen_run.sh` and `mesen_lib.lua`).
The first school scene (先生「またかね!? ユーリ・・・。」, around frame 3000 with the scripted input) was used as the test case.

1. **Loader** `$00:E9CA` (A = block number, X = destination address): sets D = $0420 and the destination [$04] = $7E:X.
   It then reads the word at `$00:EC59 + 2*A`, a block table of (index, bank) pairs: 00/03, 01/03 … 0E/03, 00/04 …,
   and calls `JSL $00:C1A4`. There are 78 block entries (banks $03-$06, 153,276 bytes once decompressed).
2. **Decompressor** `$00:C1A4` (helper `$00:C17C`): sets D = $0420 and DB = bank `$01`.
   It reads the pointer `bank:8000 + 2*index` into Y, and the source is read with `LDA $0000,x` (DB = ROM bank).
   - Header word: bit 15 = compressed (if clear, `BRL $C27D` takes the stored/raw path). Output length = (w & 0x7FFF) + 1.
   - Flag byte, 8 flags read LSB first. 1 = literal: `STA [$04],y` to the WRAM destination, plus a copy into the ring at `$7F:F000,x`.
   - 0 = back-reference word w: source = w & 0x0FFF (absolute position in the 4 KiB ring at $7F:F000), length = 2*(w>>12) + 3 (3..33, odd only).
     Bytes are copied ring → [$04],y and back into the ring. The ring write pointer starts at 0, and the ring is not cleared.
3. The test scene's block is bank 03 index 04, decompressed to **$7E:7800** (2,902 bytes).
   `tools/py/lzss.py 03 04` reproduces WRAM $7E:7960.. byte for byte (`2F 01 FD 20 … 70 1F 10 06 18 74 75 …` = 『またかね!?).
4. **Display**: the window routines in bank $02 (`$02:AE33`/`$02:AE58` read the string at $7E:7960…; `$02:B0xx`-`$02:BFxx`)
   write tilemap entries into the WRAM buffer $7E:4680-$7E:4E7F (for example $7E:4A82…).
   The NMI-side routine at `$00:86B5` copies it to VRAM with DMA channel 0 (mode 1, $2118/9, source $7E:xx80) every frame.
   The character-name list sits at $7E:D200 (FF-separated) and is read by `$02:B104`.

## Next
- Decode the FD control codes and the speaker/name references; dump all 78 blocks to build/jp (never committed).
- Write an LZSS compressor (or a raw-block path via bit 15 = 0) for re-insertion; check the size limits per bank.
