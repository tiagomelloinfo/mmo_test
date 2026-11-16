# Fardo de feno e barril redesenhados em pixel art realista, em isométrico, pixel a pixel na resolução 2x.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,1)
a=s.index("function sprHay(){");b=s.index("\n",a)+1
s=s[:a]+r"""// fardo de feno retangular em isométrico: topo e lateral com fibras no comprimento, ponta cortada, dois barbantes
function sprHay(){
  const CWd=40,CHd=30,c=scv(CWd,CHd),q=c.getContext('2d');
  const Lx=17,Ly=10,H=10,X0=16.5,Y0=17.5;
  const PAL=['#3e2c0c','#5a4214','#76591c','#927026','#ae8830','#c69e3c','#d8b450','#e6c86a','#f2dc92'].map(hex);
  const W2=c.width,H2=c.height,img=q.createImageData(W2,H2),d=img.data;
  const tw=[Lx*.27,Lx*.73];
  const strand=(u,v,seed)=>{const row=Math.floor(v*K*1.6),off=hash2(row,seed,3)*4;return hash2(row,Math.floor(u/2.6+off),seed)};
  for(let Y=0;Y<H2;Y++)for(let X=0;X<W2;X++){
    const x=(X+.5)/K,y=(Y+.5)/K;let tone=null,face='';
    // topo (h=H)
    {const s1=x-X0,s2=2*(y-Y0+H),a=(s1+s2)/2,b=(s2-s1)/2;
      if(a>=0&&a<=Lx&&b>=0&&b<=Ly){face='t';
        tone=.25+strand(a,b,11)*.7+vnoise(a*.18,b*.25,12)*.2+hash2(X,Y,13)*.1+1.1;if(strand(a+1.3,b,15)<.12)tone-=.6;
        const ed=Math.min(b,Ly-b,a,Lx-a);if(ed<.8)tone+=(Ly-b<.8||Lx-a<.8)?.35:-.35;
        for(const t of tw){const dt=Math.abs(a-t);if(dt<.7){tone=dt<.25?.9:.2;face='tw'}else if(dt<1.3)tone-=.45}}}
    // lateral comprida (b=Ly), voltada para a esquerda-baixo
    if(tone===null){const a=x-X0+Ly,h=Y0+(a+Ly)/2-y;
      if(a>=0&&a<=Lx&&h>=0&&h<=H){face='l';
        tone=.1+strand(a,h,21)*.7+vnoise(a*.2,h*.3,22)*.18+hash2(X,Y,23)*.1;if(strand(a+1.3,h,25)<.12)tone-=.6;
        if(H-h<.8)tone+=.4;if(h<2.5)tone-=(2.5-h)*.35;if(a<.7)tone-=.3;
        for(const t of tw){const dt=Math.abs(a-t);if(dt<.7){tone=dt<.25?.55:-.05;face='tw'}else if(dt<1.3)tone-=.4}}}
    // ponta cortada (a=Lx), voltada para a direita-baixo: talos cortados, mais escura
    if(tone===null){const b=X0+Lx-x,h=Y0+(Lx+b)/2-y;
      if(b>=0&&b<=Ly&&h>=0&&h<=H){face='e';
        tone=-.55+hash2(X,Y,31)*.55+vnoise(b*.7,h*.7,32)*.45;
        if(hash2(X>>1,Y>>1,33)<.08)tone+=.7;if(hash2(X,Y,34)<.05)tone-=.6;
        if(H-h<.8)tone+=.3;if(h<2.5)tone-=(2.5-h)*.3;if(b<.6)tone+=.25}}
    if(tone===null)continue;
    let col;
    if(face==='tw'){col=tone>.7?[150,98,48]:tone>.3?[110,70,34]:[74,46,22]}
    else{const i=clamp(Math.round(tone*3.2+bay(X,Y)*.6+2.4),0,PAL.length-1);col=PAL[i]}
    const o=(Y*W2+X)*4;d[o]=col[0];d[o+1]=col[1];d[o+2]=col[2];d[o+3]=255;
  }
  q.save();q.setTransform(1,0,0,1,0,0);q.putImageData(img,0,0);q.restore();
  const p=P(q),S=['#f2dc92','#e6c86a','#d8b450','#c69e3c'];
  // fiapos soltos saindo das quinas de cima
  for(let i=0;i<24;i++){const a=rand(0,Lx),edge=Math.random()<.5;const bx=edge?X0+a-Ly:X0+Lx-rand(0,Ly),by=edge?Y0+(a+Ly)/2-H:Y0+(Lx+(X0+Lx-bx))/2-H;
    const ang=rand(-2.6,-.5),len=rand(1.5,3.5);line(p,bx,by,bx+Math.cos(ang)*len,by+Math.sin(ang)*len,pick(S),.5)}
  return outline(c,'#2e2008');
}
// palha caída no chão e sombra de contato (por fora do contorno)
function hayGround(c){
  const q=c.getContext('2d');q.save();q.setTransform(K,0,0,K,0,0);const p=P(q),X0=17.5,Y0=18.5,Lx=17,Ly=10;
  q.fillStyle='rgba(30,20,0,.32)';q.beginPath();q.moveTo(X0+Lx,Y0+Lx/2);q.lineTo(X0+Lx+3,Y0+Lx/2+1.5);q.lineTo(X0+Lx-Ly+3,Y0+(Lx+Ly)/2+1.5);q.lineTo(X0+Lx-Ly,Y0+(Lx+Ly)/2);q.closePath();q.fill();
  for(let i=0;i<16;i++){const x=rand(4,34),y=rand(22,29),ang=rand(-.6,.6),len=rand(1.5,3);line(p,x,y,x+Math.cos(ang)*len,y+Math.sin(ang)*len*.5,pick(['#d8b450','#c69e3c','#e6c86a','#ae8830']),.5)}
  q.restore();return c;
}
"""+s[b:]
a=s.index("function sprBarrel(){");b=s.index("\n",a)+1
s=s[:a]+r"""// barril de aduelas: barriga abaulada, veio, três aros de ferro com rebites e ferrugem, tampa com tábuas e batoque
function sprBarrel(){
  const c=scv(15,20),q=c.getContext('2d'),W2=c.width,H2=c.height,img=q.createImageData(W2,H2),d=img.data;
  const cx=7.5,y0=4.6,Hh=13.4,R0=5.6,BUL=.13,RYF=.4;
  const WOOD=['#2e1c0e','#4a2e16','#643e1e','#7e5028','#9a6434','#b47a42','#cc9252'].map(hex),IRON=['#1c1c22','#2e2e36','#46464f','#62626e','#8a8a98','#c4c4d0'].map(hex),RUST=hex('#7a4a26');
  const rAt=t=>R0*(1+BUL*Math.sin(Math.PI*clamp(t,0,1)));
  const hoops=[[.06,.15],[.43,.5],[.85,.94]];
  for(let Y=0;Y<H2;Y++)for(let X=0;X<W2;X++){
    const x=(X+.5)/K,y=(Y+.5)/K;let col=null;
    // corpo: entre a borda de cima e a de baixo
    const t=(y-y0)/Hh,r=rAt(t),nx=(x-cx)/r;
    if(Math.abs(nx)<=1){
      const ez=Math.sqrt(1-nx*nx),yt=y0+R0*RYF*ez,yb=y0+Hh+rAt(1)*RYF*ez;
      if(y>=yt&&y<=yb){
        const th=Math.asin(nx),sf=(th/Math.PI+.5)*10,si=Math.floor(sf),fr=sf-si;
        let l=.5-nx*.42+ez*.25+(Math.abs(nx+.45)<.12?.18:0);
        let hp=null;for(const[h0,h1]of hoops)if(t>=h0&&t<=h1)hp=(t-h0)/(h1-h0);
        if(hp!==null){
          let li=l+(hp<.25?.25:hp>.8?-.3:0);if(Math.abs(fr-.5)<.08&&Math.abs(hp-.5)<.2)li+=.5;
          col=IRON[clamp(Math.round(li*4.2+bay(X,Y)*.5),0,5)];if(hash2(X>>1,Y>>1,41)<.07)col=RUST;
        }else{
          l+=(hash2(si,0,42)-.5)*.2+(vnoise(si*3.1,y*.9,43)-.5)*.28;
          if(fr<.07||fr>.96)l-=.55;
          if(y>yb-1.2)l-=.35;if(y<yt+.8)l+=.15;
          col=WOOD[clamp(Math.round(l*5+bay(X,Y)*.6),0,6)];
        }
      }
    }
    // tampa: elipse de cima com borda das aduelas, tábuas e batoque
    if(col===null){const rx=R0,ry=R0*RYF,ex=(x-cx)/rx,ey=(y-y0)/ry,e=ex*ex+ey*ey;
      if(e<=1){
        if(e>.62){const ang=Math.atan2(ey,ex);col=WOOD[ey<0?4:(Math.floor((ang+3.2)*3)%2?5:4)];if(e>.9)col=WOOD[ey<0?2:3]}
        else{const pl=Math.floor((x-cx+rx)/2.2),fp=((x-cx+rx)/2.2)%1;let l=.42+(hash2(pl,1,44)-.5)*.2-ey*.12;if(fp<.1)l-=.4;
          if(Math.hypot(x-(cx+1.6),(y-y0)/RYF*.4)<.55)l=-.2;
          col=WOOD[clamp(Math.round(l*5+bay(X,Y)*.5),0,6)]}
      }}
    if(col===null)continue;
    const o=(Y*W2+X)*4;d[o]=col[0];d[o+1]=col[1];d[o+2]=col[2];d[o+3]=255;
  }
  q.save();q.setTransform(1,0,0,1,0,0);q.putImageData(img,0,0);q.restore();
  return outline(c,'#1a1008');
}
"""+s[b:]
rep("SPR.hay=sprHay();","SPR.hay=hayGround(sprHay());")
rep("addObj('hay',a,b,{spr:SPR.hay});","addObj('hay',a,b,{spr:SPR.hay,noSh:true});")
rep("if(['shelfP','books','shelfJ','rack','board','fire','bed'].includes(k))o.noSh=true;","if(['shelfP','books','shelfJ','rack','board','fire','bed','hay'].includes(k))o.noSh=true;")
open(p,'w',encoding='utf-8').write(s);print('ok')
