# Camada de realismo: placas penduradas, casas com desgaste/sombra/palha/persianas/floreiras,
# paliçada de estacas, chão com sombra das casas e textura, moita e poço redesenhados.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,1)

# ---------------- casas
rep("  const wallCol=(face,u,h,len)=>{\n    const U=u*16;\n    if(face===o.door){",
    "  const weather=(col,u,h)=>{const U=u*16;let f=1;\n    if(h<5)f*=.8+h/5*.2;\n    if(o.roof!=='flat'&&h>WH-5)f*=.8+(WH-h)/5*.2;\n    f*=.95+vnoise(U*.25,h*.08,33)*.1;\n    if(h<7&&vnoise(U*.18,h*.35,44)>.62)f*=.86;\n    return mul(col,f)};\n  const SHUT=hex(o.shut||'#3a6a3a'),SHUTD=hex(shade(o.shut||'#3a6a3a').replace(/rgb\\((\\d+),(\\d+),(\\d+)\\)/,(m,a,b2,c2)=>'#'+[a,b2,c2].map(v=>(+v).toString(16).padStart(2,'0')).join(''))),BOX=hex('#6b4426'),FLW=['#e84a5a','#ffd84a','#ffffff','#b48aff'].map(hex),LEAF=hex('#3a7a32');\n  const wallCol=(face,u,h,len)=>weather(wallBase(face,u,h,len),u,h);\n  const wallBase=(face,u,h,len)=>{\n    const U=u*16;\n    if(face===o.door){")
rep("      if(du<.25&&Math.abs(h-(wy0-.5))<.5)return SILL;",
    "      if(du<.25&&Math.abs(h-(wy0-.5))<.5)return SILL;\n      if(o.shut&&du>=.22&&du<.36&&h>=wy0&&h<=wy1){const sp=(du-.22)*16*2;return(sp%1.4<.35||h<wy0+.5||h>wy1-.5)?SHUTD:SHUT}\n      if(o.flowers&&face==='L'&&du<.26&&h>=wy0-4&&h<wy0-1){if(h>=wy0-2){const fh2=hash2(Math.floor(u*16*K),Math.floor(h*K),71);return fh2<.45?LEAF:FLW[Math.floor(fh2*9)%4]}return(h<wy0-3.6||du>.25)?mul(BOX,.7):BOX}")
rep("    if(st==='stone'||h<3){const row=Math.floor(h/4),off=(row%2)*4,hh=hash2(Math.floor((U+off)/8),row,7);if(h%4<.5||(U+off)%8<.5)return MORT;return mul(STONE,.86+hh*.26+(h%4>3?-.06:0))}",
    "    if(st==='stone'||h<3.5){const row=Math.floor(h/4),off=(row%2)*4+hash2(row,0,8)*2,hh=hash2(Math.floor((U+off)/8),row,7);if(h%4<.5||(U+off)%8<.5)return MORT;\n      if(h<2.5&&vnoise(U*.3,h,55)>.6)return[78,104,52];\n      return mul(STONE,.84+hh*.28+(h%4>3?-.07:0)+(h%4<1.2?.05:0))}")
# palha nos telhados de R.straw e variação de cor nas telhas
rep("    if(o.roof==='gable'){\n      const dr=Math.abs(gy-fh/2),front=gy>fh/2,sv=dr*16/2.4,row=Math.floor(sv);idx=front?2:1;",
    "    if(o.roof==='gable'&&o.rr===R.straw){\n      const dr=Math.abs(gy-fh/2),front=gy>fh/2,sv=dr*16,row=Math.floor(sv/3.5),fr=sv/3.5-row,fib=hash2(Math.floor(gx*16*K+row*5),row,11);\n      idx=front?2:1;if(fr>.78)idx--;if(fib<.22)idx--;else if(fib>.9)idx++;\n      if(dr<.1)idx=hash2(Math.floor(gx*16*K),0,13)<.5?0:1;\n      if(dr>fh/2+ov-.06||gx<gx0+.05||gx>gx1-.05)idx=hash2(Math.floor(gx*16*K),Math.floor(gy*16*K),14)<.5?0:1;\n    }else if(o.roof==='gable'){\n      const dr=Math.abs(gy-fh/2),front=gy>fh/2,sv=dr*16/2.4,row=Math.floor(sv);idx=front?2:1;")
rep("    put(ox+(gx-gy)*16,oy+(gx+gy)*8-hr(gx,gy),R4[clamp(idx,0,3)],gx+gy);",
    "    put(ox+(gx-gy)*16,oy+(gx+gy)*8-hr(gx,gy),mul(R4[clamp(idx,0,3)],.92+vnoise(gx*5,gy*5,77)*.14),gx+gy);")
