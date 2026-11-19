# O jogo passa a CARREGAR os assets prontos (assets/) em vez de desenhar em tempo real:
# - cenário, ícones, NPCs, monstros, chão dos mapas e interiores vêm das folhas PNG/JSON;
# - o protagonista é montado de camadas prontas (capa, pernas, tronco, cabeça, cabelo, arma),
#   com troca de paleta para tom de pele e cor de cabelo;
# - os mapas usam semente fixa, para o chão pronto bater com árvores e montanhas.
# Abrindo com ?gerar (ou direto do disco, file://), o jogo volta a desenhar tudo; é assim que as folhas são exportadas.
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:100]);s=s.replace(a,b)

# sprHuman com camadas
a=s.index("function sprHuman(o,dir,state,f){");b=s.index("function sprTree(kind){")
s=s[:a]+open('tools/_sprHuman_real.js',encoding='utf-8').read()+s[b:]

# visual do herói a partir de parâmetros (usado pelo jogo e pelo exportador)
rep("""function heroLook(){
  const A=Object.assign({},APP_DEF,me.app||{});
  const k='hero_'+A.sex+A.hs+'_'+A.hc+'_'+A.sk+'_'+(me.conj?'cj_'+me.conj.el:me.eq.weapon)+'_'+me.eq.armor+'_'+me.eq.legs;""",
"""function heroLook(){return heroLookFrom(Object.assign({},APP_DEF,me.app||{}),me.eq,me.conj)}
function heroLookFrom(A,eq,conj){
  const k='hero_'+A.sex+A.hs+'_'+A.hc+'_'+A.sk+'_'+(conj?'cj_'+conj.el:eq.weapon)+'_'+eq.armor+'_'+eq.legs;""")
a=s.index("function heroLookFrom(A,eq,conj){");b=s.index("// =====================================================================\n// Pathfinding")
body=s[a:b].replace("me.eq","eq").replace("me.conj","conj")
s=s[:a]+body+s[b:]

