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
