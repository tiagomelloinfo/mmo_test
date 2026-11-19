# Mapa inicial redesenhado (oeste montanhoso, rio ao norte, passagens bloqueadas por guardas,
# bosque a leste com portal) e segundo mapa: Bosque do Orvalho (lebres e javalis, caverna ao norte).
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]);s=s.replace(a,b)

# ---------- tipos de chão, mapa atual
rep("const T_GRASS=0,T_GRASS2=1,T_DIRT=2,T_SAND=3,T_WATER=4,T_STONE=5,T_VOID=6,T_FLOOR=7;",
    "const T_GRASS=0,T_GRASS2=1,T_DIRT=2,T_SAND=3,T_WATER=4,T_STONE=5,T_VOID=6,T_FLOOR=7,T_BRIDGE=8;\nlet curMap='vila',warping=null,mapBanner=null;const MAPS={};")
rep("const inCityTile=(x,y)=>x>=C-CW","const inCityTile=(x,y)=>curMap==='vila'&&x>=C-CW")
rep("4:['#1f4f8f','#265e9e','#2f6eae','#3a80c0','#4a92d0'],","4:['#1f4f8f','#265e9e','#2f6eae','#3a80c0','#4a92d0'],8:['#4a2e18','#6b4426','#7e5530','#94643a','#a87444'],")
rep("    if(base!==T_STONE){const jx=(vnoise(px*.09,py*.18,5)-.5)*.8,jy=(vnoise(px*.09,py*.18,9)-.5)*.8;const tj=typeAt(t0.x+jx,t0.y+jy);if(tj>=0&&tj!==T_STONE)t=tj}",
    "    if(base!==T_STONE&&base!==T_BRIDGE){const jx=(vnoise(px*.09,py*.18,5)-.5)*.8,jy=(vnoise(px*.09,py*.18,9)-.5)*.8;const tj=typeAt(t0.x+jx,t0.y+jy);if(tj>=0&&tj!==T_STONE&&tj!==T_BRIDGE)t=tj}")
rep("    else if(t===T_WATER)v=1.6+",
    "    else if(t===T_BRIDGE){const u=t0.x*3,fr=u-Math.floor(u);v=fr<.1?0:fr>.9?1:2+hash2(Math.floor(u),0,7)*2;if((t0.y%1)<.06||(t0.y%1)>.94)v=0}\n    else if(t===T_WATER)v=1.6+")