# ---------- sistema de assets
rep("function startGame(data){",r"""// =====================================================================
// Assets prontos: o jogo lê as folhas de assets/ em vez de desenhar os sprites
// =====================================================================
const GERAR=/[?&]gerar/.test(location.search)||location.protocol==='file:';
const SEED_VILA=20261119,SEED_BOSQUE=20261120;
const ASSETS={ok:false,layers:{},npc:{},mon:{},ground:{},rooms:{}};
function withSeed(seed,fn){let a=seed>>>0;const r0=Math.random;Math.random=()=>{a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296};try{return fn()}finally{Math.random=r0}}
function loadImg(src){return new Promise((res,rej)=>{const i=new Image();i.onload=()=>res(i);i.onerror=()=>rej(new Error('não carregou '+src));i.src=src})}
async function loadSheet(base){
  const meta=await fetch('assets/'+base+'.json').then(r=>{if(!r.ok)throw new Error('não carregou '+base);return r.json()});
  const img=await loadImg('assets/'+base.replace(/[^/]+$/,'')+meta.imagem),out={};
  for(const n in meta.quadros){const f=meta.quadros[n],c=canvas(f.w,f.h);c.getContext('2d').drawImage(img,f.x,f.y,f.w,f.h,0,0,f.w,f.h);c.k=f.k;out[n]={c,meta:f}}
  return out;
}
function setPath(o,path,v){for(let i=0;i<path.length-1;i++){const k=path[i];if(o[k]==null)o[k]=typeof path[i+1]==='number'?[]:{};o=o[k]}o[path[path.length-1]]=v}
async function loadAssets(){
  const man=await fetch('assets/manifesto.json').then(r=>{if(!r.ok)throw new Error('sem manifesto');return r.json()});
  const sheets=await Promise.all([...man.cenario,...man.camadas,man.npcs,man.monstros,man.interiores].map(loadSheet));
  let i=0;
  for(const base of man.cenario){const sh=sheets[i++];for(const n in sh){const{c,meta}=sh[n];setPath(SPR,meta.path,meta.ax!=null?{c,ax:meta.ax,ay:meta.ay,mc:meta.mc}:c)}}
  for(const base of man.camadas){const sh=sheets[i++],id=base.split('/').pop();ASSETS.layers[id]={};for(const n in sh)ASSETS.layers[id][n]=sh[n].c}
  {const sh=sheets[i++];for(const n in sh)ASSETS.npc[n]=sh[n].c}
  {const sh=sheets[i++];for(const n in sh)ASSETS.mon[n]=sh[n].c}
  {const sh=sheets[i++];for(const n in sh)ASSETS.rooms[n]={c:sh[n].c,off:sh[n].meta.off}}
  const gs=await Promise.all(Object.values(man.chao).map(f=>loadImg('assets/'+f)));Object.keys(man.chao).forEach((k,j)=>ASSETS.ground[k]=gs[j]);
  ASSETS.ok=true;
}
// ---------- protagonista montado de camadas, com troca de paleta (pele e cabelo)
function _hx(a,b,t){const A=hex(a),B=hex(b);return'#'+A.map((v,i)=>Math.max(0,Math.min(255,Math.round(v+(B[i]-v)*t))).toString(16).padStart(2,'0')).join('')}
function _hr(b){return[_hx(b,'#160c24',.6),_hx(b,'#22163a',.4),_hx(b,'#2a2244',.18),_hx(b,'#000000',0),_hx(b,'#fff2d0',.22),_hx(b,'#fffaf0',.46)]}
function skinDerived(s){return[_hx(s,'#6a2e30',.5),_hx(s,'#9a5048',.32),_hx(s,'#c07060',.16),_hx(s,'#000000',0),_hx(s,'#fff4e8',.3),_hx(s,'#ffffff',.5),..._hr(s),_hx(s,'#f08080',.22),_hx(s,'#f08080',.3),_hx(s,'#c05a5a',.45),_hx(s,'#e07070',.4),_hx(s,'#000000',.25)]}
function hairDerived([H0,H1,H2]){return[_hx(H0,'#100818',.45),_hx(H0,'#000000',0),_hx(H0,H1,.5),_hx(H1,'#000000',0),_hx(H1,H2,.55),_hx(H2,'#000000',0)]}
function colorMap(from,to){const m=new Map(),iv=c=>{const a=hex(c);return(a[0]<<16)|(a[1]<<8)|a[2]};from.forEach((f,i)=>{const a=iv(f);if(!m.has(a))m.set(a,iv(to[i]))});return m}
function recolor(cv,map){if(!map)return cv;const c=canvas(cv.width,cv.height);c.k=cv.k;const q=c.getContext('2d');q.drawImage(cv,0,0);const im=q.getImageData(0,0,c.width,c.height),d=im.data;
  for(let i=0;i<d.length;i+=4){if(!d[i+3])continue;const t=map.get((d[i]<<16)|(d[i+1]<<8)|d[i+2]);if(t!==undefined){d[i]=t>>16;d[i+1]=t>>8&255;d[i+2]=t&255}}q.putImageData(im,0,0);return c}
const HERO_BASE={sk:1,hc:2};
function heroComposite(A,eq,conjEl,dir,state,f){
  A=Object.assign({},APP_DEF,A||{});
  const arm=eq.armor||'nenhuma',legs=eq.legs||'nenhuma',wpn=conjEl?(CONJ[conjEl].wt==='desarmado'?null:'cj_'+conjEl):eq.weapon,pose=dir+'_'+state+'_'+f;
  return cached(['hc',A.sex,A.hs,A.hc,A.sk,arm,legs,wpn,pose].join('|'),()=>{
    const L=ASSETS.layers;
    const sm=A.sk===HERO_BASE.sk?null:cached('skm'+A.sk,()=>colorMap(skinDerived(SKIN_TONES[HERO_BASE.sk].c[0]),skinDerived(SKIN_TONES[A.sk].c[0])));
    const hm=A.hc===HERO_BASE.hc?null:cached('hrm'+A.hc,()=>colorMap(hairDerived(HAIR_COLORS[HERO_BASE.hc].c),hairDerived(HAIR_COLORS[A.hc].c)));
    const part=(sheet,name,...maps)=>{const c=L[sheet]&&L[sheet][name];if(!c)return null;let r=c;for(const m of maps)r=recolor(r,m);return r};
    const cape=arm==='jaqueta'?part('capa_jaqueta',pose):null,lg=part('pernas_'+legs,pose,sm),to=part('tronco_'+A.sex+'_'+arm,pose,sm),hd=part('cabeca_'+A.sex,pose,sm,hm),
      hA=part('cabelo_'+A.hs,'hairA_'+pose,sm,hm),hB=part('cabelo_'+A.hs,'hairB_'+pose,sm,hm),hC=part('cabelo_'+A.hs,'hairC_'+pose,sm,hm),w=wpn?part('arma_'+wpn,pose):null;
    const order=dir==='f'?[cape,lg,hA,to,hB,hd,hC,w]:[w,lg,to,hd,hC];
    const base=order.find(x=>x);const c=canvas(base.width,base.height),q=c.getContext('2d');for(const x of order)if(x)q.drawImage(x,0,0);
    const out=outline(c,'#1a1020',2);out.k=KH;return out});
}
function startGame(data){""")

