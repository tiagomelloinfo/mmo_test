# Tira moitas, carrinho de frutas e barraquinha do vilarejo; postes apagados de dia e acesos com fogo à noite;
# ciclo de dia e noite (1 hora do jogo = 1 minuto real), com escuridão e luz dos postes.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,1)
rep("  addObj('stall',C+4,C-3,{spr:SPR.stall});\n","")
rep("  addObj('cart',C+3,C+1,{spr:SPR.cart});\n","")
rep("  for(const[a,b]of[[C-3,C-11],[C+4,C+2],[C-6,C+5]])addObj('bush',a,b,{spr:SPR.bush});\n","")
# poste: lanterna de vidro apagada (pavio) ou acesa (chama)
a=s.index("function sprLamp(){");b=s.index("\n",a)+1
s=s[:a]+"""function sprLamp(lit){
  const c=scv(9,36),q=c.getContext('2d'),p=P(q);
  p(3,9,3,24,'#5e3c20');p(3,9,.5,24,'#8e6034');p(5.5,9,.5,24,'#3e2614');for(let y=12;y<32;y+=3)p(4,y,.5,1.5,'#3e2614');
  p(1,32,7,3,'#4a2e18');p(1,32,7,.5,'#6b4426');
  p(1,2,7,8,'#2e2c36');p(1,2,.5,8,'#4a4858');p(2,0,5,2,'#2e2c36');p(3.5,-.5,2,1,'#2e2c36');p(2,1.5,5,.5,'#5a5868');
  if(lit){p(2,3,5,6,'#ffb050');p(2.5,3.5,4,5,'#ffd27a');blob(q,4.5,6.5,1.4,2.2,['#ff8a2a','#ffb040','#ffe08a','#fffbe0']);p(4.25,7.5,.5,1,'#3a2a20')}
  else{p(2,3,5,6,'#3a4450');p(2,3,5,.5,'#56606c');p(2.5,3.5,1,3,'#7a8a9a');p(2.5,3.5,.5,1,'#c8d4e0');p(4.25,6.5,.5,2,'#2a2018');p(4,8.5,1,.5,'#d8d0b8')}
  p(4.25,2,.5,7,'#2e2c36');
  return outline(c);
}
"""+s[b:]
rep("SPR.lamp=sprLamp();","SPR.lamp=sprLamp(false);SPR.lampOn=sprLamp(true);")
# relógio do mundo
rep("const SAVE_KEY='valhen_save_v2'","""// relógio: 1 hora do jogo = 1 minuto real; começa às 7h
let CLOCK0=7;
function hourNow(){return(CLOCK0+TIME/60)%24}
function hhmm(){const h=hourNow(),m=Math.floor((h%1)*60);return String(Math.floor(h)).padStart(2,'0')+':'+String(m).padStart(2,'0')}
function lampsLit(){const h=hourNow();return h>=18||h<6}
// escuridão de 0 (dia) a .62 (madrugada), com tom alaranjado no fim de tarde
function darkness(){const h=hourNow();if(h>=7&&h<17)return 0;if(h>=17&&h<20)return(h-17)/3*.62;if(h>=20||h<4)return .62;return .62*(1-(h-4)/3)}
function duskTint(){const h=hourNow();return h>=16.5&&h<19.5?Math.sin((h-16.5)/3*Math.PI)*.18:h>=5&&h<7?Math.sin((h-5)/2*Math.PI)*.12:0}
const SAVE_KEY='valhen_save_v2'""")
rep("const k=['name','xp','inv','eq','cards','zeny','learned','quests','hp','sp','last'];const o={};for(const x of k)o[x]=me[x];o.hot=hot;",
    "const k=['name','xp','inv','eq','cards','zeny','learned','quests','hp','sp','last'];const o={};for(const x of k)o[x]=me[x];o.hot=hot;o.clock=hourNow();")
rep("function startGame(data){\n  initHero(data);","function startGame(data){\n  initHero(data);CLOCK0=(typeof data.clock==='number'?data.clock:7)-TIME/60;")
# postes: sprite aceso só à noite, com chama e brilho de fogo
rep("      if(o.kind==='lamp'){g.globalAlpha=.12+.04*Math.sin(TIME*6+o.x);g.fillStyle='#ffe08a';g.beginPath();g.arc(s.x,s.y-30,10,0,7);g.fill();g.globalAlpha=1}",
    "      if(o.kind==='lamp'&&lampsLit()&&Math.random()<.25)parts.push({x:s.x+rand(-1,1),y:s.y-29,vx:rand(-3,3),vy:-rand(6,14),g:0,life:rand(.2,.4),max:.4,col:pick(['#ffd060','#ff8a3a']),s:.5});")
