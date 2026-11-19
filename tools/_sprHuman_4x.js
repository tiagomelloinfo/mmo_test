// personagens em 4x: cada pixel lógico vira 4x4 pixels de verdade, com detalhe em quartos de pixel
const KH=4;
function hcv(w,h){const c=canvas(w*KH,h*KH);c.k=KH;c.getContext('2d').setTransform(KH,0,0,KH,0,0);return c}
function sprHuman(o,dir,state,f){
  const c=hcv(32,39),q=c.getContext('2d'),p0=P(q),OX=6,OY=8;
  const p=(x,y,w,h,col)=>p0(x+OX,y+OY,w,h,col);
  const ln=(a,b,c2,d,col,w)=>line(p0,a+OX,b+OY,c2+OX,d+OY,col,w);
  // ponta afinada (mecha de cabelo, barra): colunas de 1/4 que encolhem até a ponta
  const spike=(cx,y,w,h,col,colD)=>{for(let x=-w/2;x<w/2-1e-6;x+=.25){const t=1-Math.abs(x+.125)/(w/2),hh=Math.max(.25,Math.round(h*t*4)/4);p(cx+x,y,.25,hh,x>=0&&colD?colD:col)}};
  const front=dir!=='b';
  let by=0,lL=0,lR=0,aL=0,aR=0;
  if(state==='walk'){if(f===1){lL=1;aL=1;aR=-1;by=-1}if(f===3){lR=1;aL=-1;aR=1;by=-1}}
  if(state==='sit')by=4;
  const hb=by+(state==='idle'&&f===1?.5:0);
  let hand=[15,17+by+aR],tip=[18,23+by+aR];
  if(state==='attack'){hand=[[14,6],[16,12],[16,18]][f];tip=[[8,-2],[22,9],[21,25]][f]}
  if(state==='cast'){hand=[15,10+by];tip=[17,3+by]}
  const S=o.skin,SD=o.skinD,SDD=shade(SD),SL=lighten(S,1.06),T=o.tunic,TD=o.tunicD,TL=lighten(T),TDD=shade(TD),PA=o.pants,PD=o.pantsD,PL=lighten(PA),BO=o.boot,BD=shade(BO),BL=lighten(BO,1.3);
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
  if(!front)weapon();
  const CP=o.cape,CPD=CP&&shade(CP),CPL=CP&&lighten(CP,1.2);
  const hem=(col,colD)=>{for(let x=3.5;x<17;x+=1.5)spike(x,23.5,1.5,.75+((x*7)%3)*.25,col,colD)};
  if(CP&&front&&state!=='sit'){p(3,13+by,14,11-by,CPD);p(3,13+by,1,11-by,CP);p(3.25,14+by,.25,9-by,CPL);p(16,13+by,1,11-by,shade(CPD));hem(CPD,shade(CPD))}
  // pernas e pés
  const leg=(x,lift)=>{const y=21-lift;
    p(x,y,3,4,PA);p(x+2,y,1,4,PD);p(x+2.75,y,.25,4,shade(PD));p(x+.5,y+.5,.25,3,PL);p(x+1.25,y+1,.25,2.25,PD);p(x,y+3.5,3,.5,PD);
    if(o.legsJeans){p(x+.5,y,.25,3.5,'#5a7ab8');p(x+2.25,y+.5,.25,3,'#d8b040');for(let yy=y+.5;yy<y+3.5;yy+=.75)p(x+.75,yy,.25,.25,'#8aa8d8');p(x,y+3.25,3,.25,'#6a8ac8')}
    if(o.tallBoot){p(x-.5,y,4,2.5,PA);p(x+2.5,y,1,2.5,PD);p(x+3.25,y,.25,2.5,shade(PD));p(x-.5,y+.5,.5,1.5,PL);p(x+.75,y+.5,.25,1.75,PD);p(x+1.75,y+.75,.25,1.25,PL);p(x,y+2.5,3,.5,PD);
      p(x,y+3,3,3,BO);p(x+2,y+3,1,3,BD);p(x+.5,y+3.25,.25,2.25,BL);p(x+.75,y+3.5,.25,1,lighten(BO,1.6));p(x-.25,y+2.75,3.5,.5,lighten(BO,1.5));p(x-.25,y+3,3.5,.25,BO);
      p(x+1,y+4,1,.25,BD);p(x-.25,y+5.25,3.75,.25,BO);p(x-.25,y+5.5,3.75,.5,shade(BD));return}
    p(x,y+4,3,2,BO);p(x+2,y+4,1,2,BD);p(x+.5,y+4,1.5,.5,BL);p(x+.5,y+4,.5,.25,lighten(BO,1.6));p(x-.25,y+5,.5,.5,BO);p(x-.25,y+5.5,3.5,.5,BD);p(x-.25,y+5.75,3.5,.25,shade(BD));
    if(o.legsJeans){p(x-.25,y+5.25,3.5,.5,'#b8bcc8');p(x-.25,y+5.75,3.5,.25,'#8a8e9a');for(let xx=x+.5;xx<x+2.5;xx+=.75)p(xx,y+4.5,.5,.25,'#c8ccd8')}};
  if(state==='sit'){p(4,23,5,2,PA);p(4,23,5,.25,PL);p(4,24.5,5,.5,PD);p(11,23,5,2,PA);p(11,23,5,.25,PL);p(11,24.5,5,.5,PD);p(3,24,2,2,BO);p(15,24,2,2,BO);p(3,24,.5,.5,BL);p(15,24,.5,.5,BL);p(3,25.5,2,.5,BD);p(15,25.5,2,.5,BD)}
  else if(!o.robe){leg(6,lL);leg(11,lR)}
  else{p(5,20+by,10,6-by,T);p(12,20+by,3,6-by,TD);p(5,20+by,.5,6-by,TL);p(8.5,21+by,.25,4-by,TD);p(10.75,21+by,.25,4-by,TD);p(6.75,21.5+by,.25,3.5-by,TL);p(5,25,10,1,o.trim);p(5,25,10,.25,lighten(o.trim,1.2));for(let x=5.5;x<15;x+=1)p(x,25.5,.5,.25,TDD);p(6,26-lL,3,1,BO);p(11,26-lR,3,1,BO);p(6,26.5-lL,3,.5,BD);p(11,26.5-lR,3,.5,BD)}
  // tronco
  p(6,13+by,8,8,T);p(12,13+by,2,8,TD);p(13.5,13+by,.5,8,TDD);p(6,13+by,.5,7,TL);p(6.5,13.5+by,.25,5.5,TL);
  p(11.5,15+by,.25,4,TD);p(11.75,15.5+by,.25,3,TD);p(7.5,16+by,.25,3,TD);p(7.75,16.5+by,.25,2,TL);for(let x=6.5;x<14;x+=1)p(x,18.5+by,.5,.25,TD);
  if(front){p(8,13+by,4,.5,o.trim);p(8.5,13.5+by,3,.5,o.trim);p(8,13+by,4,.25,lighten(o.trim,1.2));p(9.5,13+by,1,1,S);p(9.75,13.75+by,.5,.25,SD);
    if(o.print){p(8,15+by,4,2.5,o.print);p(8,15+by,4,.5,lighten(o.print,1.3));p(11.75,15+by,.25,2.5,shade(o.print));p(9.5,15.5+by,1,1,'#ffd040');p(9,16+by,.5,.5,'#ffd040');p(10.5,16+by,.5,.5,'#ffd040');p(9.75,15.25+by,.5,.25,'#ffd040');p(9.75,16.5+by,.5,.25,'#ffd040');p(9.75,15.75+by,.25,.25,'#fff4b0')}}
  if(o.armor){const AL=lighten(o.armor,1.25);p(6,13+by,8,4,o.armor);p(12,13+by,2,4,o.armorD);p(6,13+by,8,.5,'#e8eef8');p(6,16.5+by,8,.5,o.armorD);p(6.5,14+by,.5,2,AL);p(6,14.75+by,8,.25,o.armorD);for(let x=6.5;x<14;x+=1.5)p(x,15.25+by,.25,.25,AL);if(front){p(7,15+by,.5,.5,AL);p(12.5,15+by,.5,.5,AL)}}
  if(o.pockets&&front){for(const px of[6.5,10.5]){p(px,14.5+by,2.5,2,TD);p(px,14.5+by,2.5,.5,TL);p(px,14.75+by,2.5,.25,TDD);p(px+1,15+by,.5,.5,'#c8a060');p(px+1,15+by,.25,.25,'#fff0a0')}
    p(6.5,17.5+by,2.5,1.5,TD);p(10.5,17.5+by,2.5,1.5,TD);p(6.5,17.5+by,2.5,.25,TL);p(10.5,17.5+by,2.5,.25,TL);for(let y=14;y<19;y+=1.5){p(9.75,y+by,.5,.5,'#5a3a20');p(9.75,y+by,.25,.25,'#8e6034')}}
  p(6,19+by,8,1,o.belt);p(6,19+by,8,.25,lighten(o.belt,1.3));p(6,19.75+by,8,.25,shade(o.belt));if(front){p(9,19+by,2,1,'#c89a30');p(9.5,19.25+by,1,.5,o.belt);p(9,19+by,2,.25,'#fff0a0');p(10,19.25+by,.25,.5,'#e0b040')}
  if(o.strap&&front){ln(7,13+by,13,19+by,'#5a3a20',.5);ln(7.5,13+by,13.5,19+by,'#7a5432',.5);ln(7.25,13+by,13.25,19+by,'#9a7048',.25);p(12.5,19.5+by,2,2.5,'#7a5432');p(12.5,19.5+by,2,.5,'#9a7048');p(14.25,19.5+by,.25,2.5,'#5a3a20');p(13,20.5+by,1,.5,'#c8a060');p(13.25,20.5+by,.25,.25,'#fff0a0');p(5.5,19.5+by,1.5,2,'#6a4628');p(5.5,19.5+by,1.5,.25,'#8e6034')}
  // braços (manga com punho e mão com dedos)
  const hnd=(x,y)=>{p(x,y,2,2,S);p(x,y+1.5,2,.5,SD);p(x+.75,y+.5,.25,1,SD);p(x+1.25,y+.5,.25,1,SD);p(x+.25,y+.25,.5,.25,SL);p(x+1.75,y,.25,1.5,SD)};
  p(4,13+by,2,4+aL,T);p(4,13+by,.5,4+aL,TL);p(4.25,13.5+by,.25,3+aL,lighten(T,1.3));p(5.5,13+by,.5,4+aL,TD);p(4,16.5+by+aL,2,.5,TD);p(4,16.75+by+aL,2,.25,TDD);hnd(4,17+by+aL);
  if(state==='attack'||state==='cast'){ln(14,14+by,hand[0],hand[1],TD);ln(15,14+by,hand[0]+1,hand[1],T);ln(14.5,14+by,hand[0]+.5,hand[1],TL,.25);p(hand[0]-1,hand[1]-1,2,2,S);p(hand[0]-1,hand[1]+.5,2,.5,SD);p(hand[0]-.75,hand[1]-.75,.5,.25,SL);p(hand[0]-.25,hand[1]-.5,.25,1,SD)}
  else{p(14,13+by,2,4+aR,TD);p(14,13+by,.5,4+aR,T);p(15.75,13+by,.25,4+aR,TDD);p(14,16.5+by+aR,2,.5,TDD);hnd(14,17+by+aR)}
  if(CP&&state!=='sit'){
    if(!front){p(3,13+by,14,11-by,CP);p(13,13+by,4,11-by,CPD);p(3,13+by,.5,11-by,CPL);p(3.5,14+by,.25,9-by,CPL);for(const x of[6,9,12]){p(x,15+by,.5,8-by,CPD);p(x+.5,15+by,.25,8-by,CPL)}
      hem(CP,CPD);p(5,11.5+hb,10,3,CP);p(5,13.5+hb,10,.5,CPD);p(6,12+hb,8,.5,CPL)}
    else{p(4,12+by,12,2,CP);p(4,13.5+by,12,.5,CPD);p(4.5,12+by,11,.5,CPL);p(4.5,12.75+by,11,.25,CPD);p(9,13+by,2,1,'#c89a30');p(9.5,13+by,1,.5,'#fff0a0');p(9.25,13.5+by,.25,.25,'#8a5a10')}}
  // cabeça: contorno arredondado em quartos de pixel
  p(5,2+hb,10,1,S);p(4,3+hb,12,7.5,S);p(4.25,10.5+hb,11.5,.5,S);p(4.75,11+hb,10.5,.5,S);p(5.5,11.5+hb,9,.5,S);p(4.5,2.5+hb,11,.5,S);
  p(13.75,4+hb,1.25,6.5,SD);p(15,4.5+hb,.75,6,SD);p(4.75,11+hb,10.5,.5,SD);p(5.5,11.5+hb,9,.5,SDD);p(5.25,4+hb,.75,4,SL);p(5,4.5+hb,.25,3,SL);
  p(8,12+hb,4,1,SD);p(8.5,12+hb,3,.25,SDD);
  if(CP&&!front&&state!=='sit'){p(5,12+hb,10,2.5,CP);p(6,12.5+hb,8,.5,CPL);p(5,14+hb,10,.5,CPD);p(13,12+hb,2,2.5,CPD)}
  const H=o.hair,H0=H[0],H1=H[1],H2=H[2];
  if(front){
    p(3.5,6.5+hb,1,2.5,S);p(3.75,7+hb,.5,1.5,SD);p(15.5,6.5+hb,1,2.5,SD);p(15.75,7+hb,.5,1.5,SDD);
    // sombra da franja na testa
    p(4.5,5+hb,11,.75,SD);
    // olhos: cílio com ponta, branco, íris em 3 tons, pupila e dois brilhos
    for(const[ex,outer]of[[6,-1],[12,1]]){const E=o.eye,ED=shade(shade(E));
      p(ex-.5,7+hb,3,2.75,'#f6f0ec');p(ex-.5,7+hb,3,.25,'#c8b8c0');
      p(ex,7+hb,2,3,E);p(ex,7+hb,2,.75,ED);p(ex+.5,7.5+hb,1,1.5,'#141018');p(ex+.25,9+hb,1.5,.75,lighten(E,1.4));p(ex,9.75+hb,2,.25,lighten(E,1.15));
      p(ex+.25,7.25+hb,.5,.5,'#ffffff');p(ex+1.25,8.75+hb,.25,.25,'#ffffff');
      p(ex-.75,6.5+hb,3.5,.5,'#2a1a20');p(outer<0?ex-1:ex+2.5,6.75+hb,.5,.5,'#2a1a20');p(outer<0?ex-1.25:ex+2.75,7+hb,.5,.25,'#2a1a20');
      p(ex,10+hb,2,.25,SD)}
    p(5.5,5.5+hb,2.5,.5,H0);p(5.25,5.75+hb,.5,.25,H0);p(12,5.5+hb,2.5,.5,H0);p(14.25,5.75+hb,.5,.25,H0);
    p(9.75,9+hb,.5,.75,SD);p(9.5,9.5+hb,.25,.25,SL);
    p(9.25,10.75+hb,1.5,.25,'#a85048');p(9.5,11+hb,1,.25,'#e08a80');
    for(const bx of[5,14])for(let i=0;i<4;i++)if(i%2===0)p(bx+i*.25,9.75+hb,.25,.25,'#f4a090');else p(bx+i*.25,10+hb,.25,.25,'#f4a090');
    p(5,9.5+hb,1,.25,'#f4b0a0');p(14,9.5+hb,1,.25,'#f4b0a0');
    if(o.beard){const B=o.beard,BDk=shade(B);p(5,9+hb,10,3,B);p(6,12+hb,8,1,B);p(7,13+hb,6,.5,B);p(8,9+hb,4,1,BDk);p(9,10.5+hb,2,.5,'#5a3030');for(let x=5.25;x<15;x+=.75)p(x,10+hb,.25,1.5+(x*3%2)*.5,BDk);p(7,13.25+hb,6,.25,BDk);p(6,9.25+hb,.25,2,lighten(B,1.2))}
  }
  // cabelo com mechas finas, pontas afinadas e brilho
  p(5,.5+hb,10,.5,H1);p(4,1+hb,12,4,H1);p(3,2+hb,14,4,H1);p(3.5,1.5+hb,13,.5,H1);
  if(front){
    p(3,5+hb,2,5.5,H1);p(15,5+hb,2,5.5,H1);p(3,5+hb,.5,5.5,H0);p(16.5,5+hb,.5,5.5,H0);p(4.5,5+hb,.25,5,H0);p(15.25,5+hb,.25,5,H0);
    spike(4,10.5+hb,2,1.5,H1,H0);spike(16,10.5+hb,2,1.5,H0,shade(H0));
    for(const[x,h]of[[5.25,1.75],[6.75,2.5],[8.25,2.75],[9.75,3],[11.25,2.5],[12.75,2.75],[14.25,2.25],[15.25,1.5]])spike(x,5+hb,2,h,H1,H0);
    for(const x of[6,7.75,9.5,11.25,13])p(x,2.75+hb,.25,2.25,H0);
    for(const x of[6.5,9.5,12,14.5])p(x,4.5+hb,.5,1,H0);
  }else{
    p(3,2+hb,14,10,H1);p(13,4+hb,3,7,H0);p(16.5,3+hb,.5,8,H0);
    for(let x=4.5;x<15.5;x+=1.25)p(x,3.5+hb,.25,7.5,H0);for(const x of[5.75,8.25,10.75])p(x,4+hb,.25,5,H2);
    for(let x=3.75;x<16.5;x+=1.5)spike(x,12+hb,1.5,1,H1,H0);p(4,11.5+hb,12,.5,H0);p(4,11.75+hb,12,.25,shade(H0))
  }
  if(o.spiky){p(4,0+hb,2,1,H1);p(4.5,-.5+hb,1,.5,H1);p(8,0+hb,2,1,H1);p(8.5,-.5+hb,1,.5,H1);p(12,0+hb,2,1,H1);p(12.5,-.5+hb,1,.5,H1);p(16,1+hb,1,2,H1);p(2,3+hb,1,2,H1)}
  if(o.ahoge){p(10,0+hb,.75,1,H1);p(10.25,-.75+hb,.75,.75,H1);p(10.75,-1.5+hb,.75,.75,H1);p(11.25,-2+hb,.5,.5,H1);p(11.5,-2.25+hb,.5,.25,H0);p(10.5,-.5+hb,.25,.5,H2)}
  // brilho em arco
  for(const[x,y,w,h]of[[5.25,2.75,.75,.5],[6,2.25,1.5,.5],[7.5,2,1.5,.25],[9.5,1.5,2,.5],[11.5,1.75,.75,.25],[6.25,3,1,.25],[12.5,2,.5,.25]])p(x,y+hb,w,h,H2);
  p(14,3+hb,2,2,H0);p(4.5,.75+hb,11,.25,shade(H1));
  // chapéus
  if(o.hat==='bandana'){p(3,4+hb,14,1,'#c83434');p(3,4+hb,14,.5,'#e85a50');p(3,4.75+hb,14,.25,'#962020');p(3,5+hb,1,1,'#962020');if(front)p(17,5+hb,1,3,'#c83434');else{p(9,5+hb,2,2,'#c83434');p(8,7+hb,1,2,'#962020');p(11,7+hb,1,2,'#962020')}}
  if(o.hat==='cap'){p(4,-1+hb,12,4,'#f2f2f6');p(4,-1+hb,12,.5,'#ffffff');p(4,2+hb,12,1,'#c8c8d4');p(4,2.75+hb,12,.25,'#a0a0b0');p(9,-1+hb,2,3,'#e0b040');p(8,0+hb,4,1,'#e0b040');p(9.5,-.5+hb,.5,.5,'#fff4b0')}
  if(o.hat==='wide'){p(1,3+hb,18,2,'#6a4426');p(1,3+hb,18,.5,'#8e6034');p(1,4.5+hb,18,.5,'#4a2e18');p(5,-1+hb,10,4,'#86582e');p(5,-1+hb,10,.5,'#a87444');p(5,2+hb,10,1,'#b04030');p(5,2.5+hb,10,.5,'#802a20');for(let x=5.5;x<15;x+=1)p(x,0+hb,.25,2,x%2<1?'#7a4e28':'#96643a')}
  if(o.hat==='wizard'){const WZ='#4a2a8a',WL='#6a4aaa';p(3,2+hb,14,2,WZ);p(5,0+hb,10,2,WZ);p(7,-3+hb,7,3,WZ);p(9,-6+hb,5,3,WZ);p(11,-8+hb,3,2,WZ);p(13,-9+hb,2,1,WZ);p(5,1+hb,10,1,'#f0d070');p(5,1+hb,10,.5,'#fff0a0');p(10,-2+hb,1,1,'#fff4a0');p(12,-5+hb,1,1,'#fff4a0');p(12,-3+hb,2,3,WL);p(7.5,-2.5+hb,.5,2,WL);p(9.5,-5.5+hb,.5,2,WL);p(10.25,-1.75+hb,.5,.5,'#ffffff')}
  if(o.hat==='beret'){p(3,1+hb,13,3,'#2a6a3a');p(4,0+hb,10,1,'#3a8a4a');p(4,.5+hb,8,.5,'#4aa85a');p(3,3.75+hb,13,.25,'#1c4a28');p(15,-3+hb,1,4,'#f4f4f4');p(15.25,-3+hb,.25,4,'#c8c8d0');p(16,-5+hb,1,3,'#e04040');p(16,-5+hb,.5,3,'#ff7070')}
  if(o.hat==='helm'){p(4,0+hb,12,5,'#9aa4b8');p(4,4+hb,12,1,'#6a7488');p(13,0+hb,3,4,'#7a8498');p(6,1+hb,3,1,'#dfe6f2');p(6,1+hb,1,.5,'#ffffff');p(9,-2+hb,2,3,'#c83434');p(9,-2+hb,.5,3,'#e85a50');for(let x=5;x<16;x+=2.5)p(x,4+hb,.5,.5,'#c8d0e0')}
  if(front)weapon();
  const out=outline(c,'#22161e',KH);out.k=KH;
  if(state==='dead'){const r=canvas(out.height,out.width),rq=r.getContext('2d');rq.translate(0,out.width);rq.rotate(-Math.PI/2);rq.drawImage(out,0,0);r.k=KH;return r}
  return out;
}

