#!/usr/bin/env python3
"""Render assets/prologue_en.txt into the 1bpp tile layout of LZSS block 19:00.
Layout (from VRAM tilemap at boot f1100): 24 lines x 12 cells of 16x16; cell = 4 tiles TL,TR,BL,BR;
line L cell c -> tiles 48L+4c..+3, 8 bytes per 1bpp tile. Output 9216 bytes."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
FONT=os.environ.get('PFONT','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
SIZE=int(os.environ.get('PSIZE','11'))
W,LINES=192,24
def wrap(text,font,d):
    out=[]
    for para in text.rstrip('\n').split('\n'):
        lead=len(para)-len(para.lstrip(' ')); words=para.split(); cur=' '*lead
        for w in words:
            t=(cur+(' ' if cur.strip() else '')+w)
            if d.textlength(t,font=font)<=W-1: cur=t
            else: out.append(cur); cur=w
        out.append(cur)
    return out
def render(txt):
    font=ImageFont.truetype(FONT,SIZE); im=Image.new('1',(W,LINES*16)); d=ImageDraw.Draw(im); d.fontmode='1'
    lines=wrap(txt,font,d)
    if len(lines)>LINES: sys.exit('too many lines: %d'%len(lines))
    for i,l in enumerate(lines): d.text((0,i*16+int(os.environ.get('PYOFF','2'))),l,font=font,fill=1)
    return im,lines
def pack(im):
    out=bytearray()
    for L in range(LINES):
        for c in range(12):
            for ty,tx in ((0,0),(0,1),(1,0),(1,1)):
                for y in range(8):
                    b=0
                    for x in range(8):
                        if im.getpixel((c*16+tx*8+x,L*16+ty*8+y)): b|=0x80>>x
                    out.append(b)
    return bytes(out)
if __name__=='__main__':
    root=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    im,lines=render(open(os.path.join(root,'assets/prologue_en.txt')).read())
    data=pack(im); assert len(data)==9216
    open(sys.argv[1],'wb').write(data)
    if len(sys.argv)>2: im.convert('L').resize((W*2,LINES*32)).save(sys.argv[2])
    print(len(lines),'lines')
