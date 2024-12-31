import{d as me,r as p,a as ce,u as pe,x as _e,y as fe,c as ve,b as ge,e as l,w as o,E as T,s as U,G as d,f as m,H as be,o as y,h as g,I as Ve,j as _,v as j,N as he,O as ye,A as we,P as Ce,Q as Ue,_ as Ae}from"./index-_txKB2za.js";import{f as ke,u as A,m as xe,n as $e,c as Ne,d as Be}from"./index-Cj3qbV5o.js";const De={class:"users-container"},Le={class:"header"},Se=me({__name:"Users",setup(Te){const E=p([]),k=p(!1),x=p(!1),V=p(!1),n=p(null),w=p(),s=ce({username:"",password:"",first_name:"",last_name:"",email:"",role:"user",is_active:!0}),H={username:[{required:!0,message:"请输入用户名"}],email:[{type:"email",message:"请输入正确的邮箱地址"}]},$=async()=>{k.value=!0;try{const a=await ke();E.value=a.data.map(e=>({...e,statusLoading:!1}))}catch(a){console.error(a),d.error("获取用户列表失败")}finally{k.value=!1}},Q=()=>{w.value&&w.value.resetFields(),s.username="",s.password="",s.first_name="",s.last_name="",s.email="",s.role="user",s.is_active=!0,n.value=null},J=()=>{Q(),V.value=!0},K=a=>{n.value=a,Object.assign(s,{username:a.username,password:"",first_name:a.first_name,last_name:a.last_name,email:a.email,role:a.role,is_active:a.is_active}),V.value=!0},W=async a=>{a&&await a.validate(async e=>{var u;if(e){x.value=!0;try{const r={username:s.username,first_name:s.first_name,last_name:s.last_name,email:s.email,role:s.role,is_active:s.is_active};s.password.trim()&&(n==null?void 0:n.username)!==((u=f.user)==null?void 0:u.username)&&(r.password=s.password),n.value?(await A(n.value.id,r),d.success("更新成功")):(await xe(r),d.success("创建成功")),V.value=!1,await $()}catch(r){console.error(r),d.error("保存失败")}finally{x.value=!1}}})},X=async a=>{var e;if(a.username===((e=f.user)==null?void 0:e.username)){d.warning("不能删除自己的账号");return}try{await Ue.confirm("确定要删除该用户吗？此操作不可恢复","警告",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}),await $e(a.id),d.success("删除成功"),await $()}catch(u){u!=="cancel"&&(console.error(u),d.error("删除失败"))}},G=a=>a?new Date(a).toLocaleString("zh-CN",{year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",second:"2-digit",hour12:!1}).replace(/\//g,"-"):"",Y=async a=>{var e;if(a.username===((e=f.user)==null?void 0:e.username)&&!a.is_active){d.warning("不能禁用自己的账号"),a.is_active=!0;return}a.statusLoading=!0;try{await A(a.id,{is_active:a.is_active}),d.success(`已${a.is_active?"启用":"禁用"}用户`)}catch(u){console.error(u),d.error("更新状态失败"),a.is_active=!a.is_active}finally{a.statusLoading=!1}},N=p(!1),I=p("notes"),M=p([]),q=p([]),B=p(!1),D=p(!1),Z=async a=>{n.value=a,N.value=!0,await Promise.all([ee(),ae()])},ee=async()=>{if(n.value){B.value=!0;try{const a=await Ne();M.value=a.data.results.map(e=>{var u;return{...e,hasAuth:(u=n.value.notes)==null?void 0:u.includes(e.id)}})}catch(a){console.error(a),d.error("获取笔记列表失败")}finally{B.value=!1}}},ae=async()=>{if(n.value){D.value=!0;try{const a=await Be();q.value=a.data.map(e=>{var u;return{...e,hasAuth:(u=n.value.note_group)==null?void 0:u.includes(e.id)}})}catch(a){console.error(a),d.error("获取分组列表失败")}finally{D.value=!1}}},le=async a=>{var e,u;if(n.value)try{const r=a.hasAuth?[...n.value.notes||[],a.id]:(n.value.notes||[]).filter(i=>i!==a.id);await A(n.value.id,{note:r,note_group:n.value.note_group||[]}),n.value.notes=r,d.success("笔记授权更新成功")}catch(r){console.error(r),d.error(((u=(e=r.response)==null?void 0:e.data)==null?void 0:u.detail)||"笔记授权更新失败"),a.hasAuth=!a.hasAuth}},te=async a=>{var e,u;if(n.value)try{const r=a.hasAuth?[...n.value.note_group||[],a.id]:(n.value.note_group||[]).filter(i=>i!==a.id);await A(n.value.id,{note:n.value.notes||[],note_group:r}),n.value.note_group=r,d.success("分组授权更新成功")}catch(r){console.error(r),d.error(((u=(e=r.response)==null?void 0:e.data)==null?void 0:u.detail)||"分组授权更新失败"),a.hasAuth=!a.hasAuth}},f=pe(),oe=_e(()=>{var a;return((a=f.user)==null?void 0:a.role)==="admin"});return fe(()=>{$()}),(a,e)=>{var R;const u=m("el-icon"),r=m("el-button"),i=m("el-table-column"),se=m("el-tag"),C=m("el-switch"),ne=m("el-button-group"),L=m("el-table"),h=m("el-input"),b=m("el-form-item"),F=m("el-option"),re=m("el-select"),ue=m("el-form"),O=m("el-dialog"),P=m("el-tab-pane"),ie=m("el-tabs"),S=be("loading");return y(),ve("div",De,[ge("div",Le,[l(r,{type:"primary",onClick:J},{default:o(()=>[l(u,null,{default:o(()=>[l(g(Ve))]),_:1}),e[12]||(e[12]=_("新建用户 "))]),_:1})]),T((y(),U(L,{data:E.value,stripe:""},{default:o(()=>[l(i,{prop:"username",label:"用户名"}),l(i,{prop:"first_name",label:"姓"}),l(i,{prop:"last_name",label:"名"}),l(i,{prop:"email",label:"邮箱"}),l(i,{prop:"role",label:"角色"},{default:o(({row:t})=>[l(se,null,{default:o(()=>[_(j(t.role),1)]),_:2},1024)]),_:1}),l(i,{prop:"is_active",label:"状态",width:"100"},{default:o(({row:t})=>{var c;return[l(C,{modelValue:t.is_active,"onUpdate:modelValue":v=>t.is_active=v,loading:t.statusLoading,onChange:v=>Y(t),"active-text":t.is_active?"启用":"禁用",disabled:t.username===((c=g(f).user)==null?void 0:c.username),"inline-prompt":""},null,8,["modelValue","onUpdate:modelValue","loading","onChange","active-text","disabled"])]}),_:1}),l(i,{prop:"last_active_at",label:"最后活跃时间"},{default:o(({row:t})=>[_(j(G(t.last_active_at)),1)]),_:1}),l(i,{prop:"date_joined",label:"加入时间"},{default:o(({row:t})=>[_(j(G(t.date_joined)),1)]),_:1}),l(i,{label:"操作",width:"280",fixed:"right"},{default:o(({row:t})=>[l(ne,null,{default:o(()=>{var c;return[l(r,{type:"primary",icon:g(he),onClick:v=>K(t)},{default:o(()=>e[13]||(e[13]=[_(" 编辑 ")])),_:2},1032,["icon","onClick"]),oe.value?(y(),U(r,{key:0,type:"success",icon:g(ye),onClick:v=>Z(t)},{default:o(()=>e[14]||(e[14]=[_(" 授权 ")])),_:2},1032,["icon","onClick"])):we("",!0),l(r,{type:"danger",icon:g(Ce),disabled:t.username===((c=g(f).user)==null?void 0:c.username),onClick:v=>X(t)},{default:o(()=>e[15]||(e[15]=[_(" 删除 ")])),_:2},1032,["icon","disabled","onClick"])]}),_:2},1024)]),_:1})]),_:1},8,["data"])),[[S,k.value]]),l(O,{modelValue:V.value,"onUpdate:modelValue":e[9]||(e[9]=t=>V.value=t),title:n.value?"编辑用户":"新建用户",width:"500px"},{footer:o(()=>[l(r,{onClick:e[7]||(e[7]=t=>V.value=!1)},{default:o(()=>e[16]||(e[16]=[_("取消")])),_:1}),l(r,{type:"primary",onClick:e[8]||(e[8]=t=>W(w.value)),loading:x.value},{default:o(()=>e[17]||(e[17]=[_(" 确定 ")])),_:1},8,["loading"])]),default:o(()=>[l(ue,{ref_key:"formRef",ref:w,model:s,rules:H,"label-width":"100px"},{default:o(()=>[l(b,{label:"用户名",prop:"username"},{default:o(()=>[l(h,{modelValue:s.username,"onUpdate:modelValue":e[0]||(e[0]=t=>s.username=t)},null,8,["modelValue"])]),_:1}),l(b,{label:"密码",prop:"password",rules:[{required:!n.value,message:"请输入密码"}]},{default:o(()=>{var t,c,v,z;return[l(h,{modelValue:s.password,"onUpdate:modelValue":e[1]||(e[1]=de=>s.password=de),type:"password",disabled:((t=n.value)==null?void 0:t.username)===((c=g(f).user)==null?void 0:c.username),placeholder:((v=n.value)==null?void 0:v.username)===((z=g(f).user)==null?void 0:z.username)?"不能修改自己的密码":n.value?"不修改请留空":"请输入密码"},null,8,["modelValue","disabled","placeholder"])]}),_:1},8,["rules"]),l(b,{label:"姓",prop:"first_name"},{default:o(()=>[l(h,{modelValue:s.first_name,"onUpdate:modelValue":e[2]||(e[2]=t=>s.first_name=t)},null,8,["modelValue"])]),_:1}),l(b,{label:"名",prop:"last_name"},{default:o(()=>[l(h,{modelValue:s.last_name,"onUpdate:modelValue":e[3]||(e[3]=t=>s.last_name=t)},null,8,["modelValue"])]),_:1}),l(b,{label:"邮箱",prop:"email"},{default:o(()=>[l(h,{modelValue:s.email,"onUpdate:modelValue":e[4]||(e[4]=t=>s.email=t)},null,8,["modelValue"])]),_:1}),l(b,{label:"角色",prop:"role"},{default:o(()=>[l(re,{modelValue:s.role,"onUpdate:modelValue":e[5]||(e[5]=t=>s.role=t)},{default:o(()=>[l(F,{label:"管理员",value:"admin"}),l(F,{label:"普通用户",value:"user"})]),_:1},8,["modelValue"])]),_:1}),l(b,{label:"状态",prop:"is_active"},{default:o(()=>[l(C,{modelValue:s.is_active,"onUpdate:modelValue":e[6]||(e[6]=t=>s.is_active=t)},null,8,["modelValue"])]),_:1})]),_:1},8,["model"])]),_:1},8,["modelValue","title"]),l(O,{modelValue:N.value,"onUpdate:modelValue":e[11]||(e[11]=t=>N.value=t),title:`${((R=n.value)==null?void 0:R.name)||""} 的授权管理`,width:"800px"},{default:o(()=>[l(ie,{modelValue:I.value,"onUpdate:modelValue":e[10]||(e[10]=t=>I.value=t)},{default:o(()=>[l(P,{label:"笔记授权",name:"notes"},{default:o(()=>[T((y(),U(L,{data:M.value,style:{width:"100%"}},{default:o(()=>[l(i,{prop:"title",label:"笔记名称"}),l(i,{prop:"group_detail.name",label:"所属分组"}),l(i,{label:"授权",width:"100",align:"center"},{default:o(({row:t})=>[l(C,{modelValue:t.hasAuth,"onUpdate:modelValue":c=>t.hasAuth=c,onChange:c=>le(t)},null,8,["modelValue","onUpdate:modelValue","onChange"])]),_:1})]),_:1},8,["data"])),[[S,B.value]])]),_:1}),l(P,{label:"分组授权",name:"groups"},{default:o(()=>[T((y(),U(L,{data:q.value,style:{width:"100%"}},{default:o(()=>[l(i,{prop:"name",label:"分组名称"}),l(i,{prop:"description",label:"描述"}),l(i,{label:"授权",width:"100",align:"center"},{default:o(({row:t})=>[l(C,{modelValue:t.hasAuth,"onUpdate:modelValue":c=>t.hasAuth=c,onChange:c=>te(t)},null,8,["modelValue","onUpdate:modelValue","onChange"])]),_:1})]),_:1},8,["data"])),[[S,D.value]])]),_:1})]),_:1},8,["modelValue"])]),_:1},8,["modelValue","title"])])}}}),Ge=Ae(Se,[["__scopeId","data-v-3f2f9ea2"]]);export{Ge as default};