# placa pendurada: suporte de ferro, correntes, tábuas, moldura, medalhão pintado e sombra na parede
a=s.index("  if(o.sign&&SPR.icons[o.sign]){\n    q.setTransform(K,0,0,K,0,0);")
b=s.index("    q.setTransform(1,0,0,1,0,0);\n  }\n",a)+len("    q.setTransform(1,0,0,1,0,0);\n  }\n")
s=s[:a]+"""  if(o.sign&&SPR.icons[o.sign]){
    q.setTransform(K,0,0,K,0,0);const pq=P(q),L=o.door==='L';
    const u=L?Math.min(fw-.25,o.doorAt+.85):Math.max(.25,o.doorAt-.85),hb=dh+7;
    const wx=L?ox-fh*16+u*16:ox+fw*16-u*16,wy=(L?oy+(u+fh)*8:oy+(fw+u)*8)-hb;
    const dx=L?-7:7,ex=Math.round(wx+dx),ey=Math.round(wy+3.5);
    // suporte de ferro preso na parede
    pq(Math.round(wx)-1,Math.round(wy)-2,2,4,'#2a2a30');pq(Math.round(wx)-.5,Math.round(wy)-1.5,.5,3,'#5a5a66');
    line(pq,wx,wy,ex,ey,'#2a2a30');line(pq,wx,wy-.5,ex,ey-.5,'#5a5a66',.5);line(pq,wx,wy+2.5,wx+dx*.55,wy+.5,'#2a2a30',.5);
    pq(ex-.5,ey-.5,1.5,1.5,'#3a3a44');
    const bw=17,bh=14,bx=ex-bw/2,by=ey+3;
    // correntes
    for(const cx of[bx+2.5,bx+bw-3])for(let yy=ey;yy<by;yy+=1)pq(cx,yy,.5,.5,yy%2?'#6a6a74':'#a8a8b4');
    // sombra da placa na parede
    q.fillStyle='rgba(20,10,0,.28)';q.fillRect(bx+(L?2:-2),by+2,bw,bh);
    // tábuas com veio e moldura
    const W0='#5a3a20',W1='#8a5a30',W2='#a8743e',W3='#c08a50';
    pq(bx,by,bw,bh,W0);
    for(let r=0;r<3;r++){const ty=by+.5+r*4.4;pq(bx+.5,ty,bw-1,4,r%2?W1:W2);pq(bx+.5,ty,bw-1,.5,W3);pq(bx+.5,ty+3.5,bw-1,.5,W0);
      for(let k=0;k<3;k++){const gx2=bx+1.5+hash2(r,k,91)*(bw-6);pq(gx2,ty+1.5+(k%2),3+hash2(k,r,92)*3,.5,W1)}}
    pq(bx,by,.5,bh,'#3a2410');pq(bx+bw-.5,by,.5,bh,'#3a2410');pq(bx,by+bh-.5,bw,.5,'#3a2410');
    q.clearRect(bx,by,.5,.5);q.clearRect(bx+bw-.5,by,.5,.5);q.clearRect(bx,by+bh-.5,.5,.5);q.clearRect(bx+bw-.5,by+bh-.5,.5,.5);
    // medalhão pintado com o ícone
    const mx=bx+bw/2,my=by+bh/2;blob(q,mx,my,6.5,5.8,['#c8b48a','#e4d4a8','#f2e6c4','#fff6dc']);
    for(let a2=0;a2<6.28;a2+=.12)pq(mx+Math.cos(a2)*6.3,my+Math.sin(a2)*5.6,.5,.5,'#7a4a20');
    const ic=SPR.icons[o.sign];q.drawImage(ic,mx-6,my-6,ic.width/K,ic.height/K);
    // pregos
    for(const[nx,ny]of[[bx+1,by+1],[bx+bw-1.5,by+1],[bx+1,by+bh-1.5],[bx+bw-1.5,by+bh-1.5]]){pq(nx,ny,.5,.5,'#d8d8e0');pq(nx+.5,ny+.5,.5,.5,'#4a4a52')}
    q.setTransform(1,0,0,1,0,0);
  }
"""+s[b:]
# persianas e floreiras nas casas de moradia, taverna, venda e hospedaria
for bid,extra in [('tavern',"shut:'#3a5a8a',flowers:1"),('shop',"shut:'#3a6a3a',flowers:1"),('inn',"shut:'#7a3a2a',flowers:1"),('h3',"shut:'#3a6a3a',flowers:1"),('chapel',"shut:'#6a5a3a'")]:
    i=s.index("{id:'%s'"%bid);j=s.index("door:",i);s=s[:j]+extra+","+s[j:]

