# Resolução 2x: o mundo continua nas mesmas unidades (posições, velocidades, cliques),
# mas a tela do jogo e todos os sprites passam a ter o dobro de pixels (K=2).
import sys,re
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,cnt)
def body(name):
    a=s.index('function '+name+'(');b=s.index('\n}\n',a)+3;return a,b

# ---------- primitivas
rep("function canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c}",
"""function canvas(w,h){const c=document.createElement('canvas');c.width=w;c.height=h;return c}
// resolução da arte: cada pixel lógico do mundo vira KxK pixels de verdade
const K=2;
// tela de sprite: desenha em unidades lógicas (aceita meio pixel), guarda K vezes mais pixels
function scv(w,h){const c=canvas(Math.round(w*K),Math.round(h*K));c.getContext('2d').setTransform(K,0,0,K,0,0);return c}""")
rep("function P(q){return(x,y,w,h,c)=>{q.fillStyle=c;q.fillRect(Math.floor(x),Math.floor(y),w,h)}}",
    "function P(q){const k=q.getTransform().a;return(x,y,w,h,c)=>{q.fillStyle=c;q.fillRect(Math.floor(x*k+1e-6)/k,Math.floor(y*k+1e-6)/k,w,h)}}")
rep("function line(p,x0,y0,x1,y1,c){x0=Math.round(x0);y0=Math.round(y0);x1=Math.round(x1);y1=Math.round(y1);const dx=Math.abs(x1-x0),dy=-Math.abs(y1-y0),sx=x0<x1?1:-1,sy=y0<y1?1:-1;let e=dx+dy;for(let k=0;k<200;k++){p(x0,y0,1,1,c);",
    "function line(p,x0,y0,x1,y1,c,w=1){x0=Math.round(x0*K);y0=Math.round(y0*K);x1=Math.round(x1*K);y1=Math.round(y1*K);const dx=Math.abs(x1-x0),dy=-Math.abs(y1-y0),sx=x0<x1?1:-1,sy=y0<y1?1:-1;let e=dx+dy;for(let k=0;k<400;k++){p(x0/K,y0/K,w,w,c);")
a,b=body('blob')
s=s[:a]+"""function blob(q,cx,cy,rx,ry,ramp,o={}){
  // percorre os pixels de verdade da tela (K por unidade), com sombreado e pontilhado finos
  const k=q.getTransform().a;q.save();q.setTransform(1,0,0,1,0,0);
  for(let Y=Math.floor((cy-ry)*k);Y<=Math.ceil((cy+ry)*k);Y++){
    const y=(Y+.5)/k;if(o.maxY!==undefined&&Y/k>=o.maxY+1)break;
    for(let X=Math.floor((cx-rx)*k);X<=Math.ceil((cx+rx)*k);X++){
      const x=(X+.5)/k,dx=(x-cx)/rx,dy=(y-cy)/ry,d=dx*dx+dy*dy;if(d>1)continue;
      const l=-dx*.5-dy*.7+(1-d)*.55+bay(X,Y)*.3;
      const i=l<-.3?0:l<.25?1:l<.7?2:3;
      q.fillStyle=ramp[Math.min(i,ramp.length-1)];q.fillRect(X,Y,1,1);
    }
  }
  q.restore();
}
"""+s[b:]
a,b=body('outline')
s=s[:a]+"""function outline(src,col='#22161e',t=K){
  const sw=src.width,sh=src.height,w=sw+2*t,h=sh+2*t,c=canvas(w,h),q=c.getContext('2d');
  const sd=src.getContext('2d').getImageData(0,0,sw,sh).data,out=q.createImageData(w,h),od=out.data,[r,gg,b]=hex(col);
  const A=(x,y)=>x>=0&&y>=0&&x<sw&&y<sh&&sd[(y*sw+x)*4+3]>100,N=[];
  for(let dy=-t;dy<=t;dy++)for(let dx=-t;dx<=t;dx++)if((dx||dy)&&Math.abs(dx)+Math.abs(dy)<=t+(t>1?1:0))N.push([dx,dy]);
  for(let y=0;y<h;y++)for(let x=0;x<w;x++){
    const sx=x-t,sy=y-t,i=(y*w+x)*4;
    if(A(sx,sy)){const j=(sy*sw+sx)*4;od[i]=sd[j];od[i+1]=sd[j+1];od[i+2]=sd[j+2];od[i+3]=255}
    else if(N.some(([dx,dy])=>A(sx+dx,sy+dy))){od[i]=r;od[i+1]=gg;od[i+2]=b;od[i+3]=255}
  }
  q.putImageData(out,0,0);return c;
}
"""+s[b:]

