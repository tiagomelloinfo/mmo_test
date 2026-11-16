# Aplica no index.html: interiores, taverna/hospedaria, início isekai sem itens.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,cnt)
def before(a,b):
    global s
    if a not in s: print('NAO ACHOU (before):',a[:100]); return
    s=s.replace(a,b+a,1)

# ---------- itens iniciais (roupas do outro mundo)
rep("  roupa:{name:'Camisa de Algodão'","  camiseta:{name:'Camiseta Estampada',type:'armor',icon:'tshirt',def:1,price:10,desc:'Veio com você do outro mundo. Ninguém aqui entende a estampa. DEF +1'},\n  jeans:{name:'Calça Jeans',type:'legs',icon:'pants',def:1,price:10,desc:'Tecido azul grosso com rebites de metal. Veio com você do outro mundo. DEF +1'},\n  roupa:{name:'Camisa de Algodão'")
rep("return{name,xp:sk,inv:[{id:'pocao_v',n:10},{id:'pocao_a',n:2},{id:'maca',n:5},{id:'asa_mosca',n:3},{id:'asa_borb',n:1}],\n    eq:{weapon:'faca',armor:'roupa'},cards:[],zeny:300,",
    "return{name,xp:sk,inv:[],\n    eq:{weapon:null,armor:'camiseta',legs:'jeans'},cards:[],zeny:0,")
rep("const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,ar=me.eq.armor?ITEMS[me.eq.armor].def:0;",
    "const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,ar=(me.eq.armor?ITEMS[me.eq.armor].def:0)+(me.eq.legs?ITEMS[me.eq.legs].def:0);")
rep("""function heroLook(){
  const k='hero_'+me.eq.weapon;
  return cached('look_'+k,()=>{const w=me.eq.weapon?ITEMS[me.eq.weapon]:null;
    return Object.assign(look('hero',w?{weapon:1,wtype:w.wt,blade:w.blade||'#e6ecf6',bladeD:w.bladeD||'#8a93ad'}:{weapon:0}),{id:k})});
}""","""function heroLook(){
  const k='hero_'+me.eq.weapon+'_'+me.eq.armor+'_'+me.eq.legs;
  return cached('look_'+k,()=>{const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,x={};
    if(me.eq.armor==='camiseta')Object.assign(x,{tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34'});
    else if(me.eq.armor==='cota')Object.assign(x,{armor:'#a8b0c0',armorD:'#707888'});
    else if(!me.eq.armor)Object.assign(x,{tunic:'#f8d0b0',tunicD:'#e0a888',trim:'#f8d0b0'});
    if(me.eq.legs==='jeans')Object.assign(x,{pants:'#3a5a9a',pantsD:'#2a4070',boot:'#f0f0f0'});
    Object.assign(x,w?{weapon:1,wtype:w.wt,blade:w.blade||'#e6ecf6',bladeD:w.bladeD||'#8a93ad'}:{weapon:0});
    return Object.assign(look('hero',x),{id:k})});
}""")
rep("  hero:{spiky:1,hat:'bandana'},","  hero:{spiky:1},\n  barkeep:{hair:['#3a2a1a','#5a3e24','#7a5634'],beard:'#6a4a2a',tunic:'#f0ece0',tunicD:'#c8c0a8',armor:'#8a5a30',armorD:'#6a4220',trim:'#f0ece0',belt:'#3a2a1a',pants:'#4a3a2a',pantsD:'#33281c',boot:'#2a1e14'},\n  innkeep:{hair:['#8a2a1a','#c85a2a','#f09050'],tunic:'#4a7a3a',tunicD:'#33582a',trim:'#f4eedc',belt:'#f4eedc',robe:1,boot:'#3a2a1a',eye:'#2a6a3a'},\n  farmer:{hair:['#5a4a2a','#8a6a3a','#b08a50'],tunic:'#8a6a3a',tunicD:'#6a4e2a',trim:'#c8a060',pants:'#5a6a8a',pantsD:'#3e4a66',hat:'wide'},\n  patron2:{hair:['#606068','#9a9aa4','#d0d0d8'],tunic:'#8a3a5a',tunicD:'#6a2a44',robe:1,trim:'#f0d070',belt:'#5a3a20',boot:'#3a2a1a'},")
rep("if(it.type==='weapon'||it.type==='armor'){equip(id);return}","if(it.type==='weapon'||it.type==='armor'||it.type==='legs'){equip(id);return}")
rep("for(const[s,lb]of[['weapon','Arma'],['armor','Armadura']]){","for(const[s,lb]of[['weapon','Arma'],['armor','Roupa'],['legs','Calças']]){")
rep("`data-tip=\"${s==='weapon'?'Sem arma: treina Desarmado':'Sem armadura'}\"`","`data-tip=\"${s==='weapon'?'Sem arma: treina Desarmado':'Vazio'}\"`")
rep("(invTab==='equip'&&(it.type==='weapon'||it.type==='armor'))","(invTab==='equip'&&(it.type==='weapon'||it.type==='armor'||it.type==='legs'))")
rep("it.type==='weapon'||it.type==='armor'?'equipar':'usar'","it.type==='weapon'||it.type==='armor'||it.type==='legs'?'equipar':'usar'")
# ícones novos
rep("    case'shirt':","    case'tshirt':p(2,2,8,9,'#f2f2f4');p(0,2,2,3,'#f2f2f4');p(10,2,2,3,'#f2f2f4');p(8,2,2,9,'#c4c8d2');p(4,2,4,1,'#9aa0b0');p(4,5,4,3,'#3a6ac8');p(5,6,2,1,'#ffd040');break;\n    case'pants':p(2,1,8,2,'#3a5a9a');p(2,3,3,8,'#3a5a9a');p(7,3,3,8,'#2a4070');p(2,1,8,1,'#2a3a6a');p(5,1,1,1,'#d8b040');p(3,4,1,3,'#5a7ab8');break;\n    case'sign_tavern':p(2,3,6,7,'#c08a40');p(2,3,6,1,'#fff8e8');p(2,2,6,1,'#ffffff');p(8,4,2,1,'#8a5a20');p(9,4,1,4,'#8a5a20');p(8,7,2,1,'#8a5a20');p(3,5,1,4,'#e8b860');p(2,9,6,1,'#7a4a20');break;\n    case'sign_inn':p(1,6,10,3,'#8e6034');p(1,4,2,6,'#6b4426');p(9,6,2,4,'#6b4426');p(3,5,7,2,'#c83434');p(2,4,3,2,'#ffffff');p(2,9,1,2,'#4a2e18');p(10,9,1,2,'#4a2e18');p(7,1,1,1,'#e0e8ff');p(9,0,1,1,'#e0e8ff');p(8,2,1,1,'#e0e8ff');break;\n    case'shirt':")
rep("['buff_bless','buff_agi','sign_guild','sign_magic']","['buff_bless','buff_agi','sign_guild','sign_magic','sign_tavern','sign_inn']")