rep("      drawSpr(o.spr,s.x,s.y+(o.kind==='well'?11:2),false,al);",
    "      drawSpr(o.kind==='lamp'&&lampsLit()?SPR.lampOn:o.spr,s.x,s.y+(o.kind==='well'?11:2),false,al);")
# escuridão da noite com luz dos postes e um pouco em volta do herói
rep("  if(fadeT>0){g.globalAlpha=Math.min(1,fadeT/.35);",
"""  if(scene==='world'){const dk=darkness(),tn=duskTint();
    if(tn>0){g.globalAlpha=tn;g.fillStyle='#ff8a40';g.fillRect(0,0,W,H);g.globalAlpha=1}
    if(dk>0){
      if(!window._lightC||_lightC.width!==W*K||_lightC.height!==H*K)window._lightC=canvas(W*K,H*K);
      const lq=_lightC.getContext('2d');lq.setTransform(1,0,0,1,0,0);lq.globalCompositeOperation='source-over';lq.clearRect(0,0,_lightC.width,_lightC.height);
      lq.fillStyle=`rgba(6,10,32,${dk})`;lq.fillRect(0,0,_lightC.width,_lightC.height);lq.globalCompositeOperation='destination-out';
      const hole=(x,y,r,a)=>{const gr=lq.createRadialGradient(x*K,y*K,0,x*K,y*K,r*K);gr.addColorStop(0,`rgba(0,0,0,${a})`);gr.addColorStop(.55,`rgba(0,0,0,${a*.6})`);gr.addColorStop(1,'rgba(0,0,0,0)');lq.fillStyle=gr;lq.beginPath();lq.arc(x*K,y*K,r*K,0,7);lq.fill()};
      const lit=lampsLit(),warm=[];
      if(lit)for(const o of objects)if(o.kind==='lamp'){const ls=scr(o);if(ls.x<-80||ls.x>W+80||ls.y<-80||ls.y>H+120)continue;const fl=1+Math.sin(TIME*11+o.x*3)*.04+Math.sin(TIME*23+o.y)*.03;hole(ls.x,ls.y-26,58*fl,1);warm.push([ls.x,ls.y-26,fl])}
      const hs=scr(me);hole(hs.x,hs.y-12,34,.55);
      g.drawImage(_lightC,0,0,W,H);
      g.globalCompositeOperation='lighter';
      for(const[x,y,fl]of warm){const gr=g.createRadialGradient(x,y,0,x,y,46*fl);gr.addColorStop(0,`rgba(255,150,60,${.32*dk})`);gr.addColorStop(1,'rgba(255,120,40,0)');g.fillStyle=gr;g.beginPath();g.arc(x,y,46*fl,0,7);g.fill()}
      g.globalCompositeOperation='source-over';
    }
  }
  if(fadeT>0){g.globalAlpha=Math.min(1,fadeT/.35);""")
# hora no mapa
rep("$('mapName').textContent=scene!=='world'?`${ROOMS[scene].name} · Vilarejo do Sabiá`:`${inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (${Math.floor(me.x)}, ${Math.floor(me.y)})`;",
    "$('mapName').textContent=(scene!=='world'?`${ROOMS[scene].name} · Vilarejo do Sabiá`:`${inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (${Math.floor(me.x)}, ${Math.floor(me.y)})`)+` · ${hhmm()}`;")
# pernoitar na hospedaria leva até as 7h da manhã seguinte
rep("me.zeny-=15;me.hp=me.maxHp;me.sp=me.maxSp;fadeT=1.4;","me.zeny-=15;me.hp=me.maxHp;me.sp=me.maxSp;fadeT=1.4;CLOCK0=7-TIME/60;")
# casa só fica transparente quando o herói está de fato atrás dos pixels dela
rep("if(o.kind==='bld'&&behind(me,o.box)){const hs=scr(me);if(hs.x>x+4&&hs.x<x+o.spr.width/K-4&&hs.y>y&&hs.y-28<y+o.spr.height/K)al=.5}","if(o.kind==='bld'&&behind(me,o.box)){const hs=scr(me);if(!o.alpha)o.alpha=o.spr.getContext('2d').getImageData(0,0,o.spr.width,o.spr.height).data;\n        for(const dy of[4,12,22]){const px=Math.floor((hs.x-x)*K),py=Math.floor((hs.y-dy-y)*K);if(px>=0&&py>=0&&px<o.spr.width&&py<o.spr.height&&o.alpha[(py*o.spr.width+px)*4+3]>100){al=.5;break}}}")
open(p,'w',encoding='utf-8').write(s);print('ok')
