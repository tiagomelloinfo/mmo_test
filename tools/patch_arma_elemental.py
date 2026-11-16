# Magias de conjurar arma elemental: uma por elemento, cada uma com um tipo de arma.
# Enquanto ativa: drena SP continuamente, a arma conjurada substitui a equipada e cada golpe soma dano do elemento.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,1)
# magias (ensinadas pela Sábia Yselda, por terem elemento)
rep("  eclipse:{","""  arma_fogo:{name:'Espada Flamejante',icon:'cj_fogo',el:'fogo',conj:true,self:true,price:1500,req:['fogo',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Conjura uma espada de fogo. Treina Espada.'},
  arma_agua:{name:'Lança Glacial',icon:'cj_agua',el:'agua',conj:true,self:true,price:1500,req:['agua',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Conjura uma lança de gelo. Treina Lança e alcança 2 quadros.'},
  arma_terra:{name:'Machado de Rocha',icon:'cj_terra',el:'terra',conj:true,self:true,price:1500,req:['terra',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Conjura um machado de pedra. Treina Machado.'},
  arma_ar:{name:'Adaga do Vento',icon:'cj_ar',el:'ar',conj:true,self:true,price:1500,req:['ar',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Conjura uma adaga de vento. Treina Adaga e acerta críticos com mais facilidade.'},
  arma_luz:{name:'Maça Radiante',icon:'cj_luz',el:'luz',conj:true,self:true,price:1500,req:['luz',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Conjura uma maça de luz. Treina Maça e ignora parte da defesa.'},
  arma_sombras:{name:'Garras Sombrias',icon:'cj_sombras',el:'sombras',conj:true,self:true,price:1500,req:['sombras',10],sp:12,drain:1.5,cd:2,cast:.8,desc:'Envolve os punhos em garras de sombra. Treina Desarmado.'},
  eclipse:{""")
# descrição comum e dados das armas
rep("const ALLSK=Object.assign({},PASSIVE,ACTIVE);","""const CONJ={
  fogo:{wt:'espada',blade:'#ffd070',bladeD:'#e04a10',wicon:'sword'},
  agua:{wt:'lanca',blade:'#e0f8ff',bladeD:'#4aa8e0',wicon:'spear'},
  terra:{wt:'machado',blade:'#d8b070',bladeD:'#7a5a30',wicon:'axe'},
  ar:{wt:'adaga',blade:'#f0fff8',bladeD:'#7adcc0',wicon:'dagger'},
  luz:{wt:'maca',blade:'#fff4a0',bladeD:'#e0b040',wicon:'mace'},
  sombras:{wt:'desarmado',blade:'#b07ae8',bladeD:'#5a2a8a',wicon:'s_desarmado'},
};
for(const id in ACTIVE){const a=ACTIVE[id];if(a.conj)a.desc+=` Fica ativa até você desfazê-la (use de novo) ou o SP acabar: drena ${a.drain} SP por segundo, menos conforme sobe de nível. A arma conjurada substitui a equipada, fica mais forte com ${ELN[a.el]} e cada golpe soma dano de ${ELN[a.el]}.`}
const ALLSK=Object.assign({},PASSIVE,ACTIVE);""")
# arma em uso
rep("function wtype(){return me.eq.weapon?ITEMS[me.eq.weapon].wt:'desarmado'}","""function wtype(){if(me.conj)return CONJ[me.conj.el].wt;return me.eq.weapon?ITEMS[me.eq.weapon].wt:'desarmado'}
function conjAtk(){const c=me.conj;return Math.floor(10+me.E(c.el)*1.4+me.L[c.id]*.6+me.E('inteligencia')*.3)}
function conjDrain(){const a=ACTIVE[me.conj.id];return Math.max(.3,a.drain*(1-me.L[me.conj.id]*.006))}
function endConj(why){if(!me.conj)return;const a=ACTIVE[me.conj.id];me.conj=null;calc();renderStats();renderBuffs();renderHot();if(why)msg(why,'#c0c8e0');else msg(`${a.name} se desfez.`,'#c0c8e0');burst(me.x,me.y,ELC[a.el],10,16)}""")
rep("const w=me.eq.weapon?ITEMS[me.eq.weapon]:null,ar=","const w=me.conj?{atk:conjAtk()}:me.eq.weapon?ITEMS[me.eq.weapon]:null,ar=")
rep("me.crit=Math.floor(2+D*.12+(wt==='adaga'?5:0));","me.crit=Math.floor(2+D*.12+(wt==='adaga'?5:0)+(me.conj&&me.conj.el==='ar'?5:0));")
rep("cd:{},regT:0,","conj:null,conjAcc:0,cd:{},regT:0,")
# visual da arma conjurada
rep("""function heroLook(){
  const k='hero_'+me.eq.weapon+'_'+me.eq.armor+'_'+me.eq.legs;""","""function heroLook(){
  const k='hero_'+(me.conj?'cj_'+me.conj.el:me.eq.weapon)+'_'+me.eq.armor+'_'+me.eq.legs;""")