# ---------- sprites: montanha, barricada, pedregulho, caverna
rep("function sprWell(){",r"""// montanha por campo de altura com luz, rocha estratificada, grama na base e neve no topo
function sprMount(fw,fh,H,seed,snow){
  const M=4,ox=M+fh*16,oy=Math.ceil(H)+M+8,cw=(fw+fh)*16+2*M,ch=oy+(fw+fh)*8+M;
  const CW2=cw*K,CH2=ch*K,c=canvas(CW2,CH2),q=c.getContext('2d'),img=q.createImageData(CW2,CH2),d=img.data,zb=new Float32Array(CW2*CH2).fill(-1e9);
  const put=(x,y,col,z)=>{x=Math.round(x*K);y=Math.round(y*K);if(x<0||y<0||x>=CW2||y>=CH2)return;const k=y*CW2+x;if(z<zb[k])return;zb[k]=z;const i=k*4;d[i]=col[0];d[i+1]=col[1];d[i+2]=col[2];d[i+3]=255};
  const ROCK=['#2a2628','#3e3836','#554c48','#6e645c','#887c70','#a49686','#c0b2a0'].map(hex),GRS=['#2c5c26','#386c2c','#447c32','#528c3a'].map(hex),SNW=['#8e98ae','#bcc6d4','#e2e8f2','#ffffff'].map(hex);
  const cx=fw/2,cy=fh/2;
  const hf=(gx,gy)=>{const dx=(gx-cx)/(fw/2),dy=(gy-cy)/(fh/2),a=Math.atan2(dy,dx);const r=Math.hypot(dx,dy)*(1+(vnoise(a*1.4+seed,seed*3.1,61)-.5)*.4);if(r>=1)return -1;
    let h=Math.pow(1-r,1.1)*H;h*=.8+fbm(gx*.8+seed*7,gy*.8,62)*.4;h+=(vnoise(gx*2.4+seed,gy*2.4,63)-.5)*H*.1*(1-r);return Math.max(0,h)};
  const st=1/(K*16),hp=h=>Math.max(0,h);
  for(let gy=0;gy<fh;gy+=st)for(let gx=0;gx<fw;gx+=st){const h=hf(gx,gy);if(h<0)continue;
    const e=.06,hx=(hp(hf(gx+e,gy))-hp(hf(gx-e,gy)))/(2*e),hy=(hp(hf(gx,gy+e))-hp(hf(gx,gy-e)))/(2*e),sc=H/Math.max(fw,fh)*1.1,lx=hx/sc,ly=hy/sc;
    const nz=fbm(gx*2.6+seed,gy*2.6,64);
    let lit=.5+lx*.4-ly*.2+(nz-.5)*.3+Math.sin(h*.5+nz*5)*.07;
    let col;const gl=H*.12+nz*H*.12;
    if(snow&&h>H*.72+(nz-.5)*H*.16)col=SNW[clamp(Math.round(lit*3.6),0,3)];
    else if(h<gl&&Math.abs(lx)+Math.abs(ly)<1.5)col=GRS[clamp(Math.round(lit*3.4),0,3)];
    else col=ROCK[clamp(Math.round(lit*6.4),0,6)];
    const sx=ox+(gx-gy)*16,sy=oy+(gx+gy)*8-h,hn=Math.min(hp(hf(gx+st,gy)),hp(hf(gx,gy+st))),span=Math.max(1/K,h-hn+.5/K);
    for(let j=0;j<span;j+=1/K)put(sx,sy+j,col,gx+gy)}
  q.putImageData(img,0,0);
  return{c:outline(c,'#1a1618'),ax:ox+(fw-fh)*16+1,ay:oy+(fw+fh)*8+1,mc:'#6a625c'};
}
function sprBarricade(){
  const c=scv(30,22),q=c.getContext('2d'),p=P(q);
  for(const x0 of[4,24]){line(p,x0-3,20,x0+3,8,'#5a3a20');line(p,x0+3,20,x0-3,8,'#6b4426');line(p,x0-2.5,20,x0+3.5,8,'#8e6034',.5)}
  p(1,9,28,4,'#e8dcc4');for(let x=1;x<29;x+=4){for(let k=0;k<2;k+=.5)p(x+k+(1-k)*0,9+k*2,2,.5,'#b83030')}
  for(let x=1;x<29;x+=4){p(x,9,2,1,'#c83434');p(x+.5,10,2,1,'#c83434');p(x+1,11,2,1,'#c83434');p(x+1.5,12,1.5,1,'#a02828')}
  p(1,9,28,.5,'#fff8ec');p(1,12.5,28,.5,'#8a7a64');
  return outline(c);
}
function sprBoulder(seed){const c=scv(24,17),q=c.getContext('2d');blob(q,12,10,10,6,R.rock);blob(q,5+seed%3,12,4,3,R.rock);blob(q,18,13,4.5,3,R.stone);blob(q,9,14,6,2.4,R.brown,{maxY:16});return outline(c,'#1e1c22')}
function sprCave(){
  const c=scv(76,58),q=c.getContext('2d'),p=P(q);
  blob(q,38,30,36,26,['#2a2628','#433d3c','#5c5450','#776c64']);blob(q,20,36,16,16,['#2a2628','#3e3836','#554c48','#6e645c']);blob(q,56,36,16,16,['#2a2628','#3e3836','#554c48','#6e645c']);
  for(let y=30;y<57;y+=.5){const t=(y-30)/27,w=Math.sqrt(Math.max(0,1-Math.pow(1-t,2)))*12.5;for(let x=-w;x<w;x+=.5){const e=Math.abs(x)/Math.max(1,w);p(38+x,y,.5,.5,e>.85?'#2a2220':y<36?'#140e0c':'#0a0706')}}
  for(const[x,h]of[[30,4],[34,6],[39,3],[44,5],[47,3]])for(let i=0;i<h;i+=.5)p(x+i*.1,31+i,.5*(1-i/h)+.5,.5,'#3a3230');
  for(let i=0;i<14;i++){const x=24+Math.random()*28;p(x,26+Math.random()*4,1,2+Math.random()*3,'#3a6a2a')}
  for(let x=22;x<55;x+=.5)p(x,56.5,.5,.5,'#2a2220');
  return outline(c,'#141010');
}
function sprWell(){""")
rep("  SPR.rock=sprRock();","  SPR.mount={1:[0,1,2].map(i=>sprMount(1,1,18+i*5,i*3.1,false)),2:[0,1,2].map(i=>sprMount(2,2,34+i*8,10+i*2.7,false)),3:[0,1,2].map(i=>sprMount(3,3,54+i*10,20+i*1.9,i===2)),4:[0,1].map(i=>sprMount(4,4,78+i*14,30+i*4.3,true))};\n  SPR.barricade=sprBarricade();SPR.boulders=[0,1,2].map(sprBoulder);SPR.cave=sprCave();\n  SPR.rock=sprRock();")

