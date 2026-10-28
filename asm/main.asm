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
  db $80,$09        ; BRA $02B09A (asar mis-assembled the long-address BRA as 80 9A)
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

; ---------------------------------------------------------------------------
; Rumble (struktured labs): Limited Run Games "SNES Rumble" protocol, same as
; rcr-rumble: after the joypad read, 16 bits MSB first on port-1 IOBit
; (WRIO $4201 bit 6, bit 7 kept 1), each clocked by one $4016 read:
; $72 sentry, then level (hi nibble strong motor, lo nibble weak motor).
; A plain pad ignores all of it. Events come from the battle HP-damage
; routine at $15:81A7 (X = target struct+1 from $1286, damage in $1288).
!R_T   = $7E97F8    ; frames left in the pulse (0 = none)
!R_L   = $7E97F9    ; level byte of the pulse
!R_OFF = $7E97FA    ; trailing $7200 (off) packets still to send
!R_MAX = 40

org $00E07A          ; in-game joypad reader tail: STA $127D / PLP / RTS
  JML rumble_frame

org $1581A7          ; damage applier entry: PHP / REP #$20 / LDX $1286
  JML rumble_dmg
  NOP
  NOP

org $3FC000
rumble_frame:
  STA $127D         ; the routine's own PHP is undone by the PLP below
  REP #$30
  PHA
  PHX
  PHY
  SEP #$30
  LDA.l !R_T
  BEQ .off
  CMP #!R_MAX+1
  BCS .clear
  DEC
  STA.l !R_T
  LDA #$02
  STA.l !R_OFF
  LDA.l !R_L
  BRA .send
.off:
  LDA.l !R_OFF
  BEQ .out
  CMP #$03
  BCS .clear
  DEC
  STA.l !R_OFF
  LDA #$00
.send:
  PHA
  LDA #$72
  JSR rumble_send8
  PLA
  JSR rumble_send8
  LDA #$FF
  STA.l $004201
.out:
  REP #$30
  PLY
  PLX
  PLA
  PLP
  JML $00E07E
.clear:
  LDA #$00
  STA.l !R_T
  STA.l !R_OFF
  BRA .out

rumble_send8:        ; A8/X8: send A, MSB first
  LDY #$08
.bit:
  ASL
  TAX
  LDA #$80
  BCC +
  LDA #$C0
+ STA.l $004201
  LDA.l $004016
  TXA
  DEY
  BNE .bit
  RTS

rumble_dmg:
  PHP
  REP #$20
  LDX $1286
  LDA $1288
  BEQ .done
  CPX.w #$110E        ; party structs $1000-$10E1, monsters from $110E
  BCS .enemy
  CMP $0003,x
  BCS .ko
  LSR
  LSR
  LSR
  LSR
  CLC
  ADC #$0006
  CMP #$0010
  BCC +
  LDA #$000F
+ ASL
  ASL
  ASL
  ASL
  ORA #$0008
  SEP #$20
  STA.l !R_L
  LDA #14
  BRA .set
.ko:
  SEP #$20
  LDA #$FF
  STA.l !R_L
  LDA #28
  BRA .set
.enemy:
  SEP #$20
  LDA.l !R_T
  BNE .done8
  LDA #$05
  STA.l !R_L
  LDA #6
.set:
  STA.l !R_T
.done8:
  REP #$20
.done:
  LDX $1286
  JML $1581AD
incsrc "splash.asm"

; ---- Prologue crawl: English 1bpp bitmap (raw block, tools/py/prologue.py) replaces LZSS block 19:00 ----
org $00C755 : ldx.w #$3A00     ; was ldx #$1900 (bank $19 idx 0) -> bank $3A idx 0
org $3A8000
  dw $8002
  dw 9216-1                    ; bit15=0: raw copy, size-1
  incbin "prologue.bin"

; ---- Shop quantity box: "合計" (total) -> "Cost", drop the "コ"/個 counter after the quantity ----
org $02BBA4 : db $00             ; lda #$243E (counter glyph after quantity, sta $481A) -> blank tile
; Inn cost box: "100G x1人" -> drop the 人 (person) counter glyph (lda #$24C8 / sta $47DA at 02:8DBF)
org $028DC0 : db $00
org $028DC5
  JSL shop_total : NOP #8
org $02BB72
  JSL shop_total : NOP #8
org $3FD000
shop_total:                       ; A16, DB=$7E (as at the call sites)
  LDA #$2482 : STA $4844          ; C
  LDA #$240F : STA $4846          ; o
  LDA #$2413 : STA $4848          ; s
  LDA #$2414 : STA $484A          ; t
  RTL
