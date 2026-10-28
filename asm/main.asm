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
