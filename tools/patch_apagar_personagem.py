# Botão para apagar personagem na tela inicial, com confirmação.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
a=s.index("  const chars=loadChars(),names=");b=s.index("startGame(chars[b.dataset.play])}}",a)+len("startGame(chars[b.dataset.play])}}")
s=s[:a]+"""  const chars=loadChars();let delAsk=null;
  const drawChars=()=>{const names=Object.keys(chars).sort((a,b)=>(chars[b].at||0)-(chars[a].at||0));
    $('charBox').classList.toggle('hidden',!names.length);
    $('charList').innerHTML=names.map(n=>{const nm=n.replace(/</g,'&lt;');return delAsk===n
      ?`<div class="ch"><span style="color:#c03030">Apagar <b>${nm}</b> para sempre?</span><span><button data-delok="${esc(n)}">Apagar</button><button data-delno="1">Cancelar</button></span></div>`
      :`<div class="ch"><span><b>${nm}</b> <small style="color:#6a7698">Combate ${chars[n].cb||1} · ${fmt(chars[n].zeny||0)}c</small></span><span><button data-play="${esc(n)}">Jogar</button><button data-del="${esc(n)}" title="Apagar personagem">Apagar</button></span></div>`}).join('')};
  if(Object.keys(chars).length)$('nameIn').value='';
  drawChars();
  $('charList').onclick=e=>{
    const b=e.target.closest('[data-play]');if(b){audio();sfx('click');startGame(chars[b.dataset.play]);return}
    const d=e.target.closest('[data-del]');if(d){delAsk=d.dataset.del;drawChars();return}
    const ok=e.target.closest('[data-delok]');if(ok){const n=ok.dataset.delok;delete chars[n];try{const all=loadChars();delete all[n];localStorage.setItem(CHARS_KEY,JSON.stringify(all))}catch(er){}delAsk=null;drawChars();return}
    if(e.target.closest('[data-delno]')){delAsk=null;drawChars()}};"""+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok')
