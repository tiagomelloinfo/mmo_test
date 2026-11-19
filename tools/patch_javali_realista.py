# Troca sprBoar pelo javali realista em 4x (fonte em tools/_sprBoar_real.js).
p='index.html';s=open(p,encoding='utf-8').read()
a=s.index("function sprBoar(f){");b=s.index("function sprBeetle(f){")
s=s[:a]+open('tools/_sprBoar_real.js',encoding='utf-8').read()+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok')
