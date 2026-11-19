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
