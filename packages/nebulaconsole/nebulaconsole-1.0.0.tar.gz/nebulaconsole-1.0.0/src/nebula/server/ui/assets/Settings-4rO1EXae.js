import{d as b,f as C,o as c,p as u,t as e,k as t,F as h,cj as x,u as n,ck as A,A as f,cl as B,cm as w,br as N,c as P,l as o,W as T,cn as V,co as p,C as j}from"./index-tQzbzZZu.js";import{u as F}from"./usePageTitle-LpUrSePH.js";const M={class:"settings-block"},W=b({__name:"SettingsCodeBlock",props:{engineSettings:{}},setup(g){const s=g,a=C(()=>Object.entries(s.engineSettings));return(d,i)=>(c(),u("div",M,[e(n(A),{multiline:""},{default:t(()=>[(c(!0),u(h,null,x(a.value,(l,r)=>(c(),u("div",{key:r,class:"settings-block--code-line"},f(l[0])+": "+f(l[1]),1))),128))]),_:1})]))}});function D(){return B(w)}const O=b({__name:"Settings",async setup(g){let s,a;const d=[{text:"Settings"}],i=D(),[l,r]=([s,a]=N(()=>Promise.all([i.admin.getSettings(),i.admin.getVersion()])),s=await s,a(),s);return F("Settings"),(E,m)=>{const v=o("p-key-value"),k=o("p-theme-toggle"),_=o("p-label"),S=o("p-layout-default");return c(),P(S,{class:"settings"},{header:t(()=>[e(n(T),{crumbs:d},{actions:t(()=>[e(v,{class:"settings__version",label:"Version",value:n(r),alternate:""},null,8,["value"])]),_:1})]),default:t(()=>[e(_,{label:"Theme"},{default:t(()=>[e(k)]),_:1}),e(_,{label:"Color Mode",class:"settings__color-mode"},{default:t(()=>[e(n(V),{selected:n(p),"onUpdate:selected":m[0]||(m[0]=y=>j(p)?p.value=y:null)},null,8,["selected"])]),_:1}),e(_,{label:"Server Settings"},{default:t(()=>[e(W,{class:"settings__code-block","engine-settings":n(l)},null,8,["engine-settings"])]),_:1})]),_:1})}}});export{O as default};
