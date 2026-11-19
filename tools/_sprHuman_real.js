// humanos realistas em 4x: proporções de ~4,3 cabeças, volume por luz (cima-esquerda),
// tecido com dobras, cabelo em mechas, rosto proporcional. Mesmo tamanho e mesma base (pés) de antes.
function sprHuman(o,dir,state,f){
  const LW=32,LH=41,c=hcv(LW,LH),q=c.getContext('2d'),OX=6,OY=9.5,Q=.25;
  const sn=v=>Math.floor(v*4+1e-6)/4;
  const px=(x,y,col)=>{q.fillStyle=col;q.fillRect(sn(x+OX),sn(y+OY),Q,Q)};
  const p=(x,y,w,h,col)=>{q.fillStyle=col;q.fillRect(sn(x+OX),sn(y+OY),w,h)};
  const p0=P(q),ln=(a,b,c2,d,col,w)=>line(p0,a+OX,b+OY,c2+OX,d+OY,col,w);
  const hsh=(a,b)=>{let h=(a*374761393+b*668265263)^0x5bd1e995;h=Math.imul(h^(h>>>13),1274126177);return((h^(h>>>16))>>>0)/4294967296};
  const rgb=v=>String(v).startsWith('rgb')?String(v).match(/\d+/g).map(Number):hex(v);
  const mix=(a,b,t)=>{const A=rgb(a),B=rgb(b);return'#'+A.map((v,i)=>Math.max(0,Math.min(255,Math.round(v+(B[i]-v)*t))).toString(16).padStart(2,'0')).join('')};
  // rampa de 6 tons com sombra fria e luz quente
  const ramp=b=>[mix(b,'#160c24',.6),mix(b,'#22163a',.4),mix(b,'#2a2244',.18),mix(b,'#000000',0),mix(b,'#fff2d0',.22),mix(b,'#fffaf0',.46)];
  const rmat=(r,tex)=>(l,X,Y,s,t)=>{const i=l*5.3-.35+(tex?tex(X,Y,s,t):0);return r[Math.max(0,Math.min(5,Math.round(i)))]};
  const Lx=-.5,Ly=-.55,Lz=.67;
  const curve=(pts,v)=>{if(v<=pts[0][0])return pts[0][1];for(let i=1;i<pts.length;i++)if(v<=pts[i][0]){const[a0,b0]=pts[i-1],[a1,b1]=pts[i],t=(v-a0)/(a1-a0),k=(1-Math.cos(t*Math.PI))/2;return b0+(b1-b0)*k}return pts[pts.length-1][1]};
  // ---- primitivas com volume
  const ellipsoid=(cx,cy,rx,ry,mat,clip)=>{for(let y=sn(cy-ry);y<cy+ry;y+=Q)for(let x=sn(cx-rx);x<cx+rx;x+=Q){const X=x+.125,Y=y+.125;const dx=(X-cx)/rx,dy=(Y-cy)/ry,d=dx*dx+dy*dy;if(d>1)continue;if(clip&&!clip(X,Y))continue;const nz=Math.sqrt(1-d);px(x,y,mat(Math.max(0,dx*Lx+dy*Ly+nz*Lz),X,Y,dx,dy))}};
  const limb=(x0,y0,x1,y1,r0,r1,mat,clip)=>{const vx=x1-x0,vy=y1-y0,L2=vx*vx+vy*vy||1e-6,len=Math.sqrt(L2),nxp=-vy/len||1,nyp=vx/len||0,R=Math.max(r0,r1);
    for(let y=sn(Math.min(y0,y1)-R);y<Math.max(y0,y1)+R;y+=Q)for(let x=sn(Math.min(x0,x1)-R);x<Math.max(x0,x1)+R;x+=Q){const X=x+.125,Y=y+.125;let t=((X-x0)*vx+(Y-y0)*vy)/L2;t=Math.max(0,Math.min(1,t));
      const r=r0+(r1-r0)*t,dx=X-(x0+vx*t),dy=Y-(y0+vy*t);if(dx*dx+dy*dy>r*r)continue;if(clip&&!clip(X,Y,t))continue;
      let s=(dx*nxp+dy*nyp)/r;if(nxp<0)s=-s;const nz=Math.sqrt(Math.max(0,1-s*s));px(x,y,mat(Math.max(0,s*Lx+nz*Lz+.1),X,Y,s,t))}};
  const front=dir!=='b';
  let by=0,lL=0,lR=0,aL=0,aR=0;
  if(state==='walk'){if(f===1){lL=1;aL=1;aR=-1;by=-.5}if(f===3){lR=1;aL=-1;aR=1;by=-.5}}
  if(state==='sit')by=4;
  const hb=by+(state==='idle'&&f===1?.25:0);
  const FEM=o.sex==='f',HS=HAIRSTYLES[o.hs]||HAIRSTYLES.npc,HX=10,HY=1.5+hb;
  let hand=[15.2,17.4+by+aR],tip=[18.2,23.4+by+aR];
  if(state==='attack'){hand=[[14.5,1.5],[17,7],[16.5,13]][f];tip=[[9,-6],[23,4],[21,20]][f]}
  if(state==='cast'){hand=[15.8,4+by];tip=[17.8,-3+by]}
  // ---- materiais
  const SK=[mix(o.skin,'#6a2e30',.5),mix(o.skin,'#9a5048',.32),mix(o.skin,'#c07060',.16),o.skin,mix(o.skin,'#fff4e8',.3),mix(o.skin,'#ffffff',.5)],T=o.tunic,TR=ramp(T),PR=ramp(o.pants),BR=ramp(o.boot),LR=ramp(o.belt),HR=(()=>{const[H0,H1,H2]=o.hair;return[mix(H0,'#100818',.45),H0,mix(H0,H1,.5),H1,mix(H1,H2,.55),H2]})();
  const skin=rmat(SK),cloth=rmat(TR,(X,Y)=>(hsh(Math.round(X*2.6+Y*.35),Math.floor(Y*1.6))-.5)*.45);
  const pants=rmat(PR,(X,Y)=>(hsh(Math.round(X*3),Math.floor(Y*1.2))-.5)*.35+(o.legsJeans&&hsh(Math.floor(X*4),Math.floor(Y*4))>.8?.4:0));
  const boot=rmat(BR,()=>0),leather=rmat(LR,()=>0);
  const isMetal=col=>{const[r,g,b]=rgb(col),mx=Math.max(r,g,b),mn=Math.min(r,g,b);return mx>0&&(mx-mn)/mx<.18};
  const weapon=()=>{
    if(!o.weapon)return;const[hx,hy]=hand,vx=tip[0]-hx,vy=tip[1]-hy;
    const at=k=>[hx+vx*k,hy+vy*k],L=lighten(o.blade,1.1);
    const guard=()=>{p(hx-1.5,hy-1,4,1.5,'#c08a20');p(hx-1.5,hy-1,4,.5,'#ffe48a');p(hx-1.5,hy+.25,4,.25,'#8a5a10');p(hx,hy+.5,1,1.5,'#6b4426');p(hx+.25,hy+.75,.25,1,'#8e6034');p(hx,hy+2,1,.5,'#e0b040')};
    if(o.wtype==='adaga'){const[tx,ty]=at(.6);ln(hx,hy,tx,ty,o.blade);ln(hx+1,hy,tx+1,ty,o.bladeD);ln(hx,hy,tx,ty,L,.5);ln(hx+.25,hy,tx+.25,ty,'#ffffff',.25);guard()}
    else if(o.wtype==='espada'){const[tx,ty]=at(1);ln(hx,hy,tx,ty,o.blade);ln(hx+1,hy,tx+1,ty,o.bladeD);ln(hx+.5,hy,tx+.5,ty,shade(o.blade),.5);ln(hx,hy,tx,ty,L,.5);ln(hx+.25,hy,tx+.25,ty,'#ffffff',.25);guard()}
    else if(o.wtype==='lanca'){const[bx,by2]=at(-.45),[mx,my]=at(1.25),[tx,ty]=at(1.6);ln(bx,by2,mx,my,'#8e6034');ln(bx+.5,by2,mx+.5,my,'#6b4426',.5);ln(bx+.25,by2,mx+.25,my,'#a87444',.25);ln(mx,my,tx,ty,o.blade);ln(mx,my,tx,ty,L,.5);p(mx-1,my-1,3,2,o.bladeD);p(mx-1,my-1,3,.5,L)}
    else if(o.wtype==='machado'){const[tx,ty]=at(1);ln(hx,hy,tx,ty,'#8e6034');ln(hx+.5,hy,tx+.5,ty,'#6b4426',.5);p(tx-2.5,ty-2.5,4.5,4.5,o.bladeD);p(tx-2.5,ty-2.5,3.5,3.5,o.blade);p(tx-2.5,ty-2.5,.5,3.5,L);p(tx-2.25,ty-2.25,.25,3,'#ffffff');p(tx-.5,ty-.5,1,1,'#5a3a20');p(tx-.25,ty-.25,.5,.5,'#8e6034')}
    else if(o.wtype==='maca'){const[tx,ty]=at(.95),mL=o.maceL||'#a8b0c0',mD=o.maceD||'#6a7080';ln(hx,hy,tx,ty,'#6b4426');p(tx-2,ty-2,4,4,mD);p(tx-2,ty-2,3,3,mL);p(tx-1.5,ty-1.5,1,1,'#ffffff');p(tx-3,ty-.5,1,1,mD);p(tx+2,ty-.5,1,1,mD);p(tx-.5,ty-3,1,1,mD);p(tx-.5,ty+2,1,1,mD)}
  };
  const hair=rmat(HR,(X,Y)=>{const id=Math.round((X-HX)*4/(1+(Y-HY+4)*.12));const h=hsh(id,5);return(h-.5)*1.1+(hsh(id,Math.floor(Y*1.4))-.5)*.3-(h>.84?.9:0)});
  const vhair=rmat(HR,(X,Y)=>{const id=Math.round(X*4);const h=hsh(id,7);return(h-.5)*1.1-(h>.84?.9:0)});   // fios verticais (cabelo comprido)
  const JA=HS.jag??.075,JN=HS.jagN??11,VOL=HS.vol||1,SIDE=HS.sides??4.3;
  const jag=(X,Y,cy)=>{const a=Math.atan2(Y-cy,X-HX),u=(a+Math.PI)*JN/(2*Math.PI),fr=u-Math.floor(u);return Y<cy+.5?1+JA*(1-Math.abs(fr-.5)*2)*(.6+hsh(Math.floor(u),9)*.8):1};
  const crown=(X,Y,cy)=>{const dx=(X-HX)/(3.95*VOL),dy=(Y-cy)/(4.15*VOL),j=jag(X,Y,cy);return dx*dx+dy*dy<=j*j};
  const SPK=(HS.bang||[]).concat(HS.bangFlat!=null?[]:[[-3.45,SIDE,1.5],[3.45,SIDE,1.5]]);
  const bang=X=>{const dx=X-HX;if(HS.bangFlat!=null)return HY-1.05+(Math.abs(dx)<2.95?HS.bangFlat:SIDE);let m=0;for(const[o2,dp,w]of SPK){const k=1-Math.abs(dx-o2)/(w/2);if(k>0)m=Math.max(m,dp*k)}return HY-1.05+m};
  const lit=(X,Y,cy)=>{const dx=(X-HX)/3.95,dy=(Y-cy)/4.15,nz=Math.sqrt(Math.max(0,1-dx*dx-dy*dy));return Math.max(0,dx*Lx+dy*Ly+nz*Lz)};
  const shine=(X,Y,o2=0)=>Y>HY-3.1+o2+Math.abs(X-HX)*.18&&Y<HY-2.5+o2+Math.abs(X-HX)*.18&&X<HX+2.4;
  const buzz=(l,X,Y)=>mix(hair(l,X,Y),o.skin,.42);
  const strand=(pts,w0,w1,braid,mat=hair)=>{const n=pts.length-1;for(let i=0;i<n;i++){const[a,b]=pts[i],[c2,d]=pts[i+1];
    limb(a,b,c2,d,w0+(w1-w0)*i/n,w0+(w1-w0)*(i+1)/n,braid?(l,X,Y,s)=>{const k=((Y*1.6)%1+1)%1,side=k<.5?1:-1;return mat(Math.max(0,l-(s*side>.15?0:.3)),X,Y)}:mat)}};
  const tie=(x,y)=>ellipsoid(x,y,.6,.42,rmat(ramp(HS.tie||'#c83434')));
  // cabelo comprido atrás das costas
  const longBack=()=>{const Lb=HS.back||3.6;if(Lb<5.5)return;const Wb=HS.backW||4.4;
    for(let y=sn(HY+1.2);y<HY+Lb+.8;y+=Q){const t=Math.max(0,(y-HY-1.2)/(Lb-1.2)),w=3.95+(Wb-3.95)*Math.min(1,t*1.8)+(HS.wavy?Math.sin(t*10)*.4:0);
      for(let x=sn(HX-w);x<HX+w;x+=Q){const X=x+.125,Y=y+.125,s=(X-HX)/w,endY=HY+Lb+(HS.straightEnds?0:((Math.floor((X-HX)*1.3)&1)?.4:0))-(HS.vcut?(1-Math.abs(s))*-.9:0);if(Y>endY)continue;
        const l=Math.max(0,-s*.45+Math.sqrt(Math.max(0,1-s*s))*.62+(HS.wavy?Math.sin(Y*2.4+s*2)*.14:0)-(front?.28:0));px(x,y,vhair(l,X,Y))}}};
  const frontLocks=()=>{if(!HS.front)return;for(const sd of[-1,1]){const pts=[];for(let i=0;i<=4;i++){const t=i/4;pts.push([HX+sd*(3.45+t*.55)+(HS.wavy?Math.sin(t*6)*.35:0),HY+1.4+t*(HS.front-1.4)])}strand(pts,1.45,.85,false,vhair)}};
  const tails=(view)=>{
    if(HS.twintails)for(const sd of[-1,1]){const x0=HX+sd*3.7,pts=[[x0,HY-1.6],[x0+sd*1,HY+.5],[x0+sd*1.3,HY+3.5],[x0+sd*1.1,HY+6.5],[x0+sd*.7,HY+9]];strand(pts,1.7,.55,false,vhair);tie(x0,HY-1.6)}
    if(HS.twinbraids)for(const sd of[-1,1]){const x0=HX+sd*3.5,pts=[[x0,HY+1.6],[x0+sd*.5,HY+4],[x0+sd*.6,HY+6.5],[x0+sd*.5,HY+8.6]];strand(pts,1.15,.8,true);tie(x0+sd*.5,HY+8.9)}
    if(HS.sidebraid){const x0=HX+3.4,pts=[[x0,HY+1.4],[x0+.7,HY+4],[x0+.8,HY+7],[x0+.5,HY+9.6]];strand(pts,1.25,.8,true);tie(x0+.5,HY+9.9)}
    if(HS.highpony){if(view==='f'){strand([[HX+1.5,HY-3.9],[HX+3.6,HY-3],[HX+4.6,HY+.5],[HX+4.5,HY+4],[HX+4,HY+7]],1.6,.5,false,vhair)}
      else{strand([[HX,HY-3.6],[HX+.3,HY-1],[HX+.2,HY+3],[HX-.2,HY+7.5]],1.7,.55,false,vhair);tie(HX,HY-3.6)}}
    if(HS.lowpony&&view==='b'){strand([[HX,HY+3.2],[HX+.2,HY+5.5],[HX,HY+8.5],[HX-.3,HY+10.5]],1.3,.5,false,vhair);tie(HX,HY+3.3)}
    if(HS.bun){ellipsoid(HX,HY-4.7,1.85,1.6,hair);if(view==='b')tie(HX,HY-3.4)}
    if(HS.topknot){ellipsoid(HX,HY-5.1,1.2,1.05,hair);tie(HX,HY-4.1)}};
  // ---- capa (atrás do corpo na vista de frente)
  const CP=o.cape,CR=CP&&ramp(CP);
  const capeShape=(dark)=>{const top=7.2+by,bot=23.6;for(let y=sn(top);y<bot+1;y+=Q){const t=(y-top)/(bot-top),w=4.7+t*1.6;for(let x=sn(10-w);x<10+w;x+=Q){const X=x+.125,Y=y+.125,hem=bot+((Math.floor(X*1.3)*7)%3)*.3;if(Y>hem)continue;
    const s=(X-10)/w,fold=Math.sin(X*2.1)*.18,l=Math.max(0,-s*.5+.55+fold-(dark?.3:0)-t*.15);px(x,y,CR[Math.max(0,Math.min(5,Math.round(l*5)))])}}};
  if(CP&&front&&state!=='sit')capeShape(true);
  if(!front)weapon();
  // ---- pernas
  const leg=(xh,lift,side)=>{const hy=16.3+by,ky=21.2+by-lift*.7,ay=25.6-lift,kx=xh+side*.08;
    if(o.tallBoot){limb(xh,hy,kx,ky,1.5,1.2,pants);limb(kx,ky,xh,ay,1.25,1.05,pants);limb(kx,ky+1.6,xh,ay,1.15,1,boot);for(let x=-1.2;x<1.2;x+=Q)px(xh+x,ky+1.5,BR[4])}
    else{limb(xh,hy,kx,ky,1.45,1.15,pants);limb(kx,ky,xh,ay,1.12,.9,pants);
      if(o.legsJeans){for(let y=hy+.5;y<ay-.5;y+=.75)px(xh+side*.95,y,'#8aa8d8');for(let x=-.9;x<.9;x+=Q)px(xh+x,ay-.6,PR[1])}
      limb(xh,ay-.6,xh,ay+.2,1,1,boot)}
    ellipsoid(xh+side*.1,ay+.75,1.25,.75,boot);
    for(let x=-1.25;x<1.25;x+=Q)px(xh+side*.1+x,ay+1.25,o.legsJeans?'#c8ccd8':BR[0]);
    if(o.legsJeans){px(xh-.25,ay+.4,'#e8ecf4');px(xh+.25,ay+.4,'#e8ecf4')}};
  if(state==='sit'){ellipsoid(8,20.6,1.7,1.2,pants);ellipsoid(12,20.6,1.7,1.2,pants);limb(7.4,21.4,6.6,24.6,1.1,.95,pants);limb(12.6,21.4,13.4,24.6,1.1,.95,pants);ellipsoid(6.4,25.4,1.2,.75,boot);ellipsoid(13.6,25.4,1.2,.75,boot)}
  else if(!o.robe){leg(8,lL,-1);leg(12,lR,1)}
  else{// vestido/túnica longa até o tornozelo
    for(let y=sn(15+by);y<26.4;y+=Q){const t=(y-15-by)/(11.4-by),w=3.9+t*2;for(let x=sn(10-w);x<10+w;x+=Q){const X=x+.125,Y=y+.125,s=(X-10)/w,fold=Math.sin((X-10)*2.4+t*1.5)*.2;
      const l=Math.max(0,-s*.45+Math.sqrt(Math.max(0,1-s*s))*.6+fold-.05);px(x,y,TR[Math.max(0,Math.min(5,Math.round(l*5)))])}}
    for(let x=-5.9;x<5.9;x+=Q){px(10+x,26.1,o.trim);px(10+x,26.35,mix(o.trim,'#000000',.3))}
    ellipsoid(8.2-lL*.3,26.9,1.15,.6,boot);ellipsoid(11.8+lR*.3,26.9,1.15,.6,boot)}
  // roupa de baixo (sem calça equipada)
  if(o.bareLegs&&state!=='sit'&&!o.robe){const UR=ramp('#e8e0d0'),um=rmat(UR);limb(8,16.2+by,8,18.2+by-lL*.3,1.55,1.45,um);limb(12,16.2+by,12,18.2+by-lR*.3,1.55,1.45,um)}
  if(o.bareLegs&&state==='sit'){const um=rmat(ramp('#e8e0d0'));ellipsoid(8,20.4,1.75,1.1,um);ellipsoid(12,20.4,1.75,1.1,um)}
  if(front&&!HS.buzz)longBack();
  // ---- tronco
  const TW=FEM?[[6.9,1.5],[7.4,3.2],[8.1,4.25],[9.2,4.5],[10.8,4.3],[12.6,3.45],[13.9,3.15],[15,3.6],[16,4.35],[16.8,4.6],[17.2,4.6]]:[[6.9,1.7],[7.4,3.7],[8.1,4.9],[9.2,5.1],[11,4.7],[13,4],[14.6,3.65],[15.6,3.8],[16.6,4.05],[17.2,4.05]];
  const torsoAt=(X,Y)=>{const yy=Y-by;if(yy<6.9||yy>17.2)return null;const w=curve(TW,yy);const s=(X-10)/w;if(Math.abs(s)>1)return null;return{w,s,yy}};
  for(let y=sn(6.9+by);y<17.2+by;y+=Q)for(let x=4;x<16;x+=Q){const X=x+.125,Y=y+.125,t=torsoAt(X,Y);if(!t)continue;
    const ny=t.yy<8.4?-(8.4-t.yy)/1.5*.85:(t.yy>16?(t.yy-16)*.3:0),d=Math.min(1,t.s*t.s+ny*ny),nz=Math.sqrt(1-d);
    let l=Math.max(0,t.s*Lx+ny*Ly+nz*Lz);
    if(front&&t.yy>11.5&&t.yy<15&&Math.abs(t.s)<.75)l+=Math.sin(t.yy*3.2+t.s*2)*.06;            // dobras na cintura
    px(x,y,cloth(l,X,Y))}
  const cw=yy=>curve(TW,yy);
  if(FEM&&front&&!o.armor)for(const cx of[8.55,11.45])for(let x=-1.3;x<1.3;x+=Q){const k=Math.sqrt(Math.max(0,1-(x/1.35)**2));px(cx+x,10.55+by+k*.95,TR[1]);if(Math.abs(x+.4)<.5)px(cx+x,9.9+by,TR[4])}
  if(front){
    // decote / gola
    for(let x=-1.6;x<1.6;x+=Q){const d=Math.abs(x);px(10+x,7.15+by+d*.12,o.trim);px(10+x,7.4+by+d*.12,mix(o.trim,'#000000',.25))}
    if(o.print){for(let y=9.3;y<11.6;y+=Q)for(let x=8.6;x<11.4;x+=Q)px(x,y+by,y<9.6?lighten(o.print,1.25):x>11?shade(o.print):o.print);
      for(const[x,y]of[[9.75,10],[10,10],[9.5,10.25],[10.25,10.25],[9.75,10.5],[10,10.5],[10,9.75],[9.75,10.75]])px(x,y+by,'#ffd040');px(9.75,10,'#fff4b0')}
  }
  if(o.armor){const AR=ramp(o.armor),met=isMetal(o.armor);
    for(let y=sn(7.6+by);y<13.4+by;y+=Q)for(let x=4;x<16;x+=Q){const X=x+.125,Y=y+.125,t=torsoAt(X,Y);if(!t||Math.abs(t.s)>.93)continue;const yy=Y-by;
      const ny=yy<8.4?-(8.4-yy)/1.5*.85:(yy-10.5)*.15,d=Math.min(1,t.s*t.s+ny*ny);let l=Math.max(0,t.s*Lx+ny*Ly+Math.sqrt(1-d)*Lz);
      let col=AR[Math.max(0,Math.min(5,Math.round(l*5.3-.35)))];if(met&&l>.86)col='#ffffff';if(yy>13)col=AR[1];px(x,y,col)}
    if(met){for(const s of[-.7,0,.7])px(10+s*4,12.6+by,AR[5]);ellipsoid(5.2,8.3+by,1.6,1.1,rmat(AR));ellipsoid(14.8,8.3+by,1.6,1.1,rmat(AR))}
    else if(front){for(let y=8;y<13;y+=1)px(10,y+by,AR[0])}}
  if(o.pockets&&front){for(const cx of[8.1,11.9]){for(let y=9.4;y<10.7;y+=Q)for(let x=-.75;x<.75;x+=Q)px(cx+x,y+by,y<9.65?TR[4]:y<9.9?TR[1]:TR[2]);px(cx,9.75+by,'#c8a060')}
    for(let y=8.2;y<15;y+=1.4){px(10,y+by,'#3a2416');px(10,y+by-.25,'#8e6034')}}
  // cinto com fivela
  for(let x=-cw(15.4);x<cw(15.4);x+=Q){const s=x/cw(15.4);px(10+x,15+by,LR[s<0?4:3]);px(10+x,15.25+by,LR[s<0?3:2]);px(10+x,15.5+by,LR[1])}
  if(front){for(let y=14.9;y<15.8;y+=Q)for(let x=9.4;x<10.6;x+=Q){const edge=y<15.1||y>15.5||x<9.6||x>10.35;if(edge)px(x,y+by,y<15.1?'#ffe48a':'#c89a30')}px(10,15.25+by,'#8a5a10')}
  if(o.strap&&front){for(let t=0;t<=1;t+=.02){const x=6.6+t*6.5,y=7.8+by+t*7.4;px(x,y,LR[2]);px(x+.25,y,LR[4]);px(x+.5,y,LR[1])}
    ellipsoid(13.5,16.4+by,.95,1.05,leather);px(13.25,16.1+by,'#c8a060');px(13.5,16.1+by,'#fff0a0')}
  // ---- braços (manga até o punho; camiseta tem manga curta)
  const sleeve=(X,Y,s,t)=>o.short&&t>.55?null:1;
  const AW=FEM?.86:1,SHL=FEM?5.75:5.2,SHR=20-SHL;
  const arm=(sx,sy,ex,ey,hx,hy2)=>{
    limb(sx,sy,ex,ey,1.15*AW,.95*AW,(l,X,Y,s,t)=>o.short&&t>.6?skin(l,X,Y):cloth(l,X,Y));
    limb(ex,ey,hx,hy2-.6,.95*AW,.8*AW,(l,X,Y,s,t)=>o.short?skin(l,X,Y):t>.86?TR[Math.max(0,Math.min(5,Math.round(l*5.3-1.3)))]:cloth(l,X,Y));
    ellipsoid(hx,hy2,.78*AW,.9*AW,skin);px(hx-.25,hy2+.5,SK[1]);px(hx+.25,hy2+.5,SK[1])};
  arm(SHL,8.4+by,SHL-.65,12.7+by+aL*.3,SHL-.45,17.4+by+aL);
  if(state==='attack'||state==='cast'){const ex=(SHR+hand[0])/2+1.1,ey=(8.4+by+hand[1])/2;arm(SHR,8.4+by,ex,ey,hand[0],hand[1])}
  else arm(SHR,8.4+by,SHR+.65,12.7+by+aR*.3,SHR+.45,17.4+by+aR);
  // ---- capa por cima (costas) e capuz/manto (frente)
  if(CP&&state!=='sit'){
    if(!front){capeShape(false);ellipsoid(10,7.4+by,3.9,1.6,rmat(CR))}
    else{for(let y=sn(6.5+by);y<8.9+by;y+=Q){const yy=y-by,w=yy<7.2?3+(yy-6.5)*2.6:4.8+(yy-7.2)*.3;for(let x=-w;x<w;x+=Q){if(yy>7.6&&Math.abs(x)<1.3+(yy-7.6)*1.2)continue;const l=.55-x/w*.35-(yy>8.4?.25:0);px(10+x,y,CR[Math.max(0,Math.min(5,Math.round(l*5)))])}}
      for(const[x,y]of[[9.75,8.5],[10,8.5],[9.75,8.75],[10,8.75]])px(x,y+by,'#d8a838');px(9.75,8.5+by,'#fff0a0')}}
  // ---- pescoço e cabeça
  const RX=FEM?3.35:3.5,RY=3.95;
  limb(10,4.4+hb,10,7.4+by,FEM?.92:1.05,FEM?1:1.12,(l,X,Y)=>skin(Math.max(0,l-(Y<6.2+hb?.35:0)),X,Y));
  const headAt=(X,Y)=>{const dy=(Y-HY)/RY;let rx=RX;if(Y>HY+1)rx=RX*(1-Math.pow((Y-HY-1)/(RY-1),1.6)*(FEM?.5:.42));const dx=(X-HX)/rx;const d=dx*dx+dy*dy;return d<=1?{dx,dy,d}:null};
  if(front){
    if(HS.highpony||HS.bun)tails('f');
    if(!HS.buzz)ellipsoid(HX,HY-.6,4.25*VOL,4.4*VOL,hair,(X,Y)=>crown(X,Y,HY-.6)&&Y<HY+2.6);
    ellipsoid(HX-RX+.05,HY+.8,.55,.95,skin);ellipsoid(HX+RX-.05,HY+.8,.55,.95,skin);px(HX-RX,HY+.75,SK[1]);px(HX+RX-.25,HY+.75,SK[1]);
    for(let y=sn(HY-RY);y<HY+RY;y+=Q)for(let x=sn(HX-RX);x<HX+RX;x+=Q){const X=x+.125,Y=y+.125,h=headAt(X,Y);if(!h)continue;const nz=Math.sqrt(1-h.d);let l=Math.max(0,h.dx*Lx+h.dy*Ly*.6+nz*Lz)+.24;px(x,y,skin(l,X,Y))}
    if(!HS.buzz&&!HS.forehead)for(let x=-2.75;x<2.75;x+=Q)px(HX+x,HY-.6+Math.abs(x)*.05,SK[2]);
    // olhos: cílio, branco, íris em três tons, pupila e brilho
    const E=o.eye,ED=mix(E,'#000000',.5),EL=mix(E,'#ffffff',.35);
    for(const[x0,out]of[[7.75,-1],[10.5,1]]){const ey=HY+.45;
      for(let x=0;x<1.75;x+=Q)px(x0+x,ey,'#2a1418');px(out<0?x0-.25:x0+1.75,ey+.25,'#2a1418');
      if(FEM){px(out<0?x0-.5:x0+2,ey,'#2a1418');px(out<0?x0-.25:x0+1.75,ey-.25,'#2a1418');px(out<0?x0:x0+1.5,ey-.25,'#2a1418')}
      for(let x=0;x<1.75;x+=Q)for(let r=0;r<3;r++){const ix=x>=.25&&x<1.25;let col=ix?(r===0?ED:r===1?E:EL):'#f2ece6';if(ix&&r===1&&x>=.5&&x<.75)col='#0e0810';if(ix&&r===1&&x<.5)col='#ffffff';px(x0+x,ey+.25+r*.25,col)}
      for(let x=.25;x<1.5;x+=Q)px(x0+x,ey+1,SK[2])}
    for(let x=0;x<1.75;x+=Q){px(7.5+x,HY-.4+(x<.5?.25:0),o.hair[0]);px(10.75+x,HY-.4+(x>1.25?.25:0),o.hair[0])}
    px(10.25,HY+1.75,SK[1]);px(10.25,HY+2,SK[1]);px(10,HY+2,SK[2]);px(9.75,HY+1.5,SK[4]);
    if(FEM){for(let x=9.5;x<10.75;x+=Q)px(x,HY+2.85,x<9.75||x>10.25?mix(o.skin,'#c05a5a',.45):'#b04a50');px(9.75,HY+3.1,mix(o.skin,'#e07070',.4));px(10,HY+3.1,mix(o.skin,'#e07070',.4))}
    else{for(let x=9.5;x<10.75;x+=Q)px(x,HY+2.85,x<9.75||x>10.25?SK[1]:'#a0544c');px(9.75,HY+3.1,SK[4]);px(10,HY+3.1,SK[4])}
    for(const bx of[7.75,11.75])for(let x=0;x<.5;x+=Q)px(bx+x,HY+1.75,mix(o.skin,'#f08080',FEM?.3:.22));
    if(o.beard){const BRd=ramp(o.beard),bm=rmat(BRd,(X)=>(hsh(Math.round(X*4),3)-.5)*1);
      for(let y=sn(HY+1.5);y<HY+5.6;y+=Q)for(let x=sn(HX-3.4);x<HX+3.4;x+=Q){const X=x+.125,Y=y+.125,h=headAt(X,Math.min(Y,HY+RY-.1));const yy=Y-HY;const w=yy<3.9?3.4:3.4-(yy-3.9)*1.6;if(Math.abs(X-HX)>w)continue;if(!h&&yy<3.6)continue;if(yy<2.4&&Math.abs(X-HX)<1.9)continue;
        if(yy>2.6&&yy<3.2&&Math.abs(X-HX)<.7){px(x,y,'#4a2a28');continue}px(x,y,bm(.55-(X-HX)/7-(yy>3.5?.15:0),X,Y))}
      for(let x=-1.4;x<1.4;x+=Q)px(HX+x,HY+2.45+Math.abs(x)*.15,BRd[3])}
    // cabelo da frente
    if(HS.buzz){for(let y=sn(HY-RY-.3);y<HY+.6;y+=Q)for(let x=sn(HX-RX-.2);x<HX+RX+.2;x+=Q){const X=x+.125,Y=y+.125,dx=(X-HX)/(RX*1.05),dy=(Y-HY)/(RY*1.04);if(dx*dx+dy*dy>1)continue;const sd=Math.abs(X-HX),lim=HY-1+(sd>2.6?Math.min(1.5,(sd-2.6)*2.4):0);if(Y>lim)continue;
        if(HS.mohawk&&sd<1)continue;px(x,y,buzz(lit(X,Y,HY-.6),X,Y))}}
    else for(let y=sn(HY-5.4*VOL);y<HY+SIDE;y+=Q)for(let x=sn(HX-4.4*VOL);x<HX+4.4*VOL;x+=Q){const X=x+.125,Y=y+.125;if(!crown(X,Y,HY-.6)&&!(Y>HY+.5&&Math.abs(X-HX)<4.3))continue;
      if(Y>bang(X))continue;const l=lit(X,Y,HY-.6);px(x,y,shine(X,Y)&&l>.45?HR[5]:hair(l,X,Y))}
    frontLocks();
    if(HS.quiff){ellipsoid(HX+.4,HY-4.3,3.2,1.8,(l,X,Y)=>shine(X,Y,-1.4)&&l>.45?HR[5]:hair(l,X,Y));for(let x=-2.6;x<3;x+=Q)px(HX+x+.4,HY-2.6+Math.sin(x*1.7)*.15,HR[1])}
    if(!HS.highpony&&!HS.bun)tails('f');
  }else{
    if(HS.buzz){for(let y=sn(HY-RY-.3);y<HY+3.4;y+=Q)for(let x=sn(HX-RX-.2);x<HX+RX+.2;x+=Q){const X=x+.125,Y=y+.125,dx=(X-HX)/(RX*1.05),dy=(Y-HY)/(RY*1.04);if(dx*dx+dy*dy>1)continue;if(HS.mohawk&&Math.abs(X-HX)<1&&Y<HY-1)continue;px(x,y,buzz(lit(X,Y,HY-.2),X,Y))}
      ellipsoid(HX-RX+.05,HY+.8,.55,.95,skin);ellipsoid(HX+RX-.05,HY+.8,.55,.95,skin)}
    else{const BE=(HS.back||3.6)<5.5?(HS.back||3.6):3.6;
      for(let y=sn(HY-5.4*VOL);y<HY+BE+1.2;y+=Q)for(let x=sn(HX-4.4*VOL);x<HX+4.4*VOL;x+=Q){const X=x+.125,Y=y+.125;const dx=(X-HX)/(3.95*VOL),dy=(Y-(HY-.2))/(4.6*VOL),j=jag(X,Y,HY-.2);if(dx*dx+dy*dy>j*j&&!(Y>HY&&Math.abs(X-HX)<3.9*VOL))continue;
        const u=(X-HX+4)/1.15,fr=u-Math.floor(u),ends=HS.straightEnds?HY+BE:HY+BE-.5+(1-Math.abs(fr-.5)*2)*(.6+hsh(Math.floor(u),4)*.9)-Math.abs(X-HX)*.12;if(Y>ends)continue;
        const l=lit(X,Y,HY-.2);px(x,y,shine(X,Y,.1)&&l>.45?HR[5]:hair(l,X,Y))}}
    if(CP&&state!=='sit')ellipsoid(10,6.9+by,3.6,1.3,rmat(CR),(X,Y)=>Y>HY+3.4);
    longBack();tails('b');
  }
  if(HS.mohawk){for(let y=sn(HY-6.4);y<HY-.6;y+=Q)for(let x=-1;x<1;x+=Q){const X=HX+x+.125,Y=y+.125,u=(Y-HY+6.4)/1.1,fr=u-Math.floor(u),edge=.95-(1-Math.abs(fr-.5)*2)*.55;if(Math.abs(x+.125)>edge)continue;if(Y>HY-3.6&&!front&&false)continue;px(HX+x,y,hair(.55-x*.3,X,Y))}}
  if(o.spiky||HS.spiky)for(const[x,h]of[[7.2,1.5],[8.8,2],[10.4,2.2],[12,1.9],[13.3,1.3]])for(let i=0;i<h;i+=Q){const w=(1-i/h)*.95;for(let xx=-w;xx<w;xx+=Q)px(x+xx,HY-4.2-i,HR[xx<0?4:2])}
  if(o.ahoge||HS.ahoge){for(let t=0;t<1;t+=.08){const x=HX+.3+t*1.1+Math.sin(t*3)*.25,y=HY-4.4-t*1.6;px(x,y,HR[3]);px(x+.25,y,HR[2])}px(HX+1.5,HY-6.1,HR[1])}
  // ---- chapéus
  const H=o.hat;
  if(H==='bandana'){for(let x=-3.6;x<3.6;x+=Q){px(HX+x,HY-1.2,'#e85a50');px(HX+x,HY-.95,'#c83434');px(HX+x,HY-.7,'#962020')}
    if(front){ellipsoid(HX+3.7,HY-.6,.6,.5,rmat(ramp('#c83434')));limb(HX+3.9,HY-.4,HX+4.6,HY+1.6,.35,.25,rmat(ramp('#c83434')))}else{ellipsoid(HX,HY-.6,.7,.55,rmat(ramp('#c83434')));limb(HX-.3,HY-.3,HX-.9,HY+1.8,.35,.25,rmat(ramp('#c83434')));limb(HX+.3,HY-.3,HX+.9,HY+1.8,.35,.25,rmat(ramp('#c83434')))}}
  if(H==='cap'){ellipsoid(HX,HY-2.1,3.95,2.6,rmat(ramp('#e8e8f0')),(X,Y)=>Y<HY-.7);for(let x=-3.9;x<3.9;x+=Q){px(HX+x,HY-.9,'#c8c8d4');px(HX+x,HY-.65,'#a0a0b0')}
    if(front)ellipsoid(HX,HY-1.9,.75,.75,rmat(ramp('#e0b040')))}
  if(H==='wide'){const BRh=ramp('#7a5030');ellipsoid(HX,HY-.9,6.3,1.15,rmat(BRh));ellipsoid(HX,HY-2.5,3.5,2.3,rmat(ramp('#8e6034')),(X,Y)=>Y<HY-1.1);
    for(let x=-3.4;x<3.4;x+=Q){px(HX+x,HY-1.6,'#b04030');px(HX+x,HY-1.35,'#802a20')}}
  if(H==='wizard'){const WR=ramp('#4a2a8a');ellipsoid(HX,HY-1.1,5,.95,rmat(WR));
    for(let y=0;y<8;y+=Q){const t=y/8,w=3.5*(1-t)+.15,cx=HX+t*t*2.8;for(let x=-w;x<w;x+=Q){const s=x/w;px(cx+x,HY-1.5-y,WR[Math.max(0,Math.min(5,Math.round((.6-s*.35)*5)))])}}
    for(let x=-3.4;x<3.4;x+=Q){px(HX+x,HY-1.9,'#f0d070');px(HX+x,HY-1.65,'#c8a040')}for(const[x,y]of[[HX-.8,HY-3.8],[HX+1.2,HY-5.6],[HX+.2,HY-2.8]])px(x,y,'#fff4a0')}
  if(H==='beret'){const GR2=ramp('#2a6a3a');ellipsoid(HX-.4,HY-2.6,4.3,1.8,rmat(GR2));for(let x=-3.7;x<3.7;x+=Q)px(HX+x,HY-1.1,GR2[1]);
    limb(HX+3.2,HY-3,HX+4.6,HY-6.2,.35,.15,rmat(ramp('#f4f4f4')));limb(HX+3.6,HY-3.4,HX+5.2,HY-6,.25,.1,rmat(ramp('#e04040')))}
  if(H==='helm'){const MR=ramp('#9aa4b8'),mm=(l,X,Y)=>l>.88?'#ffffff':MR[Math.max(0,Math.min(5,Math.round(l*5.3-.35)))];
    ellipsoid(HX,HY-.9,4.1,3.7,mm,(X,Y)=>Y<HY+.6);for(let x=-4;x<4;x+=Q){px(HX+x,HY+.4,MR[1]);px(HX+x,HY+.65,MR[0])}
    if(front)for(let y=0;y<1.6;y+=Q)px(HX,HY+.6+y,MR[2]);for(let x=-3.5;x<3.5;x+=1.4)px(HX+x,HY+.4,MR[5]);
    limb(HX,HY-4.4,HX-1.6,HY-6.3,.55,.35,rmat(ramp('#c83434')))}
  if(front)weapon();
  const out=outline(c,'#1a1020',2);out.k=KH;
  if(state==='dead'){const r=canvas(out.height,out.width),rq=r.getContext('2d');rq.translate(0,out.width);rq.rotate(-Math.PI/2);rq.drawImage(out,0,0);r.k=KH;return r}
  return out;
}

