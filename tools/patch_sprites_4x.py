# Personagens em 4x (detalhe em quartos de pixel), mesmo tamanho na tela.
# Sprites com c.k guardam a própria resolução; o desenho divide por c.k em vez de K.
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)
rep("function P(q){const k=q.getTransform().a;return(x,y,w,h,c)=>{q.fillStyle=c;q.fillRect(Math.floor(x*k+1e-6)/k,Math.floor(y*k+1e-6)/k,w,h)}}",
    "function P(q){const k=q.getTransform().a,f=(x,y,w,h,c)=>{q.fillStyle=c;q.fillRect(Math.floor(x*k+1e-6)/k,Math.floor(y*k+1e-6)/k,w,h)};f.k=k;return f}")
rep("function line(p,x0,y0,x1,y1,c,w=1){x0=Math.round(x0*K);y0=Math.round(y0*K);x1=Math.round(x1*K);y1=Math.round(y1*K);",
    "function line(p,x0,y0,x1,y1,c,w=1){const K=p.k||2;x0=Math.round(x0*K);y0=Math.round(y0*K);x1=Math.round(x1*K);y1=Math.round(y1*K);")
rep("function tint(src,col,a){const c=canvas(src.width,src.height),q=c.getContext('2d');",
    "function tint(src,col,a){const c=canvas(src.width,src.height),q=c.getContext('2d');c.k=src.k;")
rep("  const w=c.width/K,h=c.height/K,hx=Math.floor(c.width/2)/K;",
    "  const k=c.k||K,w=c.width/k,h=c.height/k,hx=Math.floor(c.width/2)/k;")
rep("function di(c,x,y){g.drawImage(c,x,y,c.width/K,c.height/K)}",
    "function di(c,x,y){const k=c.k||K;g.drawImage(c,x,y,c.width/k,c.height/k)}")
a=s.index("function sprHuman(o,dir,state,f){");b=s.index("function sprTree(kind){")
s=s[:a]+open('tools/_sprHuman_4x.js',encoding='utf-8').read()+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok')