# ---------- sprites que desenham em unidades lógicas passam a usar scv()
for name in ['sprSlime','sprBunny','sprMush','sprBeetle','sprTree','sprRock','sprBush','sprWell','sprHay','sprCrop','sprCart','sprLamp','sprStall','sprBarrel','sprDummy','sprIcon','sprShelf','sprRack','sprBed','sprFire','sprTable','sprStool','sprCrate','sprCauldron','sprBoard','sprCandle']:
    try:a,b=body(name)
    except ValueError: print('sem funcao',name);continue
    seg=s[a:b];n=seg.count('canvas(');seg=seg.replace('=canvas(','=scv(')
    if n==0:print('sem canvas em',name)
    s=s[:a]+seg+s[b:]
rep("  const id=q.getImageData(0,0,38,48).data;\n  for(let k=0;k<(kind==='blossom'?30:14);k++){const x=irand(4,34),y=irand(3,30);if(id[(y*38+x)*4+3])p(x,y,1,1,kind==='blossom'?'#ffffff':R.leaf[3])}",
    "  const id=q.getImageData(0,0,c.width,c.height).data;\n  for(let k=0;k<(kind==='blossom'?60:30);k++){const x=rand(4,34),y=rand(3,30);if(id[(Math.round(y*K)*c.width+Math.round(x*K))*4+3])p(x,y,.5,.5,kind==='blossom'?'#ffffff':R.leaf[3])}")
rep("function sprShadow(w,h){const c=canvas(w,h),q=c.getContext('2d');q.fillStyle='rgba(0,0,0,.28)';for(let y=0;y<h;y++)for(let x=0;x<w;x++){const dx=(x+.5-w/2)/(w/2),dy=(y+.5-h/2)/(h/2);",
    "function sprShadow(w,h){w*=K;h*=K;const c=canvas(w,h),q=c.getContext('2d');q.fillStyle='rgba(0,0,0,.28)';for(let y=0;y<h;y++)for(let x=0;x<w;x++){const dx=(x+.5-w/2)/(w/2),dy=(y+.5-h/2)/(h/2);")
a,b=body('sprCell')
s=s[:a]+"""function sprCell(fill,solid){
  const W2=32*K,H2=16*K,c=canvas(W2,H2),q=c.getContext('2d');q.fillStyle=fill;
  for(let y=0;y<H2;y++){const hw=y<H2/2?(y+1)*2:(H2-y)*2;if(solid)q.fillRect(W2/2-hw,y,hw*2,1);else{q.fillRect(W2/2-hw,y,2,1);q.fillRect(W2/2+hw-2,y,2,1)}}
  return c;
}
"""+s[b:]
# texto dos números de dano: blocos K vezes maiores (mesmo tamanho na tela)
rep("function textSpr(s,col,sc){return cached('t'+s+col+sc,()=>{","function textSpr(s,col,sc){sc*=K;return cached('t'+s+col+sc,()=>{")
# ícones da interface: já têm o dobro de pixels
rep("function iconURL(k){return cached('url_'+k,()=>scaledURL(SPR.icons[k],2))}","function iconURL(k){return cached('url_'+k,()=>scaledURL(SPR.icons[k],2/K))}")

