// Exporta todas as folhas de assets do Valhen (PNG + JSON com a posição de cada quadro) e o manifesto que o jogo lê.
// Roda dentro do jogo aberto em modo de geração (index.html?gerar, servido em localhost)
// e envia os arquivos para tools/receber_png.py, que grava em assets/.
// Resolução real: personagens e javali em 4x, o resto em 2x (campo "k" de cada quadro).
// Para gerar de novo (depois de mudar algum desenho no código):
//   1. python3 tools/receber_png.py assets          (recebe os arquivos)
//   2. servir a pasta do jogo e abrir http://localhost:8796/index.html?gerar
//   3. criar um personagem e, no console: (0,eval)(await fetch('tools/exportar_assets.js').then(r=>r.text())); await exportarAssets()
async function exportarAssets(log=console.log){
  const POST=(path,data)=>fetch('http://127.0.0.1:8795/'+path,{method:'POST',body:data}).then(r=>{if(!r.ok)throw new Error(path);return r.text()});
  const b64=s=>'data:,'+btoa(unescape(encodeURIComponent(s)));
  const isCv=v=>v&&typeof v.getContext==='function';
  const vazio=cv=>{const d=cv.getContext('2d').getImageData(0,0,cv.width,cv.height).data;for(let i=3;i<d.length;i+=4)if(d[i])return false;return true};
  const PAD=2;
  // grade: linhas = animações, colunas = quadros
  const grid=rows=>{rows=rows.map(r=>({frames:r.frames.filter(f=>f.cv)})).filter(r=>r.frames.length);const all=rows.flatMap(r=>r.frames);
    const cw=Math.max(...all.map(f=>f.cv.width))+PAD*2,ch=Math.max(...all.map(f=>f.cv.height))+PAD*2,cols=Math.max(...rows.map(r=>r.frames.length));
    const out=document.createElement('canvas');out.width=cols*cw;out.height=rows.length*ch;const q=out.getContext('2d');const quadros={};
    rows.forEach((r,ri)=>r.frames.forEach((f,ci)=>{const x=ci*cw+PAD+Math.floor((cw-2*PAD-f.cv.width)/2),y=ri*ch+PAD+(ch-2*PAD-f.cv.height);q.drawImage(f.cv,x,y);
      quadros[f.name]=Object.assign({x,y,w:f.cv.width,h:f.cv.height,k:f.cv.k||K},f.meta||{})}));
    return{out,quadros,celula:{w:cw,h:ch}}};
  // prateleiras: itens de tamanhos muito diferentes
  const shelf=(items,maxW=2048)=>{const it=items.slice().sort((a,b)=>b.cv.height-a.cv.height);let x=0,y=0,rowH=0,W=0;const pos=[];
    for(const i of it){const w=i.cv.width+PAD*2,h=i.cv.height+PAD*2;if(x+w>maxW&&x>0){x=0;y+=rowH;rowH=0}pos.push([i,x+PAD,y+PAD]);x+=w;rowH=Math.max(rowH,h);W=Math.max(W,x)}
    const out=document.createElement('canvas');out.width=W;out.height=y+rowH;const q=out.getContext('2d');const quadros={};
    for(const[i,x,y2]of pos){q.drawImage(i.cv,x,y2);quadros[i.name]=Object.assign({x,y:y2,w:i.cv.width,h:i.cv.height,k:i.cv.k||K},i.meta||{})}
    return{out,quadros}};
  const salvar=async(nome,res,extra={})=>{await POST(nome+'.png',res.out.toDataURL('image/png'));
    await POST(nome+'.json',b64(JSON.stringify(Object.assign({imagem:nome.split('/').pop()+'.png',largura:res.out.width,altura:res.out.height},extra,res.celula?{celula:res.celula}:{},{quadros:res.quadros}),null,1)));
    log(`${nome}: ${Object.keys(res.quadros).length} quadros`)};
  const man={cenario:[],camadas:[],npcs:'npcs/npcs',monstros:'monstros/monstros',interiores:'mapas/interiores',chao:{}};
  // ---------------- poses do protagonista e dos NPCs
  const POSES=[];for(const d of['f','b'])for(const[st,n]of[['idle',2],['walk',4],['attack',3],['cast',1],['sit',1],['dead',1]])for(let f=0;f<n;f++)POSES.push([d,st,f]);
  const pkey=([d,st,f])=>`${d}_${st}_${f}`;
  const BASE={sex:'m',hs:'m1',hc:2,sk:1},EQ0={armor:'camiseta',legs:'jeans',weapon:null};
  const lk=(A,eq,conj)=>heroLookFrom(Object.assign({},BASE,A),Object.assign({},EQ0,eq),conj);
  const camada=(L,layer,pre='')=>({frames:POSES.map(ps=>{const cv=sprHuman(Object.assign({},L,{layer,id:L.id+'_'+layer}),...ps);return{name:pre+pkey(ps),cv:vazio(cv)?null:cv}})});
  const nota='Camada sem contorno; o jogo empilha capa, pernas, cabelo (trás), tronco, cabelo (meio), cabeça, cabelo (frente) e arma, e contorna o conjunto. Pele "Clara" e cabelo "Castanho" são trocados por paleta.';
  const salvarCamada=async(id,L,layers)=>{const rows=[];for(const ly of layers)rows.push(camada(L,ly,layers.length>1?ly+'_':''));await salvar('personagem/camadas/'+id,grid(rows),{nota});man.camadas.push('personagem/camadas/'+id)};
  await salvarCamada('capa_jaqueta',lk({},{armor:'jaqueta'}),['capeback']);
  for(const[nome,legs]of[['jeans','jeans'],['calca_v','calca_v'],['nenhuma',null]])await salvarCamada('pernas_'+nome,lk({},{legs}),['legs']);
  for(const sex of['m','f'])for(const[nome,armor]of[['camiseta','camiseta'],['roupa','roupa'],['jaqueta','jaqueta'],['cota','cota'],['nenhuma',null]])await salvarCamada(`tronco_${sex}_${nome}`,lk({sex},{armor}),['torso']);
  for(const sex of['m','f'])await salvarCamada('cabeca_'+sex,lk({sex}),['head']);
  for(const hs of[...HAIR_M,...HAIR_F])await salvarCamada('cabelo_'+hs,lk({hs,sex:hs[0]}),['hairA','hairB','hairC']);
  for(const w of Object.keys(ITEMS).filter(k=>ITEMS[k].type==='weapon'))await salvarCamada('arma_'+w,lk({},{weapon:w}),['weapon']);
  for(const el of Object.keys(CONJ).filter(e=>CONJ[e].wt!=='desarmado'))await salvarCamada('arma_cj_'+el,lk({},{},{el}),['weapon']);
  await POST('personagem/paletas.json',b64(JSON.stringify({base:{pele:SKIN_TONES[1],cabelo:HAIR_COLORS[2]},cores_de_cabelo:HAIR_COLORS,tons_de_pele:SKIN_TONES},null,1)));
  // folhas montadas só para visualizar (o jogo não lê estas)
  const NOMES={f:'frente',b:'costas'},EST={idle:'parado',walk:'andando',attack:'ataque',cast:'magia',sit:'sentado',dead:'caido'};
  const montada=L=>{const rows=[];for(const d of['f','b'])for(const st of['idle','walk','attack','cast','sit','dead'])rows.push({frames:POSES.filter(p=>p[0]===d&&p[1]===st).map(ps=>({name:`${NOMES[d]}_${EST[st]}_${ps[2]}`,cv:sprHuman(L,...ps)}))});return grid(rows)};
  for(const sex of['m','f'])for(const[nome,eq]of[['inicial',{}],['viajante',{armor:'jaqueta',legs:'calca_v'}],['cota',{armor:'cota'}]])
    await salvar(`personagem/visualizar/protagonista_${sex==='f'?'feminino':'masculino'}_${nome}`,montada(lk({sex,hs:sex==='f'?'f1':'m1'},eq)));
  for(const sex of['m','f']){const rows=(sex==='f'?HAIR_F:HAIR_M).map(hs=>({frames:['f','b'].map(d=>({name:`${hs}_${NOMES[d]}`,cv:sprHuman(lk({sex,hs}),d,'idle',0),meta:{cabelo:HAIRSTYLES[hs].name}}))}));
    await salvar(`personagem/visualizar/cabelos_${sex==='f'?'femininos':'masculinos'}`,grid(rows))}
  // ---------------- NPCs (prontos, com contorno)
  {const rows=[];for(const n of Object.keys(LOOKS).filter(n=>n!=='hero')){const L=Object.assign(look(n),{id:'exp_npc_'+n});rows.push({frames:[['f',0],['f',1],['b',0],['b',1]].map(([d,f])=>({name:`${n}_${d}_${f}`,cv:sprHuman(L,d,'idle',f)}))})}
    await salvar('npcs/npcs',grid(rows),{nota:'Uma linha por visual de NPC: frente parado 0 e 1, costas 0 e 1.'})}
  // ---------------- monstros
  {const rows=[];for(const k of Object.keys(MON)){const d=MON[k];rows.push({frames:[0,1,2,3].map(f=>({name:`${k}_${f}`,cv:monSprite({def:d,kind:k,stunT:0,anim:f/8+1e-4,moving:true}),meta:{monstro:d.name}}))})}
    await salvar('monstros/monstros',grid(rows),{nota:'Uma linha por monstro, 4 quadros. Olham para a direita; o jogo espelha.'})}
  // ---------------- cenário (cada quadro guarda o caminho dentro de SPR)
  const coletar=(v,path,lista)=>{const nm=path.join('_');if(isCv(v)){lista.push({name:nm,cv:v,meta:{path}});return}
    if(v&&isCv(v.c)){lista.push({name:nm,cv:v.c,meta:{path,ax:v.ax,ay:v.ay,mc:v.mc}});return}
    if(Array.isArray(v))v.forEach((x,i)=>coletar(x,[...path,i],lista));else if(v&&typeof v==='object')for(const k in v)coletar(v[k],[...path,k],lista)};
  const cen=async(nome,keys,maxW,nota)=>{const L=[];for(const k of keys)coletar(SPR[k],[k],L);await salvar('cenario/'+nome,shelf(L,maxW),{nota});man.cenario.push('cenario/'+nome)};
  await cen('objetos',['trees','rock','bush','well','hay','cart','crops','lamp','lampOn','stall','barrel','boulders','barricade','cave','dummy','f','shBig','shMed','shSm','cell','mark'],2048,'Objetos soltos, desenhados com a base no ponto do chão.');
  await cen('construcoes',['bld','counter','fenceA','fenceB','post','stakes'],2048,'Construções isométricas; ax/ay = canto da frente da base dentro da imagem.');
  await cen('montanhas',['mount'],2048,'mount_<tamanho em blocos>_<variação>; ax/ay = canto da frente da base.');
  await cen('icones',['icons'],1024,'Ícones de itens, habilidades e placas.');
  // ---------------- mapas e interiores
  const visao=sc=>{const d=document.createElement('canvas');d.width=Math.round(GW*sc);d.height=Math.round(GH*sc);const q=d.getContext('2d');q.imageSmoothingEnabled=false;q.drawImage(groundC,0,0,d.width,d.height);
    for(const o of objects.slice().sort((a,b)=>(a.x+a.y)-(b.x+b.y))){if(o.kind==='warp'||!o.spr)continue;const k=o.spr.k||K;
      if(o.box){const s0=iso(o.vx,o.vy);q.drawImage(o.spr,(s0.x-o.ax)*sc,(s0.y-o.ay)*sc,o.spr.width/k*sc,o.spr.height/k*sc)}
      else{const s=iso(o.x,o.y),w=o.spr.width/k,h=o.spr.height/k;q.drawImage(o.spr,(s.x-w/2)*sc,(s.y-h+(o.kind==='well'?11:2))*sc,w*sc,h*sc)}}
    for(const n of npcs){const c2=sprHuman(n.look,'f','idle',0),s=iso(n.x,n.y),w=c2.width/c2.k,h=c2.height/c2.k;q.drawImage(c2,(s.x-w/2)*sc,(s.y-h+4)*sc,w*sc,h*sc)}
    return d};
  const mapa=async(id,nome)=>{await POST(`mapas/${nome}_chao.webp`,groundC.toDataURL('image/webp',.92));man.chao[id]=`mapas/${nome}_chao.webp`;
    await POST(`mapas/visualizar/${nome}_completo.png`,visao(.5).toDataURL('image/png'));log(`mapas/${nome}: chão (jogo) e visão completa`)};
  await mapa('vila','campos_do_sabia');
  goMap('bosque',5,47);await mapa('bosque','bosque_do_orvalho');goMap('vila',C,C+3);
  {const L=[];for(const id in ROOMST)L.push({name:id,cv:ROOMST[id].gc.c,meta:{nome:ROOMS[id].name,off:ROOMST[id].gc.off}});await salvar('mapas/interiores',shelf(L,4096),{nota:'Chão e paredes de cada interior; off = deslocamento no mundo.'})}
  await POST('manifesto.json',b64(JSON.stringify(man,null,1)));
  await POST('fim','');log('fim');return man;
}
