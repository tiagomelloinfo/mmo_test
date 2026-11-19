# Lodinho -> Slime; Lebre-Galhuda -> Lebre (lebre branca, sem chifres);
# Chapéu-Pulante (drop "esporo") -> Javali, com sprite de javali e presa como drop.
# Os ids internos (gelim, coelho, cogumelo, esporo) ficam iguais para não quebrar saves.
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90]);s=s.replace(a,b)

# ---------- nomes e textos
rep("carta_gelim:{name:'Essência de Lodinho'","carta_gelim:{name:'Essência de Slime'")
rep("gelim:{name:'Lodinho',","gelim:{name:'Slime',")
rep("g_gelim:{name:'Lodo na Horta',rank:0,pts:1,desc:'Os Lodinhos estão comendo","g_gelim:{name:'Slimes na Horta',rank:0,pts:1,desc:'Os Slimes estão comendo")
rep("felpa:{name:'Tufo de Pelo',type:'etc',icon:'fluff',price:22,desc:'Pelo macio de Lebre-Galhuda.'}","felpa:{name:'Tufo de Pelo',type:'etc',icon:'fluff',price:22,desc:'Pelo branco e macio de lebre.'}")
rep("carta_coelho:{name:'Essência de Lebre-Galhuda'","carta_coelho:{name:'Essência de Lebre'")
rep("coelho:{name:'Lebre-Galhuda',","coelho:{name:'Lebre',")
rep("desc:'As Lebres-Galhudas estão roubando","desc:'As lebres estão roubando")
rep("esporo:{name:'Pó de Chapéu',type:'etc',icon:'spore',price:36,desc:'Pó que cai do Chapéu-Pulante. Faz espirrar.'}",
    "esporo:{name:'Presa de Javali',type:'etc',icon:'tusk',price:36,desc:'Presa curva de javali. O artesão da vila faz amuletos com ela.'}")
rep("carta_cogumelo:{name:'Essência de Chapéu-Pulante'","carta_cogumelo:{name:'Essência de Javali'")
rep("cogumelo:{name:'Chapéu-Pulante',lv:12,el:'sombras',","cogumelo:{name:'Javali',lv:12,el:'terra',")
rep("spr:'mush',respawn:14","spr:'boar',respawn:14")
rep("(Lodinho perto do vilarejo, Lebre-Galhuda no meio, Chapéu-Pulante nas bordas)","(Slime perto do vilarejo, Lebre no meio, Javali nas bordas)")
rep("g_cogumelo:{name:'Chapéus no Bosque',rank:1,pts:3,desc:'Os Chapéus-Pulantes estão espalhando pó pelas bordas dos campos.'",
    "g_cogumelo:{name:'Javalis no Bosque',rank:1,pts:3,desc:'Os javalis estão revirando as plantações nas bordas dos campos.'")
rep("g_esporo:{name:'Pó para o Herbalista',rank:1,pts:1,rep:true,desc:'O herbalista estuda o pó dos chapéus. Pedido repetível.'",
    "g_esporo:{name:'Presas para o Artesão',rank:1,pts:1,rep:true,desc:'O artesão da vila faz amuletos com presas de javali. Pedido repetível.'")
rep("else if(d.spr==='mush')c=sprMush(fr);","else if(d.spr==='boar')c=sprBoar(fr);")

# ---------- ícone da presa
rep("    case'spore':",
"    case'tusk':p(1,7,2,3,'#6b4426');p(1,7,2,1,'#8e6034');p(3,8,2,2,'#f4ecd8');p(5,8.5,2,2,'#f4ecd8');p(7,8,2,2,'#e8dcc0');p(8.5,6.5,2,2,'#e8dcc0');p(9.5,5,1.5,2,'#d8c8a8');p(10,4,1,1,'#c8b898');p(3,8,6,.5,'#ffffff');p(3.5,9.5,5,.5,'#c8b898');break;\n    case'spore':")