rep("    Object.assign(x,w?{weapon:1,wtype:w.wt,blade:w.blade||'#e6ecf6',bladeD:w.bladeD||'#8a93ad'}:{weapon:0});",
    "    if(me.conj){const c=CONJ[me.conj.el];Object.assign(x,c.wt==='desarmado'?{weapon:0}:{weapon:1,wtype:c.wt,blade:c.blade,bladeD:c.bladeD,maceL:c.blade,maceD:c.bladeD})}\n    else Object.assign(x,w?{weapon:1,wtype:w.wt,blade:w.blade||'#e6ecf6',bladeD:w.bladeD||'#8a93ad'}:{weapon:0});")
rep("p(tx-2,ty-2,4,4,'#6a7080');p(tx-2,ty-2,3,3,'#a8b0c0');","p(tx-2,ty-2,4,4,o.maceD||'#6a7080');p(tx-2,ty-2,3,3,o.maceL||'#a8b0c0');")
# ícones: o ícone da arma tingido com a cor do elemento
rep("  SPR.icons={};for(const k of keys)SPR.icons[k]=sprIcon(k);","  SPR.icons={};for(const k of keys)SPR.icons[k]=sprIcon(k);\n  for(const el in CONJ)SPR.icons['cj_'+el]=tint(SPR.icons[CONJ[el].wicon]||sprIcon(CONJ[el].wicon),ELC[el],.55);")
# usar / desfazer
rep("  if(!unlocked(id)){const t=teacher(id);return no(`Você ainda não aprendeu ${s.name}. Procure ${t.name} (${t.place}).`)}",
    "  if(!unlocked(id)){const t=teacher(id);return no(`Você ainda não aprendeu ${s.name}. Procure ${t.name} (${t.place}).`)}\n  if(s.conj&&me.conj&&me.conj.id===id)return true;")
rep("  me.queued=null;const s=ACTIVE[id];if(!canUse(id,true))return;\n","  me.queued=null;const s=ACTIVE[id];if(!canUse(id,true))return;\n  if(s.conj&&me.conj&&me.conj.id===id){endConj();return}\n")
rep("  if(s.el){\n    me.atkT=.3;addXp('destreza',1);","""  if(s.conj){
    const old=me.conj;me.conj={id,el:s.el};me.conjAcc=0;calc();renderStats();renderBuffs();renderHot();
    fx.push({type:'pillar',ent:me,t:0,dur:1,col:ELC[s.el]});fx.push({type:'ring',ent:me,t:0,dur:.5,col:ELC[s.el],r:26});sfx(s.el);me.say={text:s.name+'!',t:0};
    msg(old?`${ACTIVE[old.id].name} deu lugar a ${s.name}.`:`Você conjurou ${s.name}! (ATK da arma: ${conjAtk()} · −${conjDrain().toFixed(1)} SP/s)`,ELC[s.el]);
    addXp(s.el,8);addXp(id,6);return;
  }
  if(s.el){
    me.atkT=.3;addXp('destreza',1);""")
