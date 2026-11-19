# Humanos em estilo anime: sombreamento em faixas (cel shading), cabelo com mechas e brilho,
# olhos grandes com íris em degradê e dois brilhos, nariz mínimo e blush.
p='tools/_sprHuman_real.js';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:90];s=s.replace(a,b)
rep("  const rmat=(r,tex)=>(l,X,Y,s,t)=>{const i=l*5.3-.35+(tex?tex(X,Y,s,t):0);return r[Math.max(0,Math.min(5,Math.round(i)))]};",
    "  const rmat=(r,tex)=>(l,X,Y,s,t)=>{const v=l+(tex?tex(X,Y,s,t)*.12:0);return r[v<.16?1:v<.46?2:v<.84?3:4]};   // faixas chapadas (anime)")
rep("  const hair=rmat(HR,(X,Y)=>{const id=Math.round((X-HX)*4/(1+(Y-HY+4)*.12));const h=hsh(id,5);return(h-.5)*1.1+(hsh(id,Math.floor(Y*1.4))-.5)*.3-(h>.84?.9:0)});",
    "  const hband=(l,h)=>{const v=l+(h-.5)*.14;let i=v<.2?1:v<.5?2:v<.86?3:4;if(h>.88&&i>1)i--;return HR[i]};\n  const hair=(l,X,Y)=>hband(l,hsh(Math.round((X-HX)*4/(1+(Y-HY+4)*.12)),5));")
rep("  const vhair=rmat(HR,(X,Y)=>{const id=Math.round(X*4);const h=hsh(id,7);return(h-.5)*1.1-(h>.84?.9:0)});",
    "  const vhair=(l,X,Y)=>hband(l,hsh(Math.round(X*4),7));")
a=s.index("    for(const[x0,out]of[[7.75,-1],[10.5,1]]){const ey=HY+.45;")
b=s.index("    px(10.25,HY+1.75,SK[1]);")
s=s[:a]+r"""    for(const[x0,out]of[[7.6,-1],[10.65,1]]){const ey=HY+.35,W2=1.75;
      // cílio de cima grosso, com ponta para fora
      for(let x=-.25;x<W2+.25;x+=Q){px(x0+x,ey,'#1e1016');if(x>=0&&x<W2)px(x0+x,ey+.25,'#2a1418')}
      px(out<0?x0-.5:x0+W2+.25,ey+.25,'#1e1016');px(out<0?x0-.5:x0+W2+.25,ey+.5,'#2a1418');
      if(FEM){px(out<0?x0-.75:x0+W2+.5,ey,'#1e1016');px(out<0?x0-.5:x0+W2+.25,ey-.25,'#1e1016')}
      // olho grande: branco nas bordas, íris em degradê, pupila e dois brilhos
      for(let r=0;r<4;r++)for(let x=0;x<W2;x+=Q){const ix=x>=.25&&x<1.5;let col=ix?[ED,mix(E,ED,.4),E,EL][r]:(r<3?'#f6f2f0':SK[2]);
        if(ix&&(r===1||r===2)&&x>=.75&&x<1)col='#0e0810';px(x0+x,ey+.5+r*.25,col)}
      px(x0+.5,ey+.5,'#ffffff');px(x0+.25,ey+.75,'#ffffff');px(x0+.5,ey+.75,'#ffffff');px(x0+1.25,ey+1,'#ffffff');
      for(let x=.5;x<1.5;x+=Q)px(x0+x,ey+1.5,SK[1])}
    for(let x=0;x<1.75;x+=Q){px(7.4+x,HY-.6+(x<.5?.25:0),o.hair[0]);px(10.85+x,HY-.6+(x>1.25?.25:0),o.hair[0])}
"""+s[b:]
rep("    px(10.25,HY+1.75,SK[1]);px(10.25,HY+2,SK[1]);px(10,HY+2,SK[2]);px(9.75,HY+1.5,SK[4]);","    px(10.25,HY+2.1,SK[2]);px(10.25,HY+2.35,SK[1]);")
rep("    for(const bx of[7.75,11.75])for(let x=0;x<.5;x+=Q)px(bx+x,HY+1.75,mix(o.skin,'#f08080',FEM?.3:.22));",
    "    for(const bx of[7.5,11.75])for(let x=0;x<.75;x+=Q){px(bx+x,HY+2.05,mix(o.skin,'#f08080',FEM?.3:.22));if(x>0&&x<.5)px(bx+x,HY+2.3,mix(o.skin,'#f08080',FEM?.3:.22))}")
open(p,'w',encoding='utf-8').write(s)
h='index.html';t=open(h,encoding='utf-8').read()
a=t.index("function sprHuman(o,dir,state,f){");b=t.index("function sprTree(kind){")
t=t[:a]+s+t[b:];open(h,'w',encoding='utf-8').write(t);print('ok')

# olhos um pouco mais baixos para não ficarem tampados pela franja (e o resto do rosto acompanha)
s=open(p,encoding='utf-8').read()
for a,b in [("{const ey=HY+.35,W2=1.75;","{const ey=HY+.55,W2=1.75;"),
            ("px(7.4+x,HY-.6+(x<.5?.25:0),o.hair[0]);px(10.85+x,HY-.6+","px(7.4+x,HY-.4+(x<.5?.25:0),o.hair[0]);px(10.85+x,HY-.4+"),
            ("    px(10.25,HY+2.1,SK[2]);px(10.25,HY+2.35,SK[1]);","    px(10.25,HY+2.3,SK[2]);px(10.25,HY+2.55,SK[1]);"),
            ("px(bx+x,HY+2.05,mix(o.skin,'#f08080',FEM?.3:.22));if(x>0&&x<.5)px(bx+x,HY+2.3,","px(bx+x,HY+2.25,mix(o.skin,'#f08080',FEM?.3:.22));if(x>0&&x<.5)px(bx+x,HY+2.5,")]:
    assert s.count(a)==1,a;s=s.replace(a,b)
s=s.replace("px(x,HY+2.85,","px(x,HY+3.0,").replace("px(9.75,HY+3.1,","px(9.75,HY+3.25,").replace("px(10,HY+3.1,","px(10,HY+3.25,")
open(p,'w',encoding='utf-8').write(s)
t=open(h,encoding='utf-8').read();a=t.index("function sprHuman(o,dir,state,f){");b=t.index("function sprTree(kind){")
t=t[:a]+s+t[b:];open(h,'w',encoding='utf-8').write(t);print('ok 2')
