import{d as k,x as i,E as y,f as o,aE as b,c as m,k as l,a as _,l as f,o as d,t,u as c,bA as T,bB as v}from"./index-tQzbzZZu.js";import{u as g}from"./usePageTitle-LpUrSePH.js";const w=k({__name:"BlocksCatalogView",setup(B){const s=i(),a=y("blockTypeSlug"),u=o(()=>a.value?[a.value]:null),n=b(s.blockTypes.getBlockTypeBySlug,u),e=o(()=>n.response),p=o(()=>e.value?`Block Type: ${e.value.name}`:null);return g(p),(x,C)=>{const r=f("p-layout-default");return e.value?(d(),m(r,{key:0,class:"blocks-catalog-view"},{header:l(()=>[t(c(T),{"block-type":e.value},null,8,["block-type"])]),default:l(()=>[t(c(v),{"block-type":e.value},null,8,["block-type"])]),_:1})):_("",!0)}}});export{w as default};