# ---------- montanhas, rio e utilidades de geração
rep("function genMap(){",r"""function placeMountains(mask,snowy){
  const used=new Uint8Array(N*N),ok=(x,y)=>inb(x,y)&&mask(x,y)&&!used[gi(x,y)]&&!block[gi(x,y)];
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){if(!ok(x,y))continue;
    for(const sz of[4,3,2,1]){if(sz>1&&Math.random()<.25)continue;let fit=true;for(let j=0;j<sz&&fit;j++)for(let i=0;i<sz;i++)if(!ok(x+i,y+j)){fit=false;break}
      if(!fit)continue;for(let j=0;j<sz;j++)for(let i=0;i<sz;i++){used[gi(x+i,y+j)]=1;ground[gi(x+i,y+j)]=T_GRASS2}
      const vars=SPR.mount[sz].filter((v,k)=>snowy||sz<4||k===0);addBox('mount',x,y,sz,sz,pick(vars),{h:sz*20});break}}
}
function paintPath(pts,rad,fn){for(let y=0;y<N;y++)for(let x=0;x<N;x++){let dm=1e9;for(let i=0;i<pts.length-1;i++){const[a,b]=pts[i],[c2,d2]=pts[i+1],vx=c2-a,vy=d2-b,L2=vx*vx+vy*vy;let t=((x+.5-a)*vx+(y+.5-b)*vy)/L2;t=Math.max(0,Math.min(1,t));dm=Math.min(dm,Math.hypot(x+.5-a-vx*t,y+.5-b-vy*t))}fn(x,y,dm)}}
function addWarp(x,y,tiles,to,tx,ty,name){objects.push({kind:'warp',x,y,noSh:true,tiles,to,tx,ty,name})}
function genMap(){""")
# chão base sem lagos aleatórios
rep("    const w=fbm(x*.07+3,y*.07+5,23);\n    if(cheb(x,y)>16){if(w>.64)t=T_WATER;else if(w>.6)t=T_SAND}\n","")
# estradas retas (sem a do oeste)
rep("  [[1,0],[-1,0],[0,1],[0,-1]].forEach(([dx,dy],k)=>{","  [[1,0],[0,1],[0,-1]].forEach(([dx,dy],k)=>{")
rep("if(!inCityTile(Math.round(px),Math.round(py))){const wig=(vnoise(s*.15,k*10,77)-.5)*1.1;if(dx)py+=wig*.5;else px+=wig*.5}","")
# rio (nasce nas montanhas do sudoeste, passa a oeste da vila e beira a estrada do norte) + ponte na porteira oeste
rep("  // paliçada de troncos com 4 porteiras\n",r"""  const RIVER=[[24,76],[28,69],[31.5,62],[32.5,50],[32.6,40],[33.2,33.5],[37,30.2],[41.5,28.8],[44,26],[44.2,12],[44,0]];
  paintPath(RIVER,0,(x,y,dm)=>{const w=1.15+(vnoise(x*.2,y*.2,71)-.5)*.5;if(dm<w)ground[gi(x,y)]=T_WATER;else if(dm<w+.9&&vnoise(x*.3,y*.3,72)>.45&&ground[gi(x,y)]!==T_DIRT)ground[gi(x,y)]=T_SAND});
  for(let y=C-1;y<=C;y++)for(let x=28;x<36;x++)if(ground[gi(x,y)]===T_WATER||ground[gi(x,y)]===T_SAND)ground[gi(x,y)]=T_BRIDGE;
  // paliçada de troncos com 4 porteiras
""")
# montanhas, guardas, barricadas, portal e bosque a leste (antes da vegetação)
rep("  const canPut=(x,y)=>{const t=ground[gi(x,y)];return(t===T_GRASS||t===T_GRASS2)&&!block[gi(x,y)]};\n  for(let y=0;y<N;y++)for(let x=0;x<N;x++){\n    if(!canPut(x,y))continue;\n    const edge=",
r"""  // montanhas: cercam o oeste e fecham o sul (com a passagem da estrada)
  const mj=(x,y)=>Math.round((vnoise(x*.18,y*.18,81)-.5)*4);
  const MT=(x,y)=>{const t=ground[gi(x,y)];if(t===T_WATER||t===T_DIRT||t===T_BRIDGE)return false;const j=mj(x,y);
    if(x<5+j)return true;if(x<40&&y<25+j)return true;if(x<46&&y>71+j)return true;if(y>=84+j&&(x<45||x>50))return true;return false};
  placeMountains(MT,false);
  // passagem do sul: barricada, guarda e entulho do deslizamento
  for(const x of[46,47,49])addObj('barricade',x,C+35,{spr:SPR.barricade});
  for(let y=C+38;y<=C+42;y++)for(let x=45;x<=50;x++)if(!block[gi(x,y)]&&Math.random()<.8)addObj('boulder',x,y,{spr:pick(SPR.boulders)});
  // estrada do norte fechada: barricada, cerca e o soldado
  for(const x of[46,47,49,50])addObj('barricade',x,5,{spr:SPR.barricade});
  for(let x=51;x<=60;x++)if(!block[gi(x,5)])addBox('wall',x,5,1,1,x===60?SPR.stakes.post:SPR.stakes.x[x%3]);
  // portal para o Bosque do Orvalho no fim da estrada do leste
  addWarp(93,48,[[92,47],[92,48],[93,47],[93,48]],'bosque',5,47,'Bosque do Orvalho');
  const canPut=(x,y)=>{const t=ground[gi(x,y)];return(t===T_GRASS||t===T_GRASS2)&&!block[gi(x,y)]};
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!canPut(x,y))continue;
    const treeKind0=()=>{const v=vnoise(x*.09,y*.09,91);return v>.62?'pine':v<.3?'blossom':'oak'};
    if(x>=70&&Math.random()<(x>=74?.5:.25)){addObj('tree',x,y,{spr:pick(SPR.trees[vnoise(x*.2,y*.2,93)>.5?'oak':'pine'])});continue}
    if(y<5&&x>50&&Math.random()<.7){addObj('tree',x,y,{spr:pick(SPR.trees[treeKind0()])});continue}
    if(x<32&&y>24&&y<72){if(Math.random()<.014)addObj('tree',x,y,{spr:pick(SPR.trees[treeKind0()])});else if(Math.random()<.01)addObj('rock',x,y,{spr:SPR.rock});continue}
    const edge=""")
