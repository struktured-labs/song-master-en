# Findings

Target: Song Master (Japan), LoROM, 1 MiB, CRC32 4FA5FC25, MD5 568BD0C48ACBA2109C8097A23D4C1167.
Expected internal header at file offset 0x7FC0 (LoROM).

## Status
- ROM not yet available on the research machine; header parse and dialogue-decompressor trace pending.

## Plan
1. Verify hashes; document header (title, map mode 0x7FD5, ROM/SRAM size, checksum).
2. Run headless Mesen2, breakpoint on writes to the text window in WRAM/VRAM, walk back to the read routine.
3. Disassemble with tools/py/dis65816.py; locate script pointer tables with tools/py/findscripts.py.