# ---------- prédios: mesmo desenho, amostrado em meio pixel, com texturas mais finas
a,b=body('sprBuilding')
s=s[:a]+"""function sprBuilding(o){
  const fw=o.fw,fh=o.fh,WH=o.wh,RH=o.rh||0,ov=o.roof==='flat'?0:(o.ov??.35),M=6+Math.ceil(ov*32);
  const ox=M+fh*16,oy=WH+RH+Math.ceil(ov*16)+3,cw=(fw+fh)*16+2*M,ch=oy+(fw+fh)*8+3;
  const CW2=cw*K,CH2=ch*K,c=canvas(CW2,CH2),q=c.getContext('2d'),img=q.createImageData(CW2,CH2),d=img.data,zb=new Float32Array(CW2*CH2).fill(-1e9);
  const put=(x,y,col,z)=>{x=Math.round(x*K);y=Math.round(y*K);if(x<0||y<0||x>=CW2||y>=CH2)return;const k=y*CW2+x;if(z!==undefined){if(z<zb[k])return;zb[k]=z}const i=k*4;d[i]=col[0];d[i+1]=col[1];d[i+2]=col[2];d[i+3]=255};
  const mul=(col,f)=>[Math.min(255,col[0]*f)|0,Math.min(255,col[1]*f)|0,Math.min(255,col[2]*f)|0];
  const hr=(gx,gy)=>o.roof==='gable'?WH+RH*(1-Math.abs(gy-fh/2)/(fh/2+ov)):o.roof==='pyr'?WH+RH*(1-Math.max(Math.abs(gx-fw/2)/(fw/2+ov),Math.abs(gy-fh/2)/(fh/2+ov))):WH;
  const WALL=hex(o.wc||'#efe6cf'),BEAM=hex(o.bc||'#5a3a20'),BEAML=hex('#7a5232'),STONE=hex(o.sc||'#a49e94'),MORT=hex('#6a645e'),DOOR=hex('#7a4a26'),DOORD=hex('#5a3418'),DOORL=hex('#94603a'),FRAME=hex('#3a2414'),GLASS=hex('#8ec8ec'),GLASSD=hex('#6aa8d0'),GLASSL=hex('#d8f0ff'),GOLD=hex('#e0b040'),SILL=hex('#c8b090');
  const dh=Math.min(WH*.66,20),wy0=o.wy??Math.round(WH*.42),wy1=wy0+(o.wsz??8),hs=1/K;
  const wallCol=(face,u,h,len)=>{
    const U=u*16;
    if(face===o.door){const du=Math.abs(u-o.doorAt);if(du<.4&&h<dh){
      if(du>.34||h>dh-1)return FRAME;
      if(Math.abs(u-o.doorAt-.2)<.04&&Math.abs(h-dh*.45)<.75)return GOLD;
      if(Math.abs(h-dh*.25)<.3||Math.abs(h-dh*.75)<.3)return DOORD;
      const pl=(U*2)%5;return pl<.6?DOORD:pl<1.2?DOORL:DOOR}}
    if(o.win!==false&&h<=WH)for(let k=0;k<len;k++){const cu=k+.5;if(face===o.door&&Math.abs(cu-o.doorAt)<1)continue;const du=Math.abs(u-cu);
      if(du<.25&&Math.abs(h-(wy0-.5))<.5)return SILL;
      if(du<.22&&h>=wy0&&h<=wy1){if(du>.165||h<wy0+.5||h>wy1-.5)return FRAME;if(du<.02||Math.abs(h-(wy0+wy1)/2)<.3)return FRAME;
        return h>wy1-2.5&&u<cu?GLASSL:(h<wy0+2?GLASSD:GLASS)}}
    const st=o.wall||'timber';
    if(st==='stone'||h<3){const row=Math.floor(h/4),off=(row%2)*4,hh=hash2(Math.floor((U+off)/8),row,7);if(h%4<.5||(U+off)%8<.5)return MORT;return mul(STONE,.86+hh*.26+(h%4>3?-.06:0))}
    if(st==='log'){const lg=Math.floor(U/3),f=U%3;return mul(hex(R.log[f<.5?0:f<1.8?2:1]),.9+hash2(lg,Math.floor(h/6),5)*.25)}
    if(st==='timber'){const beam=U%16<1.5||U>len*16-1.5||(h>WH-2.5&&h<=WH)||(Math.abs(h-Math.round(WH*.3))<.75);if(beam)return(U%16<.5||h>WH-.5)?BEAML:BEAM}
    if(st==='plaster'&&(U<1.5||U>len*16-1.5))return mul(STONE,.95);
    return mul(WALL,.94+hash2(U*K|0,h*K|0,3)*.09);
  };
  for(let px=0;px<=fw*16;px+=hs){const u=px/16,sx=ox-fh*16+px,base=oy+(u+fh)*8;for(let h=0;h<=WH;h+=hs)put(sx,base-h,mul(wallCol('L',u,h,fw),h<2?.8:1))}
  for(let px=0;px<=fh*16;px+=hs){const u=px/16,sx=ox+fw*16-px,base=oy+(fw+u)*8,top=o.roof==='gable'?hr(fw,u):WH;for(let h=0;h<=top;h+=hs)put(sx,base-h,mul(wallCol('R',u,h,fh),.78*(h<2?.8:1)))}
  const R4=(o.rr||R.red).map(hex),stp=1/(32*K),gx0=-ov,gx1=fw+ov,gy0=-ov,gy1=fh+ov;
  for(let gy=gy0;gy<=gy1+1e-6;gy+=stp)for(let gx=gx0;gx<=gx1+1e-6;gx+=stp){
    let idx;
    if(o.roof==='gable'){
      const dr=Math.abs(gy-fh/2),front=gy>fh/2,sv=dr*16/2.4,row=Math.floor(sv);idx=front?2:1;
      if(sv-row<.22)idx--;const sh=gx*16+(row%2)*2.2;if(sh-4.4*Math.floor(sh/4.4)<.5)idx--;
      if(front&&idx===2&&hash2(Math.floor(gx*32),row,9)<.07)idx=3;
      if(dr<.05||dr>fh/2+ov-.05||gx<gx0+.05||gx>gx1-.05)idx=0;
    }else if(o.roof==='pyr'){
      const ax=Math.abs(gx-fw/2)/(fw/2+ov),ay=Math.abs(gy-fh/2)/(fh/2+ov),m=Math.max(ax,ay),sv=(1-m)*(fh/2+ov)*16/2.2,row=Math.floor(sv);
      idx=ay>=ax&&gy>fh/2?2:1;if(sv-row<.22)idx--;if(Math.abs(ax-ay)<.02||m>.98)idx=0;
    }else{const e=Math.min(gx,gy,fw-gx,fh-gy);idx=e<.07?3:2}
    put(ox+(gx-gy)*16,oy+(gx+gy)*8-hr(gx,gy),R4[clamp(idx,0,3)],gx+gy);
  }
  if(o.roof==='pyr'){const ax=ox+(fw-fh)*8,ay=oy+(fw+fh)*4-WH-RH;for(let k=hs;k<6;k+=hs)put(ax,ay-k,k>3.5?[255,240,150]:[224,176,64])}
  q.putImageData(img,0,0);
  if(o.sign&&SPR.icons[o.sign]){
    q.setTransform(K,0,0,K,0,0);
    const u=o.door==='L'?Math.min(fw-.3,o.doorAt+.75):Math.max(.3,o.doorAt-.75),hh=dh+2;
    const sx=Math.round(o.door==='L'?ox-fh*16+u*16:ox+fw*16-u*16),sy=Math.round(o.door==='L'?oy+(u+fh)*8-hh:oy+(fw+u)*8-hh);
    const pq=P(q);pq(sx-8,sy-17,16,15,'#4a2e18');pq(sx-7,sy-16,14,13,'#e8d4a0');pq(sx-7,sy-16,14,.5,'#f8ecc8');pq(sx-6,sy-2,1,2,'#3a3a44');pq(sx+5,sy-2,1,2,'#3a3a44');q.drawImage(SPR.icons[o.sign],sx-7,sy-16,SPR.icons[o.sign].width/K,SPR.icons[o.sign].height/K);
    q.setTransform(1,0,0,1,0,0);
  }
  const out=o.noOutline?c:outline(c,'#1e1a1e'),e=o.noOutline?0:1;
  return{c:out,ax:ox+(fw-fh)*16+e,ay:oy+(fw+fh)*8+e,mc:o.rr?o.rr[1]:'#86827e'};
}
"""+s[b:]

