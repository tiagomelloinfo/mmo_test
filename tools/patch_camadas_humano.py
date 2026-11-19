# sprHuman com camadas: o.layer escolhe uma parte só (capeback, legs, hairA, torso, hairB, head, hairC, hat, weapon),
# sem contorno, para o protagonista ser montado de peças prontas. Sem o.layer desenha tudo, como antes.
p='tools/_sprHuman_real.js';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:90];s=s.replace(a,b)
rep("  const sn=v=>Math.floor(v*4+1e-6)/4;\n","  const sn=v=>Math.floor(v*4+1e-6)/4;\n  const LYR=o.layer;let cur='x';\n")
rep("  const px=(x,y,col)=>{q.fillStyle=col;","  const px=(x,y,col)=>{if(LYR&&LYR!==cur)return;q.fillStyle=col;")
rep("  const p=(x,y,w,h,col)=>{q.fillStyle=col;","  const p=(x,y,w,h,col)=>{if(LYR&&LYR!==cur)return;q.fillStyle=col;")
rep("  const p0=P(q),ln=(a,b,c2,d,col,w)=>line(p0,","  const p0=P(q),ln=(a,b,c2,d,col,w)=>(LYR&&LYR!==cur)?0:line(p0,")
rep("  if(CP&&front&&state!=='sit')capeShape(true);\n  if(!front)weapon();\n  // ---- pernas\n",
    "  cur='capeback';if(CP&&front&&state!=='sit')capeShape(true);\n  if(!front){cur='weapon';weapon()}\n  cur='legs';\n  // ---- pernas\n")
rep("  if(front&&!HS.buzz)longBack();\n  // ---- tronco\n","  cur='hairA';if(front&&!HS.buzz)longBack();\n  cur='torso';\n  // ---- tronco\n")
rep("  // ---- pescoço e cabeça\n","  cur='head';\n  // ---- pescoço e cabeça\n")
rep("    if(HS.highpony||HS.bun)tails('f');\n","    cur='hairB';if(HS.highpony||HS.bun)tails('f');\n")
rep("&&Y<HY+2.6);\n","&&Y<HY+2.6);\n    cur='head';\n")
rep("    // cabelo da frente\n","    cur='hairC';\n    // cabelo da frente\n")
rep("  }else{\n    if(HS.buzz){","  }else{cur='hairC';\n    if(HS.buzz){")
rep("    if(CP&&state!=='sit')ellipsoid(10,6.9+by,3.6,1.3,rmat(CR),(X,Y)=>Y>HY+3.4);\n","    if(CP&&state!=='sit'){cur='torso';ellipsoid(10,6.9+by,3.6,1.3,rmat(CR),(X,Y)=>Y>HY+3.4);cur='hairC'}\n")
rep("  // ---- chapéus\n","  cur='hat';\n  // ---- chapéus\n")
rep("  if(front)weapon();\n  const out=outline(c,'#1a1020',2);out.k=KH;\n",
    "  if(front){cur='weapon';weapon()}\n  if(LYR){c.k=KH;if(state==='dead'){const r=canvas(c.height,c.width),rq=r.getContext('2d');rq.translate(0,c.width);rq.rotate(-Math.PI/2);rq.drawImage(c,0,0);r.k=KH;return r}return c}\n  const out=outline(c,'#1a1020',2);out.k=KH;\n")
# sombra da franja na testa vai para a camada do cabelo, porque depende do penteado
rep("    if(!HS.buzz&&!HS.forehead)for(let x=-2.75;x<2.75;x+=Q)px(HX+x,HY-.6+Math.abs(x)*.05,SK[2]);\n",
    "    cur='hairC';if(!HS.buzz&&!HS.forehead)for(let x=-2.75;x<2.75;x+=Q)px(HX+x,HY-.6+Math.abs(x)*.05,SK[2]);cur='head';\n")
open(p,'w',encoding='utf-8').write(s);print('ok')
