# Personagens redesenhados com o dobro de detalhe (meio pixel lógico = 1 pixel de verdade).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
a=s.index('function sprHuman(');b=s.index('\n}\n',a)+3
s=s[:a]+r"""function lighten(col,f=1.18){const[r,g2,b]=hex(col);const h=v=>Math.min(255,Math.round(v*f)).toString(16).padStart(2,'0');return'#'+h(r)+h(g2)+h(b)}
function sprHuman(o,dir,state,f){
  const c=scv(32,39),q=c.getContext('2d'),p0=P(q),OX=6,OY=8;
  const p=(x,y,w,h,col)=>p0(x+OX,y+OY,w,h,col);
  const ln=(a,b,c2,d,col,w)=>line(p0,a+OX,b+OY,c2+OX,d+OY,col,w);
  const front=dir!=='b';
  let by=0,lL=0,lR=0,aL=0,aR=0;
  if(state==='walk'){if(f===1){lL=1;aL=1;aR=-1;by=-1}if(f===3){lR=1;aL=-1;aR=1;by=-1}}
  if(state==='sit')by=4;
  const hb=by+(state==='idle'&&f===1?.5:0);
  let hand=[15,17+by+aR],tip=[18,23+by+aR];
  if(state==='attack'){hand=[[14,6],[16,12],[16,18]][f];tip=[[8,-2],[22,9],[21,25]][f]}
  if(state==='cast'){hand=[15,10+by];tip=[17,3+by]}
  const S=o.skin,SD=o.skinD,SL=lighten(S,1.06),T=o.tunic,TD=o.tunicD,TL=lighten(T),TDD=shade(TD),PA=o.pants,PD=o.pantsD,PL=lighten(PA),BO=o.boot,BD=shade(BO),BL=lighten(BO,1.3);
  const weapon=()=>{
    if(!o.weapon)return;const[hx,hy]=hand,vx=tip[0]-hx,vy=tip[1]-hy;
    const at=k=>[hx+vx*k,hy+vy*k],L=lighten(o.blade,1.1);
    const guard=()=>{p(hx-1.5,hy-1,4,1.5,'#c08a20');p(hx-1.5,hy-1,4,.5,'#ffe48a');p(hx,hy+.5,1,1.5,'#6b4426');p(hx,hy+2,1,.5,'#e0b040')};
    if(o.wtype==='adaga'){const[tx,ty]=at(.6);ln(hx,hy,tx,ty,o.blade);ln(hx+1,hy,tx+1,ty,o.bladeD);ln(hx,hy,tx,ty,L,.5);guard()}
    else if(o.wtype==='espada'){const[tx,ty]=at(1);ln(hx,hy,tx,ty,o.blade);ln(hx+1,hy,tx+1,ty,o.bladeD);ln(hx+.5,hy,tx+.5,ty,shade(o.blade),.5);ln(hx,hy,tx,ty,L,.5);guard()}
    else if(o.wtype==='lanca'){const[bx,by2]=at(-.45),[mx,my]=at(1.25),[tx,ty]=at(1.6);ln(bx,by2,mx,my,'#8e6034');ln(bx+.5,by2,mx+.5,my,'#6b4426',.5);ln(mx,my,tx,ty,o.blade);ln(mx,my,tx,ty,L,.5);p(mx-1,my-1,3,2,o.bladeD);p(mx-1,my-1,3,.5,L)}
    else if(o.wtype==='machado'){const[tx,ty]=at(1);ln(hx,hy,tx,ty,'#8e6034');ln(hx+.5,hy,tx+.5,ty,'#6b4426',.5);p(tx-2.5,ty-2.5,4.5,4.5,o.bladeD);p(tx-2.5,ty-2.5,3.5,3.5,o.blade);p(tx-2.5,ty-2.5,.5,3.5,L);p(tx-.5,ty-.5,1,1,'#5a3a20')}
    else if(o.wtype==='maca'){const[tx,ty]=at(.95),mL=o.maceL||'#a8b0c0',mD=o.maceD||'#6a7080';ln(hx,hy,tx,ty,'#6b4426');p(tx-2,ty-2,4,4,mD);p(tx-2,ty-2,3,3,mL);p(tx-1.5,ty-1.5,1,1,'#ffffff');p(tx-3,ty-.5,1,1,mD);p(tx+2,ty-.5,1,1,mD);p(tx-.5,ty-3,1,1,mD);p(tx-.5,ty+2,1,1,mD)}
  };
  if(!front)weapon();
  // pernas e pés
  const leg=(x,lift)=>{const y=21-lift;
    p(x,y,3,4,PA);p(x+2,y,1,4,PD);p(x+.5,y+1.5,1,.5,PL);p(x,y+3.5,3,.5,PD);
    if(o.legsJeans){p(x+.5,y,.5,3.5,'#5a7ab8');p(x+2,y+.5,.5,3,'#d8b040')}
    p(x,y+4,3,2,BO);p(x,y+5.5,3,.5,BD);p(x+.5,y+4,1.5,.5,BL);if(o.legsJeans)p(x,y+5,3,.5,'#b8bcc8')};
  if(state==='sit'){p(4,23,5,2,PA);p(4,24.5,5,.5,PD);p(11,23,5,2,PA);p(11,24.5,5,.5,PD);p(3,24,2,2,BO);p(15,24,2,2,BO);p(3,25.5,2,.5,BD);p(15,25.5,2,.5,BD)}
  else if(!o.robe){leg(6,lL);leg(11,lR)}
  else{p(5,20+by,10,6-by,T);p(12,20+by,3,6-by,TD);p(5,20+by,.5,6-by,TL);p(8.5,21+by,.5,4-by,TD);p(5,25,10,1,o.trim);for(let x=5.5;x<15;x+=2)p(x,25.5,.5,.5,TDD);p(6,26-lL,3,1,BO);p(11,26-lR,3,1,BO);p(6,26.5-lL,3,.5,BD);p(11,26.5-lR,3,.5,BD)}
  // tronco
  p(6,13+by,8,8,T);p(12,13+by,2,8,TD);p(6,13+by,.5,7,TL);p(11.5,15+by,.5,4,TD);p(7.5,16+by,.5,3,TD);
  if(front){p(8,13+by,4,.5,o.trim);p(8.5,13.5+by,3,.5,o.trim);p(9.5,13+by,1,1,S);
    if(o.print){p(8,15+by,4,2.5,o.print);p(8,15+by,4,.5,lighten(o.print,1.3));p(9.5,15.5+by,1,1,'#ffd040');p(9,16+by,.5,.5,'#ffd040');p(10.5,16+by,.5,.5,'#ffd040')}}
  if(o.armor){const AL=lighten(o.armor,1.25);p(6,13+by,8,4,o.armor);p(12,13+by,2,4,o.armorD);p(6,13+by,8,.5,'#e8eef8');p(6,16.5+by,8,.5,o.armorD);p(6.5,14+by,.5,2,AL);if(front){p(7,15+by,.5,.5,AL);p(12.5,15+by,.5,.5,AL)}}
  p(6,19+by,8,1,o.belt);p(6,19.5+by,8,.5,shade(o.belt));if(front){p(9,19+by,2,1,'#c89a30');p(9.5,19+by,1,.5,'#fff0a0')}
  // braços
  p(4,13+by,2,4+aL,T);p(4,13+by,.5,4+aL,TL);p(5.5,13+by,.5,4+aL,TD);p(4,17+by+aL,2,2,S);p(4,18.5+by+aL,2,.5,SD);
  if(state==='attack'||state==='cast'){ln(14,14+by,hand[0],hand[1],TD);ln(15,14+by,hand[0]+1,hand[1],T);p(hand[0]-1,hand[1]-1,2,2,S);p(hand[0]-1,hand[1]+.5,2,.5,SD)}
  else{p(14,13+by,2,4+aR,TD);p(14,13+by,.5,4+aR,T);p(14,17+by+aR,2,2,S);p(14,18.5+by+aR,2,.5,SD)}
  // cabeça
  p(5,2+hb,10,10,S);p(4,3+hb,12,8,S);p(13.5,4+hb,1.5,7,SD);p(5,11+hb,10,1,SD);p(5,11.5+hb,10,.5,shade(SD));p(5.5,4+hb,1,4,SL);
  p(8,12+hb,4,1,SD);
  const H=o.hair,H0=H[0],H1=H[1],H2=H[2];
  if(front){
    p(3.5,6.5+hb,1,2.5,S);p(3.5,7+hb,.5,1.5,SD);p(15.5,6.5+hb,1,2.5,SD);
    // olhos: cílio, íris, pupila e dois brilhos
    for(const ex of[6,12]){p(ex-.5,6.5+hb,3,.5,'#2a1a20');p(ex,7+hb,2,3,o.eye);p(ex+.5,7.5+hb,1,2,shade(o.eye));p(ex,9.5+hb,2,.5,lighten(o.eye,1.35));p(ex,7+hb,.5,.5,'#ffffff');p(ex+1.5,8.5+hb,.5,.5,'#ffffff')}
    p(5.5,5.5+hb,2.5,.5,H0);p(12,5.5+hb,2.5,.5,H0);
    p(9.5,9+hb,.5,.5,SD);p(9,10.5+hb,2,.5,'#a85048');p(9.5,11+hb,1,.5,'#e08a80');
    p(5,9.5+hb,1,.5,'#f4a090');p(14,9.5+hb,1,.5,'#f4a090');
    if(o.beard){const B=o.beard;p(5,9+hb,10,3,B);p(6,12+hb,8,1,B);p(7,13+hb,6,.5,B);p(8,9+hb,4,1,shade(B));p(9,10.5+hb,2,.5,'#5a3030');for(let x=5.5;x<15;x+=1.5)p(x,10+hb,.5,1.5,shade(B))}
  }
  // cabelo com mechas e brilho
  p(4,1+hb,12,4,H1);p(3,2+hb,14,4,H1);
  if(front){
    p(3,5+hb,2,6,H1);p(15,5+hb,2,6,H1);p(3,5+hb,.5,6,H0);p(16.5,5+hb,.5,6,H0);
    const fr=[[5,2],[5.5,2.5],[6,2],[6.5,1.5],[7,1],[8,2],[8.5,2.5],[9,2],[9.5,1.5],[10,1],[11,2],[11.5,1.5],[12,1],[13,2],[13.5,2.5],[14,2],[14.5,1.5]];
    for(const[x,h]of fr)p(x,5+hb,.5,h,H1);
    for(const x of[6.5,9.5,12,14.5])p(x,4.5+hb,.5,1,H0);
    p(3,10+hb,2,1,H0);p(15,10+hb,2,1,H0);
  }else{p(3,2+hb,14,10,H1);p(4,11+hb,12,1,H0);p(13,4+hb,3,7,H0);for(const x of[5,7,9.5,11.5])p(x,4+hb,.5,7,H0);p(4,11.5+hb,12,.5,shade(H0))}
  if(o.spiky){p(4,0+hb,2,1,H1);p(4.5,-.5+hb,1,.5,H1);p(8,0+hb,2,1,H1);p(8.5,-.5+hb,1,.5,H1);p(12,0+hb,2,1,H1);p(12.5,-.5+hb,1,.5,H1);p(16,1+hb,1,2,H1);p(2,3+hb,1,2,H1)}
  p(6,2+hb,3,.5,H2);p(5,2.5+hb,1,1,H2);p(9.5,1.5+hb,2,.5,H2);p(6.5,3+hb,1.5,.5,H2);p(14,3+hb,2,2,H0);p(4,1+hb,12,.5,shade(H1));
  // chapéus
  if(o.hat==='bandana'){p(3,4+hb,14,1,'#c83434');p(3,4+hb,14,.5,'#e85a50');p(3,5+hb,1,1,'#962020');if(front)p(17,5+hb,1,3,'#c83434');else{p(9,5+hb,2,2,'#c83434');p(8,7+hb,1,2,'#962020');p(11,7+hb,1,2,'#962020')}}
  if(o.hat==='cap'){p(4,-1+hb,12,4,'#f2f2f6');p(4,-1+hb,12,.5,'#ffffff');p(4,2+hb,12,1,'#c8c8d4');p(9,-1+hb,2,3,'#e0b040');p(8,0+hb,4,1,'#e0b040');p(9.5,-.5+hb,.5,.5,'#fff4b0')}
  if(o.hat==='wide'){p(1,3+hb,18,2,'#6a4426');p(1,3+hb,18,.5,'#8e6034');p(1,4.5+hb,18,.5,'#4a2e18');p(5,-1+hb,10,4,'#86582e');p(5,-1+hb,10,.5,'#a87444');p(5,2+hb,10,1,'#b04030');p(5,2.5+hb,10,.5,'#802a20');for(let x=5.5;x<15;x+=2)p(x,0+hb,.5,2,'#7a4e28')}
  if(o.hat==='wizard'){const WZ='#4a2a8a',WL='#6a4aaa';p(3,2+hb,14,2,WZ);p(5,0+hb,10,2,WZ);p(7,-3+hb,7,3,WZ);p(9,-6+hb,5,3,WZ);p(11,-8+hb,3,2,WZ);p(13,-9+hb,2,1,WZ);p(5,1+hb,10,1,'#f0d070');p(5,1+hb,10,.5,'#fff0a0');p(10,-2+hb,1,1,'#fff4a0');p(12,-5+hb,1,1,'#fff4a0');p(12,-3+hb,2,3,WL);p(7.5,-2.5+hb,.5,2,WL);p(9.5,-5.5+hb,.5,2,WL)}
  if(o.hat==='beret'){p(3,1+hb,13,3,'#2a6a3a');p(4,0+hb,10,1,'#3a8a4a');p(4,.5+hb,8,.5,'#4aa85a');p(15,-3+hb,1,4,'#f4f4f4');p(16,-5+hb,1,3,'#e04040');p(16,-5+hb,.5,3,'#ff7070')}
  if(o.hat==='helm'){p(4,0+hb,12,5,'#9aa4b8');p(4,4+hb,12,1,'#6a7488');p(6,1+hb,3,1,'#dfe6f2');p(6,1+hb,1,.5,'#ffffff');p(9,-2+hb,2,3,'#c83434');p(9,-2+hb,.5,3,'#e85a50');for(let x=5;x<16;x+=2.5)p(x,4+hb,.5,.5,'#c8d0e0')}
  if(front)weapon();
  const out=outline(c);
  if(state==='dead'){const r=canvas(out.height,out.width),rq=r.getContext('2d');rq.translate(0,out.width);rq.rotate(-Math.PI/2);rq.drawImage(out,0,0);return r}
  return out;
}
"""+s[b:]
# roupas do outro mundo: estampa da camiseta e costuras do jeans
s=s.replace("if(me.eq.armor==='camiseta')Object.assign(x,{tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34'});",
            "if(me.eq.armor==='camiseta')Object.assign(x,{tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34',print:'#3a6ac8'});",1)
s=s.replace("if(me.eq.legs==='jeans')Object.assign(x,{pants:'#3a5a9a',pantsD:'#2a4070',boot:'#f0f0f0'});",
            "if(me.eq.legs==='jeans')Object.assign(x,{pants:'#3a5a9a',pantsD:'#2a4070',boot:'#f0f0f0',legsJeans:1});",1)
open(p,'w',encoding='utf-8').write(s);print('ok')