# ---------- chão do mundo em 2x
rep("  const c=canvas(GW,GH),q=c.getContext('2d'),img=q.createImageData(GW,GH),d=img.data,types=new Int8Array(GW*GH).fill(-1);",
    "  const GW2=GW*K,GH2=GH*K,c=canvas(GW2,GH2),q=c.getContext('2d'),img=q.createImageData(GW2,GH2),d=img.data,types=new Int8Array(GW2*GH2).fill(-1);")
a=s.index("  for(let py=0;py<GH;py++)for(let px=0;px<GW;px++){\n    const t0=unIso(px+.5,py+.5)")
b=s.index("  q.putImageData(img,0,0);\n  const p=P(q);",a)
s=s[:a]+"""  for(let PY=0;PY<GH2;PY++)for(let PX=0;PX<GW2;PX++){
    const px=PX/K,py=PY/K,t0=unIso(px+.25,py+.25),base=typeAt(t0.x,t0.y);if(base<0)continue;
    let t=base;
    if(base!==T_STONE){const jx=(vnoise(px*.09,py*.18,5)-.5)*.8,jy=(vnoise(px*.09,py*.18,9)-.5)*.8;const tj=typeAt(t0.x+jx,t0.y+jy);if(tj>=0&&tj!==T_STONE)t=tj}
    let v;
    if(t===T_STONE){const ux=t0.x*2,uy=t0.y*2,u=ux-Math.floor(ux),w=uy-Math.floor(uy),slab=hash2(Math.floor(ux),Math.floor(uy),3);v=(u<.04||w<.04)?0:(u>.96||w>.96)?1:1.6+slab*1.7+(vnoise(PX*.3,PY*.6,4)-.5)}
    else if(t===T_WATER)v=1.6+(vnoise(px*.04,py*.12,6)-.5)*2.6;
    else v=fbm(px*.045,py*.09,t*31+1)*5-.3+(vnoise(PX*.5,PY*1,17)-.5)*1.2;
    const i=clamp(Math.round(v+bay(PX,PY)*1.1),0,4),col=cols[t][i],o=(PY*GW2+PX)*4;
    d[o]=col[0];d[o+1]=col[1];d[o+2]=col[2];d[o+3]=255;types[PY*GW2+PX]=t;
  }
  for(let py=3*K;py<GH2;py++)for(let px=0;px<GW2;px++){
    const k=py*GW2+px;if(types[k]!==T_WATER)continue;
    const up=j=>types[k-j*GW2],o=k*4;let col=null;
    const land=j=>{const a=up(j);return a>=0&&a!==T_WATER};
    if(land(1)||land(2))col=[18,46,92];else if(land(3)||land(4))col=[26,62,116];else if(land(5)||land(6))col=[140,190,232];
    if(col){d[o]=col[0];d[o+1]=col[1];d[o+2]=col[2]}
  }
"""+s[b:]
rep("  q.putImageData(img,0,0);\n  const p=P(q);","  q.putImageData(img,0,0);q.setTransform(K,0,0,K,0,0);\n  const p=P(q);")
rep("for(let k=0;k<4200;k++){const s=randPt();if(s.t!==T_GRASS&&s.t!==T_GRASS2)continue;p(s.x,s.y-1,1,2,s.t===T_GRASS?'#8cc85a':'#5c9a40');p(s.x-1,s.y,1,1,'#2c5a22');p(s.x+1,s.y-1,1,2,s.t===T_GRASS?'#74b04a':'#4a8436')}",
    "for(let k=0;k<4200*K*K;k++){const s=randPt();if(s.t!==T_GRASS&&s.t!==T_GRASS2)continue;const x=s.x+rand(-.5,.5),y=s.y+rand(-.5,.5);p(x,y-1,.5,1.5,s.t===T_GRASS?'#8cc85a':'#5c9a40');p(x-.5,y,.5,.5,'#2c5a22');p(x+.5,y-.5,.5,1,s.t===T_GRASS?'#74b04a':'#4a8436')}")
