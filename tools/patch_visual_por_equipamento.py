# O visual do herói vem só do que está equipado: sem calça equipada, pernas e pés descalços
# (antes aparecia a calça roxa padrão). Sem arma: mãos vazias (já era assim).
p='index.html';s=open(p,encoding='utf-8').read()
a="    if(me.eq.legs==='calca_v')"
assert s.count(a)==1
s=s.replace(a,"    if(!me.eq.legs)Object.assign(x,{pants:'#f8d0b0',pantsD:'#e0a888',boot:'#f8d0b0',bareLegs:1});\n"+a)
open(p,'w',encoding='utf-8').write(s);print('ok')
