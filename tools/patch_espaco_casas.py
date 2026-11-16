# Vilarejo maior (CW 12), casas mais espaçadas e mais altas; portas sempre livres.
import sys,re
p=sys.argv[1];s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    if a not in s: print('NAO ACHOU:',a[:100]); return
    s=s.replace(a,b,1)
a=s.index("const BUILDINGS=[");b=s.index("];",a)+2
s=s[:a]+"""const BUILDINGS=[
  {id:'tower',name:'Cabana da Sábia',room:'tower',bx:-11,by:-10,spec:{fw:3,fh:3,wh:28,rh:30,roof:'pyr',rr:R.purple,wall:'stone',door:'L',doorAt:1.5,ov:.3,sign:'sign_magic'}},
  {id:'school',name:'Galpão de Treino',room:'school',bx:-6,by:-10,spec:{fw:3,fh:3,wh:30,rh:22,roof:'gable',rr:R.red,wall:'log',door:'L',doorAt:1.5,win:false,sign:'sword'}},
  {id:'tavern',name:'Taverna do Caneco',room:'tavern',bx:2,by:-10,spec:{fw:4,fh:3,wh:32,rh:24,roof:'gable',rr:R.straw,wall:'timber',door:'L',doorAt:1.5,sign:'sign_tavern'}},
  {id:'shop',name:'Venda do Tomas',room:'shop',bx:8,by:-10,spec:{fw:3,fh:3,wh:28,rh:20,roof:'gable',rr:R.red,wall:'timber',door:'L',doorAt:1.5,sign:'potion_r'}},
  {id:'chapel',name:'Capelinha',bx:-11,by:1,spec:{fw:3,fh:3,wh:32,rh:24,roof:'gable',rr:R.straw,wall:'plaster',wc:'#f6f2ea',door:'R',doorAt:1.5,sign:'a_cura'}},
  {id:'inn',name:'Hospedaria do Sabiá',room:'inn',bx:4,by:4,spec:{fw:4,fh:3,wh:30,rh:22,roof:'gable',rr:R.brown,wall:'plaster',wc:'#efe2c8',door:'L',doorAt:1.5,sign:'sign_inn'}},
  {id:'h3',bx:-11,by:7,spec:{fw:3,fh:3,wh:28,rh:20,roof:'gable',rr:R.straw,wall:'timber',door:'R',doorAt:1.5}},
];"""+s[b:]
rep("const N=96,C=48,CW=10,","const N=96,C=48,CW=12,")
rep("if(cheb(x,y)<12)continue;","if(cheb(x,y)<14)continue;")
rep("['gelim',26,13,28]","['gelim',26,15,30]")
rep("    if(dc<11.5)continue;","    if(dc<13.5)continue;")
rep("    if(cheb(x,y)>14){if(w>.64)t=T_WATER;","    if(cheb(x,y)>16){if(w>.64)t=T_WATER;")
rep("addObj('barrel',C+6,C-3,{spr:SPR.barrel});addObj('barrel',C+2,C-5,{spr:SPR.barrel});","addObj('barrel',C+6,C-4,{spr:SPR.barrel});addObj('barrel',C+1,C-5,{spr:SPR.barrel});")
a=s.index("  // hortas, feno e uma carroça");b=s.index("\n",s.index("addObj('bush',a,b,{spr:SPR.bush});",a))+1
s=s[:a]+"""  // hortas, feno e uma carroça
  for(let y=C+9;y<=C+10;y++)for(let x=C+3;x<=C+9;x++){if(block[gi(x,y)])continue;ground[gi(x,y)]=T_DIRT;addObj('crop',x,y,{spr:SPR.crops[(x*7+y*3)%3]})}
  for(let y=C-4;y<=C-3;y++)for(let x=C+8;x<=C+10;x++){ground[gi(x,y)]=T_DIRT;addObj('crop',x,y,{spr:SPR.crops[(x+y)%3]})}
  for(const[a,b]of[[C-9,C-3],[C-8,C-4],[C+9,C+2],[C-5,C+7]])addObj('hay',a,b,{spr:SPR.hay});
  addObj('cart',C+3,C+1,{spr:SPR.cart});
  for(const[a,b]of[[C-6,C+10],[C+10,C+4],[C-11,C-4],[C-3,C+10]])addObj('tree',a,b,{spr:pick(SPR.trees.oak)});
  for(const[a,b]of[[C-3,C-11],[C+4,C+2],[C-6,C+5]])addObj('bush',a,b,{spr:SPR.bush});
  // a frente de cada porta fica sempre livre
  for(const d of DOORS){const k=gi(d.ox,d.oy);for(let i=objects.length-1;i>=0;i--){const o=objects[i];if(!o.box&&Math.floor(o.x)===d.ox&&Math.floor(o.y)===d.oy)objects.splice(i,1)}block[k]=0}
"""+s[b:]
rep("mk('healer','Irmã Liesel','priest',-5,3)","mk('healer','Irmã Liesel','priest',-7,3)")
rep("mk('guard','Seu Bento, o Vigia','guard',2,10)","mk('guard','Seu Bento, o Vigia','guard',2,12)")
rep("me.x=C+.5;me.y=C+12.5;","me.x=C+.5;me.y=C+13.5;")
open(p,'w',encoding='utf-8').write(s);print('ok')
