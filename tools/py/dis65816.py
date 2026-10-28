"""Minimal 65816 disassembler for LoROM Song Master. usage: dis65816.py SNESADDR(hex) count [m8 x8]"""
import sys
import os;ROM=open(os.environ.get('DROM','/workspace/song-master-en/rom/Song Master (Japan).sfc'),'rb').read()
def s2p(a):  # LoROM snes->pc
    return ((a>>16)&0x7F)*0x8000+(a&0x7FFF)
names="BRK ORA COP ORA TSB ORA ASL ORA PHP ORA ASL PHD TSB ORA ASL ORA BPL ORA ORA ORA TRB ORA ASL ORA CLC ORA INC TCS TRB ORA ASL ORA JSR AND JSL AND BIT AND ROL AND PLP AND ROL PLD BIT AND ROL AND BMI AND AND AND BIT AND ROL AND SEC AND DEC TSC BIT AND ROL AND RTI EOR WDM EOR MVP EOR LSR EOR PHA EOR LSR PHK JMP EOR LSR EOR BVC EOR EOR EOR MVN EOR LSR EOR CLI EOR PHY TCD JML EOR LSR EOR RTS ADC PER ADC STZ ADC ROR ADC PLA ADC ROR RTL JMP ADC ROR ADC BVS ADC ADC ADC STZ ADC ROR ADC SEI ADC PLY TDC JMP ADC ROR ADC BRA STA BRL STA STY STA STX STA DEY BIT TXA PHB STY STA STX STA BCC STA STA STA STY STA STX STA TYA STA TXS TXY STZ STA STZ STA LDY LDA LDX LDA LDY LDA LDX LDA TAY LDA TAX PLB LDY LDA LDX LDA BCS LDA LDA LDA LDY LDA LDX LDA CLV LDA TSX TYX LDY LDA LDX LDA CPY CMP REP CMP CPY CMP DEC CMP INY CMP DEX WAI CPY CMP DEC CMP BNE CMP CMP CMP PEI CMP DEC CMP CLD CMP PHX STP JML CMP DEC CMP CPX SBC SEP SBC CPX SBC INC SBC INX SBC NOP XBA CPX SBC INC SBC BEQ SBC SBC SBC PEA SBC INC SBC SED SBC PLX XCE JSR SBC INC SBC".split()
# addressing modes per column pattern
modes=[None]*256
col={0x01:'(d,x)',0x03:'d,s',0x05:'d',0x07:'[d]',0x09:'#m',0x0D:'a',0x0F:'al',0x11:'(d),y',0x12:'(d)',0x13:'(d,s),y',0x15:'d,x',0x17:'[d],y',0x19:'a,y',0x1D:'a,x',0x1F:'al,x'}
for op in range(256):
    lo=op&0x1F
    if lo in col: modes[op]=col[lo]
