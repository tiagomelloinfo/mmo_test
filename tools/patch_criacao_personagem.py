# Criação de personagem: corpo masculino/feminino, 10 cabelos de cada, cor do cabelo e da pele.
# A aparência fica em me.app = {sex, hs, hc, sk} e é salva junto com o personagem.
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

# sprHuman novo (corpo feminino + penteados)
a=s.index("function sprHuman(o,dir,state,f){");b=s.index("function sprTree(kind){")
s=s[:a]+open('tools/_sprHuman_real.js',encoding='utf-8').read()+s[b:]

# penteados, cores e aparência padrão
rep("function look(name,extra){",r"""const HAIRSTYLES={
  npc:{bang:[[-2.35,1.3,1.1],[-1.35,1.9,1.2],[-.3,1.45,1.1],[.75,2.1,1.25],[1.85,1.5,1.1],[2.75,1.2,1]]},
  m1:{name:'Bagunçado',bang:[[-2.35,1.3,1.1],[-1.35,1.9,1.2],[-.3,1.45,1.1],[.75,2.1,1.25],[1.85,1.5,1.1],[2.75,1.2,1]],ahoge:1},
  m2:{name:'Raspado',buzz:1},
  m3:{name:'Topete',bang:[],sides:1.6,jag:.03,quiff:1,forehead:1,back:3.2},
  m4:{name:'Espetado',bang:[[-2.3,2.2,1.3],[-1,2.8,1.4],[.4,2.3,1.4],[1.7,2.9,1.4],[2.8,1.8,1.1]],jag:.2,jagN:9,spiky:1,sides:3.6},
  m5:{name:'Repartido de lado',bang:[[-2.6,2.7,1.7],[-1.3,2.1,1.9],[.2,1.4,1.9],[1.6,.7,1.7],[2.8,.4,1]],jag:.025,sides:3.4},
  m6:{name:'Médio',bang:[[-2.3,1.9,1.3],[-1.1,2.4,1.3],[.2,2.1,1.3],[1.4,2.5,1.3],[2.6,1.9,1.2]],sides:5,back:5.2,jag:.05},
  m7:{name:'Rabo de cavalo',bang:[[-2.1,1.5,1.4],[-.6,1.9,1.4],[.9,1.6,1.4],[2.3,1.3,1.2]],sides:3.8,jag:.03,lowpony:1,tie:'#3a2a1a'},
  m8:{name:'Longo solto',bang:[[-2.4,2.2,1.6],[-.9,1.4,1.5],[.9,1.4,1.5],[2.4,2.2,1.6]],sides:5.2,back:11,backW:4.6,front:8,jag:.04},
  m9:{name:'Coque samurai',bang:[],sides:2.4,forehead:1,jag:.02,topknot:1,back:3.2,tie:'#3a2a1a'},
  m10:{name:'Moicano',buzz:1,mohawk:1},
  f1:{name:'Longo liso',bangFlat:1.9,sides:5.4,back:13,backW:4.6,front:9.5,straightEnds:1,jag:.02},
  f2:{name:'Rabo de cavalo alto',bang:[[-2.3,1.8,1.5],[-.8,2.1,1.5],[.8,1.7,1.5],[2.3,1.9,1.4]],sides:4.6,jag:.03,highpony:1},
  f3:{name:'Maria-chiquinha',bang:[[-2.2,2,1.4],[-.8,2.3,1.4],[.6,2,1.4],[2.1,2.2,1.4]],sides:4.2,jag:.04,twintails:1},
  f4:{name:'Chanel',bangFlat:1.8,sides:5,back:5.2,backW:4.6,straightEnds:1,jag:.015,vol:1.04},
  f5:{name:'Pixie',bang:[[-2.5,1.6,1.3],[-1.2,2.2,1.4],[.2,1.7,1.3],[1.5,1.2,1.3]],sides:3,jag:.06},
  f6:{name:'Coque',bang:[[-2.6,2.4,1.8],[-1.1,1.6,1.8],[.6,.9,1.6]],sides:3.4,jag:.02,bun:1,forehead:1,tie:'#e8c860'},
  f7:{name:'Trança lateral',bang:[[-2.5,2.3,1.8],[-1,1.7,1.8],[.6,1.2,1.7],[2.1,.8,1.4]],sides:4.4,jag:.03,sidebraid:1,back:5},
  f8:{name:'Ondulado',bang:[[-2.6,2.4,1.6],[-1.4,1.4,1.4],[1.4,1.4,1.4],[2.6,2.4,1.6]],sides:5.4,back:12,backW:5,front:9,wavy:1,jag:.05},
  f9:{name:'Franja lateral',bang:[[-2.5,2.6,1.9],[-1,2.2,1.9],[.6,1.6,1.9],[2.2,1,1.6]],sides:5.2,back:11,backW:4.5,front:7.5,jag:.03},
  f10:{name:'Tranças duplas',bang:[[-1.8,1.3,1.6],[1.8,1.3,1.6]],sides:4,jag:.02,twinbraids:1,forehead:1},
};
const HAIR_M=['m1','m2','m3','m4','m5','m6','m7','m8','m9','m10'],HAIR_F=['f1','f2','f3','f4','f5','f6','f7','f8','f9','f10'];
const HAIR_COLORS=[
  {name:'Preto',c:['#141018','#262230','#45404f']},{name:'Castanho-escuro',c:['#2a1a12','#4a2e1e','#6e4a32']},
  {name:'Castanho',c:['#4a301c','#7a5532','#a87c4c']},{name:'Castanho-claro',c:['#6a4a2a','#9a7044','#c8a070']},
  {name:'Ruivo',c:['#7a2a14','#b8481e','#e8783e']},{name:'Loiro',c:['#a07a2a','#d8b048','#f8e08a']},
  {name:'Platinado',c:['#a8a49a','#dcd8cc','#fffcf0']},{name:'Grisalho',c:['#5a5a62','#8e8e98','#c8c8d0']},
  {name:'Azul',c:['#1a2a6a','#2e4aa8','#5a80e0']},{name:'Rosa',c:['#a03a6a','#d86a9a','#f8a8c8']}];
const SKIN_TONES=[
  {name:'Muito clara',c:['#fbe2d0','#e8baa2']},{name:'Clara',c:['#f8d0b0','#e0a888']},{name:'Média',c:['#e8b890','#c89068']},
  {name:'Morena',c:['#c8916a','#a06c48']},{name:'Escura',c:['#a06a48','#7e4e32']},{name:'Muito escura',c:['#6e4630','#52321f']}];
const APP_DEF={sex:'m',hs:'m1',hc:2,sk:1};
function look(name,extra){""")
rep("  hero:{hair:['#4a301c','#7a5532','#a87c4c'],eye:'#3e7a44',ahoge:1},","  hero:{hair:['#4a301c','#7a5532','#a87c4c'],eye:'#3e7a44'},")
rep("  innkeep:{hair:","  innkeep:{sex:'f',hs:'f6',hair:")
rep("  patron2:{hair:","  patron2:{sex:'f',hs:'f4',hair:")
rep("  mage:{hair:","  mage:{sex:'f',hs:'f1',hair:")

