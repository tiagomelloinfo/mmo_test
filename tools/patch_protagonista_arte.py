# O protagonista passa a usar a folha desenhada à mão (assets/personagem/protagonista),
# com a arma equipada desenhada por cima (atrás, na vista de costas).
import json
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:90];s=s.replace(a,b)
rep("const ASSETS={ok:false,layers:{},npc:{},mon:{},ground:{},rooms:{}};","const ASSETS={ok:false,layers:{},npc:{},mon:{},ground:{},rooms:{},heroArt:null};")
rep("  const gs=await Promise.all(Object.values(man.chao).map(f=>loadImg('assets/'+f)));",
    "  if(man.protagonista){const sh=await loadSheet(man.protagonista);ASSETS.heroArt={};for(const n in sh)ASSETS.heroArt[n]=sh[n].c}\n  const gs=await Promise.all(Object.values(man.chao).map(f=>loadImg('assets/'+f)));")
rep("  const arm=eq.armor||'nenhuma',legs=eq.legs||'nenhuma',wpn=conjEl?(CONJ[conjEl].wt==='desarmado'?null:'cj_'+conjEl):eq.weapon,pose=dir+'_'+state+'_'+f;\n",
"""  const arm=eq.armor||'nenhuma',legs=eq.legs||'nenhuma',wpn=conjEl?(CONJ[conjEl].wt==='desarmado'?null:'cj_'+conjEl):eq.weapon,pose=dir+'_'+state+'_'+f;
  if(ASSETS.heroArt){const art=ASSETS.heroArt[pose]||ASSETS.heroArt[dir+'_idle_0'];
    return cached(['ha',wpn,pose].join('|'),()=>{const wl=wpn&&ASSETS.layers['arma_'+wpn]&&ASSETS.layers['arma_'+wpn][pose];if(!wl)return art;
      const wo=outline(wl,'#1a1020',2),k=art.k,c=canvas(art.width,art.height);c.k=k;const q=c.getContext('2d');q.imageSmoothingEnabled=false;const dw=wo.width/KH*k,dh=wo.height/KH*k;
      if(dir==='b'){q.drawImage(wo,0,0,dw,dh);q.drawImage(art,0,0)}else{q.drawImage(art,0,0);q.drawImage(wo,0,0,dw,dh)}return c})}
""")
open(p,'w',encoding='utf-8').write(s)
m='assets/manifesto.json';man=json.load(open(m,encoding='utf-8'));man['protagonista']='personagem/protagonista';json.dump(man,open(m,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
