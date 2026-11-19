// javali realista em 4x: volume por iluminação esférica, pelo em mechas, crina, presas e patas articuladas
function sprBoar(f){
  const LW=30,LH=22,c=hcv(LW,LH),q=c.getContext('2d'),Q=.25;
  const px=(x,y,col)=>{q.fillStyle=col;q.fillRect(Math.floor(x*4+1e-6)/4,Math.floor(y*4+1e-6)/4,Q,Q)};
  const hsh=(a,b)=>{let h=(a*374761393+b*668265263)^0x5bd1e995;h=Math.imul(h^(h>>>13),1274126177);return((h^(h>>>16))>>>0)/4294967296};
  const F=['#120d0b','#1d1512','#2a1f19','#3a2b22','#4c3a2e','#5f4b3c','#76604e','#8e7a66','#a89682'];
  const fur=(l,x,y,grizzle)=>{
    // mechas inclinadas para trás e para baixo, com pontas claras
    const s=hsh(Math.round(x*4+y*1.2),Math.floor((y*4+x*2)/6)),s2=hsh(Math.round(x*4+y*1.2)+9,Math.floor((y*4+x*2+3)/6)),t=hsh(Math.floor(x*4),Math.floor(y*4));
    let i=l*7.4+(s-.5)*1.1+(s2-.5)*.5;if(grizzle&&t>.93)i+=1.5;
    return F[Math.max(0,Math.min(F.length-1,Math.round(i)))]};
  const Lx=-.45,Ly=-.62,Lz=.64;
  const bob=[0,-.25,0,-.25][f];
  // ---------- silhueta do corpo: linha do dorso e da barriga por pontos de controle
  const curve=(pts,x)=>{if(x<=pts[0][0])return pts[0][1];for(let i=1;i<pts.length;i++)if(x<=pts[i][0]){const[x0,y0]=pts[i-1],[x1,y1]=pts[i],t=(x-x0)/(x1-x0),k=(1-Math.cos(t*Math.PI))/2;return y0+(y1-y0)*k}return pts[pts.length-1][1]};
  const TOP=[[2.2,10.4],[3,8.9],[5,7.7],[9,6.7],[13,5.4],[16,4.5],[18.5,4.9],[21,6.2],[22.5,7.4]];
  const BOT=[[2.2,11.2],[3,13],[4.5,14.6],[8,15.5],[13,15.7],[17.5,15.5],[20.5,14.8],[22.5,13.8]];
  const ell=(x,y)=>{if(x<2.2||x>22.5)return null;const t0=curve(TOP,x)+bob,b0=curve(BOT,x)+bob;if(y<t0||y>b0)return null;
    const ny=(y-t0)/(b0-t0)*2-1,ex=x<5?(5-x)/2.8:0;const nx=-Math.min(1,ex);const d=Math.min(1,ny*ny+nx*nx);return{d,dx:nx,dy:ny}};
  const shadeE=(b)=>{const nz=Math.sqrt(Math.max(0,1-b.d));return Math.max(0,b.dx*Lx+b.dy*Ly+nz*Lz)};
  // ---------- patas: segmentos afinando, coxa grossa e canela fina
  const sw=[[.9,-.9,-.9,.9],[0,0,0,0],[-.9,.9,.9,-.9],[0,0,0,0]][f],lift=[[0,0,0,0],[.6,0,0,.6],[0,0,0,0],[0,.6,.6,0]][f];
  const seg=(x0,y0,x1,y1,w0,w1,far)=>{const n=Math.ceil(Math.hypot(x1-x0,y1-y0)*8);
    for(let i=0;i<=n;i++){const t=i/n,cx=x0+(x1-x0)*t,cy=y0+(y1-y0)*t,r=(w0+(w1-w0)*t)/2;
      for(let y=Math.floor((cy-r)*4)/4;y<=cy+r;y+=Q)for(let x=Math.floor((cx-r)*4)/4;x<=cx+r;x+=Q){
        const dx=(x+.125-cx)/r,dy=(y+.125-cy)/r;if(dx*dx+dy*dy>1)continue;
        const l=(far?.12:.3)+(-dx)*.22+(t<.5?.06:0);px(x,y,fur(l,x,y,false))}}};
  const hoof=(x,y,far)=>{for(let yy=0;yy<1;yy+=Q)for(let xx=-.75;xx<.75;xx+=Q){const w=.55+yy*.2;if(Math.abs(xx+.125)>w)continue;px(x+xx,y+yy,yy<.25?'#3a302c':far?'#0e0a09':'#16110f')}
    px(x-.125,y+.25,'#060404');px(x-.875,y-.5,far?'#16110f':'#241c18')};
  const legF=(x,swing,lf,far)=>{const fx=x+swing,fy=19.4-lf;seg(x,14.4+bob,x+.15+swing*.3,16.9+bob-lf*.5,1.7,1.05,far);seg(x+.15+swing*.3,16.9+bob-lf*.5,fx,fy,.95,.75,far);hoof(fx,fy,far)};
  const legH=(x,swing,lf,far)=>{const kx=x-1.1+swing*.4,ky=16.8+bob-lf*.5,fx=x-.4+swing,fy=19.4-lf;seg(x-.3,14+bob,kx,ky,2.2,1.2,far);seg(kx,ky,fx,fy,.95,.75,far);hoof(fx,fy,far)};
  // pernas do lado de lá (mais escuras)
  legF(16.2,sw[1],lift[1],true);legH(7.2,sw[3],lift[3],true);
  // ---------- rabo fino com tufo
  for(let t=0;t<1;t+=.05){const x=3.1-t*1.1+Math.sin(t*3)*.2,y=9.4+bob+t*3.4;px(x,y,F[2]);px(x+.25,y,F[1])}
  for(const[dx,dy]of[[-.25,0],[0,.25],[.25,.25],[-.5,.5],[0,.75],[.25,.5]])px(1.9+dx,12.7+bob+dy,F[1]);
  // ---------- corpo
  const top=new Array(LW*4).fill(99);
  for(let y=3;y<17.5;y+=Q)for(let x=2;x<23;x+=Q){const b=ell(x+.125,y+.125);if(!b)continue;
    const xi=Math.round(x*4);if(y<top[xi])top[xi]=y;
    let l=shadeE(b);
    if(y>13.5+bob)l*=.72;                       // barriga na sombra
    if(x>12&&x<21&&b.dy<-.3)l*=.9;if(x>11.5&&x<13.5)l*=.94;               // capa escura dos ombros
    px(x,y,fur(l,x,y,b.dy<.1))}
  // ---------- cabeça: crânio + focinho cônico
  const headAt=(x,y)=>{const dx=(x-22.4)/3.2,dy=(y-10.6-bob)/3.6,d=dx*dx+dy*dy;if(d<=1)return{d,dx,dy};
    if(x>=22.4&&x<=28.6){const t=(x-22.4)/6.2,cy=10.9+bob+t*1.9,r=3.2-t*1.9,dy2=(y-cy)/r;if(Math.abs(dy2)<=1)return{d:dy2*dy2*.9,dx:.3,dy:dy2}}return null};
  for(let y=6;y<16;y+=Q)for(let x=19.5;x<29;x+=Q){const b=headAt(x+.125,y+.125);if(!b)continue;
    let l=shadeE(b)*1.02;if(y>12.6+bob+(x-23)*.25)l*=.74;if(x>26)l*=.9;
    const cheek=x>21&&x<24.5&&y>12+bob&&y<14.2+bob;     // bochecha grisalha
    px(x,y,fur(l+(cheek?.12:0),x,y,true))}
  // testa: linha reta descendo até o focinho (mais escura)
  for(let x=21.5;x<28.4;x+=Q){const y=7.5+bob+(x-21.5)*.5;px(x,y,F[2]);if(x<25.5)px(x,y+.25,F[5])}
  // disco do focinho, narina e boca
  for(let y=11;y<14.6;y+=Q)for(let x=28;x<29.5;x+=Q){const dy=(y+.125-12.8)/1.45,dx=(x+.125-28.5)/.95;if(dx*dx+dy*dy>1)continue;px(x,y+bob,dx>.35?'#4e3834':dy<-.45?'#a08078':'#7e625a')}
  px(28.75,12.5+bob,'#140c0a');px(28.75,12.75+bob,'#140c0a');px(29,12.75+bob,'#2a1a16');
  for(let x=23.8;x<28.1;x+=Q){const y=13.7+bob+(x-23.8)*.12;px(x,y,'#120c0a');px(x,y-.25,'#3e2e26')}
  // presa de baixo curvando para cima e presa de cima (amoladeira)
  const tusk=(x0,y0,x1,y1,x2,y2,w0,w1)=>{for(let t=0;t<=1;t+=.04){const a=(1-t)*(1-t),b=2*(1-t)*t,cc=t*t,x=a*x0+b*x1+cc*x2,y=a*y0+b*y1+cc*y2,r=(w0+(w1-w0)*t)/2;
    for(let yy=-r;yy<=r;yy+=Q)for(let xx=-r;xx<=r;xx+=Q){if(xx*xx+yy*yy>r*r+.01)continue;px(x+xx,y+yy,t>.85?'#fffaf0':yy>0||xx>0?'#c8b898':'#f2ead6')}}};
  tusk(26.2,14.3+bob,27.7,14.2,27.6,11.7+bob,.75,.3);
  tusk(25.5,13.8+bob,26,13.4,25.9,12.9+bob,.45,.25);
  // olho pequeno no alto da cabeça, com sulco e brilho
  for(let x=22.4;x<24.2;x+=Q)px(x,9.1+bob+(x-22.4)*.2,F[1]);
  for(const[dx,dy]of[[-.25,0],[-.25,.25],[0,.5],[.25,.5],[.5,.5],[.75,.25],[.75,0],[0,-.25],[.25,-.25],[.5,-.25]])px(23.25+dx,9.85+bob+dy,F[6]);px(23.25,9.85+bob,'#0a0706');px(23.5,9.85+bob,'#0a0706');px(23.25,10.1+bob,'#0a0706');px(23.5,10.1+bob,'#2a1a14');px(23.25,9.85+bob,'#f0e4d4');
  // ---------- crina: cerdas compridas no dorso, mais altas sobre o ombro
  for(let x=7;x<23;x+=Q){const xi=Math.round(x*4),t0=top[xi];if(t0>90)continue;
    const h=.4+1.7*Math.exp(-(((x-15.5)/4.2)**2)),r=hsh(xi,7);if(r<.25)continue;
    const len=h*(.55+r*.6);for(let y=t0-len;y<t0+.6;y+=Q)px(x+(t0-y)*-.12,y,y<t0-len+.3&&r>.7?F[5]:F[1])}
  // orelha pequena, peluda e em pé
  for(let y=4.6;y<8.4;y+=Q){const t=(y-4.6)/3.8,x0=20.4-t*.5,x1=20.9+t*1.2;for(let x=x0;x<x1;x+=Q){const inner=x>x0+.5&&x<x1-.5&&t>.35;px(x,y+bob,inner?'#7a5c4e':x<x0+.3?F[6]:fur(.45,x,y,true))}}
  px(20.4,4.35+bob,F[1]);px(20.65,4.1+bob,F[1]);
  // ---------- pernas do lado de cá
  legF(19.4,sw[0],lift[0],false);legH(9.6,sw[2],lift[2],false);
  // sombra de contato entre perna e barriga
  for(let x=7;x<21;x+=Q)if(hsh(Math.round(x*4),3)>.45)px(x,curve(BOT,x)+bob,F[1]);
  const out=outline(c,'#0c0807',KH);out.k=KH;return out;
}
