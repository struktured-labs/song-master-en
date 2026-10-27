import sys; sys.path.insert(0,'/workspace/trinea/tools/py')
from walk import R,LEN,msg
def tryw(p,limit=4000):
    items=0; msgs=0; chars=0
    for _ in range(limit):
        if p>=len(R)-2: return None
        op=R[p]
        if op==0:
            if R[p+1]==0xFF: return (p+2,items,msgs,chars)
            p+=2; items+=1; continue
        if op>0x46: return None
        L=LEN[op]
        if L==0xFF:
            q=p+1; n=0
            while R[q] not in (0xFE,0xFF):
                if R[q] in (0,1):
                    if R[q]==1 and R[q+1]>=0xF0: pass
                    q+=2; n+=1
                elif R[q] in (0x80,0x82,0x83,0x88,0x8A,0x81,0x84,0x85,0x86,0x87,0x89,0x8B,0x8C): q+=1
                else: return None
                if q-p>600: return None
            p=q+1; msgs+=1; chars+=n
        elif L in (0xFE,0xFD):
            return None if False else (lambda: None)() or None
        elif L==0:
            q=p+2
            while R[q]!=0xFF and q-p<40: q+=1
            if R[q]!=0xFF: return None
            p=q+1
        else: p+=L
        items+=1
    return None
if __name__=='__main__':
    lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
    p=lo; out=[]
    while p<hi:
        if R[p]==0 and R[p+1]!=0xFF and R[p+1]!=0:
            r=tryw(p)
            if r and r[2]>=2:
                print('%06X-%06X items=%d msgs=%d chars=%d'%(p,r[0],r[1],r[2],r[3])); p=r[0]; continue
        p+=1