# ---------- ranks: o taverneiro só repassa missões E e D
rep("const RANKS=[['F',0],['E',3],['D',7],['C',14]];","const RANKS=[['E',0],['D',4],['C',12]];")
for q in ['g_gelim','g_geleia']: pass
s=s.replace("rank:1,pts:2,desc:'As Lebres","rank:0,pts:2,desc:'As Lebres").replace("rank:1,pts:1,rep:true,desc:'A tecelã","rank:0,pts:1,rep:true,desc:'A tecelã")
s=s.replace("rank:2,pts:3,desc:'Os Chapéus","rank:1,pts:3,desc:'Os Chapéus").replace("rank:2,pts:1,rep:true,desc:'O herbalista","rank:1,pts:1,rep:true,desc:'O herbalista").replace("rank:2,pts:4,desc:'O posto da guilda quer","rank:1,pts:4,desc:'A guilda quer")
rep("<span>Guilda dos Aventureiros</span><span class=\"x\" data-close=\"winGuild\">","<span>Quadro de Missões · Taverna do Caneco</span><span class=\"x\" data-close=\"winGuild\">")
rep("'entregue na guilda'","'entregar na taverna'")
rep("'Sem missões. Visite a <b>Guilda dos Aventureiros</b>.'","'Sem missões. Fale com o <b>Gaspar</b> na <b>Taverna do Caneco</b>.'")
rep("Pegue e entregue missões na <b>Guilda dos Aventureiros</b> para ganhar cobres, itens e subir de rank.","Pegue e entregue missões com o taverneiro na <b>Taverna do Caneco</b>, que responde pela Guilda dos Aventureiros: ganhe cobres, itens e suba de rank.<br>Entre nas casas clicando nelas ou andando até a porta.")
rep("if(n.id==='guild')mark=","if(n.id==='tavern')mark=")

# ---------- prédios: taverna, venda e hospedaria
rep("{id:'guild',name:'Posto da Guilda',bx:2,by:-9,spec:{fw:4,fh:3,wh:24,rh:20,roof:'gable',rr:R.straw,wall:'timber',door:'L',doorAt:1.5,sign:'sign_guild'}},",
    "{id:'tavern',name:'Taverna do Caneco',room:'tavern',bx:2,by:-9,spec:{fw:4,fh:3,wh:24,rh:20,roof:'gable',rr:R.straw,wall:'timber',door:'L',doorAt:1.5,sign:'sign_tavern'}},")
rep("{id:'school',name:'Galpão de Treino',","{id:'school',name:'Galpão de Treino',room:'school',")
rep("{id:'tower',name:'Cabana da Sábia',","{id:'tower',name:'Cabana da Sábia',room:'tower',")
rep("{id:'h1',bx:6,by:-9,spec:{fw:3,fh:3,wh:20,rh:16,roof:'gable',rr:R.straw,wall:'timber',door:'L',doorAt:1.5}},",
    "{id:'shop',name:'Venda do Tomas',room:'shop',bx:6,by:-9,spec:{fw:3,fh:3,wh:20,rh:16,roof:'gable',rr:R.red,wall:'timber',door:'L',doorAt:1.5,sign:'potion_r'}},")
rep("{id:'h2',bx:5,by:3,spec:{fw:3,fh:3,wh:20,rh:16,roof:'gable',rr:R.brown,wall:'plaster',wc:'#efe2c8',door:'L',doorAt:1.5}},",
    "{id:'inn',name:'Hospedaria do Sabiá',room:'inn',bx:4,by:3,spec:{fw:4,fh:3,wh:22,rh:18,roof:'gable',rr:R.brown,wall:'plaster',wc:'#efe2c8',door:'L',doorAt:1.5,sign:'sign_inn'}},")
# portas: o quadro da porta fica livre e leva para dentro
rep("  for(const b of BUILDINGS)addBox('bld',C+b.bx,C+b.by,b.spec.fw,b.spec.fh,SPR.bld[b.id],{name:b.name});\n  // hortas",
    "  DOORS.length=0;\n  for(const b of BUILDINGS){const o=addBox('bld',C+b.bx,C+b.by,b.spec.fw,b.spec.fh,SPR.bld[b.id],{name:b.name});\n    if(b.room){const sp=b.spec,L=sp.door==='L',x=L?C+b.bx+Math.floor(sp.doorAt):C+b.bx+sp.fw-1,y=L?C+b.by+sp.fh-1:C+b.by+Math.floor(sp.doorAt);\n      const d={x,y,ox:L?x:x+1,oy:L?y+1:y,room:b.room,name:b.name};block[gi(x,y)]=0;DOORS.push(d);o.door=d}}\n  // hortas")
