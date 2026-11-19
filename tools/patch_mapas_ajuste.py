# Montanhas mais maciças e menos pontudas, luz mais suave; entulho com pedras de verdade.
p='index.html';s=open(p,encoding='utf-8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:90];s=s.replace(a,b)
rep("    let h=Math.pow(1-r,1.1)*H;h*=.8+fbm(gx*.8+seed*7,gy*.8,62)*.4;h+=(vnoise(gx*2.4+seed,gy*2.4,63)-.5)*H*.1*(1-r);return Math.max(0,h)};",
    "    const b=1-r;let h=(b*.55+Math.sqrt(b)*.45)*H*(.62+fbm(gx*1.1+seed*7,gy*1.1,62)*.62);h+=(vnoise(gx*2.8+seed,gy*2.8,63)-.5)*H*.16*b;return Math.max(0,h)};")
rep("    let lit=.5+lx*.4-ly*.2+(nz-.5)*.3+Math.sin(h*.5+nz*5)*.07;","    let lit=.6+lx*.26-ly*.12+(nz-.5)*.3+Math.sin(h*.5+nz*5)*.06;")
rep("    else col=ROCK[clamp(Math.round(lit*6.4),0,6)];","    else col=ROCK[clamp(Math.round(.6+lit*5.4),0,6)];")
rep("  SPR.mount={1:[0,1,2].map(i=>sprMount(1,1,18+i*5,i*3.1,false)),2:[0,1,2].map(i=>sprMount(2,2,34+i*8,10+i*2.7,false)),3:[0,1,2].map(i=>sprMount(3,3,54+i*10,20+i*1.9,i===2)),4:[0,1].map(i=>sprMount(4,4,78+i*14,30+i*4.3,true))};",
    "  SPR.mount={1:[0,1,2].map(i=>sprMount(1,1,13+i*4,i*3.1,false)),2:[0,1,2].map(i=>sprMount(2,2,24+i*6,10+i*2.7,false)),3:[0,1,2].map(i=>sprMount(3,3,38+i*7,20+i*1.9,i===2)),4:[0,1].map(i=>sprMount(4,4,54+i*10,30+i*4.3,true))};")
rep("function sprBoulder(seed){const c=scv(24,17),q=c.getContext('2d');blob(q,12,10,10,6,R.rock);blob(q,5+seed%3,12,4,3,R.rock);blob(q,18,13,4.5,3,R.stone);blob(q,9,14,6,2.4,R.brown,{maxY:16});return outline(c,'#1e1c22')}",
    "function sprBoulder(seed){const c=scv(26,20),q=c.getContext('2d'),RK=['#3e3836','#5c5450','#7e746a','#a09484'];const pts=[[8,12,6,5],[17,11,7,6],[12,7,5,4],[21,15,4,3],[5,16,4,3]];for(let i=0;i<pts.length;i++){if((seed+i)%4===3)continue;const[x,y,rx,ry]=pts[i];blob(q,x+seed%2,y,rx,ry,i%2?R.rock:RK)}blob(q,13,17,10,2,['#4a3a2a','#5e4a34','#6e5a40','#7e6a4a'],{maxY:19});return outline(c,'#1e1c22')}")
open(p,'w',encoding='utf-8').write(s);print('ok')

s=open(p,encoding='utf-8').read()
rep("    if(x>=70&&Math.random()<(x>=74?.5:.25)){","    if(x>=70&&Math.abs(y+.5-48)<3.6)continue;\n    if(x>=70&&Math.random()<(x>=74?.5:.25)){")
rep("  const t=TIME;g.save();g.globalCompositeOperation='lighter';",
    "  const t=TIME;g.save();g.globalAlpha=.55;g.strokeStyle='#bfe6ff';g.lineWidth=1.5;g.beginPath();g.ellipse(s.x,s.y,15,7.5,0,0,7);g.stroke();g.strokeStyle='#3a6aff';g.beginPath();g.ellipse(s.x,s.y,18,9,0,0,7);g.stroke();g.globalCompositeOperation='lighter';")
open(p,'w',encoding='utf-8').write(s);print('ok 2')
