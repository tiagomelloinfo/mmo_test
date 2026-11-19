# Corpo feminino e 20 penteados no sprHuman (tools/_sprHuman_real.js).
p='tools/_sprHuman_real.js';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:90];s=s.replace(a,b)
rep("  const hb=by+(state==='idle'&&f===1?.25:0);\n",
    "  const hb=by+(state==='idle'&&f===1?.25:0);\n  const FEM=o.sex==='f',HS=HAIRSTYLES[o.hs]||HAIRSTYLES.npc,HX=10,HY=1.5+hb;\n")
rep("  // ---- capa (atrás do corpo na vista de frente)\n",open('tools/_hair_helpers.js',encoding='utf-8').read()+"  // ---- capa (atrás do corpo na vista de frente)\n")
# cabelo comprido atrás do corpo (vista de frente)
rep("  // ---- tronco\n","  if(front&&!HS.buzz)longBack();\n  // ---- tronco\n")
# tronco feminino: ombros estreitos, cintura fina, quadril largo
rep("  const TW=[[6.9,1.7],[7.4,3.7],[8.1,4.9],[9.2,5.1],[11,4.7],[13,4],[14.6,3.65],[15.6,3.8],[16.6,4.05],[17.2,4.05]];",
    "  const TW=FEM?[[6.9,1.5],[7.4,3.2],[8.1,4.25],[9.2,4.5],[10.8,4.3],[12.6,3.45],[13.9,3.15],[15,3.6],[16,4.35],[16.8,4.6],[17.2,4.6]]:[[6.9,1.7],[7.4,3.7],[8.1,4.9],[9.2,5.1],[11,4.7],[13,4],[14.6,3.65],[15.6,3.8],[16.6,4.05],[17.2,4.05]];")
rep("  const cw=yy=>curve(TW,yy);\n",
    "  const cw=yy=>curve(TW,yy);\n  if(FEM&&front&&!o.armor)for(const cx of[8.55,11.45])for(let x=-1.3;x<1.3;x+=Q){const k=Math.sqrt(Math.max(0,1-(x/1.35)**2));px(cx+x,10.55+by+k*.95,TR[1]);if(Math.abs(x+.4)<.5)px(cx+x,9.9+by,TR[4])}\n")
# braços: mais finos e ombros mais estreitos no corpo feminino
rep("  const arm=(sx,sy,ex,ey,hx,hy2)=>{\n    limb(sx,sy,ex,ey,1.15,.95,",
    "  const AW=FEM?.86:1,SHL=FEM?5.75:5.2,SHR=20-SHL;\n  const arm=(sx,sy,ex,ey,hx,hy2)=>{\n    limb(sx,sy,ex,ey,1.15*AW,.95*AW,")
rep("limb(ex,ey,hx,hy2-.6,.95,.8,","limb(ex,ey,hx,hy2-.6,.95*AW,.8*AW,")
rep("ellipsoid(hx,hy2,.78,.9,skin);","ellipsoid(hx,hy2,.78*AW,.9*AW,skin);")
rep("  arm(5.2,8.4+by,4.55,12.7+by+aL*.3,4.75,17.4+by+aL);","  arm(SHL,8.4+by,SHL-.65,12.7+by+aL*.3,SHL-.45,17.4+by+aL);")
rep("const ex=(14.8+hand[0])/2+1.1,ey=(8.4+by+hand[1])/2;arm(14.8,8.4+by,ex,ey,hand[0],hand[1])","const ex=(SHR+hand[0])/2+1.1,ey=(8.4+by+hand[1])/2;arm(SHR,8.4+by,ex,ey,hand[0],hand[1])")
rep("  else arm(14.8,8.4+by,15.45,12.7+by+aR*.3,15.25,17.4+by+aR);","  else arm(SHR,8.4+by,SHR+.65,12.7+by+aR*.3,SHR+.45,17.4+by+aR);")
# cabeça e cabelo novos
a=s.index("  // ---- pescoço e cabeça");b=s.index("  // ---- chapéus")
s=s[:a]+open('tools/_hair_head.js',encoding='utf-8').read()+s[b:]
open(p,'w',encoding='utf-8').write(s);print('ok')
