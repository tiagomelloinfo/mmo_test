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
