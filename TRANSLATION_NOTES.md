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
- pass4 chunk 4 (labels 104-151: b11-b13, Lancafarn and Vanvar) viewed. Speaker tags that used lowercase common-noun terms showed as "goblin", "goblin Soldier" and so on. Every speaker-line use of terms 09/0A/0F/15/1F (broker/goblin/merchant/dwarf/fairy) is now literal capitalized text: Goblin, Goblin Soldier, Dwarf Guard, Broker, Merchant, Fairy (54 lines). The inline uses stay lowercase. Shops show "LthArmor 650G" and so on. The "Not enough money" popup is fine.

## Chunk 5 (b14–b18) + map box
- Speaker tags now literal (Thief added); "thiefs" -> "thieves", "fairys" -> "fairies"; b17 "Lord ^0!" keeps the JP trailing space.
- World-map place-name box ($02:B072) holds 10 tiles; it now reads short place names from bank $3D table 0
  (lists_short.json "places", <=10 chars, e.g. Lesa, Sombayu, Cybele, GoblinCave). Needs on-screen check.

## Chunk 6 (b18 18 – b19 7b), viewed
- Shops/inn/clinic/temple/broker/stagecoach screens read cleanly; stagecoach map opened with "Meritus" box.
- Fixed: "donated 100 / G!!" split -> "donated / 100G!!"; b19 7a "butit" (two concatenated messages) -> line break.
- Forced-label artifacts (empty "Where to?" choice, half-drawn popups) are not bugs.

## Chunk 7 (b19 7d – b1d 0a), viewed
- Tavern, Nimens story, Meritus gate, Eddie/Ferion briefing, Singer Guild all read cleanly; no fixes needed.
- Map boxes seen: Meritus, Vilne Pass, Lancafarn (all <=10, fit).
- Speaker-only boxes (Soldier/Man/Youth) are forced-label artifacts (tag label without its body).

## Chunk 8 (b1d 0f – b1f 19), viewed
- Selena vision, Ferion news, Meritus/Lancafarn shops, stagecoach (Lancafarn map box), Alesia: clean.
- b1f 0a / b1f 19: lines using the "old man" term ([FD0F:0D]) broke a line early and lost the indent.
  The cause in the engine isn't pinned down, so those 4 lines now spell out "old man" as plain text (in the recheck list).

## Chunk 9 (b1f 1f – b24 cd), viewed
- Farion (ファリオン, b20 64) is a different man from Ferion, as in the JP. Christ = クリスト.
- Map box showed the shortened name "Barahat" (was "Barahat Pass") in full (b22 06/09), plus Farhan, Watts Pass, Christ.
- Travel Pass office, Farhan shops, and the old-man line all read correctly. No fixes.

## Chunk 10 (b24 d2 – b27 02), viewed
- Log lines 427–476 viewed (sheets c1000–c1007). Inn, Alster guards/townsfolk, Palm Pass map box, El Ran/Selena lines, rock-paper-scissors gambler all render cleanly.
- Fix: b25 0d "just a drunkold guy" — fragment 50e0ea2589 lost the space before the soft-continued 0ce32c7286; now "just a drunk " (trailing space). Queued in recheck.
- Open: RPS hand-choice popup (uid 368155822f, `[x5A][x5B][x5C]Rock/Scissors/Paper`) shows only cursor + "c" under forced labels. JP is ヨラリ + グ-/チョキ/パ- (2–3 chars). Queued in recheck (b26 52) to check in a real flow before changing.

## Chunk 11 (b27 04 – b28 6f), viewed
- Log lines 477–532 viewed (sheets c1100–c1110). Singer Guild/Hudson, Alster townsfolk, Purge Blade seller, temple, weapon/armor/item/clinic/inn shops, sailors' inn, stagecoach station all render cleanly; shop lists and "Not enough money" fit.
- Fix: b27 8c "rock-paper- scissors" split at the hyphen with a stray space; the compound is now on one source line so it wraps whole.
- Forced-label artifacts (same class as the earlier stagecoach "=a"): option popups showing a single letter ("c", "d", "sd", "ud") and the trailing "bミ b" after the broker/stagecoach prompts. Broker b28 4b added to recheck for a real-flow check.

