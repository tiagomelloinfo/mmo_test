# Detalhes de meio pixel nos monstros e em alguns objetos do cenário.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,1)
# Lodinho: brilho, olhos com reflexo, boca e sombra na base
rep("  p(6,top+2,2,1,ramp[3]);p(5,top+3,1,2,ramp[3]);\n  const ey=Math.round(cy)-1;\n  p(7,ey,1,2,OUT);p(12,ey,1,2,OUT);p(9,ey+2,2,1,OUT);",
    "  p(6,top+2,2,1,ramp[3]);p(5,top+3,1,2,ramp[3]);p(6.5,top+1.5,1,.5,'#ffffff');p(5,top+3,.5,.5,'#ffffff');p(12.5,top+2.5,1,.5,ramp[3]);\n  const ey=Math.round(cy)-1;\n  p(4,h-2,12,.5,ramp[0]);p(6,h-1.5,8,.5,ramp[0]);\n  p(7,ey,1,2,OUT);p(12,ey,1,2,OUT);p(7,ey,.5,.5,'#ffffff');p(12,ey,.5,.5,'#ffffff');p(9,ey+2,2,.5,OUT);p(9.5,ey+2.5,1,.5,'#c0405a');")
rep("  if(sprout){const st=top-4;p(10,st+1,1,4,'#3a6a1e');p(7,st,3,2,'#6ab83a');p(8,st,1,1,'#a8e070');p(11,st-1,3,2,'#6ab83a');p(12,st-1,1,1,'#a8e070')}",
    "  if(sprout){const st=top-4;p(10,st+1,1,4,'#3a6a1e');p(10.5,st+1,.5,4,'#2a4a14');p(7,st,3,2,'#6ab83a');p(7,st+1.5,3,.5,'#3a7a22');p(8,st,1,1,'#a8e070');p(8.5,st+.5,1.5,.5,'#4a8a2a');p(11,st-1,3,2,'#6ab83a');p(11,st+.5,3,.5,'#3a7a22');p(12,st-1,1,1,'#a8e070');p(11.5,st-.5,1.5,.5,'#4a8a2a')}")
# Lebre-Galhuda: orelha interna, galhos com pontas, focinho, bigode e pelagem
rep("  const A='#e8dcc0',a=(x,y,w,h)=>p(x,y+yo,w,h,A);a(8,1,1,6);a(7,1,1,1);a(9,2,2,1);a(11,0,1,6);a(10,0,1,1);a(12,1,2,1);",
    "  p(5.5,4+yo,.5,4,'#d89a8a');p(12,4+yo,.5,4,'#d89a8a');\n  const A='#e8dcc0',a=(x,y,w,h)=>p(x,y+yo,w,h,A);a(8,1,1,6);a(7,1,1,1);a(9,2,2,1);a(11,0,1,6);a(10,0,1,1);a(12,1,2,1);a(8.5,1,.5,6);p(8.5,1+yo,.5,6,'#c8b898');p(11.5,0+yo,.5,6,'#c8b898');p(6.5,.5+yo,.5,.5,'#fff8ec');p(13.5,.5+yo,.5,.5,'#fff8ec');")
rep("  p(12,9+yo,1,2,OUT);p(14,11+yo,1,1,'#5a3a22');",
    "  p(12,9+yo,1,2,OUT);p(12,9+yo,.5,.5,'#ffffff');p(14,11+yo,1,1,'#5a3a22');p(14.5,11+yo,.5,.5,'#f0a0a0');p(13.5,12+yo,1.5,.5,'#5a3a22');\n  p(14,12.5+yo,2,.5,'#f8f0e0');p(14,11.5+yo,2,.25,'#f8f0e0');for(const[x,y]of[[5,13],[7,12],[9,14],[4,16],[11,15]])p(x,y+yo,.5,1,'#6e4c30');")
# Chapéu-Pulante: lamelas, pintas e brilho
rep("  p(2,12+yo,14,1,'#2a1040');\n  p(4,8+yo,10,1,'#e8c84a');p(6,5+yo,6,1,'#e8c84a');",
    "  p(2,12+yo,14,1,'#2a1040');for(let x=3;x<15;x+=1.5)p(x,12.5+yo,.5,.5,'#5a3a7a');\n  p(4,8+yo,10,1,'#e8c84a');p(4,8.5+yo,10,.5,'#b8982a');p(6,5+yo,6,1,'#e8c84a');p(6,5.5+yo,6,.5,'#b8982a');\n  p(5,6.5+yo,1,1,'#d0b0f8');p(12,6+yo,1,1,'#d0b0f8');p(9,3+yo,1,.5,'#ffffff');p(6,4+yo,.5,.5,'#ffffff');\n  p(7,14+yo,1,2,OUT);p(7,14+yo,.5,.5,'#ffffff');p(10,14+yo,.5,.5,'#ffffff');p(8.5,18+yo,1,.5,'#8a6040');")
# Besouro-Arado: brilho no casco e pontos
rep("  p(11,4,1,10,R.beetle[0]);p(6,5,3,1,R.beetle[3]);p(5,6,1,1,R.beetle[3]);",
    "  p(11,4,1,10,R.beetle[0]);p(6,5,3,1,R.beetle[3]);p(5,6,1,1,R.beetle[3]);p(6.5,5,1,.5,'#ffffff');p(13,6,2,.5,R.beetle[2]);for(const[x,y]of[[7,9],[9,11],[14,9],[15,12]])p(x,y,.5,.5,R.beetle[3]);")
# árvores: casca com veios
rep("  p(16,30,6,16,'#6b4426');p(20,30,2,16,'#4a2e18');p(17,30,1,16,'#87582f');",
    "  p(16,30,6,16,'#6b4426');p(20,30,2,16,'#4a2e18');p(17,30,1,16,'#87582f');for(let y=32;y<44;y+=3)p(18.5,y,.5,1.5,'#4a2e18');p(16.5,36,.5,2,'#4a2e18');p(19.5,40,.5,2,'#87582f');")
open(p,'w',encoding='utf-8').write(s);print('ok')