rep("const col=pick(['#fff4f0','#ffd84a','#ff7aa0','#b48aff','#ffffff']);p(s.x,s.y-1,1,1,col);p(s.x-1,s.y,1,1,col);p(s.x+1,s.y,1,1,col);p(s.x,s.y+1,1,1,col);p(s.x,s.y,1,1,'#f0c020');p(s.x,s.y+2,1,1,'#2c5a22')}",
    "const col=pick(['#fff4f0','#ffd84a','#ff7aa0','#b48aff','#ffffff']);p(s.x,s.y-1,1,1,col);p(s.x-1,s.y,1,1,col);p(s.x+1,s.y,1,1,col);p(s.x,s.y+1,1,1,col);p(s.x,s.y,1,1,'#f0c020');p(s.x+.5,s.y+.5,.5,.5,'#c89010');p(s.x,s.y-1,.5,.5,'#ffffff');p(s.x,s.y+2,.5,1.5,'#2c5a22')}")
rep("for(let k=0;k<700;k++){const s=randPt();if(s.t!==T_DIRT&&s.t!==T_SAND)continue;p(s.x,s.y,2,1,'#c8b898');p(s.x,s.y+1,2,1,'#5a4630')}",
    "for(let k=0;k<700*K*K;k++){const s=randPt();if(s.t!==T_DIRT&&s.t!==T_SAND)continue;const w=pick([.5,1,1.5]);p(s.x,s.y,w,.5,'#c8b898');p(s.x,s.y+.5,w,.5,'#5a4630')}")