## Chunk 12 (b28 70 – b2a 05), viewed
- Log lines 533–592 viewed (sheets c1200–c1207). Stagecoach 500G prompt + Lancafarn/Alster map boxes, tavern, Alster castle guards, black panther cell, King Colman/Orb, kitchen all render cleanly.
- Fix: "[FD0F:14] Guild" (thief term + Guild) broke the line early like the old-man term ("thief / Guild" on its own lines). Replaced with literal "Thieves' Guild" in b36/b41/b44. b28 e2 queued in recheck.

## Chunk 13 (b2b 01 – b2f 8a), viewed
- Log lines 593–662 viewed (sheets c1300–c1309). Dorfas thieves' town, shops, informant, Lamia/Sam/King Eric, Marsha knights, Alster/Triangle/Lesa map boxes, Lismore Troll arc, "Got 5000G!", "Object Clear x1 obtained!" all render cleanly.
- Consistency: the rest of the "[FD0F:14] Guild" uses (b26/b41/b44) now read "Thieves' Guild", replacing "thief Guild" (seen at b2c 73).
- Informant choice popup "d" (b2c 4b): the same forced-label artifact class as before.

## Term-wrap root cause (investigation)
- The encoder's wrap is correct: "the [FD0F:14] Guild." wraps to " the thief Guild." (17 columns). On screen (pass4 b28_e2) the game breaks right after the term, and "Guild." starts at column 0 with no indent. So the space byte (0x00) that directly follows a list term is being drawn as a line break by the game's term path (`lh_*` → `$02:B0F5`). Terms followed by `[c0]` and then a space (e.g. "[c1]culprit[c0] who") render fine. That matches every bad case: "an [FD0F:0D] named" and "[c2][FD0F:14] Guild".
- Experimental fix in encode_en.py: when a term is followed directly by a space, re-emit the current colour tag between them. To test it, b36 6d048dfee1 (label b28 e2) uses the term again. Pending on-screen confirmation in the recheck run; the other literal workarounds stay in place until then.

## Chunk 14 (b2f 8b – b31 14), viewed
- Log lines 663–680 viewed (sheets c1400–c1403). Lismore girl/Troll quest, clinic, item and arms shops (Boomrang/Drop, Bastard/IceBlade/BrnzHarp), inn and Lismore map box are fine.
- Fix: the Troll Lord and Troll shouts used the lowercase "human" term plus a suffix, which rendered "humans!" and "humanS! YOU NOT PASS". They are now literal "Humans!" / "HUMANS! …" / "KILL HUMANS!!" (b46). b31 0a/0f added to recheck.
- The battle "Fireball:" / "Fireball-" header flicker is mid-animation under forced labels; not judged.

## Chunk 15 (b31 19 – b38 05), viewed
- Log lines 681–755 viewed (sheets c1500–c1511). The Troll battle (the new HUMANS literals are confirmed on screen at b31 28/2d/32/37/3c), Laura rescue, Durham dwarves, the Charms → Gaia Sword trade, Durham shops, the mine, King Rimbelt and the Amulet barrier are fine.
- Fixes: the b54 header "[FD0F:15] Guard" rendered as "dwarf Guard" in lowercase, so it is now the literal "Dwarf Guard" (3 places). b46 30d7076d4a: "Lots of the mines around" (JP ここいらには鉱山がたくさん) is now "Lots of mines around here!!". 33 05 and 37 37 added to recheck.
- Forced-label artifact: b34 0f "it's a trade!!" ran straight into the next "Dwarf" message without a break. That comes from chaining labels; check it in real play.

