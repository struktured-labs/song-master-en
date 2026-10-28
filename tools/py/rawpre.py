import sys,hashlib
sys.path.insert(0,'tools/py')
from sm_script import load, parse
want=set(sys.argv[2:]);i=int(sys.argv[1])
d=load(i);p,_=parse(d)
for k,s,e in p:
    if k=='text':
        u=hashlib.sha1(d[s:e]).hexdigest()[:10]
        if u in want: print(u,d[s:e][:6].hex(' '))
