import{d as T,x as U,E as d,f as o,e as v,as as S,y as D,q as E,aq as M,c as V,k as a,a as Y,l as p,o as j,t as u,u as e,cc as A,bm as F,cd as f,C as O,ce as z,aB as G}from"./index-tQzbzZZu.js";import{u as H}from"./usePageTitle-LpUrSePH.js";const L=T({__name:"WorkPoolQueue",setup(I){const c=U(),l=d("workPoolName"),b=o(()=>[l.value]),s=d("workPoolQueueName"),_=o(()=>[s.value]),k={interval:3e5},i=v(c.workPoolQueues.getWorkPoolQueueByName,[l.value,s.value],k),t=o(()=>i.response),P=v(c.workPools.getWorkPoolByName,[l.value],k),q=o(()=>P.response),w=o(()=>{var n;return((n=q.value)==null?void 0:n.type)==="nebula-agent"}),y=o(()=>t.value?`Your work pool ${t.value.name} is ready to go!`:"Your work queue is ready to go!"),g=o(()=>`nebula ${w.value?"agent":"worker"} start --pool "${l.value}" --work-queue "${s.value}"`),N=o(()=>`Work queues are scoped to a work pool to allow ${w.value?"agents":"workers"} to pull from groups of queues with different priorities.`),{filter:Q}=S({workPoolQueues:{name:_},workPools:{name:b}}),x=o(()=>[{label:"Details",hidden:D.xl},{label:"Upcoming Runs"},{label:"Runs"}]),r=E("tab","Details"),{tabs:B}=M(x,r),C=o(()=>s.value?`Work Pool Queue: ${s.value}`:"Work Pool Queue");return H(C),(n,m)=>{const W=p("p-tabs"),h=p("p-layout-well"),$=p("p-layout-default");return t.value?(j(),V($,{key:0,class:"work-pool-queue"},{header:a(()=>[u(e(A),{"work-pool-queue":t.value,"work-pool-name":e(l),onUpdate:e(i).refresh},null,8,["work-pool-queue","work-pool-name","onUpdate"])]),default:a(()=>[u(h,{class:"work-pool-queue__body"},{header:a(()=>[u(e(F),{command:g.value,title:y.value,subtitle:N.value},null,8,["command","title","subtitle"])]),well:a(()=>[u(e(f),{alternate:"","work-pool-name":e(l),"work-pool-queue":t.value},null,8,["work-pool-name","work-pool-queue"])]),default:a(()=>[u(W,{selected:e(r),"onUpdate:selected":m[0]||(m[0]=R=>O(r)?r.value=R:null),tabs:e(B)},{details:a(()=>[u(e(f),{"work-pool-name":e(l),"work-pool-queue":t.value},null,8,["work-pool-name","work-pool-queue"])]),"upcoming-runs":a(()=>[u(e(z),{"work-pool-name":e(l),"work-pool-queue":t.value},null,8,["work-pool-name","work-pool-queue"])]),runs:a(()=>[u(e(G),{filter:e(Q),prefix:"runs"},null,8,["filter"])]),_:1},8,["selected","tabs"])]),_:1})]),_:1})):Y("",!0)}}});export{L as default};