open(p,'w',encoding='utf-8').write(s);print('ok 1')

s=open(p,encoding='utf-8').read()
# entulho fechado de vez e barricada larga no sul
rep("  for(const x of[46,47,49])addObj('barricade',x,C+35,{spr:SPR.barricade});\n  for(let y=C+38;y<=C+42;y++)for(let x=45;x<=50;x++)if(!block[gi(x,y)]&&Math.random()<.8)addObj('boulder',x,y,{spr:pick(SPR.boulders)});",
    "  for(const x of[44,45,46,47,49,50,51])if(!block[gi(x,C+35)])addObj('barricade',x,C+35,{spr:SPR.barricade});\n  for(let y=C+38;y<=C+42;y++)for(let x=44;x<=51;x++)if(!block[gi(x,y)]&&(y<=C+40||Math.random()<.6))addObj('boulder',x,y,{spr:pick(SPR.boulders)});")

# ---------- NPCs: guardas das estradas fechadas
rep("  guard:{hair:","  soldier:{hair:['#1a1418','#2e2628','#4a3e3e'],tunic:'#2a3a6a',tunicD:'#1c2850',armor:'#8a94a8',armorD:'#5a6478',trim:'#c8a040',belt:'#2a1a10',pants:'#2a2a3a',pantsD:'#1c1c2a',boot:'#1a1410',hat:'helm',weapon:1,wtype:'lanca'},\n  guard:{hair:")
rep("    mk('guard','Seu Bento, o Vigia','guard',2,12),\n",
"""    mk('guard','Seu Bento, o Vigia','guard',2,12),
    Object.assign(mk('guard_s','Cabo Rufino','guard',0,35),{warn:'Alto lá! A estrada para as montanhas está fechada: um deslizamento de terra soterrou a passagem.'}),
    Object.assign(mk('guard_n','Sentinela Odo','soldier',0,-43),{warn:'Pare! Esta estrada está fechada por ordem do Rei dos 9 dedos.'}),
""")
rep("""  }else if(n.id==='trainer_m'){""","""  }else if(n.id==='guard_s'){
    dialog(n.name,'Alto lá, forasteiro! A estrada para as montanhas está <b>fechada</b>.<br><br>Choveu três dias seguidos e um <b>deslizamento de terra</b> soterrou a passagem. Ainda tem pedra rolando lá de cima. Ninguém passa até a turma do vilarejo terminar de limpar.',[bye]);
  }else if(n.id==='guard_n'){
    dialog(n.name,'Pare aí. A estrada para o norte está <b>fechada</b>.<br><br>Ordem do <b>Rei dos 9 dedos</b>: ninguém sobe o rio sem salvo-conduto da coroa. E não me pergunte do dedo que falta, se quiser manter os seus.',[bye]);
  }else if(n.id==='trainer_m'){""")
