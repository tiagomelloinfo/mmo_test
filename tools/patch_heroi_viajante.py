# Herói baseado na arte de referência: cabelo castanho com fio arrepiado, olhos verdes,
# e o Traje de Viajante (jaqueta verde com capa e capuz; calça bege bufante com botas altas).
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:80]);s=s.replace(a,b)

rep("  hero:{spiky:1},","  hero:{hair:['#4a301c','#7a5532','#a87c4c'],eye:'#3e7a44',ahoge:1},")

# capa atrás do corpo (vista de frente): desenhada antes das pernas
rep("  if(!front)weapon();\n  // pernas e pés",
"""  if(!front)weapon();
  const CP=o.cape,CPD=CP&&shade(CP),CPL=CP&&lighten(CP,1.2);
  if(CP&&front&&state!=='sit'){p(3,13+by,14,11-by,CPD);p(3,13+by,1,11-by,CP);p(16,13+by,1,11-by,shade(CPD));
    for(let x=3;x<17;x+=1.5)p(x,23.5+((x*7)%3)*.5,1,.5,CPD)}
  // pernas e pés""")

# calça bufante e botas altas
rep("    if(o.legsJeans){p(x+.5,y,.5,3.5,'#5a7ab8');p(x+2,y+.5,.5,3,'#d8b040')}\n",
"""    if(o.legsJeans){p(x+.5,y,.5,3.5,'#5a7ab8');p(x+2,y+.5,.5,3,'#d8b040')}
    if(o.tallBoot){p(x-.5,y,4,2.5,PA);p(x+2.5,y,1,2.5,PD);p(x-.5,y+.5,.5,1.5,PL);p(x,y+2.5,3,.5,PD);
      p(x,y+3,3,3,BO);p(x+2,y+3,1,3,BD);p(x+.5,y+3,.5,2.5,BL);p(x-.25,y+2.75,3.5,.5,lighten(BO,1.5));p(x,y+5.5,3.5,.5,BD);return}
""")

# bolsos, alça e bolsa na jaqueta
rep("  p(6,19+by,8,1,o.belt);p(6,19.5+by,8,.5,shade(o.belt));if(front){p(9,19+by,2,1,'#c89a30');p(9.5,19+by,1,.5,'#fff0a0')}",
"""  if(o.pockets&&front){for(const px of[6.5,10.5]){p(px,14.5+by,2.5,2,TD);p(px,14.5+by,2.5,.5,TL);p(px+1,15+by,.5,.5,'#c8a060')}
    p(6.5,17.5+by,2.5,1.5,TD);p(10.5,17.5+by,2.5,1.5,TD);for(let y=14;y<19;y+=1.5)p(9.75,y+by,.5,.5,'#5a3a20')}
  p(6,19+by,8,1,o.belt);p(6,19.5+by,8,.5,shade(o.belt));if(front){p(9,19+by,2,1,'#c89a30');p(9.5,19+by,1,.5,'#fff0a0')}
  if(o.strap&&front){ln(7,13+by,13,19+by,'#5a3a20',.5);ln(7.5,13+by,13.5,19+by,'#7a5432',.5);p(12.5,19.5+by,2,2.5,'#7a5432');p(12.5,19.5+by,2,.5,'#9a7048');p(13,20.5+by,1,.5,'#c8a060');p(5.5,19.5+by,1.5,2,'#6a4628')}""")

# capa por cima (costas) e capuz caído (frente e costas)
rep("  // cabeça\n  p(5,2+hb,10,10,S);",
"""  if(CP&&state!=='sit'){
    if(!front){p(3,13+by,14,11-by,CP);p(13,13+by,4,11-by,CPD);p(3,13+by,.5,11-by,CPL);for(const x of[6,9,12])p(x,15+by,.5,8-by,CPD);
      for(let x=3;x<17;x+=1.5)p(x,23.5+((x*7)%3)*.5,1,.5,CP);p(5,11.5+hb,10,3,CP);p(5,13.5+hb,10,.5,CPD);p(6,12+hb,8,.5,CPL)}
    else{p(4,12+by,12,2,CP);p(4,13.5+by,12,.5,CPD);p(4.5,12+by,11,.5,CPL);p(9,13+by,2,1,'#c89a30');p(9.5,13+by,1,.5,'#fff0a0')}}
  // cabeça
  p(5,2+hb,10,10,S);""")

# fio arrepiado
rep("  if(o.spiky){",
"  if(o.ahoge){p(9.5,0+hb,1,1,H1);p(10,-1+hb,1,1,H1);p(10.5,-1.5+hb,1,.5,H1);p(11,-2+hb,.5,.5,H2);p(10,-.5+hb,.5,.5,H2)}\n  if(o.spiky){")

# itens
rep("  cota:{name:'Cota Acolchoada'",
"""  jaqueta:{name:'Jaqueta de Viajante',type:'armor',icon:'jacket',def:5,price:600,desc:'Lona verde com bolsos, alça de couro e uma capa com capuz para a estrada. DEF +5'},
  calca_v:{name:'Calça de Viajante',type:'legs',icon:'pants_v',def:3,price:320,desc:'Calça bufante de linho com botas altas de couro. DEF +3'},
  cota:{name:'Cota Acolchoada'""")
rep("const SHOP=['pocao_v','pocao_l','pocao_a','asa_mosca','asa_borb','roupa',",
    "const SHOP=['pocao_v','pocao_l','pocao_a','asa_mosca','asa_borb','roupa','jaqueta','calca_v',")
rep("    case'shirt':",
"""    case'jacket':p(0,1,12,10,'#4a3a2c');p(2,2,8,9,'#4a7a3a');p(0,2,2,5,'#4a7a3a');p(10,2,2,5,'#4a7a3a');p(8,2,2,9,'#33582a');p(3,4,2,2,'#33582a');p(7,4,2,2,'#33582a');p(3,2,6,1,'#5a3a20');p(5.5,3,1,8,'#5a3a20');p(2,8,8,1,'#5a3a20');break;
    case'pants_v':p(1,1,10,2,'#d8ccb0');p(1,3,4,5,'#d8ccb0');p(7,3,4,5,'#b0a284');p(1,1,10,1,'#5a3a20');p(2,8,3,3,'#2a2420');p(7,8,3,3,'#2a2420');p(2,8,3,1,'#5a5048');p(7,8,3,1,'#5a5048');break;
    case'shirt':""")
rep("    else if(me.eq.armor==='cota')",
    "    else if(me.eq.armor==='jaqueta')Object.assign(x,{tunic:'#4a7a3a',tunicD:'#33582a',trim:'#5a3a20',belt:'#5a3a20',cape:'#4a3a2c',pockets:1,strap:1});\n    else if(me.eq.armor==='cota')")
rep("    if(me.eq.legs==='jeans')",
    "    if(me.eq.legs==='calca_v')Object.assign(x,{pants:'#d8ccb0',pantsD:'#b0a284',boot:'#2e2622',tallBoot:1});\n    if(me.eq.legs==='jeans')")
open(p,'w',encoding='utf-8').write(s);print('ok')

# capuz caído nas costas por cima do pescoço (vista de costas)
s=open(p,encoding='utf-8').read()
a="  // chapéus\n"
assert s.count(a)==1
s=s.replace(a,"  if(CP&&!front&&state!=='sit'){p(5,12+hb,10,2.5,CP);p(6,12+hb,8,.5,CPL);p(5,14+hb,10,.5,CPD);p(13,12+hb,2,2.5,CPD)}\n"+a)
open(p,'w',encoding='utf-8').write(s);print('ok 2')