# ---------------- paliçada de estacas pontudas
rep("function sprDummy(){","""// paliçada: estacas pontudas ao longo da casa (dir 'x' = ao longo de x, 'y' = ao longo de y)
function sprStakes(dir,seed,post){
  const H=28,c=scv(34,H+18),q=c.getContext('2d'),p=P(q);
  const at=t=>dir==='x'?[8+16*t,H+4+8*t]:[24-16*t,H+4+8*t];
  const n=post?2:4,pts=[];for(let i=0;i<n;i++){const t=post?.3+i*.4:.125+i*.25;pts.push(t)}
  pts.sort((a,b)=>at(a)[1]-at(b)[1]);
  // travessa amarrada no meio
  const r0=at(0),r1=at(1);for(const hh of[7,13]){line(p,r0[0],r0[1]-hh,r1[0],r1[1]-hh,'#4a2e18');line(p,r0[0],r0[1]-hh-.5,r1[0],r1[1]-hh-.5,'#7e5530',.5)}
  for(const t of pts){const[x,y]=at(t),k=hash2(Math.floor(t*100),seed,61),hgt=(post?21:15)+k*4,w=post?3.5:2.5;
    const x0=x-w/2;
    for(let yy=0;yy<hgt;yy+=.5){const tip=hgt-yy<w?(hgt-yy)/w:1,ww=w*tip,xs=x-ww/2;
      p(xs,y-yy,ww,.5,'#6b4426');p(xs,y-yy,Math.min(.5,ww),.5,'#8e6034');p(xs+ww-.5,y-yy,.5,.5,'#4a2e18');
      if(hash2(Math.floor(yy*2),Math.floor(t*100)+seed,62)<.12)p(xs+.5+hash2(yy|0,seed,63)*(ww-1),y-yy,.5,.5,'#3e2614')}
    p(x0,y-1,w,1,'#3e2614');
    for(const hh of[7,13])p(x0-.25,y-hh-.5,w+.5,1,'#c8b07a');
    if(post)p(x-.5,y-hgt+1,1,.5,'#a07444')}
  return{c:outline(c,'#1a120c'),ax:17,ay:H+17,mc:'#6b4426'};
}
function sprDummy(){""")
rep("    addBox('wall',x,y,1,1,post?SPR.post:(along%2?SPR.fenceA:SPR.fenceB));",
    "    const dir=(y===C-CW||y===C+CW-1)?'x':'y';\n    addBox('wall',x,y,1,1,corner?SPR.stakes.post:post?SPR.stakes.post:SPR.stakes[dir][(x*7+y*3)%3]);")
rep("  SPR.fenceA=sprBuilding(","  SPR.stakes={x:[0,1,2].map(i=>sprStakes('x',i)),y:[0,1,2].map(i=>sprStakes('y',i)),post:sprStakes('x',9,true)};\n  SPR.fenceA=sprBuilding(")

# ---------------- moita
a=s.index("function sprBush(){");b=s.index("\n",a)+1
s=s[:a]+"""function sprBush(){
  const c=scv(24,16),q=c.getContext('2d'),p=P(q),LF=['#1f4a26','#2e6a32','#4a8e3e','#78b85a'];
  // vários tufos de folhas sobrepostos, do fundo para a frente
  for(const[x,y,rx,ry]of[[7,7,5,4],[16,6.5,5.5,4.2],[12,5,5,4],[5,10.5,4.6,3.6],[18.5,10.5,4.6,3.6],[12,10,6.5,4.6]]){
    const k=q.getTransform().a;q.save();q.setTransform(1,0,0,1,0,0);
    for(let Y=Math.floor((y-ry)*k);Y<=Math.ceil((y+ry)*k);Y++)for(let X=Math.floor((x-rx)*k);X<=Math.ceil((x+rx)*k);X++){
      const px=(X+.5)/k,py=(Y+.5)/k,dx=(px-x)/rx,dy=(py-y)/ry,d=dx*dx+dy*dy;
      const leaf=vnoise(px*1.6,py*1.9,X%7)*.5+vnoise(px*3.1,py*3.4,17)*.35;
      if(d>1-.25*leaf)continue;
      const l=-dx*.55-dy*.75+(1-d)*.4+(leaf-.4)*.9+bay(X,Y)*.25;
      q.fillStyle=LF[l<-.35?0:l<.15?1:l<.6?2:3];q.fillRect(X,Y,1,1)}
    q.restore()}
  for(let i=0;i<26;i++){const x=rand(3,21),y=rand(2,12),id=q.getImageData(Math.round(x*K),Math.round(y*K),1,1).data;if(id[3]&&y<9)p(x,y,.5,.5,'#a8d878')}
  for(const[x,y]of[[6,6],[11,4],[16,7],[9,10],[18,10],[13.5,8.5]]){p(x,y,1.5,1.5,'#b81e30');p(x,y,1.5,.5,'#e03a4a');p(x,y,.5,.5,'#ffc0c0');p(x+1,y+1,.5,.5,'#6a0e18')}
  return outline(c,'#0c2010');
}
"""+s[b:]