rep("  addObj('dummy',C-7,C-4,{spr:SPR.dummy});addObj('dummy',C-5,C-4,{spr:SPR.dummy});\n","")
rep("const objects=[];","const objects=[],DOORS=[];")
# poço não espirra água
rep("  const fs=iso(C,C);if(Math.random()<.9)parts.push({x:fs.x+rand(-1,1),y:fs.y-31,vx:rand(-14,14),vy:-rand(20,34),g:70,life:.8,max:.8,col:pick(['#cfe8ff','#9ccaf0','#ffffff']),s:1});\n","")

# ---------- NPCs do lado de fora
a=s.index("  npcs=[\n    mk('healer'");b=s.index("  ];",a)+4
s=s[:a]+"""  npcs=[
    mk('healer','Irmã Liesel','priest',-5,3),
    mk('guard','Seu Bento, o Vigia','guard',2,10),
  ];"""+s[b:]

# ---------- terreno vazio e piso
rep("const T_GRASS=0,T_GRASS2=1,T_DIRT=2,T_SAND=3,T_WATER=4,T_STONE=5;","const T_GRASS=0,T_GRASS2=1,T_DIRT=2,T_SAND=3,T_WATER=4,T_STONE=5,T_VOID=6,T_FLOOR=7;")
rep("const walkable=(x,y)=>inb(x,y)&&ground[gi(x,y)]!==T_WATER&&!block[gi(x,y)];","const walkable=(x,y)=>inb(x,y)&&ground[gi(x,y)]!==T_WATER&&ground[gi(x,y)]!==T_VOID&&!block[gi(x,y)];")

# ---------- sprites de mobília
before("function sprDummy(){","""// mobília dos interiores
function sprShelf(kind){
  const c=canvas(22,32),q=c.getContext('2d'),p=P(q);
  p(1,0,20,31,'#5e3c20');p(2,1,18,29,'#3e2614');p(1,0,20,2,'#8e6034');
  for(let r=0;r<3;r++){const y=9+r*10;p(2,y,18,2,'#8e6034');
    for(let i=0;i<5;i++){const x=3+i*3.5;
      if(kind==='books'){const col=['#a83030','#2f62c8','#3a8a3a','#c08a30','#6a3a9a'][(i+r*2)%5];p(x,y-7+(i%2),3,7-(i%2),col);p(x,y-6+(i%2),1,5,'rgba(255,255,255,.25)')}
      else if(kind==='jars'){p(x,y-5,3,5,['#d8c8a0','#c0a070','#e8e0c8'][(i+r)%3]);p(x,y-6,3,1,'#8a6a3a')}
      else{const col=[R.red[1],R.blue[1],R.orange[1],R.green[1]][(i+r)%4];p(x+.5,y-6,2,1,'#dfe8f0');p(x,y-5,3,5,col);p(x,y-4,1,2,'#fff')}}}
  return outline(c);
}
function sprRack(){
  const c=canvas(22,30),q=c.getContext('2d'),p=P(q);
  p(1,6,20,2,'#6b4426');p(1,22,20,2,'#6b4426');p(1,4,2,26,'#5e3c20');p(19,4,2,26,'#5e3c20');
  line(p,5,3,5,27,'#dfe6f2');line(p,6,3,6,27,'#8a93ad');p(4,20,4,2,'#e0b040');
  line(p,10,1,10,28,'#8e6034');p(9,0,3,4,'#e6ecf6');
  line(p,15,8,15,28,'#6b4426');p(13,6,5,4,'#a8b0c0');p(13,6,4,3,'#e6ecf6');
  return outline(c);
}
function sprBed(){
  const c=canvas(30,22),q=c.getContext('2d'),p=P(q);
  p(1,4,4,16,'#6b4426');p(25,9,4,11,'#6b4426');p(4,10,22,8,'#8e6034');
  p(4,8,22,6,'#c83434');p(4,8,22,1,'#e85a4e');p(5,6,7,4,'#f4f4f0');p(5,6,7,1,'#ffffff');p(12,12,14,2,'#962020');
  p(2,19,2,3,'#4a2e18');p(26,19,2,3,'#4a2e18');
  return outline(c);
}
function sprFire(){
  const c=canvas(28,38),q=c.getContext('2d'),p=P(q);
  for(let y=0;y<36;y+=4)for(let x=0;x<28;x+=7){const o=(y/4)%2?3:0;p(x+o,y,6,3,['#86827e','#96928c','#a8a49c'][(x+y)%3])}
  p(0,0,28,3,'#6a645e');p(6,16,16,20,'#1a1210');p(7,15,14,1,'#1a1210');
  blob(q,14,30,6,5,R.orange);blob(q,14,32,4,3,['#ffd890','#fff4b8','#fff4b8','#ffffff']);p(10,34,8,2,'#5e3c20');
  return outline(c,'#1e1c22');
}
function sprTable(){
  const c=canvas(26,18),q=c.getContext('2d'),p=P(q);
  blob(q,13,6,12,4.5,R.brown);p(12,10,3,7,'#5e3c20');p(8,16,11,2,'#4a2e18');
  p(6,1,4,4,'#c08a40');p(6,1,4,1,'#ffffff');p(10,2,1,2,'#8a5a20');p(16,3,5,2,'#e8e0c8');
  return outline(c);
}
function sprStool(){const c=canvas(12,11),q=c.getContext('2d'),p=P(q);blob(q,6,3,5,2.4,R.brown);p(2,4,2,7,'#5e3c20');p(8,4,2,7,'#5e3c20');return outline(c)}
function sprCrate(){const c=canvas(14,14),q=c.getContext('2d'),p=P(q);p(0,0,14,14,'#a07444');p(0,0,14,2,'#c08a50');p(0,6,14,1,'#7e5530');p(0,12,14,2,'#7e5530');line(p,1,2,12,12,'#7e5530');p(0,0,1,14,'#7e5530');p(13,0,1,14,'#7e5530');return outline(c)}
function sprCauldron(){
  const c=canvas(22,22),q=c.getContext('2d'),p=P(q);
  p(4,18,3,4,'#2a2a30');p(15,18,3,4,'#2a2a30');p(7,19,8,3,'#ff8a3a');p(9,20,4,2,'#ffe080');
  blob(q,11,12,10,7,['#18181e','#2a2a34','#3a3a48','#5a5a6a']);blob(q,11,7,8,2.4,['#2a8a3a','#4ac85a','#8af08a','#d8ffd0']);p(4,6,15,1,'#5a5a6a');
  return outline(c);
}
function sprBoard(){
  const c=canvas(24,30),q=c.getContext('2d'),p=P(q);
  p(2,10,2,20,'#5e3c20');p(20,10,2,20,'#5e3c20');p(0,0,24,18,'#6b4426');p(2,2,20,14,'#c8a070');
  for(const[x,y,w,h]of[[4,3,6,6],[12,4,7,5],[5,10,7,5],[14,10,5,5]]){p(x,y,w,h,'#f4ecd8');p(x+1,y+2,w-2,1,'#8a7a5a');p(x+1,y+4,w-3,1,'#8a7a5a');p(x+w/2,y,1,1,'#c83434')}
  return outline(c);
}
function sprCandle(){const c=canvas(8,14),q=c.getContext('2d'),p=P(q);p(1,11,6,2,'#c8a040');p(3,5,2,6,'#f4eedc');p(3,2,2,3,'#ffd060');p(3,1,1,1,'#fff4b8');return outline(c)}
""")
rep("  SPR.dummy=sprDummy();","  SPR.dummy=sprDummy();\n  SPR.f={shelfP:sprShelf('potions'),books:sprShelf('books'),shelfJ:sprShelf('jars'),rack:sprRack(),bed:sprBed(),fire:sprFire(),table:sprTable(),stool:sprStool(),crate:sprCrate(),cauldron:sprCauldron(),board:sprBoard(),candle:sprCandle(),barrel:SPR.barrel,hay:SPR.hay,dummy:SPR.dummy};\n  SPR.counter={};for(const n of[3,4])SPR.counter[n]=sprBuilding({fw:n,fh:1,wh:14,roof:'flat',rr:R.brown,wall:'log',win:false});")