rep("mq.drawImage(c,0,0,GW,GH,0,0,184,96);","mq.drawImage(c,0,0,c.width,c.height,0,0,184,96);")

# ---------- chão dos interiores em 2x
a,b=body('buildRoomGround')
seg=s[a:b]
seg=seg.replace("const c=canvas(cw,ch),q=c.getContext('2d'),img=q.createImageData(cw,ch),d=img.data;\n  const put=(x,y,col)=>{x=Math.round(x);y=Math.round(y);if(x<0||y<0||x>=cw||y>=ch)return;const i=(y*cw+x)*4;",
                "const c=canvas(cw*K,ch*K),q=c.getContext('2d'),img=q.createImageData(cw*K,ch*K),d=img.data,CW2=cw*K,CH2=ch*K;\n  const put=(x,y,col)=>{x=Math.round(x*K);y=Math.round(y*K);if(x<0||y<0||x>=CW2||y>=CH2)return;const i=(y*CW2+x)*4;")
seg=seg.replace("  for(let py=0;py<ch;py++)for(let px=0;px<cw;px++){\n    const t=unIso(px+ox+.5,py+oy+.5);",
                "  for(let PY=0;PY<CH2;PY++)for(let PX=0;PX<CW2;PX++){\n    const px=PX/K,py=PY/K,t=unIso(px+ox+.25,py+oy+.25);")
seg=seg.replace("col=F[clamp(Math.round(fbm(px*.08,py*.16,3)*3.4+bay(px,py)),0,3)]","col=F[clamp(Math.round(fbm(px*.08,py*.16,3)*3.4+bay(PX,PY)),0,3)]")
seg=seg.replace("col=(fr<.13||j<.05)?F[0]:F[1+Math.floor(hash2(Math.floor((lx+off)/1.5),row,7)*2.99)]",
                "col=(fr<.09||j<.03)?F[0]:(fr>.9?F[1]:F[1+Math.floor(hash2(Math.floor((lx+off)/1.5),row,7)*2.99)])")
