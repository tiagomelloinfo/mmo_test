# Menu do Esc (continuar, controles, som, trocar de personagem, fechar o jogo) e vários personagens salvos.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,1)
# CSS
rep("#winDeath{left:50%;top:40%;transform:translate(-50%,-50%);width:280px;text-align:center}",
    "#winDeath{left:50%;top:40%;transform:translate(-50%,-50%);width:280px;text-align:center}\n#winMenu{left:50%;top:42%;transform:translate(-50%,-50%);width:220px;z-index:60}\n#winMenu button{display:block;width:100%;margin:4px 0;padding:4px}\n#menuShade{position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:59}\n#closed{position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#0b0d10;color:#e8f0ff;font-size:13px;gap:12px}\n#charList .ch{display:flex;justify-content:space-between;align-items:center;padding:3px 0;border-bottom:1px solid #d8e0f0}\n#charList .ch button{margin-left:4px}\n#titleErr{color:#c03030;font-size:11px;min-height:14px}")
# HTML do menu e da tela de jogo fechado
rep('<div class="win hidden" id="winDeath">','''<div id="menuShade" class="hidden"></div>
<div class="win hidden" id="winMenu">
  <div class="title"><span>Menu</span><span class="x" data-close="winMenu">x</span></div>
  <div class="body">
    <button id="mnBack">Voltar ao jogo</button>
    <button id="mnHelp">Controles</button>
    <button id="mnSound">Som: on</button>
    <button id="mnChar">Trocar de personagem</button>
    <button id="mnQuit">Fechar o jogo</button>
  </div>
</div>
<div id="closed" class="hidden"><div>Jogo salvo. Você já pode fechar esta aba.</div><button id="btnReopen">Voltar à tela inicial</button></div>
<div class="win hidden" id="winDeath">''')
# tela inicial: lista de personagens
rep('''      Nome do personagem
      <input id="nameIn" maxlength="16" value="Herói">
      <div style="display:flex;gap:6px;justify-content:flex-end">
        <button id="btnNew">Novo jogo</button><button id="btnCont" class="hidden">Continuar</button>
      </div>''','''      <div id="charBox" class="hidden" style="margin-bottom:10px">Personagens salvos<div id="charList"></div></div>
      Novo personagem
      <input id="nameIn" maxlength="16" value="Herói">
      <div id="titleErr"></div>
      <div style="display:flex;gap:6px;justify-content:flex-end">
        <button id="btnNew">Criar e jogar</button>
      </div>''')
# saves por personagem
a=s.index("const SAVE_KEY='valhen_save_v2';");b=s.index("addEventListener('beforeunload',save);",a)
s=s[:a]+"""const SAVE_KEY='valhen_save_v2',CHARS_KEY='valhen_chars_v1';
function loadChars(){
  let ch={};try{ch=JSON.parse(localStorage.getItem(CHARS_KEY)||'{}')||{}}catch(e){}
  // save antigo (um personagem só) entra na lista uma vez
  try{const old=localStorage.getItem(SAVE_KEY);if(old){const o=JSON.parse(old);if(o&&o.name&&!ch[o.name])ch[o.name]=o;localStorage.setItem(CHARS_KEY,JSON.stringify(ch));localStorage.removeItem(SAVE_KEY)}}catch(e){}
  return ch;
}
function save(){if(!me||!started)return;try{const k=['name','xp','inv','eq','cards','zeny','learned','quests','hp','sp','last'];const o={};for(const x of k)o[x]=me[x];o.hot=hot;o.cb=me.cb;o.at=Date.now();const ch=loadChars();ch[me.name]=o;localStorage.setItem(CHARS_KEY,JSON.stringify(ch))}catch(e){}}
"""+s[b:]
# menu do Esc
rep("    case'escape':for(const w of['winStats','winInv','winSkill','winHelp','winShop','winDlg','winLearn','winGuild'])$(w).classList.add('hidden');pendingSkill=null;updCursor();break;",
    "    case'escape':{const ws=['winStats','winInv','winSkill','winHelp','winShop','winDlg','winLearn','winGuild'].filter(w=>!$(w).classList.contains('hidden'));\n      if(!$('winMenu').classList.contains('hidden'))closeMenu();else if(ws.length||pendingSkill){ws.forEach(w=>$(w).classList.add('hidden'));pendingSkill=null;updCursor()}else openMenu();break}")
rep("$('btnSound').onclick=()=>{muted=!muted;$('btnSound').textContent='Som: '+(muted?'off':'on')};",
    """function setMuted(v){muted=v;$('btnSound').textContent=$('mnSound').textContent='Som: '+(muted?'off':'on')}
$('btnSound').onclick=()=>setMuted(!muted);
function openMenu(){if(me&&me.dead)return;$('winMenu').classList.remove('hidden');$('menuShade').classList.remove('hidden');sfx('click')}
function closeMenu(){$('winMenu').classList.add('hidden');$('menuShade').classList.add('hidden')}
$('menuShade').onclick=closeMenu;
$('winMenu').querySelector('[data-close]').addEventListener('click',()=>$('menuShade').classList.add('hidden'));
$('mnBack').onclick=()=>{sfx('click');closeMenu()};
$('mnHelp').onclick=()=>{closeMenu();toggle('winHelp')};
$('mnSound').onclick=()=>{setMuted(!muted);sfx('click')};
$('mnChar').onclick=()=>{save();started=false;location.reload()};
$('mnQuit').onclick=()=>{save();started=false;closeMenu();$('closed').classList.remove('hidden');try{window.close()}catch(e){}};
$('btnReopen').onclick=()=>location.reload();""")
# tela inicial
rep("  const sv=loadSave();if(sv){$('btnCont').classList.remove('hidden');$('nameIn').value=sv.name||'Herói'}",
    """  const chars=loadChars(),names=Object.keys(chars).sort((a,b)=>(chars[b].at||0)-(chars[a].at||0));
  if(names.length){$('charBox').classList.remove('hidden');$('nameIn').value='';
    $('charList').innerHTML=names.map(n=>`<div class="ch"><span><b>${n.replace(/</g,'&lt;')}</b> <small style="color:#6a7698">Combate ${chars[n].cb||1} · ${fmt(chars[n].zeny||0)}c</small></span><button data-play="${esc(n)}">Jogar</button></div>`).join('');
    $('charList').onclick=e=>{const b=e.target.closest('[data-play]');if(!b)return;audio();sfx('click');startGame(chars[b.dataset.play])}}""")
rep("  $('btnNew').onclick=()=>{audio();sfx('click');const n=($('nameIn').value.trim()||'Herói').slice(0,16);startGame({name:n})};\n  $('btnCont').onclick=()=>{audio();sfx('click');startGame(sv)};",
    "  $('btnNew').onclick=()=>{audio();sfx('click');const n=$('nameIn').value.trim().slice(0,16);if(!n){$('titleErr').textContent='Digite um nome.';return}if(chars[n]){$('titleErr').textContent='Já existe um personagem com esse nome.';return}startGame({name:n})};")
rep("function loadSave(){try{const s=localStorage.getItem(SAVE_KEY);return s?JSON.parse(s):null}catch(e){return null}}\n","")
# ajuda menciona o Esc
rep("<b>Enter</b> conversar · <b>Esc</b> fecha janelas","<b>Enter</b> conversar · <b>Esc</b> fecha janelas ou abre o menu")
open(p,'w',encoding='utf-8').write(s);print('ok')