# ---------- interiores
before("function dialog(name,text,buttons){","""// =====================================================================
// Interiores (cada sala é uma cena própria, montada no mesmo grid)
// =====================================================================
const ROOMS={
  shop:{name:'Venda do Tomas',w:9,h:7,exit:[4,6],floor:'wood',wall:'#e8dcc0',winR:[6.5],winL:[4.5],rug:[3,4,5,5],rugCol:['#4a1414','#a83030','#c84a3a','#e8c060'],
    furn:[['shelfP',1,0],['shelfP',2,0],['shelfJ',3,0],['rack',6,0],['rack',7,0],['crate',8,0],['barrel',0,1],['barrel',0,2],['shelfJ',0,4],['counter',2,2,4],['crate',8,2],['barrel',8,3]],
    npcs:[['merchant','Tomas, o Vendeiro','merchant',4,1]]},
  school:{name:'Galpão de Treino',w:9,h:7,exit:[4,6],floor:'dirt',style:'log',winR:[4.5],winL:[],
    furn:[['rack',1,0],['rack',2,0],['rack',3,0],['hay',7,0],['hay',8,1],['barrel',0,1],['dummy',2,3],['dummy',6,3],['crate',0,4]],
    npcs:[['trainer_f','Mestre Brann','master',5,1]]},
  tower:{name:'Cabana da Sábia',w:7,h:7,exit:[3,6],floor:'dark',style:'stone',wall:'#b8b0c8',winR:[5.5],winL:[4.5],rug:[2,3,4,4],rugCol:['#1a0e30','#5a3a9a','#7a5ac0','#e8c060'],
    furn:[['books',1,0],['books',2,0],['books',0,1],['books',0,2],['cauldron',5,2],['table',1,4],['candle',4,0],['crate',6,0]],
    npcs:[['trainer_m','Sábia Yselda','mage',3,1]]},
  inn:{name:'Hospedaria do Sabiá',w:9,h:7,exit:[4,6],floor:'wood',wall:'#efe2c8',winR:[5.5,7.5],winL:[5.5],rug:[5,3,7,4],rugCol:['#14381a','#3a7a3a','#4f9a42','#e8c060'],
    furn:[['counter',1,2,3],['shelfJ',1,0],['barrel',0,0],['bed',5,0],['bed',7,0],['bed',8,2],['fire',0,4],['table',6,4],['stool',7,4],['candle',3,0]],
    npcs:[['inn','Dona Marta','innkeep',2,1]]},
  tavern:{name:'Taverna do Caneco',w:10,h:8,exit:[5,7],floor:'wood',wall:'#e8d8b8',winR:[7.5],winL:[5.5],rug:[6,5,8,6],rugCol:['#3a1a0a','#8a4a1a','#a85a24','#e8c060'],
    furn:[['counter',1,2,4],['barrel',0,0],['barrel',1,0],['shelfJ',3,0],['shelfP',4,0],['board',6,0],['fire',0,5],['table',7,3],['table',3,5],['stool',4,5],['table',8,6],['stool',9,6],['barrel',9,0]],
    npcs:[['tavern','Gaspar, o Taverneiro','barkeep',2,1],['patron','Zeca, o Lavrador','farmer',8,3,true],['patron','Dona Cida','patron2',2,5]]},
};
const PATRON_LINES={
  'Zeca, o Lavrador':['As lebres comeram metade da minha horta de novo...','Dizem que um lodo do tamanho de uma carroça vive pra lá do rio.','Mais uma, Gaspar! Essa é por conta do forasteiro!'],
  'Dona Cida':['Você não é daqui, né? Tem cara de quem caiu do céu.','Já é o terceiro forasteiro de roupa esquisita este ano.','O Gaspar paga bem pelos serviços da guilda. Aproveite.'],
};
const FLOORS={wood:['#4e321c','#6e4a2a','#805a34','#946a40'],dark:['#2e2016','#4c3424','#5a3e2c','#6a4a34'],dirt:['#5e4630','#7e623e','#8e7048','#a08052'],stone:['#5a5654','#807c78','#96928c','#aaa69e']};
let scene='world',sceneDoor=null,WORLDSNAP=null,worldGC=null,worldNPCs=null,worldMons=[],worldItems=[],gOff={x:0,y:0},fadeT=0;
const ROOMST={};
function snapScene(){return{ground:ground.slice(),block:block.slice(),objects:objects.slice()}}
function loadScene(st){ground.set(st.ground);block.set(st.block);objects.length=0;for(const o of st.objects)objects.push(o)}
function buildRoomGround(rm){
  const x0=rm.x0,y0=rm.y0,w=rm.w,h=rm.h,x1=x0+w,y1=y0+h,WH=46;
  const L=iso(x0,y1),Rt=iso(x1,y0),T=iso(x0,y0),B=iso(x1,y1);
  const ox=Math.floor(L.x)-4,oy=Math.floor(T.y)-WH-6,cw=Math.ceil(Rt.x)+4-ox,ch=Math.ceil(B.y)+10-oy;
  const c=canvas(cw,ch),q=c.getContext('2d'),img=q.createImageData(cw,ch),d=img.data;
  const put=(x,y,col)=>{x=Math.round(x);y=Math.round(y);if(x<0||y<0||x>=cw||y>=ch)return;const i=(y*cw+x)*4;d[i]=col[0];d[i+1]=col[1];d[i+2]=col[2];d[i+3]=255};
  const mul=(col,f)=>[Math.min(255,col[0]*f)|0,Math.min(255,col[1]*f)|0,Math.min(255,col[2]*f)|0];
  const F=FLOORS[rm.floor].map(hex),RG=rm.rug?rm.rugCol.map(hex):null,MAT=[hex('#8a6a3a'),hex('#b08a4a')];
  for(let py=0;py<ch;py++)for(let px=0;px<cw;px++){
    const t=unIso(px+ox+.5,py+oy+.5);if(t.x<x0||t.y<y0||t.x>=x1||t.y>=y1)continue;
    const lx=t.x-x0,ly=t.y-y0;let col;
    const r=rm.rug;
    if(r&&lx>=r[0]+.15&&ly>=r[1]+.15&&lx<=r[2]+.85&&ly<=r[3]+.85){const e=Math.min(lx-r[0]-.15,ly-r[1]-.15,r[2]+.85-lx,r[3]+.85-ly);col=e<.06?RG[0]:e<.16?RG[3]:((Math.floor(lx*3)+Math.floor(ly*3))%2?RG[1]:RG[2])}
    else if(Math.floor(lx)===rm.exit[0]&&Math.floor(ly)===rm.exit[1]){const fx=lx%1,fy=ly%1;col=(fx<.12||fx>.88||fy<.12||fy>.88)?F[0]:MAT[Math.floor(fy*6)%2]}
    else if(rm.floor==='stone'){const ux=lx*2,uy=ly*2,u=ux%1,v=uy%1;col=(u<.07||v<.07)?F[0]:F[1+Math.floor(hash2(Math.floor(ux),Math.floor(uy),3)*2.99)]}
    else if(rm.floor==='dirt'){col=F[clamp(Math.round(fbm(px*.08,py*.16,3)*3.4+bay(px,py)),0,3)]}
    else{const v=ly*3,row=Math.floor(v),fr=v-row,off=hash2(row,0,5)*1.5,j=(lx+off)%1.5;col=(fr<.13||j<.05)?F[0]:F[1+Math.floor(hash2(Math.floor((lx+off)/1.5),row,7)*2.99)]}
    put(px,py,col);
  }
  const WALL=hex(rm.wall||'#e8dcc0'),BEAM=hex('#5a3a20'),WAIN=hex('#6e4a2a'),WAIND=hex('#4a2e18'),GL=hex('#a8d8f0'),GLL=hex('#e0f4ff'),FR=hex('#3a2414'),LOG=R.log.map(hex),ST=hex('#a49e94'),MORT=hex('#6a645e');
  const wallAt=(u,hh,wins)=>{
    if(hh>WH-3)return BEAM;
    for(const wu of wins){const du=Math.abs(u-wu);if(du<.32&&hh>=20&&hh<=36){if(du>.25||hh<21||hh>35)return FR;return hh>31&&u<wu?GLL:GL}}
    if(rm.style==='log'){const row=Math.floor(hh/5),f=hh%5;return mul(LOG[f<1?0:f<3?2:1],.9+hash2(row,Math.floor(u*2),5)*.2)}
    if(rm.style==='stone'){const row=Math.floor(hh/5),off=(row%2)*.3,U=u*16;if(hh%5<1||(U/10+off)%1<.08)return MORT;return mul(ST,.85+hash2(Math.floor(U/10+off),row,7)*.25)}
    if(hh<12)return hh>10?WAIND:mul(WAIN,Math.floor(u*8)%2?1:.88);
    if(u%1<.06)return BEAM;
    return mul(WALL,.96+hash2(u*16|0,hh,3)*.06);
  };
  for(let sx=Math.floor(T.x);sx<=Math.ceil(Rt.x);sx++){const k=(sx-T.x)/(Rt.x-T.x);if(k<0||k>1)continue;const base=T.y+k*(Rt.y-T.y);for(let hh=0;hh<=WH;hh++)put(sx-ox,base-hh-oy,wallAt(k*w,hh,rm.winR||[]))}
  for(let sx=Math.floor(L.x);sx<=Math.ceil(T.x);sx++){const k=(T.x-sx)/(T.x-L.x);if(k<0||k>1)continue;const base=T.y+k*(L.y-T.y);for(let hh=0;hh<=WH;hh++)put(sx-ox,base-hh-oy,mul(wallAt(k*h,hh,rm.winL||[]),.8))}
  const edge=(A,Bp)=>{for(let sx=Math.floor(A.x);sx<=Math.ceil(Bp.x);sx++){const k=(sx-A.x)/(Bp.x-A.x);if(k<0||k>1)continue;const base=A.y+k*(Bp.y-A.y);for(let j=1;j<=5;j++)put(sx-ox,base+j-oy,j<2?F[0]:j<4?[58,38,22]:[34,24,16])}};
  edge(L,B);edge(B,Rt);
  q.putImageData(img,0,0);
  return{c,off:{x:ox,y:oy}};
}
function buildRooms(){
  WORLDSNAP=snapScene();worldGC=groundC;worldNPCs=npcs;
  for(const id in ROOMS){
    const rm=ROOMS[id];rm.x0=C-Math.floor(rm.w/2);rm.y0=C-Math.floor(rm.h/2);
    ground.fill(T_VOID);block.fill(0);objects.length=0;
    for(let y=0;y<rm.h;y++)for(let x=0;x<rm.w;x++)ground[gi(rm.x0+x,rm.y0+y)]=T_FLOOR;
    for(const[k,x,y,n]of rm.furn){const ax=rm.x0+x,ay=rm.y0+y;
      if(k==='counter'){addBox('furn',ax,ay,n,1,SPR.counter[n]);continue}
      const o=addObj(k,ax,ay,{spr:SPR.f[k]});
      if(['shelfP','books','shelfJ','rack','board','fire','bed'].includes(k))o.noSh=true;
      if(k==='fire')o.glow={col:'#ffb040',y:8,r:18};if(k==='candle')o.glow={col:'#ffe08a',y:12,r:9};if(k==='cauldron')o.glow={col:'#7af07a',y:14,r:12}}
    const ns=rm.npcs.map(([nid,name,lk,x,y,flip])=>{const n={id:nid,name,look:Object.assign(look(lk),{id:lk}),x:rm.x0+x+.5,y:rm.y0+y+.5,face:{flip:!!flip,front:true},anim:Math.random()*3,talkT:rand(6,14)};block[gi(rm.x0+x,rm.y0+y)]=1;return n});
    rm.ex=rm.x0+rm.exit[0];rm.ey=rm.y0+rm.exit[1];
    ROOMST[id]=Object.assign(snapScene(),{gc:buildRoomGround(rm),npcs:ns});
  }
  loadScene(WORLDSNAP);
}
function clearActs(){me.path=[];me.target=null;me.npc=null;me.pick=null;me.queued=null;me.sit=false;me.cast=null;pendingSkill=null;marker=null}
function enterRoom(d){
  const rm=ROOMS[d.room],st=ROOMST[d.room];
  scene=d.room;sceneDoor=d;loadScene(st);groundC=st.gc.c;gOff=st.gc.off;npcs=st.npcs;
  worldMons=monsters;monsters=[];worldItems=items;items=[];projs.length=0;
  for(const m of worldMons)if(m.target===me){m.target=null;m.path=[]}
  clearActs();me.x=rm.ex+.5;me.y=rm.ey-.5;me.face={flip:false,front:false};fadeT=.35;sfx('door');
  msg(`Você entrou em: ${rm.name}.`,'#d8e0f0');
}
function leaveRoom(place=true){
  if(scene==='world')return;const d=sceneDoor;
  scene='world';sceneDoor=null;loadScene(WORLDSNAP);groundC=worldGC;gOff={x:0,y:0};npcs=worldNPCs;monsters=worldMons;items=worldItems;projs.length=0;
  clearActs();if(place){me.x=d.ox+.5;me.y=d.oy+.5;me.face={flip:false,front:true}}fadeT=.35;sfx('door');
}
function doorCheck(){
  const tx=Math.floor(me.x),ty=Math.floor(me.y);
  if(scene==='world'){const d=DOORS.find(d=>d.x===tx&&d.y===ty);if(d)enterRoom(d)}
  else{const rm=ROOMS[scene];if(tx===rm.ex&&ty===rm.ey)leaveRoom()}
}
// casa sob o cursor (pelo pixel do sprite), para clicar e entrar
function bldAt(mx,my){
  if(scene!=='world')return null;let best=null,bd=-1e9;
  for(const o of objects){if(o.kind!=='bld'||!o.door)continue;
    const s0=iso(o.vx,o.vy),x=Math.round(mx-(s0.x-CAM.x-o.ax)),y=Math.round(my-(s0.y-CAM.y-o.ay));
    if(x<0||y<0||x>=o.spr.width||y>=o.spr.height)continue;
    if(!o.alpha)o.alpha=o.spr.getContext('2d').getImageData(0,0,o.spr.width,o.spr.height).data;
    if(o.alpha[(y*o.spr.width+x)*4+3]<100)continue;
    const dd=o.vx+o.vy;if(dd>bd){bd=dd;best=o}}
  return best;
}
""")
# som de porta
rep("    case'click':tone(700,.03,'square',.02);break;","    case'click':tone(700,.03,'square',.02);break;\n    case'door':tone(180,.08,'triangle',.05,60);tone(120,.12,'triangle',.04,-30,.07);break;")