# ---------------- poço
a=s.index("function sprWell(){");b=s.index("\n}\n",a)+3
s=s[:a]+"""function sprWell(){
  const c=scv(40,48),q=c.getContext('2d'),p=P(q);
  const cx=20,rimY=33,RX=16,RY=6,IX=12.5,IY=4.6,BOT=42;
  // parede cilíndrica de pedras
  for(let y=rimY;y<=BOT+RY;y+=.5)for(let x=cx-RX;x<=cx+RX;x+=.5){
    const dx=(x+.25-cx)/RX;if(Math.abs(dx)>1)continue;const ey=Math.sqrt(1-dx*dx)*RY;if(y<rimY+ey-.5||y>BOT+ey)continue;
    const th=Math.asin(dx),row=Math.floor((y-rimY-ey)/3),col=Math.floor((th+1.6+(row%2)*.18)/.36),fr=((th+1.6+(row%2)*.18)/.36)%1,fy=((y-rimY-ey)/3)%1;
    const lit=.78+(-dx*.18)+hash2(col,row,3)*.16;let base=[150,144,134];
    if(fy<.17||fr<.08)base=[92,86,80];else if(y>BOT+ey-2.5&&vnoise(x*.6,y,5)>.55)base=[84,108,58];
    p(x,y,.5,.5,`rgb(${base.map(v=>Math.min(255,v*lit)|0).join(',')})`)}
  // borda de cima: anel de pedras
  for(let y=rimY-RY-1;y<=rimY+RY+1;y+=.5)for(let x=cx-RX;x<=cx+RX;x+=.5){
    const dx=(x+.25-cx)/RX,dy=(y+.25-rimY)/RY,d=dx*dx+dy*dy,di=((x+.25-cx)/IX)**2+((y+.25-rimY)/IY)**2;if(d>1)continue;
    if(di<=1){const wv=(y-rimY)/IY;const dark=wv<-.2?'#0c1c2c':'#12283c';p(x,y,.5,.5,dark);continue}
    const a2=Math.atan2(dy,dx),st=Math.floor((a2+3.2)/.42),fr=((a2+3.2)/.42)%1;
    p(x,y,.5,.5,fr<.1?'#5c5650':(dy<0?['#b8b2a6','#aaa498','#c4beb2'][st%3]:['#9a948a','#8e887e','#a8a296'][st%3]))}
  // água: reflexo do céu
  p(cx-6,rimY+1,5,.5,'#3a6a90');p(cx+1.5,rimY+1.5,3,.5,'#2a5274');p(cx-3,rimY+2.5,2,.5,'#5a8ab0');
  // postes de madeira com veio
  for(const px of[4.5,32.5]){p(px,10,3,rimY-8,'#6b4426');p(px,10,.5,rimY-8,'#8e6034');p(px+2.5,10,.5,rimY-8,'#4a2e18');for(let y=12;y<rimY;y+=2.5)p(px+1+hash2(y,px,2)*1,y,.5,1.5,'#4a2e18')}
  // sarilho com corda enrolada e manivela
  p(6,15,28,3,'#5e3c20');p(6,15,28,.5,'#8e6034');p(6,17.5,28,.5,'#3e2614');
  for(let x=14;x<26;x+=1)p(x,15,.5,3,x%2?'#c8b07a':'#a8905a');
  p(34,14.5,1.5,4,'#5a5a66');p(35,18,3,1,'#5a5a66');p(37.5,18,1,3,'#7e5530');
  // corda e balde
  p(19.75,18,.5,7,'#c8b07a');p(20.25,18,.5,7,'#a8905a');
  p(17,25,6,5,'#7e5530');p(17,25,6,.5,'#a07444');p(17,26,6,.5,'#4a4a52');p(17,28.5,6,.5,'#4a4a52');p(22.5,25,.5,5,'#5e3c20');p(16.5,24.5,7,.5,'#3e2614');
  // telhado de palha em duas águas
  for(let y=0;y<10;y+=.5){const w=4+y*1.9,x0=cx-w;for(let x=x0;x<cx+w;x+=.5){const fib=hash2(Math.floor(x*2),Math.floor(y/2.2),21);let col=x<cx?R.straw[2]:R.straw[1];if((y%2.2)>1.7||fib<.18)col=R.straw[0];else if(fib>.9)col=R.straw[3];p(x,y,.5,.5,col)}}
  p(cx-23,9.5,46,1,R.straw[0]);p(cx-.5,0,1,10,'#8a6420');
  return outline(c,'#1e1c22');
}
"""+s[b:]
rep("drawSpr(o.spr,s.x,s.y+(o.kind==='well'?10:2),false,al);","drawSpr(o.spr,s.x,s.y+(o.kind==='well'?11:2),false,al);")
open(p,'w',encoding='utf-8').write(s);print('ok')
