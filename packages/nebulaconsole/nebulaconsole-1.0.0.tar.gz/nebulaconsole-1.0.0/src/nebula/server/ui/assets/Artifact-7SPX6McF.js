import{d as S,x as h,E,e as N,f as p,g as R,q as T,h as _,i as V,c,k as e,l as n,o as l,u as t,m as $,a as i,n as d,p as q,t as s,v as D,y as J,I as v,z as j,A as z,B as m,C as F}from"./index-tQzbzZZu.js";import{u as H}from"./usePageTitle-LpUrSePH.js";const P={key:0},M=S({__name:"Artifact",setup(U){const b=h(),k=E("artifactId"),y=N(b.artifacts.getArtifact,[k]),a=p(()=>y.response),r=R(!1),w=[{label:"Artifact"},{label:"Details"},{label:"Raw"}],u=T("tab","Artifact"),x=p(()=>a.value?`${_.info.artifact}: ${a.value.key??V(a.value.type)}`:_.info.artifact);return H(x),(G,o)=>{const C=n("p-divider"),g=n("p-button"),A=n("p-content"),B=n("p-tabs"),I=n("p-layout-well");return l(),c(I,{class:"artifact"},{header:e(()=>[a.value?(l(),c(t($),{key:0,artifact:a.value},null,8,["artifact"])):i("",!0)]),well:e(()=>[a.value?(l(),c(t(d),{key:0,artifact:a.value,alternate:""},null,8,["artifact"])):i("",!0)]),default:e(()=>[a.value?(l(),q("section",P,[s(t(D),{artifact:a.value},null,8,["artifact"]),s(C),t(J).xl?(l(),c(A,{key:0},{default:e(()=>[s(t(v),{artifact:a.value},null,8,["artifact"]),s(g,{class:"artifact__raw-data-button",small:"",onClick:o[0]||(o[0]=f=>r.value=!r.value)},{default:e(()=>[j(z(r.value?"Hide":"Show")+" raw data ",1)]),_:1}),r.value?(l(),c(t(m),{key:0,artifact:a.value},null,8,["artifact"])):i("",!0)]),_:1})):(l(),c(B,{key:1,selected:t(u),"onUpdate:selected":o[1]||(o[1]=f=>F(u)?u.value=f:null),tabs:w},{artifact:e(()=>[s(t(v),{artifact:a.value},null,8,["artifact"])]),details:e(()=>[s(t(d),{artifact:a.value},null,8,["artifact"])]),raw:e(()=>[s(t(m),{artifact:a.value},null,8,["artifact"])]),_:1},8,["selected"]))])):i("",!0)]),_:1})}}});export{M as default};