# ---------- lebre branca (sem chifres)
a=s.index("function sprBunny(f){");b=s.index("function sprMush(f){")
s=s[:a]+"""function sprBunny(f){
  const c=scv(17,24),q=c.getContext('2d'),p=P(q),yo=[0,-2,-3,-1][f]+3,W=['#9a9aac','#d2d2de','#eeeef6','#ffffff'];
  // orelhas longas com o miolo rosado
  blob(q,9.5,4.5+yo,1.3,4.2,W);blob(q,12,5+yo,1.3,4,W);
  p(9.25,2+yo,.5,4.5,'#e8b4b8');p(11.75,2.5+yo,.5,4,'#e8b4b8');p(9.75,.75+yo,.5,.5,'#ffffff');p(12.25,1.5+yo,.5,.5,'#ffffff');
  p(9.5,7.5+yo,.5,.5,'#b8b8c8');p(12,8+yo,.5,.5,'#b8b8c8');
  // corpo, cabeça e rabo
  blob(q,8,15+yo,6,4.3,W);blob(q,11,10.5+yo,4.2,3.6,W);blob(q,2.5,14+yo,1.8,1.8,W);
  p(5,12.5+yo,4,.5,'#c2c2d0');p(4,17.5+yo,8,.5,'#b8b8c8');
  // olho escuro, focinho rosado e bigodes
  p(12.5,9+yo,1,1.5,'#2a1a24');p(12.5,9+yo,.5,.5,'#ffffff');p(12.75,10.25+yo,.5,.25,'#6a4a5a');
  p(14.5,11+yo,.75,.75,'#e89aa0');p(14,12+yo,1,.25,'#9a8a9a');
  p(14.5,12+yo,1.5,.25,'#c8c8d4');p(14.5,11.25+yo,1.5,.25,'#c8c8d4');
  // patas
  p(4,19+yo,3,1,W[1]);p(10,19+yo,3,1,W[1]);p(4,19.5+yo,3,.5,W[0]);p(10,19.5+yo,3,.5,W[0]);
  return outline(c,'#3a3448');
}
"""+s[b:]

# ---------- javali
a=s.index("function sprBeetle(f){")
s=s[:a]+"""function sprBoar(f){
  const c=scv(26,20),q=c.getContext('2d'),p=P(q),BR=['#2a1e18','#46342a','#66503e','#86705a'],yo=[0,-.5,0,-.5][f];
  // patas (pares alternados) com cascos
  const lift=[[0,1],[0,0],[1,0],[0,0]][f];
  for(const[x,i,dk]of[[5,0,1],[16,1,1],[7.5,1,0],[18.5,0,0]]){const l=lift[i];const col=dk?'#2a1e18':'#3a2a20';p(x,14.5+yo,2,4.5-l,col);p(x,18.5-l,2,1,'#1a1210');p(x+.25,15+yo,.5,2.5-l,'#4a382c')}
  // corpo
  blob(q,11.5,11+yo,8.5,5.2,BR);
  // crina eriçada no dorso
  for(let x=5;x<17;x+=.75){const h=1+((x*4)%3)*.4;p(x,6.2+yo-(x>8&&x<15?.5:0)-h*.5,.5,h,'#1e1612')}
  // barriga mais clara e pelos
  p(6,14.5+yo,10,.5,'#7a6250');for(const[x,y]of[[6,9],[9,8],[12,10],[8,12],[14,8],[11,13]])p(x,y+yo,.5,1,'#2e221a');
  // cabeça inclinada para a frente
  blob(q,19.5,11.5+yo,4.2,3.6,BR);
  p(16.75,5.5+yo,1.75,3,'#2a1e18');p(17,4.75+yo,1,.75,'#2a1e18');p(17.25,6+yo,.5,2,'#7a5a4a');
  // focinho, narinas, presa e boca
  p(22,11+yo,2.5,3,'#b08070');p(22,11+yo,2.5,.5,'#c89888');p(24,11+yo,.5,3,'#8a5a50');
  p(23,12+yo,.5,.5,'#3a2018');p(23,13+yo,.5,.5,'#3a2018');
  p(21,14+yo,2.5,.5,'#2a1a14');
  p(21,13+yo,1.25,1.25,'#f8f2e0');p(21.75,12+yo,1,1,'#f8f2e0');p(22.25,11+yo,.75,1,'#f8f2e0');p(22.5,10.5+yo,.5,.5,'#e8dcc0');p(21,14+yo,1.25,.25,'#c8b898');
  // olho
  p(19.25,9.75+yo,1.5,1.25,'#7a5a4a');p(19.5,10+yo,1,1,'#120c0a');p(19.5,10+yo,.5,.5,'#e8c8a8');
  // rabo
  p(2.5,9+yo,1,.5,'#2a1e18');p(2,9.5+yo,.5,1,'#2a1e18');p(1.5,10.5+yo,.5,.5,'#2a1e18');
  return outline(c,'#120c0a');
}
"""+s[a:]
open(p,'w',encoding='utf-8').write(s);print('ok')

# fala do Bento com os nomes novos
s=open(p,encoding='utf-8').read()
a="contra os <b>Lodinhos</b> aqui perto. Mais longe ficam as <b>Lebres-Galhudas</b> e os <b>Chapéus-Pulantes</b>."
assert s.count(a)==1
s=s.replace(a,"contra os <b>Slimes</b> aqui perto. Mais longe ficam as <b>Lebres</b> e os <b>Javalis</b>.")
open(p,'w',encoding='utf-8').write(s);print('ok 2')