# visual do herói a partir da aparência escolhida
rep("  const k='hero_'+(me.conj?","  const A=Object.assign({},APP_DEF,me.app||{});\n  const k='hero_'+A.sex+A.hs+'_'+A.hc+'_'+A.sk+'_'+(me.conj?")
rep("  return cached('look_'+k,()=>{const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,x={};",
    "  return cached('look_'+k,()=>{const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,SKN=SKIN_TONES[A.sk]||SKIN_TONES[1],x={sex:A.sex,hs:A.hs,hair:(HAIR_COLORS[A.hc]||HAIR_COLORS[2]).c,skin:SKN.c[0],skinD:SKN.c[1]};")
rep("else if(!me.eq.armor)Object.assign(x,{tunic:'#f8d0b0',tunicD:'#e0a888',trim:'#f8d0b0'});",
    "else if(!me.eq.armor)Object.assign(x,A.sex==='f'?{tunic:'#e8e0d0',tunicD:'#c8c0b0',trim:'#e8e0d0',belt:'#c8c0b0'}:{tunic:SKN.c[0],tunicD:SKN.c[1],trim:SKN.c[0]});")
rep("if(!me.eq.legs)Object.assign(x,{pants:'#f8d0b0',pantsD:'#e0a888',boot:'#f8d0b0',bareLegs:1});",
    "if(!me.eq.legs)Object.assign(x,{pants:SKN.c[0],pantsD:SKN.c[1],boot:SKN.c[0],bareLegs:1});")

# salvar aparência
rep("const k=['name','xp','inv','eq','cards','zeny','learned','quests','hp','sp','last'];","const k=['name','app','xp','inv','eq','cards','zeny','learned','quests','hp','sp','last'];")

