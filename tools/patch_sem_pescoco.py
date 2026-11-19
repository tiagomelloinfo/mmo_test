# Sem pescoço: a cabeça desce até o queixo encostar na gola (estilo anime chibi).
p='tools/_sprHuman_real.js';s=open(p,encoding='utf-8').read()
for a,b in [("HX=10,HY=1.5+hb;","HX=10,HY=3.1+hb;"),("  limb(10,4.4+hb,10,7.4+by,","  limb(10,HY+2.9,10,7.4+by,")]:
    assert s.count(a)==1,a;s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s)
h='index.html';t=open(h,encoding='utf-8').read();a=t.index("function sprHuman(o,dir,state,f){");b=t.index("function sprTree(kind){")
t=t[:a]+s+t[b:];open(h,'w',encoding='utf-8').write(t);print('ok')
