import{d as xe,C as Z,r,a as Ae,u as Ge,m as ee,D as Ue,p as $e,q as Ne,c as te,b as v,e,w as l,h as c,E as M,s as h,G as f,f as s,H as Be,g as Ee,o as m,I as De,j as i,J as Le,K as Te,L as Se,y as g,N as le,O as ae,z as oe,P as ne,F as Fe,v as Ie,Q as Me,T as je,_ as Re}from"./index-Df5Rugzl.js";import{c as qe,j as ze,k as Ke,l as Oe,e as He,u as Je,b as Pe}from"./index-DzkZSsWB.js";import{r as Qe}from"./relativeTime-BUFJGuxk.js";const We={class:"groups-container"},Xe={class:"header"},Ye={class:"left"},Ze={class:"right"},et={class:"group-header"},tt={class:"title"},lt={class:"group-content"},at={class:"group-footer"},ot={class:"time"},nt=xe({__name:"Groups",setup(st){Z.extend(Qe);const A=r("grid"),se=a=>Z(a).fromNow(),G=r([]),U=r(!1),$=r(!1),w=r(!1),k=r(),p=Ae({name:"",description:""}),re={name:[{required:!0,message:"请输入分组名称",trigger:"blur"}]},N=async()=>{U.value=!0;try{const a=await qe();console.log("获取到的分组数据:",a),G.value=a.data||[]}catch(a){console.error("获取分组失败:",a),f.error("获取分组失败")}finally{U.value=!1}},j=()=>{k.value&&k.value.resetFields(),p.name="",p.description=""},ue=()=>{j(),w.value=!0},R=a=>{b.value=a,p.name=a.name,p.description=a.description||"",w.value=!0},de=async()=>{k.value&&await k.value.validate(async a=>{if(a){$.value=!0;try{b.value?await ze(b.value.id,p):await Ke(p),f.success("保存成功"),w.value=!1,N()}catch(t){console.error("保存失败:",t),f.error("保存失败")}finally{$.value=!1}}})},q=async a=>{try{await Me.confirm("删除分组将同时删除该分组下的所有笔记，是否继续？","警告",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}),await Oe(a.id),f.success("删除成功"),await N()}catch(t){t!=="cancel"&&(console.error("删除失败:",t),f.error("删除失败"))}},B=r(!1),z=r([]),E=r(!1),y=r(null),ie=Ge(),D=ee(()=>{var a;return((a=ie.user)==null?void 0:a.role)==="admin"}),K=async a=>{y.value=a,B.value=!0,await ce()},ce=async()=>{if(y.value){E.value=!0;try{const a=await He();z.value=a.data.map(t=>({...t,hasAuth:Array.isArray(t.note_group)&&t.note_group.includes(y.value.id)}))}catch(a){console.error(a),f.error("获取用户列表失败")}finally{E.value=!1}}},pe=async a=>{var t,_;if(y.value)try{const n=Array.isArray(a.note_group)?[...a.note_group]:[];if(a.hasAuth)n.includes(y.value.id)||n.push(y.value.id);else{const C=n.indexOf(y.value.id);C>-1&&n.splice(C,1)}await Je(a.id,{note_group:n,note:a.notes||[]}),a.note_group=n,f.success("授权更新成功")}catch(n){console.error(n),f.error(((_=(t=n.response)==null?void 0:t.data)==null?void 0:_.detail)||"授权更新失败"),a.hasAuth=!a.hasAuth}},V=r(""),O=ee(()=>{if(!V.value)return G.value;const a=V.value.toLowerCase();return G.value.filter(t=>t.name.toLowerCase().includes(a)||t.description&&t.description.toLowerCase().includes(a))}),H=Ue(()=>{},300);$e(V,()=>{H()});const x=r(!1),J=r([]),L=r(!1),b=r(null),P=async a=>{b.value=a,x.value=!0,await _e(a.id)},_e=async a=>{L.value=!0;try{const t=await Pe({group__id:a});J.value=t.data.results||[]}catch(t){console.error(t),f.error("获取笔记列表失败")}finally{L.value=!1}},fe=Ee(),me=a=>{x.value=!1,fe.push(`/notes/view/${a.id}`)};return Ne(()=>{N()}),(a,t)=>{var X;const _=s("el-icon"),n=s("el-button"),C=s("el-input"),Q=s("el-radio-button"),ve=s("el-radio-group"),d=s("el-table-column"),ye=s("el-button-group"),T=s("el-table"),S=s("el-dropdown-item"),he=s("el-dropdown-menu"),ge=s("el-dropdown"),we=s("el-card"),be=s("el-col"),Ce=s("el-row"),W=s("el-form-item"),ke=s("el-form"),F=s("el-dialog"),Ve=s("el-switch"),I=Be("loading");return m(),te("div",We,[v("div",Xe,[v("div",Ye,[e(n,{type:"primary",onClick:ue},{default:l(()=>[e(_,null,{default:l(()=>[e(c(De))]),_:1}),t[8]||(t[8]=i("新建分组 "))]),_:1})]),v("div",Ze,[e(C,{modelValue:V.value,"onUpdate:modelValue":t[0]||(t[0]=o=>V.value=o),placeholder:"搜索分组",class:"search-input",onInput:c(H)},{prefix:l(()=>[e(_,null,{default:l(()=>[e(c(Le))]),_:1})]),_:1},8,["modelValue","onInput"]),e(ve,{modelValue:A.value,"onUpdate:modelValue":t[1]||(t[1]=o=>A.value=o),size:"small"},{default:l(()=>[e(Q,{value:"table"},{default:l(()=>[e(_,null,{default:l(()=>[e(c(Te))]),_:1})]),_:1}),e(Q,{value:"grid"},{default:l(()=>[e(_,null,{default:l(()=>[e(c(Se))]),_:1})]),_:1})]),_:1},8,["modelValue"])])]),A.value==="table"?M((m(),h(T,{key:0,data:O.value,stripe:""},{default:l(()=>[e(d,{prop:"name",label:"名称"}),e(d,{prop:"description",label:"描述"}),e(d,{prop:"note_count",label:"笔记数量",width:"120",align:"center"},{default:l(({row:o})=>[e(n,{text:"",style:{color:"#E6A23C"},onClick:u=>P(o)},{default:l(()=>[i(g(o.note_count)+" 篇笔记 ",1)]),_:2},1032,["onClick"])]),_:1}),e(d,{prop:"created_at",label:"创建时间",width:"180"}),e(d,{prop:"updated_at",label:"更新时间",width:"180"}),e(d,{label:"操作",width:D.value?280:200,fixed:"right"},{default:l(({row:o})=>[e(ye,null,{default:l(()=>[e(n,{type:"primary",icon:c(le),onClick:u=>R(o)},{default:l(()=>t[9]||(t[9]=[i(" 编辑 ")])),_:2},1032,["icon","onClick"]),D.value?(m(),h(n,{key:0,type:"success",icon:c(ae),onClick:u=>K(o)},{default:l(()=>t[10]||(t[10]=[i(" 授权 ")])),_:2},1032,["icon","onClick"])):oe("",!0),e(n,{type:"danger",icon:c(ne),onClick:u=>q(o)},{default:l(()=>t[11]||(t[11]=[i(" 删除 ")])),_:2},1032,["icon","onClick"])]),_:2},1024)]),_:1},8,["width"])]),_:1},8,["data"])),[[I,U.value]]):(m(),h(Ce,{key:1,gutter:20},{default:l(()=>[(m(!0),te(Fe,null,Ie(O.value,o=>(m(),h(be,{span:6,key:o.id},{default:l(()=>[e(we,{class:"group-card","body-style":{padding:"15px"},shadow:"hover"},{default:l(()=>[v("div",et,[v("span",tt,g(o.name),1),e(ge,{trigger:"click"},{dropdown:l(()=>[e(he,null,{default:l(()=>[e(S,{onClick:u=>R(o)},{default:l(()=>[e(_,null,{default:l(()=>[e(c(le))]),_:1}),t[12]||(t[12]=i("编辑 "))]),_:2},1032,["onClick"]),D.value?(m(),h(S,{key:0,onClick:u=>K(o)},{default:l(()=>[e(_,null,{default:l(()=>[e(c(ae))]),_:1}),t[13]||(t[13]=i("授权 "))]),_:2},1032,["onClick"])):oe("",!0),e(S,{onClick:u=>q(o),class:"danger"},{default:l(()=>[e(_,null,{default:l(()=>[e(c(ne))]),_:1}),t[14]||(t[14]=i("删除 "))]),_:2},1032,["onClick"])]),_:2},1024)]),default:l(()=>[e(n,{type:"text"},{default:l(()=>[e(_,null,{default:l(()=>[e(c(je))]),_:1})]),_:1})]),_:2},1024)]),v("div",lt,g(o.description||"暂无描述"),1),v("div",at,[e(n,{text:"",style:{color:"#E6A23C"},onClick:u=>P(o)},{default:l(()=>[i(g(o.note_count)+" 篇笔记 ",1)]),_:2},1032,["onClick"]),v("span",ot,g(se(o.updated_at)),1)])]),_:2},1024)]),_:2},1024))),128))]),_:1})),e(F,{title:b.value?"编辑分组":"新建分组",modelValue:w.value,"onUpdate:modelValue":t[5]||(t[5]=o=>w.value=o),width:"500px",onClose:j},{footer:l(()=>[e(n,{onClick:t[4]||(t[4]=o=>w.value=!1)},{default:l(()=>t[15]||(t[15]=[i("取消")])),_:1}),e(n,{type:"primary",onClick:de,loading:$.value},{default:l(()=>t[16]||(t[16]=[i(" 确定 ")])),_:1},8,["loading"])]),default:l(()=>[e(ke,{model:p,rules:re,ref_key:"formRef",ref:k,"label-width":"80px"},{default:l(()=>[e(W,{label:"名称",prop:"name"},{default:l(()=>[e(C,{modelValue:p.name,"onUpdate:modelValue":t[2]||(t[2]=o=>p.name=o),placeholder:"请输入分组名称"},null,8,["modelValue"])]),_:1}),e(W,{label:"描述",prop:"description"},{default:l(()=>[e(C,{modelValue:p.description,"onUpdate:modelValue":t[3]||(t[3]=o=>p.description=o),type:"textarea",rows:3,placeholder:"请输入分组描述"},null,8,["modelValue"])]),_:1})]),_:1},8,["model"])]),_:1},8,["title","modelValue"]),e(F,{modelValue:B.value,"onUpdate:modelValue":t[6]||(t[6]=o=>B.value=o),title:"分组授权",width:"600px"},{default:l(()=>[M((m(),h(T,{data:z.value,style:{width:"100%"}},{default:l(()=>[e(d,{prop:"username",label:"用户名"}),e(d,{prop:"name",label:"姓名"}),e(d,{label:"授权",width:"100"},{default:l(({row:o})=>[e(Ve,{modelValue:o.hasAuth,"onUpdate:modelValue":u=>o.hasAuth=u,onChange:u=>pe(o)},null,8,["modelValue","onUpdate:modelValue","onChange"])]),_:1})]),_:1},8,["data"])),[[I,E.value]])]),_:1},8,["modelValue"]),e(F,{modelValue:x.value,"onUpdate:modelValue":t[7]||(t[7]=o=>x.value=o),title:`${((X=b.value)==null?void 0:X.name)||""} 的笔记列表`,width:"800px"},{default:l(()=>[M((m(),h(T,{data:J.value,style:{width:"100%"}},{default:l(()=>[e(d,{prop:"title",label:"笔记名称"},{default:l(({row:o})=>[e(n,{text:"",style:{color:"#E6A23C"},onClick:u=>me(o)},{default:l(()=>[i(g(o.title),1)]),_:2},1032,["onClick"])]),_:1}),e(d,{label:"创建人"},{default:l(({row:o})=>{var u,Y;return[i(g(((u=o.creator)==null?void 0:u.name)||((Y=o.creator)==null?void 0:Y.username)),1)]}),_:1}),e(d,{prop:"created_at",label:"创建时间",width:"180"}),e(d,{prop:"updated_at",label:"更新时间",width:"180"})]),_:1},8,["data"])),[[I,L.value]])]),_:1},8,["modelValue","title"])])}}}),it=Re(nt,[["__scopeId","data-v-80361f4e"]]);export{it as default};
