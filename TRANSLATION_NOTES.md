# Translation notes
Authoring: script/en/t_bNN.txt. `>uid` starts a string; `@X:` = speaker line ([wait]X[tab][n]); `{N}` = party name N; `~` = [wait]; newline = [n]; other [tags] literal. Terminator is kept from the original.
Window: about 22 visible columns, 4 rows; long lines are auto-wrapped at 24 by the encoder. Check this in the emulator.
## Doubtful lines
- b01 db70364501: Ahharu shouts "ユ・リ・ア・ン". Rendered as "Yurian". Need to confirm whether this is the hero's true name or a different character.
- b01: the FD10:xx codes inside the cutscene (likely sound/effect cues in this context) were kept in roughly the same positions.
- b01 ab565f48b9: "フォーン" is romanized as "Fone" (tentative).
- Authoring: a line starting with a space continues the previous line and gets reflowed (24 cols; [nameN] counted as 6). Lines without a leading space are hard breaks. `%X:` = coloured speaker header, `^N` = coloured party name, `+` = join with no newline, `!` after uid or `nowrap` in the file name = no auto-wrap.
- Wrap width: the window is 24 columns (cols 4-27, wrap limit $0F=1C), and this matches the screenshots. 24 is kept.
- b02/b03 (system/battle messages): the battle window width has NOT been verified in the emulator yet. Lines are kept to 28 chars or fewer, single line, as in the JP.
- b02 name-entry kana grids are left as-is (tile layouts).
- Term-list fragments (FD0F:28 ありがとう, 29 わたしは, 3D ・・・ etc.) are inlined as English where possible. The b00 list will be translated separately.
- b05 40cde41361: the hero's surname フェルム is rendered "Ferm" (tentative).
- b05 3899c61324: the ranks are Bard < Singer < Song Master.