# ---------- laço: cenas
rep("  const moved=stepMove(me,dt);if(me.moving){","  const moved=stepMove(me,dt);if(moved>0||!me.path.length)doorCheck();if(me.moving){")
rep("  updHero(dt);\n  for(const m of monsters)updMon(m,dt);","  updHero(dt);\n  if(scene==='world')for(const m of monsters)updMon(m,dt);\n  fadeT=Math.max(0,fadeT-dt);")
rep("  for(const n of npcs){n.anim+=dt;if(n.say&&(n.say.t+=dt)>4)n.say=null}",
    "  for(const n of npcs){n.anim+=dt;if(n.say&&(n.say.t+=dt)>4)n.say=null;if(n.id==='patron'&&(n.talkT-=dt)<=0){n.talkT=rand(9,18);n.say={text:pick(PATRON_LINES[n.name]),t:0}}}")
rep("  mouse.over=(!mouse.overUI&&started)?pickAt(mouse.x,mouse.y):null;updCursor();",
    "  mouse.over=(!mouse.overUI&&started)?pickAt(mouse.x,mouse.y):null;mouse.bld=(!mouse.overUI&&started&&!mouse.over)?bldAt(mouse.x,mouse.y):null;updCursor();")
rep("  const t=mouseTile();if(t){me.target=null;me.npc=null;me.pick=null;me.queued=null;moveTo(t.x,t.y,true)}\n}",
    "  const b=bldAt(mouse.x,mouse.y);if(b){me.target=null;me.npc=null;me.pick=null;me.queued=null;moveTo(b.door.x,b.door.y,true);return}\n  const t=mouseTile();if(t){me.target=null;me.npc=null;me.pick=null;me.queued=null;moveTo(t.x,t.y,true)}\n}")
