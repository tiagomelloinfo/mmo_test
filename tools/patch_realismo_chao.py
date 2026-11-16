# Chão: sombra projetada das casas e da paliçada, oclusão no pé das paredes, textura de grama e terra.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,1)
rep("SHUTD=hex(shade(o.shut||'#3a6a3a').replace(/rgb\\((\\d+),(\\d+),(\\d+)\\)/,(m,a,b2,c2)=>'#'+[a,b2,c2].map(v=>(+v).toString(16).padStart(2,'0')).join(''))),",
    "SHUTD=mul(SHUT,.72),")
# altura das casas para a sombra
rep("const o=addBox('bld',C+b.bx,C+b.by,b.spec.fw,b.spec.fh,SPR.bld[b.id],{name:b.name});","const o=addBox('bld',C+b.bx,C+b.by,b.spec.fw,b.spec.fh,SPR.bld[b.id],{name:b.name,h:b.spec.wh+(b.spec.rh||0)*.5});")
rep("  const cols={};for(const k in GR)cols[k]=GR[k].map(hex);\n  for(let PY=0;PY<GH2;PY++)",
"""  const cols={};for(const k in GR)cols[k]=GR[k].map(hex);
  // mapa de sombra (8 células por quadro): oclusão em volta dos objetos com base e sombra projetada para +x
  const SR=8,SN=N*SR,SG=new Float32Array(SN*SN).fill(1);
  for(const o of objects){if(!o.box)continue;const b=o.box,hh=o.h||16,Ls=o.kind==='bld'?hh/16*.75:.45,ao=o.kind==='bld'?.5:.3;
    for(let gy=Math.max(0,(b.by-1)*SR);gy<Math.min(SN,(b.by+b.fh+2)*SR);gy++)for(let gx=Math.max(0,(b.bx-1)*SR);gx<Math.min(SN,Math.ceil(b.bx+b.fw+Ls+1)*SR);gx++){
      const x=(gx+.5)/SR,y=(gy+.5)/SR,ddx=Math.max(b.bx-x,0,x-(b.bx+b.fw)),ddy=Math.max(b.by-y,0,y-(b.by+b.fh)),dd=Math.hypot(ddx,ddy);
      let f=dd<ao?.78+dd/ao*.22:1;
      const sx=x-(b.bx+b.fw);if(sx>=0&&sx<Ls){const y0=b.by+sx*.35,y1=b.by+b.fh+sx*.35;if(y>=y0&&y<=y1)f=Math.min(f,.66+sx/Ls*.26)}
      const k=gy*SN+gx;if(f<SG[k])SG[k]=f}}
  const shadeAt=(tx,ty)=>{const gx=Math.floor(tx*SR),gy=Math.floor(ty*SR);return gx>=0&&gy>=0&&gx<SN&&gy<SN?SG[gy*SN+gx]:1};
  for(let PY=0;PY<GH2;PY++)""")
rep("    else v=fbm(px*.045,py*.09,t*31+1)*5-.3+(vnoise(PX*.5,PY*1,17)-.5)*1.2;\n    const i=clamp(Math.round(v+bay(PX,PY)*1.1),0,4),col=cols[t][i],o=(PY*GW2+PX)*4;\n    d[o]=col[0];d[o+1]=col[1];d[o+2]=col[2];d[o+3]=255;types[PY*GW2+PX]=t;",
"""    else{v=fbm(px*.045,py*.09,t*31+1)*5-.3+(vnoise(PX*.5,PY*1,17)-.5)*1.2;
      if(t===T_GRASS||t===T_GRASS2)v+=(vnoise(PX*.22,PY*.44,21)-.5)*.9+(hash2(PX,PY,23)<.04?-1:0);
      else if(t===T_DIRT||t===T_SAND)v+=(hash2(PX>>1,PY>>1,8)-.5)*.7+(vnoise(PX*.08,PY*.16,24)-.5)*.6}
    const i=clamp(Math.round(v+bay(PX,PY)*1.1),0,4),col=cols[t][i],o=(PY*GW2+PX)*4;
    const sh=t===T_WATER?1:shadeAt(t0.x,t0.y)+(bay(PX,PY))*.03;
    d[o]=col[0]*sh;d[o+1]=col[1]*sh;d[o+2]=col[2]*sh;d[o+3]=255;types[PY*GW2+PX]=t;""")
rep("const w=pick([.5,1,1.5]);p(s.x,s.y,w,.5,'#c8b898');p(s.x,s.y+.5,w,.5,'#5a4630')}",
    "const w=pick([.5,1,1.5]);p(s.x,s.y,w,.5,'#c8b898');p(s.x,s.y,.5,.5,'#ece0c4');p(s.x,s.y+.5,w,.5,'#5a4630');p(s.x+w,s.y+.5,.5,.5,'rgba(40,28,16,.5)')}")
open(p,'w',encoding='utf-8').write(s);print('ok')