rep("Mais longe ficam as <b>Lebres</b> e os <b>Javalis</b>.","Mais longe ficam as <b>Lebres</b>, e no bosque a leste vivem os <b>Javalis</b>.")

# ---------- spawns: só slime e lebre no mapa inicial
rep("const SPAWNS=[['gelim',26,15,30],['coelho',22,24,46],['cogumelo',20,36,68]];","const SPAWNS=[['gelim',26,15,30],['coelho',26,24,46]];\nconst SPAWNS_BOSQUE=[['coelho',16,8,62],['cogumelo',16,8,62]];")
rep("if(d<r0||d>r1)continue;if(cheb(x,y)<14)continue;","if(d<r0||d>r1)continue;if(curMap==='vila'&&cheb(x,y)<14)continue;if(curMap==='bosque'&&x<10&&Math.abs(y-48)<6)continue;")

# ---------- Bosque do Orvalho
rep("function makeNPCs(){",r"""function genForest(){
  ground.fill(0);block.fill(0);objects.length=0;DOORS.length=0;
  for(let y=0;y<N;y++)for(let x=0;x<N;x++)ground[gi(x,y)]=fbm(x*.11,y*.11,201)>.45?T_GRASS2:T_GRASS;
  // trilha da entrada (oeste) até a caverna (norte)
  paintPath([[0,48],[14,48],[23,43],[30,35],[38,27],[44,19],[48,13.5]],0,(x,y,dm)=>{if(dm<1.05)ground[gi(x,y)]=T_DIRT});
  // laguinho
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){const e=((x-66)/5.5)**2+((y-64)/3.8)**2;if(e<1)ground[gi(x,y)]=T_WATER;else if(e<1.5)ground[gi(x,y)]=T_SAND}
  // cadeia de montanhas no norte, com a boca da caverna
  const cj=(x)=>Math.round((vnoise(x*.15,3,211)-.5)*4);
  objects.push({kind:'cave',x:48.5,y:12.5,spr:SPR.cave,noSh:true});for(const x of[46,47,48,49,50])block[gi(x,12)]=1;
  placeMountains((x,y)=>{if(y>=12&&y<=13&&x>=45&&x<=51)return false;if(ground[gi(x,y)]===T_DIRT&&y>12)return false;return y<12+cj(x)||(y<14&&(x<44||x>52))},true);
  // portal de volta para os Campos do Sabiá
  addWarp(2,48,[[1,47],[1,48],[2,47],[2,48]],'vila',89,47,'Campos do Sabiá');
  const canPut=(x,y)=>{const t=ground[gi(x,y)];return(t===T_GRASS||t===T_GRASS2)&&!block[gi(x,y)]};
  for(let y=0;y<N;y++)for(let x=0;x<N;x++){
    if(!canPut(x,y))continue;
    const kind=()=>{const v=vnoise(x*.1,y*.1,221);return v>.58?'pine':v<.22?'blossom':'oak'};
    const e=Math.min(N-1-x,N-1-y),w=x;
    if(e<4||(w<3&&Math.abs(y-47.5)>2)){if(Math.random()<.9)addObj('tree',x,y,{spr:pick(SPR.trees[kind()])});else addObj('rock',x,y,{spr:SPR.rock});continue}
    if(x<7&&Math.abs(y-47.5)<4)continue;
    const f=fbm(x*.09+5,y*.09+1,231);
    if(Math.random()<(f>.55?.42:.07))addObj('tree',x,y,{spr:pick(SPR.trees[kind()])});
    else if(Math.random()<.03)addObj('bush',x,y,{spr:SPR.bush});
    else if(Math.random()<.012)addObj('rock',x,y,{spr:SPR.rock});
  }
  reach.fill(0);const qu=[[5,48]];reach[gi(5,48)]=1;
  while(qu.length){const[x,y]=qu.pop();for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+dx,ny=y+dy;if(walkable(nx,ny)&&!reach[gi(nx,ny)]){reach[gi(nx,ny)]=1;qu.push([nx,ny])}}}
}
// troca de mapa (a saída de um portal escurece a tela, monta o outro mapa e clareia)
function mapState(){return{snap:snapScene(),gc:groundC,mini:miniBase,reach:reach.slice(),doors:DOORS.slice()}}
function goMap(id,x,y){
  if(scene!=='world')leaveRoom(false);
  Object.assign(MAPS[curMap],{snap:snapScene(),npcs,monsters,items});
  if(!MAPS[id].snap){curMap=id;genForest();buildGround();Object.assign(MAPS[id],mapState(),{npcs:[]})}
  const M=MAPS[id];curMap=id;
  loadScene(M.snap);groundC=M.gc;miniBase=M.mini;reach.set(M.reach);DOORS.length=0;for(const d of M.doors)DOORS.push(d);
  npcs=M.npcs;items=M.items||[];WORLDSNAP=M.snap;worldGC=M.gc;worldNPCs=M.npcs;gOff={x:0,y:0};projs.length=0;
  if(!M.monsters){M.monsters=[];for(const[k,n,r0,r1]of M.spawns)for(let i=0;i<n;i++)M.monsters.push(makeMon(k,r0,r1))}
  monsters=M.monsters;for(const m of monsters)if(m.target===me){m.target=null;m.path=[]}
  clearActs();me.x=x+.5;me.y=y+.5;me.face={flip:x<C,front:true};fadeT=.7;mapBanner={text:M.name,t:0};
  msg(`Você chegou em: ${M.name}.`,'#d8e0f0');
}
function startWarp(w){if(warping||me.dead)return;clearActs();warping={w,t:0};sfx('tele')}
function drawWarp(s){
  const t=TIME;g.save();g.globalCompositeOperation='lighter';
  for(let i=5;i>0;i--){g.globalAlpha=.07*i+.04*Math.sin(t*4+i);g.fillStyle=i>3?'#2a5aff':i>1?'#6ab0ff':'#d8f0ff';g.beginPath();g.ellipse(s.x,s.y,5+i*3.4,(5+i*3.4)*.5,0,0,7);g.fill()}
  const gr=g.createLinearGradient(0,s.y-52,0,s.y);gr.addColorStop(0,'rgba(90,170,255,0)');gr.addColorStop(.7,'rgba(140,210,255,.22)');gr.addColorStop(1,'rgba(200,240,255,.45)');g.globalAlpha=1;g.fillStyle=gr;g.fillRect(s.x-11,s.y-52,22,52);
  g.fillStyle='rgba(255,255,255,.35)';g.fillRect(s.x-2,s.y-48,4,48);
  for(let k=0;k<4;k++){const ph=((t*.9+k/4)%1),y=s.y-2-ph*40,r=(15-ph*7);g.globalAlpha=(1-ph)*.8;g.strokeStyle=k%2?'#ffffff':'#8ad0ff';g.lineWidth=1;g.beginPath();g.ellipse(s.x,y,r,r*.42,0,t*3+k*1.6,t*3+k*1.6+4.4);g.stroke()}
  g.restore();
  if(Math.random()<.7)parts.push({x:s.x+rand(-11,11),y:s.y-rand(0,6),vx:rand(-2,2),vy:-rand(16,34),g:0,life:rand(.6,1.2),max:1.2,col:pick(['#ffffff','#bfe6ff','#6ab0ff']),s:.5});
}
function makeNPCs(){""")