# render
rep("  g.fillStyle='#0d1a0f';g.fillRect(0,0,W,H);\n  g.drawImage(groundC,-cx,-cy);","  g.fillStyle=scene==='world'?'#0d1a0f':'#0e0a08';g.fillRect(0,0,W,H);\n  g.drawImage(groundC,gOff.x-cx,gOff.y-cy);")
rep("else if(o.kind!=='well'&&o.kind!=='lamp'&&o.kind!=='crop')g.drawImage(SPR.shMed,s.x-9,s.y-4);","else if(!o.noSh&&o.kind!=='well'&&o.kind!=='lamp'&&o.kind!=='crop'&&o.kind!=='candle')g.drawImage(SPR.shMed,s.x-9,s.y-4);")
rep("      if(o.kind==='lamp'){g.globalAlpha=.12+.04*Math.sin(TIME*6+o.x);g.fillStyle='#ffe08a';g.beginPath();g.arc(s.x,s.y-30,10,0,7);g.fill();g.globalAlpha=1}",
    "      if(o.kind==='lamp'){g.globalAlpha=.12+.04*Math.sin(TIME*6+o.x);g.fillStyle='#ffe08a';g.beginPath();g.arc(s.x,s.y-30,10,0,7);g.fill();g.globalAlpha=1}\n      if(o.glow){g.globalAlpha=.16+.06*Math.sin(TIME*7+o.x*3);g.fillStyle=o.glow.col;g.beginPath();g.arc(s.x,s.y-o.glow.y,o.glow.r,0,7);g.fill();g.globalAlpha=1;if(o.kind==='fire'&&Math.random()<.5)parts.push({x:s.x+rand(-4,4),y:s.y-6,vx:rand(-4,4),vy:-rand(14,30),g:0,life:rand(.3,.6),max:.6,col:pick(['#ffd060','#ff8a3a','#fff4b8']),s:1})}")
