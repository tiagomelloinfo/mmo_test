# Zoom com a roda do mouse: aproxima até 2x; a distância máxima é a escala original.
p='index.html';s=open(p,encoding='utf-8').read()
a="let SCALE=2,W=0,H=0;\nfunction resize(){SCALE=innerWidth>=3000?4:2;"
b="let SCALE=2,W=0,H=0,ZOOM=1;\nfunction resize(){SCALE=(innerWidth>=3000?4:2)*ZOOM;"
assert a in s;s=s.replace(a,b)
a="cv.addEventListener('mouseleave',"
b=("cv.addEventListener('wheel',e=>{e.preventDefault();if(!started)return;"
   "const z=Math.min(2,Math.max(1,ZOOM+(e.deltaY<0?.25:-.25)));if(z===ZOOM)return;ZOOM=z;resize();"
   "mouse.x=e.clientX/SCALE;mouse.y=e.clientY/SCALE},{passive:false});\n"+a)
assert s.count(a)==1;s=s.replace(a,b)
open(p,'w',encoding='utf-8').write(s);print('ok')