spec={0x00:'#8',0x02:'#8',0x04:'d',0x06:'d',0x08:'',0x0A:'A',0x0B:'',0x0C:'a',0x0E:'a',0x10:'r',0x14:'d',0x16:'d,x',0x18:'',0x1A:'A',0x1B:'',0x1C:'a',0x1E:'a,x',
0x20:'a',0x22:'al',0x24:'d',0x26:'d',0x28:'',0x2A:'A',0x2B:'',0x2C:'a',0x2E:'a',0x30:'r',0x34:'d,x',0x36:'d,x',0x38:'',0x3A:'A',0x3B:'',0x3C:'a,x',0x3E:'a,x',
0x40:'',0x42:'#8',0x44:'mv',0x46:'d',0x48:'',0x4A:'A',0x4B:'',0x4C:'a',0x4E:'a',0x50:'r',0x54:'mv',0x56:'d,x',0x58:'',0x5A:'',0x5B:'',0x5C:'al',0x5E:'a,x',
0x60:'',0x62:'rl',0x64:'d',0x66:'d',0x68:'',0x6A:'A',0x6B:'',0x6C:'(a)',0x6E:'a',0x70:'r',0x74:'d,x',0x76:'d,x',0x78:'',0x7A:'',0x7B:'',0x7C:'(a,x)',0x7E:'a,x',
0x80:'r',0x82:'rl',0x84:'d',0x86:'d',0x88:'',0x89:'#m',0x8A:'',0x8B:'',0x8C:'a',0x8E:'a',0x90:'r',0x94:'d,x',0x96:'d,y',0x98:'',0x9A:'',0x9B:'',0x9C:'a',0x9E:'a,x',
0xA0:'#x',0xA2:'#x',0xA4:'d',0xA6:'d',0xA8:'',0xAA:'',0xAB:'',0xAC:'a',0xAE:'a',0xB0:'r',0xB4:'d,x',0xB6:'d,y',0xB8:'',0xBA:'',0xBB:'',0xBC:'a,x',0xBE:'a,y',
0xC0:'#x',0xC2:'#8',0xC4:'d',0xC6:'d',0xC8:'',0xCA:'',0xCB:'',0xCC:'a',0xCE:'a',0xD0:'r',0xD4:'d',0xD6:'d,x',0xD8:'',0xDA:'',0xDB:'',0xDC:'[a]',0xDE:'a,x',
0xE0:'#x',0xE2:'#8',0xE4:'d',0xE6:'d',0xE8:'',0xEA:'',0xEB:'',0xEC:'a',0xEE:'a',0xF0:'r',0xF4:'a',0xF6:'d,x',0xF8:'',0xFA:'',0xFB:'',0xFC:'(a,x)',0xFE:'a,x'}
for k,v in spec.items(): modes[k]=v
def dis(addr,count,m8=True,x8=True,out=print):
    for _ in range(count):
        p=s2p(addr); op=ROM[p]; md=modes[op]; n=names[op]
        sz={'':1,'A':1,'#8':2,'d':2,'d,x':2,'d,y':2,'(d,x)':2,'d,s':2,'[d]':2,'(d),y':2,'(d)':2,'(d,s),y':2,'[d],y':2,'r':2,
            'a':3,'a,x':3,'a,y':3,'(a)':3,'(a,x)':3,'[a]':3,'rl':3,'mv':3,'al':4,'al,x':4}.get(md)
        if md=='#m': sz=2 if m8 else 3
        if md=='#x': sz=2 if x8 else 3
        b=ROM[p:p+sz]; v=int.from_bytes(b[1:],'little')
        if md=='r': t=(addr+2+((v^0x80)-0x80))&0xFFFF|(addr&0xFF0000); arg='$%06X'%t
        elif md=='rl': t=(addr+3+((v^0x8000)-0x8000))&0xFFFF|(addr&0xFF0000); arg='$%06X'%t
        elif md in('#m','#x','#8'): arg='#$%0*X'%((sz-1)*2,v)
        elif md=='mv': arg='$%02X,$%02X'%(b[1],b[2])
        elif md in('','A'): arg=md
        else:
            w=(sz-1)*2; arg=md.replace('al','$%0*X'%(w,v),1) if md.startswith(('al','[a','(a','a')) and 'al' in md else md
            if 'al' not in md: arg=md.replace('a','$%0*X'%(w,v),1) if md[0] in 'a(['and 'a' in md and 'd' not in md else md.replace('d','$%02X'%v,1)
        if op==0xC2:
            if v&0x20: m8=False
            if v&0x10: x8=False
        if op==0xE2:
            if v&0x20: m8=True
            if v&0x10: x8=True
        out('%06X  %-12s %s %s'%(addr,b.hex(' '),n,arg))
        addr=(addr&0xFF0000)|((addr+sz)&0xFFFF)
        if op in(0x60,0x6B,0x40,0x4C,0x5C,0x80,0x82,0xDC,0x7C,0x6C) and len(sys.argv)<6: out('---')
    return addr
if __name__=='__main__':
    a=int(sys.argv[1],16); c=int(sys.argv[2]); m8=len(sys.argv)<4 or sys.argv[3]=='1'; x8=len(sys.argv)<5 or sys.argv[4]=='1'
    dis(a,c,m8,x8)