# ---------- portal: desenho, gatilho, minimapa, nome do mapa, aviso dos guardas e da caverna
rep("    }else if(it.k==='obj'){\n","    }else if(it.k==='obj'&&o.kind==='warp'){drawWarp(s);\n    }else if(it.k==='obj'){\n")
rep("      if(o.kind==='bld'&&behind(me,o.box)){","      if((o.kind==='bld'||o.kind==='mount')&&behind(me,o.box)){")
rep("  if(scene==='world'){const d=DOORS.find(d=>d.x===tx&&d.y===ty);if(d)enterRoom(d)}",
    "  if(scene==='world'){const d=DOORS.find(d=>d.x===tx&&d.y===ty);if(d)enterRoom(d);const w=objects.find(o=>o.kind==='warp'&&o.tiles.some(([a,b])=>a===tx&&b===ty));if(w)startWarp(w)}")
rep("  for(const mo of monsters)if(mo.def.boss&&!mo.dead){",
    "  for(const o of objects)if(o.kind==='warp'){const s=iso(o.x,o.y);m.fillStyle='#4aa8ff';m.fillRect(s.x*sx-2,s.y*sy-2,4,4)}\n  for(const mo of monsters)if(mo.def.boss&&!mo.dead){")
rep("`${inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (","`${curMap==='bosque'?MAPS.bosque.name:inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (")
rep("  fadeT=Math.max(0,fadeT-dt);\n",r"""  fadeT=Math.max(0,fadeT-dt);
  if(warping){warping.t+=dt;me.path=[];if(warping.t>.5){const w=warping.w;warping=null;goMap(w.to,w.tx,w.ty)}}
  if(mapBanner&&(mapBanner.t+=dt)>3.6)mapBanner=null;
  if(scene==='world'&&!me.dead){
    for(const n of npcs){if(!n.warn)continue;n.warnT=Math.max(0,(n.warnT||0)-dt);const past=n.id==='guard_s'?me.y>n.y-1.2:me.y<n.y+1.2;
      if(past&&dist(me.x,me.y,n.x,n.y)<3.2&&n.warnT<=0){n.warnT=7;n.say={text:n.warn,t:0};setFace(n,me.x-n.x,me.y-n.y);msg(`${n.name}: ${n.warn}`,'#ffe0a0')}}
    const cave=curMap==='bosque'&&objects.find(o=>o.kind==='cave');
    if(cave&&dist(me.x,me.y,cave.x,cave.y+.5)<1.9&&(TIME-(cave.msgT||-99))>8){cave.msgT=TIME;msg('Um vento frio sai da boca da caverna. Lá dentro está escuro como breu... ainda não dá para entrar.','#c8d8ff')}
  }
""")
rep("  if(fadeT>0){g.globalAlpha=Math.min(1,fadeT/.35);g.fillStyle='#000';g.fillRect(0,0,W,H);g.globalAlpha=1}",
    "  if(fadeT>0){g.globalAlpha=Math.min(1,fadeT/.35);g.fillStyle='#000';g.fillRect(0,0,W,H);g.globalAlpha=1}\n  if(warping){g.globalAlpha=Math.min(1,warping.t/.45);g.fillStyle='#000';g.fillRect(0,0,W,H);g.globalAlpha=1}")