rep("  drawOverlay();\n}","  if(fadeT>0){g.globalAlpha=Math.min(1,fadeT/.35);g.fillStyle='#000';g.fillRect(0,0,W,H);g.globalAlpha=1}\n  drawOverlay();\n}")
# overlay: nome da casa e saída
rep("  const h=mouse.over;\n  if(h&&h.kind==='mon'){",
    "  if(mouse.bld)otext(mouse.bld.name+' · entrar',mouse.x*S,(mouse.y-10)*S,'#ffe8a0');\n  if(scene!=='world'){const rm=ROOMS[scene],es=iso(rm.ex+.5,rm.ey+.5);otext('Saída',(es.x-CAM.x)*S,(es.y-CAM.y+4)*S,'#ffe8a0','bold 10px Verdana')}\n  const h=mouse.over;\n  if(h&&h.kind==='mon'){")
# info/minimapa
rep("$('mapName').textContent=`${inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (${Math.floor(me.x)}, ${Math.floor(me.y)})`;",
    "$('mapName').textContent=scene!=='world'?`${ROOMS[scene].name} · Vilarejo do Sabiá`:`${inCity(me.x,me.y)?'Vilarejo do Sabiá':'Campos do Sabiá'} (${Math.floor(me.x)}, ${Math.floor(me.y)})`;")