# ---------- tela de criação
rep("#titleBox{width:300px}",
"""#titleBox{width:400px}
#cc{display:flex;gap:10px;margin-top:4px}
#ccPrev{width:132px;height:170px;background:linear-gradient(#cfe0c0,#9ab884);border:1px solid #8193bd;border-radius:4px;image-rendering:pixelated;flex:none}
#ccOpts{flex:1;font-size:11px}
#ccOpts .row{margin:0 0 7px}
#ccOpts .lbl{color:#4a5a80;margin-bottom:2px}
.seg button{padding:2px 8px}.seg button.on{background:#ffe9a8;border-color:#b08a30;font-weight:bold}
.cyc{display:flex;align-items:center;gap:4px}.cyc span{flex:1;text-align:center;font-weight:bold;color:#2a3e7a}.cyc button{padding:1px 6px}
.sw{display:flex;flex-wrap:wrap;gap:3px}.sw i{width:16px;height:16px;border-radius:3px;border:1px solid #6f81aa;cursor:pointer;display:block}.sw i.on{outline:2px solid #e0a020;outline-offset:1px}""")
rep("""      <input id="nameIn" maxlength="16" value="Herói">
      <div id="titleErr"></div>""",
"""      <input id="nameIn" maxlength="16" value="Herói">
      <div id="cc">
        <canvas id="ccPrev" width="132" height="170"></canvas>
        <div id="ccOpts">
          <div class="row"><div class="lbl">Corpo</div><div class="seg" id="ccSex"><button data-sex="m">Masculino</button> <button data-sex="f">Feminino</button></div></div>
          <div class="row"><div class="lbl">Cabelo</div><div class="cyc"><button id="ccHp">◀</button><span id="ccHn"></span><button id="ccHnx">▶</button></div></div>
          <div class="row"><div class="lbl">Cor do cabelo</div><div class="sw" id="ccHc"></div></div>
          <div class="row"><div class="lbl">Cor da pele</div><div class="sw" id="ccSk"></div></div>
          <div class="row"><button id="ccTurn">Girar</button></div>
        </div>
      </div>
      <div id="titleErr"></div>""")
rep("  $('btnNew').onclick=()=>{audio();sfx('click');const n=$('nameIn').value.trim().slice(0,16);if(!n){$('titleErr').textContent='Digite um nome.';return}if(chars[n]){$('titleErr').textContent='Já existe um personagem com esse nome.';return}startGame({name:n})};",
r"""  // criação de personagem
  const app=Object.assign({},APP_DEF);let ccDir='f';
  const ccDraw=()=>{
    const list=app.sex==='f'?HAIR_F:HAIR_M;$('ccHn').textContent=`${list.indexOf(app.hs)+1}. ${HAIRSTYLES[app.hs].name}`;
    document.querySelectorAll('#ccSex button').forEach(b=>b.classList.toggle('on',b.dataset.sex===app.sex));
    document.querySelectorAll('#ccHc i').forEach((b,i)=>b.classList.toggle('on',i===app.hc));
    document.querySelectorAll('#ccSk i').forEach((b,i)=>b.classList.toggle('on',i===app.sk));
    const SKN=SKIN_TONES[app.sk].c,lk=look('hero',{sex:app.sex,hs:app.hs,hair:HAIR_COLORS[app.hc].c,skin:SKN[0],skinD:SKN[1],tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34',print:'#3a6ac8',short:1,pants:'#3a5a9a',pantsD:'#2a4070',boot:'#f0f0f0',legsJeans:1,weapon:0});
    const spr=sprHuman(lk,ccDir,'idle',0),cv2=$('ccPrev'),q=cv2.getContext('2d');q.clearRect(0,0,cv2.width,cv2.height);q.imageSmoothingEnabled=false;
    const sc=Math.min(cv2.width/spr.width,cv2.height/spr.height)*1.25;q.drawImage(spr,Math.round((cv2.width-spr.width*sc)/2),Math.round(cv2.height-spr.height*sc+8),spr.width*sc,spr.height*sc)};
  $('ccHc').innerHTML=HAIR_COLORS.map(h=>`<i title="${h.name}" style="background:${h.c[1]}"></i>`).join('');
  $('ccSk').innerHTML=SKIN_TONES.map(h=>`<i title="${h.name}" style="background:${h.c[0]}"></i>`).join('');
  $('ccHc').onclick=e=>{const i=[...$('ccHc').children].indexOf(e.target);if(i>=0){app.hc=i;ccDraw()}};
  $('ccSk').onclick=e=>{const i=[...$('ccSk').children].indexOf(e.target);if(i>=0){app.sk=i;ccDraw()}};
  $('ccSex').onclick=e=>{const b=e.target.closest('[data-sex]');if(!b||b.dataset.sex===app.sex)return;const list=app.sex==='f'?HAIR_F:HAIR_M,i=list.indexOf(app.hs);app.sex=b.dataset.sex;app.hs=(app.sex==='f'?HAIR_F:HAIR_M)[Math.max(0,i)];ccDraw()};
  const cyc=d=>{const list=app.sex==='f'?HAIR_F:HAIR_M;app.hs=list[(list.indexOf(app.hs)+d+list.length)%list.length];ccDraw()};
  $('ccHp').onclick=()=>cyc(-1);$('ccHnx').onclick=()=>cyc(1);
  $('ccTurn').onclick=()=>{ccDir=ccDir==='f'?'b':'f';ccDraw()};
  ccDraw();
  $('btnNew').onclick=()=>{audio();sfx('click');const n=$('nameIn').value.trim().slice(0,16);if(!n){$('titleErr').textContent='Digite um nome.';return}if(chars[n]){$('titleErr').textContent='Já existe um personagem com esse nome.';return}startGame({name:n,app:Object.assign({},app)})};""")
open(p,'w',encoding='utf-8').write(s);print('ok')