seg=seg.replace("for(let hh=0;hh<=WH;hh++)put(sx-ox,base-hh-oy,wallAt(k*w,hh,rm.winR||[]))","for(let hh=0;hh<=WH;hh+=1/K)put(sx-ox,base-hh-oy,wallAt(k*w,hh,rm.winR||[]))")
seg=seg.replace("for(let hh=0;hh<=WH;hh++)put(sx-ox,base-hh-oy,mul(wallAt(k*h,hh,rm.winL||[]),.8))","for(let hh=0;hh<=WH;hh+=1/K)put(sx-ox,base-hh-oy,mul(wallAt(k*h,hh,rm.winL||[]),.8))")
seg=seg.replace("for(let sx=Math.floor(T.x);sx<=Math.ceil(Rt.x);sx++){","for(let sx=Math.floor(T.x);sx<=Math.ceil(Rt.x);sx+=1/K){")
seg=seg.replace("for(let sx=Math.floor(L.x);sx<=Math.ceil(T.x);sx++){","for(let sx=Math.floor(L.x);sx<=Math.ceil(T.x);sx+=1/K){")
seg=seg.replace("for(let sx=Math.floor(A.x);sx<=Math.ceil(Bp.x);sx++){","for(let sx=Math.floor(A.x);sx<=Math.ceil(Bp.x);sx+=1/K){")
seg=seg.replace("for(let j=1;j<=5;j++)put(sx-ox,base+j-oy,","for(let j=.5;j<=5;j+=1/K)put(sx-ox,base+j-oy,")
seg=seg.replace("if(u%1<.06)return BEAM;","if(u%1<.06)return BEAM;if(hh>=12&&hh<13)return mul(WAIND,1.15);")
s=s[:a]+seg+s[b:]

# ---------- tela do jogo em 2x e desenho com di()
rep("function resize(){SCALE=innerWidth>=1900?3:2;W=Math.ceil(innerWidth/SCALE);H=Math.ceil(innerHeight/SCALE);cv.width=W;cv.height=H;",
    "function resize(){SCALE=innerWidth>=3000?4:2;W=Math.ceil(innerWidth/SCALE);H=Math.ceil(innerHeight/SCALE);cv.width=W*K;cv.height=H*K;")
a,b=body('drawSpr')
s=s[:a]+"""function drawSpr(c,x,y,flip,alpha=1){
  x=Math.round(x*K)/K;y=Math.round(y*K)/K;if(alpha<1)g.globalAlpha=alpha;
  const w=c.width/K,h=c.height/K,hx=Math.floor(c.width/2)/K;
  if(flip){g.save();g.translate(x,0);g.scale(-1,1);g.drawImage(c,-hx,y-h+1,w,h);g.restore()}
  else g.drawImage(c,x-hx,y-h+1,w,h);
  if(alpha<1)g.globalAlpha=1;
}
// desenha um sprite de alta resolução no lugar (unidades do mundo)
function di(c,x,y){g.drawImage(c,x,y,c.width/K,c.height/K)}
"""+s[b:]
rep("function scr(e){const s=iso(e.x,e.y);return{x:Math.round(s.x-CAM.x),y:Math.round(s.y-CAM.y)}}",
    "function scr(e){const s=iso(e.x,e.y);return{x:Math.round((s.x-CAM.x)*K)/K,y:Math.round((s.y-CAM.y)*K)/K}}")
rep("  const pp=iso(me.x,me.y);let cx=Math.round(pp.x-W/2),cy=Math.round(pp.y-14-H/2);",
    "  g.setTransform(K,0,0,K,0,0);g.imageSmoothingEnabled=false;\n  const pp=iso(me.x,me.y);let cx=Math.round((pp.x-W/2)*K)/K,cy=Math.round((pp.y-14-H/2)*K)/K;")