rep("function clickWorld(){\n  if(me.dead)return;","function clickWorld(){\n  if(me.dead||warping)return;")
# nome do mapa grande ao chegar
rep("  for(const f of fx)if(f.type==='label'){","  if(mapBanner){const t=mapBanner.t;og.globalAlpha=t<.6?t/.6:t>2.8?Math.max(0,(3.6-t)/.8):1;otext(mapBanner.text,ov.width/2,ov.height*.2,'#ffe9a8','bold 30px Georgia','#2a1a00');og.globalAlpha=1}\n  for(const f of fx)if(f.type==='label'){")
# volta ao vilarejo (pena de pombo e derrota)
rep("  leaveRoom(false);\n  fx.push({type:'pillar',ent:{x:me.x,y:me.y},t:0,dur:.6,col:'#9ad0ff'});sfx('tele');\n  if(kind==='town'){",
    "  leaveRoom(false);\n  fx.push({type:'pillar',ent:{x:me.x,y:me.y},t:0,dur:.6,col:'#9ad0ff'});sfx('tele');\n  if(kind==='town'&&curMap!=='vila')goMap('vila',C,C+3);\n  if(kind==='town'){")
rep("function revive(){\n  leaveRoom(false);","function revive(){\n  leaveRoom(false);if(curMap!=='vila')goMap('vila',C,C+3);")
# registra os mapas no boot
rep("buildGround();buildRooms();","buildGround();buildRooms();\n  MAPS.vila=Object.assign(mapState(),{name:'Campos do Sabiá',spawns:SPAWNS,npcs});MAPS.bosque={name:'Bosque do Orvalho',spawns:SPAWNS_BOSQUE};")
open(p,'w',encoding='utf-8').write(s);print('ok 2')