# ---------- uso dos assets
rep("""  const L=heroLook(),dir=me.face.front?'f':'b';
  return cached(`h_${L.id}_${dir}_${state}_${f}`,()=>sprHuman(L,dir,state,f));""",
"""  const dir=me.face.front?'f':'b';
  if(ASSETS.ok)return heroComposite(me.app,me.eq,me.conj&&me.conj.el,dir,state,f);
  const L=heroLook();return cached(`h_${L.id}_${dir}_${state}_${f}`,()=>sprHuman(L,dir,state,f));""")
rep("drawSpr(cached(`n_${o.look.id}_${dir}_${f}`,()=>sprHuman(o.look,dir,'idle',f)),s.x,s.y+3,o.face.flip);",
    "drawSpr((ASSETS.ok&&ASSETS.npc[`${o.look.id}_${dir}_${f}`])||cached(`n_${o.look.id}_${dir}_${f}`,()=>sprHuman(o.look,dir,'idle',f)),s.x,s.y+3,o.face.flip);")
rep("  return cached('m_'+m.kind+fr,()=>{","  if(ASSETS.ok&&ASSETS.mon[m.kind+'_'+fr])return ASSETS.mon[m.kind+'_'+fr];\n  return cached('m_'+m.kind+fr,()=>{")
rep("    const spr=sprHuman(lk,ccDir,'idle',0),cv2=$('ccPrev')",
    "    const spr=ASSETS.ok?heroComposite(app,{armor:'camiseta',legs:'jeans',weapon:null},null,ccDir,'idle',0):sprHuman(lk,ccDir,'idle',0),cv2=$('ccPrev')")
# minimapa separado do chão
rep("  groundC=c;\n  miniBase=canvas(184,96);","  groundC=c;buildMini();\n}\nfunction buildMini(){\n  miniBase=canvas(184,96);")
rep("mq.imageSmoothingEnabled=true;mq.drawImage(c,0,0,c.width,c.height,0,0,184,96);","mq.imageSmoothingEnabled=true;mq.drawImage(groundC,0,0,groundC.width,groundC.height,0,0,184,96);")
rep("    ROOMST[id]=Object.assign(snapScene(),{gc:buildRoomGround(rm),npcs:ns});","    ROOMST[id]=Object.assign(snapScene(),{gc:ASSETS.ok?ASSETS.rooms[id]:buildRoomGround(rm),npcs:ns});")
rep("  if(!MAPS[id].snap){curMap=id;genForest();buildGround();",
    "  if(!MAPS[id].snap){curMap=id;withSeed(SEED_BOSQUE,genForest);if(ASSETS.ok){groundC=ASSETS.ground.bosque;buildMini()}else withSeed(SEED_BOSQUE+1,buildGround);")
rep("""function boot(){
  buildCursors();setCur('arrow');buildSprites();genMap();makeNPCs();buildGround();buildRooms();""",
"""async function boot(){
  buildCursors();setCur('arrow');
  if(!GERAR){try{$('loading').textContent='Carregando assets…';await loadAssets()}catch(e){console.warn('Assets indisponíveis; desenhando no navegador.',e);ASSETS.ok=false}}
  if(!ASSETS.ok)buildSprites();
  withSeed(SEED_VILA,genMap);makeNPCs();
  if(ASSETS.ok){groundC=ASSETS.ground.vila;buildMini()}else withSeed(SEED_VILA+1,buildGround);
  buildRooms();""")
open(p,'w',encoding='utf-8').write(s);print('ok')