## Word lists (FD0E-FD12)
- Dialogue codes FD0E places / FD0F terms / FD10 items / FD11 magic / FD12 monsters now read from English tables in ROM bank $3C (asm `lh_*`, built from `script/en/lists.json`; lists not yet translated fall back to the JP bytes). The JP lists at $7E:D000 are untouched (other code may use them; the RAM after them is in use, so they can't grow).
- Encoder: `[0C]` (new window page) resets the wrap column; list codes count as their English length.
- Visual check: `tools/test/preview.sh UID out.png` puts any string into the first classroom line and makes a contact sheet. Viewed: 07e5149dcc (b09 Robinton/Ferion scene) - wraps cleanly, list dots render as "...".
- Doubtful: 3446a4b544 (Devi choice menu, keeps "-・" prefix); 44396273ce replaced FD0F:2A with plain text; Fern/Exelion/Amsia romanizations tentative.
- Items/magic/monsters lists translated for dialogue use (menus/battle still use their own JP data; to do). Tentative: マーダー Murder, ギルボアール Gilboal, ショックルーゼス Shock Ruses, シャーウットボウ Sha-Wood Bow, レーザープロット Laser Plot, パブロフ Pavlov, ヒベモス Hibemoth.

## b10 notes
- Term FD0F:08 (ギョ-ム) is only ever used as the currency unit; menus show "G", so it is rendered "G" with no space ("500G").
- The Tiris Noah broker speaks Kansai dialect; rendered as a folksy merchant ("ain't", "ya").
- Menu option-id bytes before the choice text are kept as raw [xHH] tags (new encoder tag).
- d0795837b5 (b07 drink menu) is now translated with the raw-byte prefix.

## b22-b29 notes
- Password (b24 menu / b25 hint): JP 『アルバイトをみつけるなら?』; menu and hint both use "Want to find work?" so they match. Menu options shortened to fit the window.
- FD0F:1F (fairy, ようせい) is reused in b26 as a pun for 要請 "request"; written as plain English. Likewise "200 grams" built from monster-list codes [FD12:C8][FD12:16]ム, written plain.
- FD12:C8 + "0" renders "2000" (monster list entry 0xC7 is the string "200"); kept as code in the broker's fee line.
- FD0F:2E in the temple (b23 fc00be5eeb) still left as code; meaning unconfirmed.

## Visual checks (headless Mesen2, viewed)
- Preview runner fixed: tools/test/mesen_run_sm.sh (own Xvfb :78, completion = last screenshot file, 3 retries) because the shared /tmp/mesen_done flag ended runs early.
- Viewed OK: 3b7531f6c0 (b25), 6309683778 (b26 long news), bf7845035e (b17 King Orin), d77b744ae7 (b21, item Circlet renders).
- Viewed OK: 3d133e958c (b12, item [Introduction] renders), 74892dd59f (b25 Nimens history). b12 trailing quote continues into the next string (same as JP).

## b41-b45 notes
- King Colman ([FD0F:0B]) is king of Marsha and father of Selena (elder, royal priestess) and Leticia (younger, captain of the royal guard). Late queen: Rianna.
- [FD12:3A] "Lamia" (monster list) is also the name of the panther-shifter woman (lycanthrope). Sam = King Eric of Farlon undercover; Eleus = "Baron Goza", his uncle.
- b44 informant menu aa86a72fc4 translated with prefix [x4D][x4F][x4C].
- Viewed: cfa90e6a19 (b36), 8768f51943 (b44) - clean wrapping.

## FD0F dictionary fragments (fixed e.g. in b58 review)
FD0F:28/29/2A/39 are JP compression fragments ("thank you", "I am", "you are", "you see."), NOT names.
Earlier blocks used them as pronoun placeholders, producing "I am cannot", "I am intend" etc.
All uses replaced with plain English across t_b*.txt (verified visually on Uther's death scene).
Avoid FD0F:28-2A, 39-43 in English; write the text out.

## b58-b65 notes
Re-read against the dump. The "ancient Marsha Empire" (こだい[FD0E:42]てい国) is literal per the game, kept.
Fern (フェルン) is tentative. Uther (FD0F:02) is high priest of Elles Noah's temple of Fariga.

## Code audit (all t_b*.txt)
Every FD0E/FD0F code in the English script was checked against WORDLISTS.md (full decoded lists).
Fixed: b45 "explain[FD0F:38]" (=let's do that) -> "Let me explain."; b01 FD0E:00/FD0F:00 (index 0, no list entry) removed;
b32 literal "[Cyan ...]" bracket now [xA4]/[xA5]. Phrase codes FD0F:2C-37 (shop/inn greetings) used only where the JP uses them.
Rule: before using any FDxx code, look it up in WORDLISTS.md.

## b69 notes (Tiamat)
Translating b69 replaced its strings with 5-byte pointers; block 69 now fits 0x1800 (no blocks over).
Names: Sirius (シリウス, unit 0007), Hilda (name9), Galactic Emperor Julian Siegfried (ユリアン・ジークフリード, 1138th),
Alan Siegfried (アラン), Avalon (アヴァロン, the planet), Matrix/Matrices, Corridor of Memory (きおくのかいろう),
First Jihad (ファースト・ジハード), King Kane (ケイン王, = St. Kane of b04/b05), Holy Songs (詩聖か; doubtful reading).
FD0F:0E = "System" (control system); FD0E:3E Fone (fortress), 35 Christ (town; consider "Krist"?), 36 North Shield.
Doubtful: "Christ" place name from the list; may want a rename.

## b46-b57 notes
- b46-53: Lismore, the Troll, Laura; Northumbria/Durham dwarves. Data/junk strings (D..., お___計) skipped as in all blocks.
- b54-57: Durham castle, Haydle's plot, the mine, King Rimbelt, Orb lost, Nordleborl Forest, Great Wall. Spellings of Haydle/Nordleborl are tentative (no GameFAQs source found).

## b74-b77 notes
- b74: Croixdor fortress, Ragnas duel, Lamia (FD12:3A) dies, Nimens (name2) dies, Fone activates. Previewed db4bc32c49, c7fb7f355c.
- b75: Ragnas betrays King Xenon (FD12:EB王 -> "King [FD12:EB]"), takes Ahharu's power, Ahharu possesses him. ユリアン = Julian (the emperor of b69); b01 "Yurian, DIE!!" changed to "Julian" to match. Previewed 4523a20bc3.
- b76-77: Meritus/Singer Guild, McPherson's mansion, Ferion (name8) dies, voyage to Elles Noah with Selena, sea monster. Previewed 8519988b89.
- Known cosmetic issue: a continuation line after a line ending in an FD0F ellipsis code ([FD0F:3D] etc.) renders with no 1-space indent (seen in pv_8519988b89 "You hold a wonderful"). Harmless.

## UI (bank 01/02) — script/en/menus.json, script/en/ui_inplace.json
- Field menu: たいけい shown as "Lineup" (Formation overflowed the 8-cell window).
- Battle command windows (01:AE8D table, 10 lists): Fight/Magic/Item/Move/Guard/Run. Battle magic: Spirit/Heal/Summon (Summon relocated into the freed battle-list bytes).
- Status ailments (02:B512): KO/Poison/Conf/Cryst/Sleep/Bind/Fear. DOUBTFUL: すいしょう rendered "Cryst" (crystal?), unverified in play.
- Status screen: Atk Pwr/Def Pwr/Speed/Rhythm/Weapon/Shield/Armor/Helm; equip screen uses Atk/Def/Spd/Rhy (4-cell limit before the number).
- Gold window: お金 label is drawn by code (02:8E50 area / shop) as two tiles; blanked, amount keeps its "G".
- FIXED: the red garbage strip on the status/equip screens was OUR bug, not an emulator artifact. The untouched JP ROM (same inputs from boot, /workspace/jp_status.png) shows no strip and prints the equipped item name there. Cause: the menu-side list lookups $02:B0A0/B0BF/B0DE JSR into the middle of the script-side routines our lh_* hooks overwrite. Now redirected (asm lhm_*) to 8-cell short names in bank $3D (script/en/lists_short.json); dialogue keeps the full names.
- Item/magic short names are abbreviated to the 8-cell JP limit (e.g. LthArmor); review wording later.
- Config screen verified (Text Speed Slow/Fast, Sound Stereo/Mono).
- Viewed on screen (field.mss harness, 2026-10-27): main menu, Magic (Spirit/Healing/Summon, MP Cost, Fireball), Equip (Atk/Def/Spd/Rhy, Weapon/Shield/Armor/Helm, LthArmor, Equip/Remove), Save (EMPTY slots, Yes/No), name-entry Latin page row 9 + End.
- Not yet verified on screen: battle windows, shop, ailment names.

## Untranslated-id audit (172 ids flagged by a dump-vs-translation diff)
- b01 ids 1-18: staff credits, already uppercase ASCII in the ROM, render natively; no translation needed.
- b02: the three name-entry pages (katakana 0x156, hiragana 0x238, Latin 0x311) - now replaced in place via script/en/raw_inplace.json (same cell geometry; hiragana page = a-z, digits, punctuation; "End").
- Everything else: parser false positives (data bytes read as text: 'D中あああ…ヨヨヨ', 'お      計', 'あくおき' etc.), and lone 「 strings (the opening quote is split off into its own op; byte 0x70 already renders as '"' in the EN font, so they need no change).

## Item/armor names: 8-char abbreviations kept (decision)
- Narrow-glyph pair / ligature tiles were considered: only ~23 free tile codes (old hiragana 1E-34), while ~134 long names would need ~5 distinct pair tiles each. A VWF would require rewriting the window renderer. Abbreviations are the more robust choice; they are polished by hand in lists_short.json.

## Test-only WRAM map (for Mesen Lua pokes; never shipped)
- Names 7E:0AF8 (16 bytes each); stats records ~7E:0A08; gold 7E:0B7A (24-bit LE); inventory = one count byte per item, indexed by item: 7E:0BDE + (list index - 97) for list items 97..150 (Nitron 0BDE, HiNitron 0BDF, Pavlov 0BE0, Darts 0BE1, Temp. Permit 0C0E). The old "(id,count) pairs" note was wrong.

## FIXED: FD0E place names froze dialogue (since f6e683e)
- asar assembled `BRA $02B09A` at $02:B08F as `80 9A` (jumped to $02:B02B), so every dialogue line using an FD0E place name stopped right after the name. Now emitted as `db $80,$09`. Verified on screen after the fix: b26 90a909543c, b76 0ef7c92c79, b77 84c5631acf / 07d2ab3f5b / e60481ecda (pv/fixgrp.png).

## b75-b77 full preview pass (Oct 28)
- All 63 translated message ids in b75-b77 previewed headless (13 + 30 + 20), sheets in /workspace/pv. Untranslated ids there are data junk or lone 「 opening quotes (render as '"'), not text.
- Preview sheets keep only stable frames, so some mid-scroll pages are not captured; the text source was cross-checked for those.
- Doubtful: b75 68868c41fc "The one who rules you is... m... e..." (JP stutters わ・・たし・・だ, "it's... m... e"); kept.

## Short-name polish (2026-10-28)
PrgBlade->PurgeBld, ChsBlade->ChaosBld, TrrBlade->TerrorBl, CrssHelm->CrossHlm, FrcHelm->ForceHlm, SylphRb->SylphRob, MdsShld->MedusaSh, MirrImg->MirrorIm. SylphRob viewed on the Equip screen (test-only WRAM poke of 7E:0A1D). Kept: SclArmor, ChnMail, ThdArmor (consistent with LthArmor etc.).

## Battle / shop access (not yet verified)
- Tiris Noah: leaving town is gated ("You can't leave town without Permission." viewed), so no random encounters from the post-intro save state.
- Field actor table: 12-byte records from 7E:0D88 (player x = 0D88, 16-bit pixel; followers at 0D94, 0DA0, 0DAC). The y offset is not confirmed yet.
- Shop counter in Tiris Noah not reached by blind scripted walking; needs y-coordinate or a later save state.

## FD0E re-check sample (2026-10-28)
9 previews of lines with distinct place ids across blocks after the fix (uids 499608c97b 2a21fa8f9c 939d6e4ed9 3703c0a8c8 dba3221193 cc2261179c df88f450d8 88e3619a43 aa9623de11). Viewed text continuing past names: Lancafarn / Mt. Barama, Albion, Farlon / Barnicia, Tir na Nog, Great Wall, North Shield. Not all 282 FD0E lines individually previewed.

## Draft delivered 2026-10-28 (build of d195e36, sfc sha1 cefd7596...)

## Battle list names (bank 01)
Battle code in bank $01 reads the JP item/monster/magic lists straight from WRAM 7E:D000
(items +0x430, monsters +0x951, magic +0xF7F). insert_sm.py now writes English copies to
bank $2D (D000 items, DA00 monsters, F000 magic) and repoints the LDX/LDA long operands.
Verified in a forced battle (test-only encounter-zone poke): spell message "Fireball",
target window "Man-Eater H·P 240", Magic submenu "Spirit/Heal/Summon".
Known: a single varying glyph (ュ/リ/る) appears after the spell name in the cast message;
it also appears in the untouched JP ROM, changes frame-to-frame, likely an animated tile
sharing VRAM with the text window. Not a text issue.
Fixed: lowercase "p" redrawn with a rounded bowl + descender (was a square P-like shape); verified in battle "Spirit".

## Prologue crawl (boot intro)
- Source: LZSS block 19:00 (9216 bytes = 1152 1bpp 8x8 tiles), loaded by 00:C755 `ldx #$1900` -> 7F:0000, shown on BG3 (tilemap $4800).
  Layout: 24 lines x 12 cells of 16x16; line L cell c = tiles 48L+4c..+3 (TL,TR,BL,BR).
- JP text was read off the decoded bitmap (not memory) and translated in assets/prologue_en.txt.
- tools/py/prologue.py renders it (DejaVu Sans 11px, 1bpp) to asm/prologue.bin; stored raw (header bit15=0) at $3A:8000; the loader is repointed to bank $3A idx 0.
- Viewed in Mesen: full crawl from first line to "the Song Master." scrolls correctly over the landscape.
- Names: ティリス = Tiris (the island capital; town is Tiris Noah), ケイン王 = King Kane, 聖詩歌 = Holy Songs, 光の神 = God of Light, 聖戦 = Holy War.

## Session 2026-10-28 (late)
- Battle Item list VIEWED (menu-aware harness): Nitron, HiNitron, Pavlov, Darts, PsnDarts, FireDart, BombDart, FlshDart with counts. Counts there were affected by a test poke at 7E:0BDE, so the odd values (x28, x21) are test artifacts; "x02" vs "x 2" spacing not compared against JP yet (doubtful).
- Ailments: the status screen shows ailments as icons (no text). The only ailment *text* is the shrine cure menu (02:B49D, names via table 02:B512, prices $78-$7A); not reached on screen. A brute-force poke of every byte of Yury's battle struct ($1000-$102C) changed only HP, so the battle ailment byte is elsewhere.
- Script interpreter: op dispatch 02:8074 jmp ($8077,x). Story flags: base 7E:0C14, MSB-first bits (flag n = byte n/8, mask $80>>(n&7)); test at 00:BEF2. Op 0B n = set flag?, 0D n L = goto L if flag n clear.
- Gate: b05 label $32 "You can't leave town without permission" (label $33 shows it). Flag 6 (7E:0C14 mask $02) is set only in b07 when the player is handed a pass to show the sailors, so the way out is the harbor. Not yet reached: scripted walking found the east bridge guard (different line: "Sir! You can't just walk in here"), not the harbor.
- Remaining 418 untranslated string uses (172 ids) all classified in docs/untranslated_ids.md: credits 18, name-entry 4, control-only 158 uses, term-list refs 37 uses (English via lists.json), data junk 136 ids / 201 uses. No real dialogue left untranslated.

## Session: harbor / shop / clinic pass
- Flags are 1-based (00:BEF2 does `dec a`), base 7E:0C14; flag n = byte (n-1)/8, mask $80>>((n-1)&7). Flag 6 = 0C14 mask $04. Script op `0d f L` = goto L if flag f SET.
- Dock guard (b05 lbl 29/2a) verified on screen; with flag 6 + [Boarding Pass] the ship sails to the world map.
- Test harness: smmenu/mk.py forces any block/label (poke 054A=block, 0C91=FF, set A at 02:8050). Labels in b07 other than 01/0a mostly fall through to the pass-holder branch, so coverage from forcing is limited.
- Clinic (b07 lbl 01, op 21) verified: Treat/Medicine/Leave and KO/Poison/Conf ailment lines with prices.
- Shop quantity box: JP 合計 (02:8DC5, 02:BB72) replaced by "Cost" via JSL to $3FD000; the counter glyph コ (lda #$243E / sta $481A at 02:BBA3) blanked. Verified on screen.
- Terms shortened to fit 24 cols: 0x2D, 0x2E, 0x30, 0x36. 0x2E/0x30 verified on screen; 0x2D/0x36 not yet seen.
- Forcing b07 label 04 shows garbage "b%dd2cbP a0": likely a non-text label hit by forcing (unverified vs JP; the JP ROM crashes with this harness walk).

## Session: sell/medicine/inn + popup widths
- Real label ids per block come from tools/py/sm_script.py parse(load(b)) (b07 town NPCs are c8..e1, not 02..22). mk.py can force a label in ANY block (054A=block), e.g. b24 lbl f7.
- System popups (b02) are 16 columns wide. In t_*.txt an indented continuation line is a SOFT join (space); start the next line without a leading space to force a hard [n]. Rewrote: Not enough money / Can't carry more\n[item] / Can't sell\n[item]! / Can't use\n[item]! / Nothing's wrong. / Can't use magic! / Not enough MP! / Can't use here! / [item]\nx[n] obtained!. Items longer than 16 chars (e.g. Provisional Permit) will still wrap in these popups.
- Item-count spacing: the count/× drawing code (01:B93D.., 02:B740.., 02:8DB3..) is byte-identical to the JP ROM and positions are fixed offsets (+9 tiles) from the item slot; short names are <=8 chars, so spacing matches JP by construction.

## Pass: b09 on-screen sweep (Oct 28)
- Some NPC lines get a JP 「 glyph (tile 0x70) from the script, outside the string. That glyph is now drawn as `"` (font/lower8.txt), so these lines show a normal opening quote.
- Because that external quote also takes a column, the wrapper doesn't count it. b09 2a8f5b4dd8 overflowed ("hav e"). It's reworded so the first line is ≤23 characters. Other entries that start with an external 「 and have a 24-character first line could have the same problem. None seen so far.
- In b09 lbl 82, "accept it.Priest" comes from forcing the label: the text falls through into the next label. It isn't a real game bug.
- The "Elixir x2 obtained!" popup has been checked on screen.
- The quote glyph lives in a VRAM font that is loaded at boot, so old save states (field.mss from 00:50) still showed the old ┌ shape. field.mss was regenerated from a fresh boot on the current ROM (03:52), and the quote then appeared as `"` (b0a lbl 28 viewed).
- Wrapper: strings that follow a lone 「 segment (`70 ff`) now wrap starting at column 1 (insert_sm QUOTED -> encode col0=1). The audit found 119 such strings. 24 of them wrapped differently and would have overflowed. b09 2a8f5b4dd8 and b0a fe5e6357aa ("There won't be a ship / to Tiris for a while.") were checked on screen.
- Popups checked on screen: "Can't carry more / Nitron." (Nitron count 99), "Can't use here!" (Nitron in the field), "Can't use / Temp. Permit!", "Can't sell / Temp. Permit!", "Introduction x1 obtained!".
- Item 145 is renamed from Provisional Permit to Temp. Permit (12 characters), so every item name now fits in the 16-column popups. Vengeance Sword is the longest at 15.
- b10 sweep: labels 1e-5c viewed (NPCs, broker, help-wanted, item/weapon/armor shops, Not enough money). They look fine. The broker menu was caught mid-draw ("Ma"), so I couldn't judge it.

## b0a sweep pass3 (labels 5f–70), viewed
- Viewed sheets for 5f, 64, 67, 68, 69, 6a, 6c, 6d, 6e, 6f, 70: clinic, inn (full/stay/500 Guillaume + Yes/No), Sion "Hey! Yury!!", stagecoach. No overflows; wraps look right.
- Stagecoach choice windows (6e, 70) show "=a" / "/a" when forced by label jump: menu data is not set up outside real play. Needs checking in real play; not counted as a text bug yet.
- pass3 labels 71–78 viewed (coach not running, caravan/Remi/Gordon): OK.
- pass3 labels 79–c6 viewed (tavern job, drinks, Sion/Yury, caravan): no overflows. Currency evidence: the game's own popup reads "Got 100G!" (b0a lbl 9d), which supports rendering FD0F:08 as "G".
- b0a lbl ac "They say Croixdor is attacking..." has no opening quote; JP b10_106 also has none in its own segment (the quote is a separate branch segment). Left as is.
- b0a c7–e3 viewed. Inn cost box showed "100G×1人" (JP person counter). Blanked the 人 tile (02:8DBF lda #$24C8 -> #$2400, asm/main.asm); viewed after the fix: "500G / 100G×1 / Cost 100G", Stay/Leave. b0a sweep complete.
- Sweeps now run from a pre-roll state (smmenu/pre.mss, frame 2390 of the mk.py route) via /workspace/sweep4.sh: ~8 s per label instead of ~17 s.
- pass4 chunk 1 (b0b/b0c, first 62 labels) viewed. Found: the item popup with an icon wraps item names at 12 characters, so "Reviving Water" showed as "er". Measured with test names (a 14-character name showed only its last 2 letters; "Introduction" at 12 fits). Every item long name is now 12 characters or fewer: Bastard Swd, Vengeance, Termin. Bow, Rhythm Rctr, Leather Mail, Lamellar, Thunder Mail, Reflect Grd, Medusa Shld, BurstThunder, Blu Melazine, Clr Melazine, Revive Water, Antidote, Crystal Wtr, Courage Wtr, Life Water, Ship Ticket (じょうせんけん). Checked on screen: "Revive Water x1 obtained!".
- b0b lbl 28 ("This is Lesa Village." followed by a blank line and then "Thanks...") happens only because the label is forced: the JP string ends in [END], and the forced run falls through into the next label.
- pass4 chunk 2 (labels 41-62: b0d inn/Remi lines, b0e bandit hideout with Jack/Thief) viewed; the text is fine. b0e lbl 0f showed an icon popup reading "mb" (dagger icon) on the pre-fix build. It goes on the recheck list.
- pass4 chunk 3 (labels 63-103: b0e-b11, goblin cave and the caravan attack) viewed; the text is fine. bf lbl 04 has an empty box and the JP is also just [LINE]. bf lbl 06 is a skipped data fragment. Suspect: world-map place-name box shows "Lesa Villa" and "Tiris Noah", so it may cap at 10 characters (b0a "Goblin Cav" too). Rechecking with a late screenshot.
