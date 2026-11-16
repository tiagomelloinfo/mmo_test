# Menu de contexto no botão direito: opções conforme o alvo (monstro, NPC, item, casa, o herói ou o chão).
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,1)
rep(".win .body{padding:6px 8px}",""".win .body{padding:6px 8px}
#ctx{position:fixed;z-index:80;min-width:150px;background:var(--win-bg);border:1px solid var(--win-bd);border-radius:6px;box-shadow:0 3px 12px rgba(0,0,0,.4);padding:3px 0;font-size:11px;color:var(--ink)}
#ctx .ch{padding:3px 10px 4px;font-weight:bold;color:#2b3d68;border-bottom:1px solid #d8e0f0;margin-bottom:2px;background:linear-gradient(var(--title-a),var(--title-b))}
#ctx .op{padding:4px 12px}#ctx .op:hover{background:#dbe6ff}#ctx .op.off{color:#a0a8b8}#ctx .op.off:hover{background:none}#ctx .sep{border-top:1px solid #e1e6f2;margin:2px 0}""")
rep('<div id="menuShade" class="hidden"></div>','<div id="ctx" class="hidden"></div>\n<div id="menuShade" class="hidden"></div>')
# botão direito abre o menu (ou cancela a magia esperando alvo)
rep("  if(e.button===2){pendingSkill=null;updCursor();return}","  if(e.button===2)return;\n  closeCtx();")
rep("cv.addEventListener('contextmenu',e=>e.preventDefault());","""cv.addEventListener('contextmenu',e=>{e.preventDefault();if(!started||me.dead)return;
  if(pendingSkill){pendingSkill=null;updCursor();msg('Alvo cancelado.','#c0c8e0');return}
  mouse.x=e.clientX/SCALE;mouse.y=e.clientY/SCALE;mouse.overUI=false;openCtx(e.clientX,e.clientY)});
// ---------- menu de contexto
function closeCtx(){$('ctx').classList.add('hidden')}
function overMe(mx,my){const s=scr(me);return mx>=s.x-9&&mx<=s.x+9&&my>=s.y-30&&my<=s.y+4}
function goSkill(id,T){if(!canUse(id,true))return;if(ACTIVE[id].self){me.path=[];me.target=null;startSkill(id,me)}else castOn(id,T)}
function openCtx(cx,cy){
  const h=pickAt(mouse.x,mouse.y),b=h?null:bldAt(mouse.x,mouse.y),t=mouseTile();let head='',ops=[];
  const sitOp={label:me.sit?'Levantar':'Sentar (X)',fn:()=>{if(!me.moving&&!me.cast){me.sit=!me.sit;me.target=null;sfx('sit')}}};
  if(h&&h.kind==='mon'){const m=h.e,d=m.def;head=`${d.name} · Nv. ${d.lv}`;
    ops.push({label:'Atacar',fn:()=>{me.target=m;me.queued=null;me.npc=null;me.pick=null;me.repath=0;me.sit=false}});
    const sk=me.learned.filter(id=>!ACTIVE[id].self);
    for(const id of sk)ops.push({label:`${ACTIVE[id].name} (SP ${skillCost(id)})`,off:!canUse(id,false),fn:()=>goSkill(id,m)});
    ops.push({sep:1},{label:'Examinar',fn:()=>msg(`${d.name} · Nível ${d.lv} · ${ELN[d.el]} · HP ${Math.ceil(m.hp)}/${d.hp} · ${d.aggro?'agressivo: ataca quem chega perto':'passivo: só reage se atacado'}.`,'#d8e8ff')})}
  else if(h&&h.kind==='npc'){const n=h.e;head=n.name;
    ops.push({label:'Conversar',fn:()=>{me.npc=n;me.target=null;me.pick=null;if(dist(me.x,me.y,n.x,n.y)>2.3)moveTo(n.x,n.y)}})}
  else if(h&&h.kind==='item'){const it=h.e,d=ITEMS[it.id];head=d.name;
    ops.push({label:'Pegar',fn:()=>{me.pick=it;me.target=null;me.npc=null;moveTo(it.x,it.y)}},{label:'Examinar',fn:()=>msg(`${d.name}: ${d.desc}`,'#d8e8ff')})}
  else if(b){head=b.name;ops.push({label:'Entrar',fn:()=>{me.target=null;me.npc=null;me.pick=null;moveTo(b.door.x,b.door.y,true)}})}
  else if(overMe(mouse.x,mouse.y)){head=me.name;
    ops.push(sitOp);for(const id of me.learned.filter(id=>ACTIVE[id].self))ops.push({label:`${ACTIVE[id].name} (SP ${skillCost(id)})`,off:!canUse(id,false),fn:()=>goSkill(id,me)});
    ops.push({sep:1},{label:'Status (A)',fn:()=>toggle('winStats')},{label:'Itens (E)',fn:()=>toggle('winInv')},{label:'Habilidades (S)',fn:()=>toggle('winSkill')})}
  else{
    if(t&&walkable(t.x,t.y))ops.push({label:'Andar até aqui',fn:()=>{me.target=null;me.npc=null;me.pick=null;me.queued=null;moveTo(t.x,t.y,true)}});
    ops.push(sitOp);
    if(scene!=='world')ops.push({label:'Sair daqui',fn:()=>{const rm=ROOMS[scene];me.target=null;me.npc=null;moveTo(rm.ex,rm.ey,true)}});
    ops.push({sep:1},{label:'Menu (Esc)',fn:openMenu})}
  ops.push({sep:1},{label:'Cancelar',fn:()=>{}});
  const el=$('ctx');el.innerHTML=(head?`<div class="ch">${head}</div>`:'')+ops.map((o,i)=>o.sep?'<div class="sep"></div>':`<div class="op${o.off?' off':''}" data-i="${i}">${o.label}</div>`).join('');
  el._ops=ops;el.classList.remove('hidden');
  const r=el.getBoundingClientRect();el.style.left=Math.min(cx,innerWidth-r.width-4)+'px';el.style.top=Math.min(cy,innerHeight-r.height-4)+'px';
  if(curCursor)el.querySelectorAll('.op').forEach(e=>e.style.cursor=curCursor);sfx('click');
}
$('ctx').addEventListener('mousedown',e=>{e.stopPropagation();const o=e.target.closest('[data-i]');if(!o)return;const op=$('ctx')._ops[+o.dataset.i];if(op.off)return;closeCtx();sfx('click');op.fn()});
$('ctx').addEventListener('contextmenu',e=>e.preventDefault());
addEventListener('mousedown',e=>{if(!e.target.closest('#ctx'))closeCtx()},true);""")
# Esc fecha o menu de contexto primeiro
rep("    case'escape':{const ws=","    case'escape':{if(!$('ctx').classList.contains('hidden')){closeCtx();break}const ws=")
# ao entrar ou sair de casa, fecha o menu
rep("function clearActs(){","function clearActs(){closeCtx();")
# ajuda
rep("<b>Clique num NPC</b> para conversar.<br>","<b>Clique num NPC</b> para conversar. <b>Botão direito</b> abre as opções do que está sob o cursor.<br>")
open(p,'w',encoding='utf-8').write(s);print('ok')