## Battle window overflow (in progress, 2026-10-28)
- Before captures (earlier build): /workspace/item8.png and /workspace/bat2.png. In the command window, "Magic", "Guard" and "Fight" end right at the right border. The item list's right-hand "x 8" column also sits against the border.
- Command window headers are at 01:AE8D (10 pointers). Each is 6 bytes, JP and EN identical: `00 01 08 11 03 06` (x=0 y=1 w=8 h=17 (or 15 for the variant) text 03 06?). The text and cursor offset bytes still need confirming. The candidate fix is a smaller text X, or a wider window that pushes the "Yury H·P" window right.
- Harness problem: with the current field.mss + enc poke, the encounter is 3 Fireball casters (Man-Eater records at 7E:10FE/112B/1158, 0x2D each, HP at +3). The player never gets a command turn and dies, and the JP ROM behaves the same way. menuUp (7F:AD4C) never fires. A new battle state is needed before any change can be viewed.
- Battle window overflow FIXED (2026-10-28): command windows (10 headers via ui_inplace "pre") width 08->09; magic-category popup width at 01:B3EC (LDA #$09 -> #$0A, sta $149A). Viewed EN before/JP/after: /workspace/batshots/{BEFORE_en_sheet,JP_sheet,AFTER_sheet}.png. Item list ("x 8" column), spell list, target window (Man-Eater H·P) and damage box match JP layout and fit; left unchanged (/workspace/batshots/*items_target_sheet.png). The widened command frame overlaps the status window's left border by one tile (text unaffected).
- Colour-tag re-emit after list terms removed from encode_en.py (did not fix "thief / Guild."). 6d048dfee1 now spells "thief Guild" literally; viewed fixed (rc6 b28 e2).
- Split message 50e0ea2589/0ce32c7286 rendered "drunkold": the wrapper drops a trailing space and a leading space at col 0. Carried as raw [x00]; viewed "just a drunk old guy!".
- Broker b28 4b (3e38b0ec88 + 3-option menu) shows "ya?" + stray glyphs and no menu under the forced label; b0a 2d shows only a "Ma" popup. Bytes match the working b25 structure. The JP forced run of 28 4b (VRAM-garbled kana) did draw a menu popup. Needs a real-play check.
- World-map route label "Tiris Noah" (b3c-b3f 05, b43 01) is the origin box. The pre.mss state is in Tiris Noah, so the label is correct for this state.
- Real-play attempt (no forced labels) from pre.mss in Tiris Noah: built /workspace/rp.sh (walk + shots + label hook) and states rp_out/rp_tav/rp_c.mss. Visited the pier, the street west and the sword-training hall (talk = label 14, "Yaah! Toh!"). The broker, stagecoach and temple were not reached by blind walking. Next: map the door/NPC tables or get a save state at a broker.

### Real-play check (2026-10-28, no forced labels)
- Ran from the Tiris Noah start state (b07/b05 town text). I talked to these NPCs normally and viewed the results: the temple Priest (fa), the ship-ticket seller (b07 28), a tavern patron (b05 dc, "Come to think of it, I heard rumors the monsters are prowling again."), and the Armor Shop (b05 1e). The armor shop showed its full Buy/Sell/Leave menu, a 500G box, the item list (LthArmor 650G, GldShld 10000G, SmlShld/Cap 300G), and "Not enough money". All text fit.
- I did not reach the b10 broker or the coach station. A guard east of the pier says "Sir! You can't just walk in here!!", so that area seems to open later in the story. The b40 (28 4b) broker is also later in the story. The temple has no choice menu at this point.
- OPEN: the b07 ticket line "Ship Ticket for Tiris Noah" is sold *inside* Tiris Noah. JP is [FD0E:01]ゆき. FD0E's index base (0-based or 1-based) is unverified, so 01 might be "Tiris" (the island) or something else. Check against a JP real-play render before changing it. The earlier map-label note ("state is in Tiris Noah so the label is correct") rested on this same unverified mapping.

### Real-play check 2: sailing (2026-10-28)
- From rp_out.mss I set flag 6 (0C14 |= 0x04) and Ship Ticket = 1 (0C12, list 0x95). Walking right to the guard gives "You have [Ship Ticket]! Then have a safe trip!!" and the ship sails. Viewed on screen. The map label during the voyage is "Tiris Noah", shown at the destination end.
- FD list indexes are 1-based, settled: in the same b07 line, [FD10:95] must be the ticket (1-based 0x95 = Ship Ticket; 0-based would be Spirit Guard). WORDLISTS.md also says 1-based. So JP [FD0E:01] is ティリス・ノア, the ticket really is "for Tiris Noah", and no text fix is needed. The b07 "Tiris Noah" header is wrong: b07 is the *departure* island port. The arrival town is Tiris Noah, and its weapon shop "Need a weapon!?" lives in b10.
- In Tiris Noah (state smmenu/rp_tn.mss) I viewed the weapon shop greeting, the tavern guide ("So you are Yury. I've heard about you from Master Robinton. First, go to the Singer Guild in Meritus and ask about Ferion."), the inn dining hall, and Sion's "Any farther and we'll be outside town." All text fits.
- Broker/stagecoach still not talked to. A bookshelf shop west of the inn (rp_brk.mss) has a clerk two tiles behind the counter who doesn't respond to A from any spot I tried. I didn't find the coach station.
- Real-play check 3: talking across a counter works when the leader stands on the tile directly below the counter (rp_brk x=1272 y=175; y=183 is one tile too far). That clerk is b07 28, which shows "There won't be a ship to Tiris for a while." This is the start town (b07 text: Singer Guild = 0a, the Limerick NPC = 14, Weapons = 55). The b10 broker and coach were still not reached.
- 28 4b compared with the JP bytes: [c1][FD0F:09][c0][n] text [wait] FF, then op 0d 61 4f, op 1e 03 4c, and the choice text with option ids 4d 4e 4c. The EN string has the same codes (terms[8] = broker, the option ids are kept as [x4D][x4E][x4C], and the ops are untouched). No missing control code was found, so there is no text change.

## Real-play check 4 (2026-10-28)
- NPC list format: 6-byte records x, y, sprite, flags, ?, talk label (00:9D2D, label from +5 to entity +03). Tiris Noah town list at 7E:F04F; label 2d there is a b07 NPC ("Mister, you're a Singer").
- Real talk to the b10 broker: Limerick NPC (record F05B) with label poked to 2d and $054A=0a held so the next talk loads b10.
- FIXED (real bug): every choice menu with [xHH] option ids was broken. Op 2E reads ids and option text inline from the block, so the FD30 string stub was read as ids and the stub bytes as text ("Ma", "=a", "/a", "c", "d" popups). Choice strings are now encoded inline in the block, with [n] (FD0D) between options as in the JP.
- Viewed after fix: b10 broker greeting and the help-wanted menu "Tavern helper / Thomas's request / Goblin hunt / Never mind" fully drawn; choosing "Ask for info" gave "Then it's the tavern to the lower right...". Coach and 28 4b menus use the same path but are not yet viewed.

## Choice-menu check 5
- Option windows wrap past 16 characters (viewed: coach, password, Jack-in-cell menu wrapped). Rule: each option ≤16 chars.
- Shortened: "Ride the coach!" (b10/25), password menu "Seeking work?/Finding work?" with matching hint in b25, "Aw, let him out!" (b16), "Can't ignore it!/No time for it!" (b46).

## Walker / NPC check (2026-10-28)
- tools/test/walk.lua + wk.sh: scripted walker. WRAM entity table at 0xD84 + 12*k (k=0 player; x at +4, y at +6; slot active if +1..+3 nonzero). 0xE44 is scroll, not map id. Step {'talk',k,timeout,side} steers next to entity k and presses A.
- School exit: corridor y=1183, go down at x=328. Viewed: classmate (b06 8f0d9869ed, JP 《うた》 rendered as <songs>), pier priest (Amsia/Limerick), tavern barkeep menu "A drink, please!/Never mind!" fits.
- 《》 emphasis: no longer carried over as <...>. Battle shouts (b03_nowrap) now use "..."; elsewhere the brackets are simply dropped (color codes already mark key terms). lists.json "<Singer>" -> "Singer". Viewed: classmate b06 8f0d9869ed now "are songs holding divine power".
