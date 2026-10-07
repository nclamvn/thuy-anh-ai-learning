import * as THREE from './vendor/three.module.js';
import {layoutPlan,validateWorldSpec} from './world.js';
const T=THREE;
export function disposeWorld(artifact){const geometries=new Set(),materials=new Set(),textures=new Set();artifact.group.traverse(o=>{if(o.geometry)geometries.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:o.material?[o.material]:[]){materials.add(m);for(const value of Object.values(m))if(value?.isTexture)textures.add(value);}});geometries.forEach(v=>v.dispose());textures.forEach(v=>v.dispose());materials.forEach(v=>v.dispose());artifact.group.removeFromParent();}
export function compileWorld(input){
 const spec=validateWorldSpec(input),plan=layoutPlan(spec),group=new T.Group(),whale=new T.Group(),city=new T.Group(),inspectables=[],lanterns=[],night=spec.world.sky==='night';
 const mat=(color,roughness=.78,extra={})=>new T.MeshStandardMaterial({color,roughness,...extra});
 const skin=mat(spec.world.whaleColor==='indigo'?'#405d8e':'#3c8393',.5),belly=mat('#a4c2d5',.8),edge=mat('#283f69'),cream=mat('#f5dca2'),walls=[mat('#edd7ad'),mat('#d6bfab'),mat('#c3d1c5')],roofs=[mat('#b77467'),mat('#375c78'),mat('#768d81')],gold=mat('#d4a15d',.35),glass=mat('#ffe4a7',.35,{emissive:'#ffca70',emissiveIntensity:night?2.1:.8}),grass=mat('#729887'),soil=mat('#ad947f'),wood=mat('#a88964');
 function mesh(geo,material,parent,x=0,y=0,z=0){const o=new T.Mesh(geo,material);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
 const sphere=(parent,m,x,y,z,sx,sy,sz,segments=24)=>{const o=mesh(new T.SphereGeometry(1,segments,16),m,parent,x,y,z);o.scale.set(sx,sy,sz);return o;};
 const box=(parent,m,x,y,z,w,h,d)=>mesh(new T.BoxGeometry(w,h,d),m,parent,x,y,z);
 const tube=(points,r,material,parent,segments=32)=>mesh(new T.TubeGeometry(new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p))),segments,r,7,false),material,parent);
 group.add(whale);whale.add(city);
 const profile=new T.CatmullRomCurve3([[-7.8,.03,.03],[-7.4,1.15,1.6],[-6.4,1.75,2.45],[-4.8,2.04,2.7],[-2,2.1,2.76],[1,1.94,2.4],[4,1.35,1.6],[6.5,.65,.78],[8.5,.24,.3]].map(v=>new T.Vector3(...v))),vertices=[],topIndices=[],bottomIndices=[];
 const rings=64,sides=40;for(let i=0;i<=rings;i++){const p=profile.getPoint(i/rings);for(let j=0;j<=sides;j++){const angle=j/sides*Math.PI*2;vertices.push(p.x,p.y*Math.cos(angle),p.z*Math.sin(angle));}}
 for(let i=0;i<rings;i++)for(let j=0;j<sides;j++){const a=i*(sides+1)+j,b=a+sides+1,indices=Math.cos((j+.5)/sides*Math.PI*2)<-.4?bottomIndices:topIndices;indices.push(a,a+1,b,b,a+1,b+1);}
 const bodyGeo=new T.BufferGeometry();bodyGeo.setAttribute('position',new T.Float32BufferAttribute(vertices,3));bodyGeo.setIndex([...topIndices,...bottomIndices]);bodyGeo.addGroup(0,topIndices.length,0);bodyGeo.addGroup(topIndices.length,bottomIndices.length,1);bodyGeo.computeVertexNormals();const body=mesh(bodyGeo,[skin,belly],whale);body.userData.inspect='whale';inspectables.push(body);
 // Tapered tail joins the rounded body; paired swept flukes lie in the water-like sky.
 const tailGeo=new T.LatheGeometry([new T.Vector2(.3,0),new T.Vector2(.58,.8),new T.Vector2(.95,1.9),new T.Vector2(1.35,3.2)],24);const stem=mesh(tailGeo,skin,whale,8.7,.2,0);stem.rotation.z=Math.PI/2;
 function fluke(side){const shape=new T.Shape();shape.moveTo(0,0);shape.quadraticCurveTo(.7,side*1.5,2.5,side*3.4);shape.quadraticCurveTo(1.1,side*3.5,-1.4,side*2.0);shape.quadraticCurveTo(-1.7,side*.8,0,0);const o=mesh(new T.ExtrudeGeometry(shape,{depth:.38,bevelEnabled:true,bevelSegments:3,steps:1,bevelSize:.2,bevelThickness:.2,curveSegments:18}),skin,whale,8.25,.5,0);o.rotation.x=Math.PI/2+side*.18;o.rotation.z=.12;return o;}
 fluke(1);fluke(-1);
 function fin(side){const shape=new T.Shape();shape.moveTo(-1.5,0);shape.bezierCurveTo(-.8,-1,1,-3.6,3.2,-3.9);shape.bezierCurveTo(3.3,-2.7,.9,-.15,-1.5,0);const o=mesh(new T.ExtrudeGeometry(shape,{depth:.26,bevelEnabled:true,bevelSize:.12,bevelThickness:.15,bevelSegments:2,curveSegments:20}),skin,whale,-1,-.1,side*2.4);o.rotation.y=side*.22;return o;}
 const fins=[fin(1),fin(-1)];
 const eyeMat=new T.MeshBasicMaterial({color:'#14243d'});sphere(whale,eyeMat,-6.45,.38,2.45,.18,.2,.09);sphere(whale,new T.MeshBasicMaterial({color:'#f9edcf'}),-6.5,.44,2.53,.04,.04,.02);sphere(whale,eyeMat,-6.45,.38,-2.45,.18,.2,.09);
 tube([[-7.35,-.35,1.55],[-6.5,-.58,2.4],[-5.4,-.64,2.66],[-4.4,-.46,2.69]],.035,edge,whale);
 for(let i=0;i<11;i++){const x=-5.3+i*.52;tube([[x,-.75,2.26],[x+.28,-1.45,1.9],[x+.52,-1.98,.6]],.026,cream,whale,16);}
 city.position.set(-.3,1.65,0);city.scale.setScalar(spec.world.cityScale);
 const land=mesh(new T.CylinderGeometry(4.5,4.15,.5,48),soil,city,0,.0,0);land.scale.set(1.23,1,.6);
 const meadow=mesh(new T.CylinderGeometry(4.55,4.55,.12,48),grass,city,0,.3,0);meadow.scale.set(1.23,1,.6);
 tube([[-4.4,.43,1],[-2,.43,.5],[0,.43,.2],[2,.43,.8],[4,.43,1]],.12,cream,city);
 for(const [i,h]of plan.houses.entries()){
  const root=new T.Group();root.position.set(h.x,.42,h.z);root.rotation.y=(i%3-1)*.14;city.add(root);const building=box(root,walls[i%3],0,h.height/2,0,1.02,h.height,.95);
  const roof=mesh(new T.ConeGeometry(.91,.92,4),roofs[h.roof],root,0,h.height+.43,0);roof.rotation.y=Math.PI/4;box(root,wood,.3,h.height+.57,-.15,.14,.6,.14);
  box(root,glass,-.22,h.height*.62,.485,.18,.33,.03);box(root,glass,.22,h.height*.62,.485,.18,.33,.03);box(root,wood,0,.3,.49,.21,.58,.04);box(root,cream,0,h.height*.62,.51,.55,.055,.04);box(root,wood,-.22,h.height*.62,.51,.025,.34,.035);box(root,wood,.22,h.height*.62,.51,.025,.34,.035);if(i%3===0){box(root,walls[i%3],.44,h.height*.52,.05,.54,h.height*.66,.66);const dormer=mesh(new T.ConeGeometry(.44,.62,4),roofs[h.roof],root,.44,h.height*.85+.3,.05);dormer.rotation.y=Math.PI/4;}if(i%4===1)box(root,roofs[0],0,.9,.64,1.16,.12,.36);
 }
 const tower=new T.Group();tower.position.set(-.4,.4,-.8);city.add(tower);const turret=mesh(new T.CylinderGeometry(.6,.72,3.8,10),cream,tower,0,1.9,0);turret.userData.inspect='tower';inspectables.push(turret);mesh(new T.ConeGeometry(.9,1.6,10),roofs[1],tower,0,4.5,0);mesh(new T.CylinderGeometry(.015,.04,1.1,8),gold,tower,0,5.6,0);sphere(tower,gold,0,6.15,0,.11,.11,.11);
 const clock=mesh(new T.CircleGeometry(.3,24),cream,tower,0,2.8,.62);tube([[-.0,2.8,.635],[.0,3.02,.635]],.028,edge,tower,4);tube([[0,2.8,.635],[.18,2.73,.635]],.028,edge,tower,4);
 function tree(x,z,height=1.3){mesh(new T.CylinderGeometry(.07,.1,height,7),wood,city,x,.55+height/2,z);sphere(city,grass,x,1+height,z,.43,.6,.43,12);sphere(city,grass,x-.25,.7+height,z,.3,.45,.35,12);}
 if(spec.world.gardens){const plot=box(city,grass,-3.9,.52,1.3,1.5,.2,1.5);plot.userData.inspect='garden';inspectables.push(plot);for(let i=0;i<6;i++)tree(-4.5+(i%3)*.48,.9+Math.floor(i/3)*.7,1.1+(i%2)*.3);for(let i=0;i<10;i++)sphere(city,roofs[0],-4.5+(i%5)*.24,.78,1.55+Math.floor(i/5)*.25,.07,.1,.07,8);}else{const gate=box(city,wood,-4.5,.7,1.4,.09,.65,1.1);gate.userData.inspect='garden';inspectables.push(gate);}
 tree(4.1,-1.2,1.4);tree(3.7,-.6,1.1);
 if(spec.world.starBridge){const pts=[];for(let i=0;i<=24;i++){const t=i/24;pts.push([3.8+t*6,3.5+Math.sin(t*Math.PI)*1.3,-1.2+t*2]);}tube(pts,.14,gold,whale,48);for(let i=0;i<11;i++){const t=i/10;const p=[3.8+t*6,3.7+Math.sin(t*Math.PI)*1.3,-1.2+t*2];sphere(whale,glass,...p,.09,.09,.09,10);}sphere(whale,gold,10,3.5,1,.25,.25,.25);}
 for(const p of plan.lanterns){const root=new T.Group();root.position.set(p.x,p.y,p.z);whale.add(root);const core=sphere(root,glass,0,0,0,.16,.24,.16,16);core.userData.lantern=p.id;mesh(new T.TorusGeometry(.22,.035,6,16),gold,root,0,.02,0).rotation.x=Math.PI/2;mesh(new T.ConeGeometry(.21,.18,8),gold,root,0,.32,0);tube([[0,.4,0],[0,.68,0],[.12,.8,0]],.025,gold,root,8);lanterns.push({id:p.id,root,mesh:core});inspectables.push(core);}
 const starsGeo=new T.BufferGeometry();starsGeo.setAttribute('position',new T.Float32BufferAttribute(plan.stars.flatMap(p=>[p.x,p.y,p.z]),3));const stars=new T.Points(starsGeo,new T.PointsMaterial({color:night?'#ffe5b1':'#f5e6d5',size:night?.12:.075,transparent:true,opacity:night?.9:.2}));group.add(stars);
 const pixels=new Uint8Array(128*64*4),blobs=[[-.65,0,.35],[-.3,.15,.42],[.15,.12,.5],[.55,-.03,.35]];for(let y=0;y<64;y++)for(let x=0;x<128;x++){let alpha=0;const px=x/64-1,py=y/32-1;for(const [bx,by,r]of blobs)alpha+=Math.exp(-((px-bx)**2/(r*r)+(py-by)**2/(r*r*.28))*2);const i=(y*128+x)*4;pixels[i]=pixels[i+1]=pixels[i+2]=255;pixels[i+3]=Math.min(255,alpha*180);}
 const cloudTexture=new T.DataTexture(pixels,128,64);cloudTexture.needsUpdate=true;const cloudMat=new T.SpriteMaterial({map:cloudTexture,color:night?'#8ca8cb':'#ffe0c6',transparent:true,opacity:.38,depthWrite:false});for(let i=0;i<6;i++){const cloud=new T.Sprite(cloudMat);cloud.position.set(-24+i*9,-4-(i%2)*2,-10+(i%3)*7);cloud.scale.set(13,6,1);group.add(cloud);}
 const skyDisk=sphere(group,new T.MeshBasicMaterial({color:night?'#fae3ad':'#ffd6a2'}),13,9,-18,1.35,1.35,1.35,32);skyDisk.name='sky-disc';
 return {group,whale,city,fins,inspectables,lanterns,spec,objectCount:group.getObjectsByProperty('isMesh',true).length,animate(time){whale.position.y=Math.sin(time*.6)*.16;fins[0].rotation.z=Math.sin(time*.45)*.04;fins[1].rotation.z=-Math.sin(time*.45)*.04;},collect(id){const lantern=lanterns.find(l=>l.id===id);if(lantern)lantern.root.visible=false;}};
}
