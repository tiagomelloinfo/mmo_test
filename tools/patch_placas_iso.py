# Placas em isométrico: penduradas perpendiculares à parede, no canto da fachada, longe da porta.
# A tábua é desenhada reta e depois cisalhada coluna a coluna (sem borrar) no ângulo da parede.
import sys
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:110]); return
    s=s.replace(a,b,1)
rep("const fw=o.fw,fh=o.fh,WH=o.wh,RH=o.rh||0,ov=o.roof==='flat'?0:(o.ov??.35),M=6+Math.ceil(ov*32);",
    "const fw=o.fw,fh=o.fh,WH=o.wh,RH=o.rh||0,ov=o.roof==='flat'?0:(o.ov??.35),M=6+Math.ceil(ov*32)+(o.sign?12:0);")
a=s.index("  if(o.sign&&SPR.icons[o.sign]){\n    q.setTransform(K,0,0,K,0,0);const pq=P(q),L=o.door==='L';")
b=s.index("    q.setTransform(1,0,0,1,0,0);\n  }\n",a)+len("    q.setTransform(1,0,0,1,0,0);\n  }\n")
s=s[:a]+"""  if(o.sign&&SPR.icons[o.sign]){
    const L=o.door==='L',BW=15,BH=13,T0=1.5;
    // tábua reta: três tábuas com veio, moldura, medalhão pintado com o ícone e pregos
    const B=scv(BW,BH),bq=B.getContext('2d'),bp=P(bq),W0='#5a3a20',W1='#8a5a30',W2='#a8743e',W3='#c08a50';
    bp(0,0,BW,BH,W0);
    for(let r=0;r<3;r++){const ty=.5+r*4;bp(.5,ty,BW-1,4,r%2?W1:W2);bp(.5,ty,BW-1,.5,W3);bp(.5,ty+3.5,BW-1,.5,W0);
      for(let k=0;k<2;k++)bp(1.5+hash2(r,k,91)*(BW-6),ty+1.5+k,2.5+hash2(k,r,92)*3,.5,W1)}
    bp(0,0,.5,BH,'#3a2410');bp(BW-.5,0,.5,BH,'#3a2410');bp(0,BH-.5,BW,.5,'#3a2410');bp(0,0,BW,.5,'#3a2410');
    bq.clearRect(0,0,.5,.5);bq.clearRect(BW-.5,0,.5,.5);bq.clearRect(0,BH-.5,.5,.5);bq.clearRect(BW-.5,BH-.5,.5,.5);
    blob(bq,BW/2,BH/2,6,5.4,['#c8b48a','#e4d4a8','#f2e6c4','#fff6dc']);
    for(let a2=0;a2<6.28;a2+=.12)bp(BW/2+Math.cos(a2)*5.8,BH/2+Math.sin(a2)*5.2,.5,.5,'#7a4a20');
    const ic=SPR.icons[o.sign];bq.drawImage(ic,BW/2-6,BH/2-6,ic.width/K,ic.height/K);
    for(const[nx,ny]of[[1,1],[BW-1.5,1],[1,BH-1.5],[BW-1.5,BH-1.5]]){bp(nx,ny,.5,.5,'#d8d8e0');bp(nx+.5,ny+.5,.5,.5,'#4a4a52')}
    // ponto da parede: canto da fachada (lado oposto à porta), logo abaixo do beiral
    const u=o.doorAt<1?(L?fw:fh)-.12:.12,hA=WH-3;
    const wx=L?ox-fh*16+u*16:ox+fw*16-u*16,wy=(L?oy+(u+fh)*8:oy+(fw+u)*8)-hA;
    // para fora da parede: face L aponta para +y (esquerda-baixo na tela), face R para +x (direita-baixo)
    const dx=L?-1:1,dy=.5,Lr=T0+BW+1;
    q.setTransform(K,0,0,K,0,0);const pq=P(q);
    // braço de ferro com mão-francesa
    pq(wx-1,wy-1.5,2,3,'#2a2a30');
    line(pq,wx,wy,wx+dx*Lr,wy+dy*Lr,'#2a2a30');line(pq,wx,wy-.5,wx+dx*Lr,wy+dy*Lr-.5,'#6a6a76',.5);
    line(pq,wx,wy+5,wx+dx*7,wy+dy*7,'#2a2a30',.5);
    pq(wx+dx*Lr-.5,wy+dy*Lr-.5,1.5,1.5,'#3a3a44');
    // correntes até a tábua
    const top=2.5;
    for(const t of[T0+2,T0+BW-2]){const cx=wx+dx*t,cy=wy+dy*t;for(let yy=0;yy<top;yy+=.5)pq(cx,cy+yy,.5,.5,(yy*2)%2?'#6a6a74':'#b0b0bc')}
    q.setTransform(1,0,0,1,0,0);
    // tábua cisalhada no plano perpendicular à parede (coluna por coluna, sem borrar)
    const n=B.width;
    for(let i=0;i<n;i++){
      const tt=L?T0+BW-i/K:T0+i/K;             // distância da parede desta coluna
      const sx=Math.round((wx+dx*tt)*K),sy=Math.round((wy+dy*tt+top)*K);
      q.drawImage(B,i,0,1,B.height,L?sx:sx-1,sy,1,B.height);
    }
    // sombra da tábua na parede, logo abaixo do braço
    q.fillStyle='rgba(20,10,0,.18)';
    for(let i=0;i<n;i+=1){const tt=L?T0+BW-i/K:T0+i/K;if(tt>5)continue;const sx=Math.round((wx+dx*tt)*K),sy=Math.round((wy+dy*tt+top+BH+1)*K);q.fillRect(sx,sy,1,K*2)}
  }
"""+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok')
