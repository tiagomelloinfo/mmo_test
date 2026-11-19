# Troca sprHuman pela versão realista (fonte em tools/_sprHuman_real.js); camiseta com manga curta.
p='index.html';s=open(p,encoding='utf-8').read()
a=s.index("function sprHuman(o,dir,state,f){");b=s.index("function sprTree(kind){")
s=s[:a]+open('tools/_sprHuman_real.js',encoding='utf-8').read()+s[b:]
x="Object.assign(x,{tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34',print:'#3a6ac8'})"
if x in s:s=s.replace(x,"Object.assign(x,{tunic:'#f2f2f4',tunicD:'#c4c8d2',trim:'#3a6ac8',belt:'#2a2a34',print:'#3a6ac8',short:1})")
else: assert "print:'#3a6ac8',short:1" in s
open(p,'w',encoding='utf-8').write(s);print('ok')
