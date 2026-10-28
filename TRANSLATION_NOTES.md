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
- Term FD0F:08 (ギョ-ム) is used as the currency unit ("500 Guillaume"). Kept as "Guillaume" for now; doubtful, may become a short unit.
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
- Known: red OBJ garbage strip appears at the bottom of the status/equip screen in the headless savestate test; it is identical in a build without UI changes (not caused by the patch, origin unverified).
- Not yet verified on screen: battle windows, config screen, save/load labels, MP Cost.