rep("  m.fillStyle='#ffe040';for(const n of npcs){const s=iso(n.x,n.y);m.fillRect(s.x*sx-1,s.y*sy-1,2,2)}\n  for(const mo of monsters)",
    "  m.fillStyle='#ffe040';for(const n of worldNPCs||npcs){const s=iso(n.x,n.y);m.fillRect(s.x*sx-1,s.y*sy-1,2,2)}\n  if(scene!=='world'){const s=iso(sceneDoor.ox+.5,sceneDoor.oy+.5);m.fillStyle='#000';m.fillRect(s.x*sx-2,s.y*sy-2,5,5);m.fillStyle='#fff';m.fillRect(s.x*sx-1,s.y*sy-1,3,3);return}\n  for(const mo of monsters)")
# teletransporte e morte saem da sala
rep("function teleport(kind){\n","function teleport(kind){\n  leaveRoom(false);\n")
rep("function revive(){\n","function revive(){\n  leaveRoom(false);\n")
rep("case'escape':for(const w of['winStats',","case'escape':for(const w of['winStats',")
# boot
rep("buildSprites();genMap();makeNPCs();buildGround();","buildSprites();genMap();makeNPCs();buildGround();buildRooms();")

# ---------- diálogos
a=s.index("  }else if(n.id==='guard'){\n");b=s.index("  }else if(n.id==='trainer_f'){",a)
s=s[:a]+"""  }else if(n.id==='guard'){
    dialog(n.name,`Acordou, forasteiro? Achei você caído aqui na beira da estrada, ${me.name}. Sem arma, sem um cobre no bolso e com essa roupa esquisita... Mais um que veio de outro mundo, aposto.<br><br>Este é o <b>Vilarejo do Sabiá</b>. Dentro da cerca, monstro nenhum entra.<br>· A <b>Irmã Liesel</b>, perto da capelinha, cuida de feridos de graça.<br>· Na <b>Taverna do Caneco</b>, ao norte, o Gaspar arruma serviço para aventureiros.<br>· A <b>Venda do Tomas</b> compra o que você trouxer dos campos e vende armas.<br>· O <b>Mestre Brann</b>, no galpão, e a <b>Sábia Yselda</b>, na cabana, ensinam técnicas.<br>· Na <b>Hospedaria</b>, a Dona Marta tem cama quente.<br><br>Sem arma? Seus punhos servem contra os <b>Lodinhos</b> aqui perto. Mais longe ficam as <b>Lebres-Galhudas</b> e os <b>Chapéus-Pulantes</b>.`,[bye]);
  }else if(n.id==='tavern'){
    const r=RANKS[rankOf()][0],first=!me.quests.reg;me.quests.reg=true;
    dialog(n.name,(first?`Forasteiro, é? Senta aí. Eu respondo pela <b>Guilda dos Aventureiros</b> aqui no vilarejo: a sede fica na cidade grande, mas os pedidos daqui passam por mim.<br>Deixa eu anotar seu nome no livro... <i>${me.name}</i>. Pronto: aventureiro de rank <span class="rank">${r}</span>.<br><br>`:`De volta, ${me.name}? Seu rank é <span class="rank">${r}</span>.<br><br>`)+`Aqui eu só repasso missões de rank <b>E</b> e <b>D</b>. Pegue até ${MAXQ} de uma vez e me traga o serviço feito. Missões rendem pontos de guilda e sobem o seu rank.`,[{label:'Ver missões',fn:()=>openGuild(qAnyDone()?'mine':'board')},bye]);
  }else if(n.id==='inn'){
    dialog(n.name,'Bem-vindo à Hospedaria do Sabiá! Cama limpa, sopa quente e lareira acesa.<br>Uma noite custa <b>15 cobres</b>, e você acorda novinho em folha.',[{label:'Pernoitar (15c)',fn:()=>{
      if(me.zeny<15){n.say={text:'Sem cobres, sem cama, querido.',t:0};return}
      me.zeny-=15;me.hp=me.maxHp;me.sp=me.maxSp;fadeT=1.4;sfx('heal');msg('Você dormiu na hospedaria e acordou renovado. (−15c)','#c8f0c8');n.say={text:'Dormiu bem?',t:0};save()}},bye]);
  }else if(n.id==='patron'){
    dialog(n.name,pick(PATRON_LINES[n.name]),[bye]);
"""+s[b:]
# fala do vendeiro
rep("'Olá, olá! Tônicos, penas e armas de todo tipo...","'Bem-vindo à minha venda! Tônicos, penas e armas de todo tipo...")

# ---------- início isekai
rep("  hot=(data.hot||[null,null,null,null,null,{type:'item',id:'pocao_v'},{type:'item',id:'pocao_a'},{type:'item',id:'asa_mosca'},{type:'item',id:'asa_borb'}])",
    "  hot=(data.hot||[null,null,null,null,null,null,null,null,null])")
a=s.index("  if(!data.hot){msg('Você acorda deitado na grama");b=s.index("  setInterval(save,20000);",a)
s=s[:a]+"""  msg('Pressione H para ver os controles.','#ffe8a0');
  msg('Aqui não há classes: tudo o que você usa fica mais forte. Abra as habilidades com S.','#c8d8ff');
  if(!data.hot){
    me.x=C+.5;me.y=C+12.5;me.face={flip:false,front:true};
    const bento=npcs.find(n=>n.id==='guard');
    dialog('???',`A última coisa de que você se lembra é o farol de um caminhão e um clarão branco.<br><br>Agora há grama sob as suas costas, um céu azul demais e dois sóis pálidos no horizonte. No bolso, nada. No corpo, só a <b>camiseta</b> e a <b>calça jeans</b> de sempre.<br><br>Este não é o seu mundo.`,[{label:'Levantar-se',fn:()=>talk(bento)}]);
  }else msg('Dica: o Gaspar, na Taverna do Caneco, repassa as missões da guilda.','#c8d8ff');
"""+s[b:]
open(p,'w',encoding='utf-8').write(s)
print('ok')