# dano do elemento a cada golpe
rep("function trainMelee(d){const wt=wtype();addXp(wt,d*1+1);addXp('forca',d*.5);addXp('destreza',1.5)}",
    """function trainMelee(d){const wt=wtype();addXp(wt,d*1+1);addXp('forca',d*.5);addXp('destreza',1.5)}
// arma conjurada: cada golpe que acerta soma dano do elemento
function conjHit(m){
  if(!me.conj||m.dead)return;const el=me.conj.el,id=me.conj.id,em=elMul(el,m.def.el);
  const dmg=Math.max(1,Math.round(me.matk*.3*(1+me.E(el)*.01)*(1+me.L[id]*.005)*em*rand(.9,1.1)));
  damageMon(m,dmg,{col:ELC[el],el,silent:true});addXp(el,dmg*.5+1);addXp(id,dmg*.3+1);
}""")
rep("const dmg=Math.floor(me.atk*1.5*rand(.95,1.05));damageMon(m,dmg,{crit:true});trainMelee(dmg);addXp('destreza',3);return}",
    "const dmg=Math.floor(me.atk*1.5*rand(.95,1.05));damageMon(m,dmg,{crit:true});trainMelee(dmg);addXp('destreza',3);conjHit(m);return}")
rep("if(Math.random()*100<hitChance(me.hit,m.def.flee)){const dmg=physDmg(m);damageMon(m,dmg,{});trainMelee(dmg)}",
    "if(Math.random()*100<hitChance(me.hit,m.def.flee)){const dmg=physDmg(m);damageMon(m,dmg,{});trainMelee(dmg);conjHit(m)}")
rep("for(const m of tg){const dmg=physDmg(m,s.power*mul);damageMon(m,dmg,{big:true,col:'#ffb060'});trainMelee(dmg);addXp(id,dmg*.6+3);if(s.stun)m.stunT=s.stun}",
    "for(const m of tg){const dmg=physDmg(m,s.power*mul);damageMon(m,dmg,{big:true,col:'#ffb060'});trainMelee(dmg);addXp(id,dmg*.6+3);if(s.stun)m.stunT=s.stun;conjHit(m)}")
# dreno contínuo de SP e aura
rep("  me.regT+=dt;me.sregT+=dt;","""  if(me.conj){
    me.conjAcc+=conjDrain()*dt;while(me.conjAcc>=1){me.conjAcc-=1;me.sp-=1;addXp('inteligencia',1.2,true)}
    if(me.sp<=0){me.sp=0;endConj(`Seu SP acabou e ${ACTIVE[me.conj.id].name} se desfez.`)}
    else if(Math.random()<.35){const s=iso(me.x,me.y);parts.push({x:s.x+rand(-8,8),y:s.y-rand(4,24),vx:rand(-4,4),vy:-rand(8,20),g:0,life:rand(.3,.6),max:.6,col:pick([ELC[me.conj.el],'#ffffff']),s:1})}
  }
  me.regT+=dt;me.sregT+=dt;""")
rep("function die(){me.hp=0;me.dead=true;","function die(){if(me.conj){me.conj=null;calc()}me.hp=0;me.dead=true;")
# buffs e status
rep("""function renderBuffs(){
  const b=$('buffs');b.innerHTML='';""","""function renderBuffs(){
  const b=$('buffs');b.innerHTML='';
  if(me.conj){const a=ACTIVE[me.conj.id];b.innerHTML+=`<div class="buff" data-tip="<b>${a.name}</b><br>ATK da arma ${conjAtk()} · dano extra de ${ELN[a.el]}<br>−${conjDrain().toFixed(1)} SP por segundo<br><i>Use de novo para desfazer</i>"><img src="${iconURL(a.icon)}"><span>∞</span></div>`}""")
rep("${r('Arma',WNAME[wtype()])}","${r('Arma',me.conj?ACTIVE[me.conj.id].name:WNAME[wtype()])}")
# menu do botão direito mostra "Desfazer"
rep("for(const id of me.learned.filter(id=>ACTIVE[id].self))ops.push({label:`${ACTIVE[id].name} (SP ${skillCost(id)})`,",
    "for(const id of me.learned.filter(id=>ACTIVE[id].self))ops.push({label:me.conj&&me.conj.id===id?`Desfazer ${ACTIVE[id].name}`:`${ACTIVE[id].name} (SP ${skillCost(id)})`,")
# texto antigo
rep("Concluída! Entregue na Guilda dos Aventureiros.","Concluída! Entregue ao Gaspar, na taverna.")
open(p,'w',encoding='utf-8').write(s);print('ok')