rep("  g.drawImage(groundC,gOff.x-cx,gOff.y-cy);","  di(groundC,gOff.x-cx,gOff.y-cy);")
rep("g.drawImage(SPR.cell,Math.round(s.x-cx-16),Math.round(s.y-cy))","di(SPR.cell,Math.round(s.x-cx-16),Math.round(s.y-cy))")
rep("g.drawImage(SPR.mark,Math.round(s.x-cx-16),Math.round(s.y-cy))","di(SPR.mark,Math.round(s.x-cx-16),Math.round(s.y-cy))")
rep("const visBox=o=>{const s=iso(o.vx,o.vy),x=s.x-cx-o.ax,y=s.y-cy-o.ay;return x<W&&x+o.spr.width>0&&y<H&&y+o.spr.height>0};",
    "const visBox=o=>{const s=iso(o.vx,o.vy),x=s.x-cx-o.ax,y=s.y-cy-o.ay;return x<W&&x+o.spr.width/K>0&&y<H&&y+o.spr.height/K>0};")
rep("const s0=iso(o.vx,o.vy),x=Math.round(s0.x-cx-o.ax),y=Math.round(s0.y-cy-o.ay);let al=1;",
    "const s0=iso(o.vx,o.vy),x=Math.round((s0.x-cx-o.ax)*K)/K,y=Math.round((s0.y-cy-o.ay)*K)/K;let al=1;")
rep("if(hs.x>x+4&&hs.x<x+o.spr.width-4&&hs.y>y&&hs.y-28<y+o.spr.height)al=.5}","if(hs.x>x+4&&hs.x<x+o.spr.width/K-4&&hs.y>y&&hs.y-28<y+o.spr.height/K)al=.5}")
rep("      if(al<1)g.globalAlpha=al;g.drawImage(o.spr,x,y);g.globalAlpha=1;","      if(al<1)g.globalAlpha=al;di(o.spr,x,y);g.globalAlpha=1;")
s=s.replace("g.drawImage(SPR.shBig,","di(SPR.shBig,").replace("g.drawImage(SPR.shMed,","di(SPR.shMed,").replace("g.drawImage(SPR.shSm,","di(SPR.shSm,")
s=s.replace("g.drawImage(sc>1?SPR.shBig:SPR.shMed,","di(sc>1?SPR.shBig:SPR.shMed,")
s=s.replace("g.drawImage(SPR.shMed,s.x-9,s.y-4);","di(SPR.shMed,s.x-9,s.y-4);")
rep("g.drawImage(ic,s.x-7,s.y-12+bob);","di(ic,s.x-7,s.y-12+bob);")
rep("g.globalAlpha=t>.8?clamp(1-(t-.8)/.4,0,1):1;g.drawImage(c,Math.round(x),Math.round(y));g.globalAlpha=1;","g.globalAlpha=t>.8?clamp(1-(t-.8)/.4,0,1):1;di(c,Math.round(x),Math.round(y));g.globalAlpha=1;")
# casa sob o cursor: teste do pixel na resolução real
rep("const s0=iso(o.vx,o.vy),x=Math.round(mx-(s0.x-CAM.x-o.ax)),y=Math.round(my-(s0.y-CAM.y-o.ay));",
    "const s0=iso(o.vx,o.vy),x=Math.floor((mx-(s0.x-CAM.x-o.ax))*K),y=Math.floor((my-(s0.y-CAM.y-o.ay))*K);")
# tela de título
rep("(function titleLoop(){if(started)return;TIME+=1/60;const t=TIME*.15;g.fillStyle='#0d1a0f';g.fillRect(0,0,W,H);const s=iso(C+Math.cos(t)*6,C+Math.sin(t)*6);g.drawImage(groundC,-Math.round(s.x-W/2),-Math.round(s.y-H/2));",
    "(function titleLoop(){if(started)return;TIME+=1/60;const t=TIME*.15;g.setTransform(K,0,0,K,0,0);g.imageSmoothingEnabled=false;g.fillStyle='#0d1a0f';g.fillRect(0,0,W,H);const s=iso(C+Math.cos(t)*6,C+Math.sin(t)*6);di(groundC,-Math.round(s.x-W/2),-Math.round(s.y-H/2));")
open(p,'w',encoding='utf-8').write(s);print('ok')
