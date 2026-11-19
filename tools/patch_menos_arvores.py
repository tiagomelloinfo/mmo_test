# Menos árvores nos dois mapas (cerca de metade a um terço da densidade anterior).
p='index.html';s=open(p,encoding='utf-8').read()
R=[("if(x>=70&&Math.random()<(x>=74?.5:.25)){","if(x>=70&&Math.random()<(x>=74?.15:.08)){"),
   ("if(y<5&&x>50&&Math.random()<.7){","if(y<5&&x>50&&Math.random()<.3){"),
   ("if(edge<2){if(edge===0||Math.random()<.85)addObj","if(edge<2){if(edge===0?Math.random()<.7:Math.random()<.3)addObj"),
   ("if(f>.6&&dc>18&&Math.random()<.55)addObj","if(f>.6&&dc>18&&Math.random()<.2)addObj"),
   ("else if(Math.random()<.022)addObj('tree'","else if(Math.random()<.01)addObj('tree'"),
   ("if(e<4||(w<3&&Math.abs(y-47.5)>2)){if(Math.random()<.9)addObj","if(e<3||(w<2&&Math.abs(y-47.5)>2)){if(Math.random()<.6)addObj"),
   ("if(Math.random()<(f>.55?.42:.07))addObj","if(Math.random()<(f>.55?.12:.025))addObj")]
for a,b in R:
    assert s.count(a)==1,a;s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s);print('ok')
