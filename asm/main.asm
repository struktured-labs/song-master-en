; Song Master English - code hooks (asar). ROM is expanded to 2 MiB by tools/py/insert_sm.py first.
lorom
!SCR = $7E9000      ; scratch copy of the current English string (main script buffer tail; blocks rebuilt <= $1800)
!SAVY = $7E97F0
!SAVT = $7E97F2
!PTR = $208000      ; 3-byte pointers, index = hi<<8|lo

org $00FFD7
  db $0B            ; 2 MiB

; text renderer FD dispatch ($02:AE53 REP #$20 / LDA $0000,y)
org $02AE53
  JML fdhook

org $3F8000
fdhook:
  REP #$20
  LDA $0000,y
  AND #$00FF
  CMP #$0030
  BEQ .redir
  CMP #$0031
  BEQ .ret
  JML $02AE58
.ret:
  LDA !SAVY
  TAY
  SEP #$20
  JML $02AE30
.redir:
  INY
  LDA $0000,y       ; lo | hi<<8
  INY
  INY
  PHA
  TYA
  STA !SAVY         ; -> original terminator in the block
  PLA
  STA !SAVT
  ASL A
  CLC
  ADC !SAVT
  TAX
  LDA $20
  PHA
  LDA $22
  PHA
  LDA !PTR,x
  STA $20
  LDA !PTR+2,x
  STA $22
  LDY #$0000
  SEP #$20
.loop:
  LDA [$20],y
  TYX
  STA !SCR,x
  INY
  CMP #$FD
  BNE .loop
  LDA [$20],y
  TYX
  STA !SCR,x
  INY
  CMP #$31
  BNE .loop
  REP #$20
  PLA
  STA $22
  PLA
  STA $20
  LDY.w #!SCR&$FFFF
  SEP #$20
  JML $02AE30

; default party names read from $3E:8000 (English, longer than the JP table at $00:BC5F)
org $00BC14
  LDA $3E8000,x

; ---- dialogue word lists (FD0E..FD12) read from English tables in ROM $3C instead of the JP lists at $7E:D000
; tables: $3C:8000 + id*$200 = 2-byte pointers (1-based index), strings FF-terminated in bank $3C.
!LBUF = $97C0       ; DB=$7E here
!LY = $97F4
!LT = $97F6
org $02B088         ; places (A = index)
  JSL lh_places
  JSR $B0F5
  BRA $02B09A
org $02B093         ; terms
  JSL lh_terms
  JSR $B0F5
  JSL lh_rest       ; $02B09A
  RTS
org $02B0B2         ; items
  JSL lh_items
  JSR $B0F5
  JSL lh_rest
  RTS
org $02B0D1         ; magic
  JSL lh_magic
  JSR $B0F5
  JSL lh_rest
  RTS
org $02B0E8         ; monsters
  JSL lh_mons
  JSR $B0F5
  JSL lh_rest
  RTS

org $3F8200
lh_places:
  LDX #$0000
  BRA lh_common
lh_terms:
  LDX #$0200
  BRA lh_read
lh_items:
  LDX #$0400
  BRA lh_read
lh_magic:
  LDX #$0600
  BRA lh_read
lh_mons:
  LDX #$0800
lh_read:
  LDA $0000,y
  INY
lh_common:
  STY !LY
  REP #$20
  AND #$00FF
  BEQ .none
  DEC A
  ASL A
  STA !LT
  TXA
  CLC
  ADC !LT
  TAX
  LDA $3C8000,x
  TAX
  SEP #$20
  LDY #$0000
.cp:
  LDA $3C0000,x
  STA !LBUF,y
  INX
  INY
  CMP #$FF
  BNE .cp
  LDY #!LBUF
  LDA #$01
  RTL
.none:
  SEP #$20
  LDA #$00
  RTL
lh_rest:
  LDY !LY
  RTL

; ---- menu-side list lookups (A = index, not from the script): $02:B0A0 items, $02:B0BF magic, $02:B0DE monsters.
; The originals JSR into the middle of the script-side routines patched above, so they must be redirected too.
org $02B0A0
  PHP
  JSL lhm_items
  PLP
  RTS
org $02B0BF
  PHP
  JSL lhm_magic
  PLP
  RTS
org $02B0DE
  PHP
  JSL lhm_mons
  PLP
  RTS
org $02C969         ; spare bytes at the tail of the bank $02 menu pool (ui_inplace.json stops at 0x14969)
  JSR $B0F5         ; render the FF-terminated string at Y (A = 1: no entries skipped)
  RTL
org $3F8300
lhm_items:
  SEP #$20
  PHB
  PHY
  PHX
  LDX #$0400
  BRA lhm
lhm_magic:
  SEP #$20
  PHB
  PHY
  PHX
  LDX #$0600
  BRA lhm
lhm_mons:
  SEP #$20
  PHB
  PHY
  PHX
  LDX #$0800
lhm:
  PHA
  LDA #$7E
  PHA
  PLB
  PLA
  JSL lhs_common
  BEQ +
  JSL $02C969
+:
  PLX
  PLY
  PLB
  RTL

; same as lh_common but reads the short-name tables in bank $3D
lhs_common:
  STY !LY
  REP #$20
  AND #$00FF
  BEQ .none
  DEC A
  ASL A
  STA !LT
  TXA
  CLC
  ADC !LT
  TAX
  LDA $3D8000,x
  TAX
  SEP #$20
  LDY #$0000
.cp:
  LDA $3D0000,x
  STA !LBUF,y
  INX
  INY
  CMP #$FF
  BNE .cp
  LDY #!LBUF
  LDA #$01
  RTL
.none:
  SEP #$20
  LDA #$00
  RTL
