webpackJsonp([8],{"1ILn":function(e,o){},UHcH:function(e,o,t){"use strict";Object.defineProperty(o,"__esModule",{value:!0});var a={name:"manage",data:function(){return{dialogVisible:!1,token:sessionStorage.getItem("token"),uid:sessionStorage.getItem("uid"),title:"",userlist:[],username:null,password:null,real_name:null,userType:"客服",loading:!1,power:{},t1:!0,id:null}},mounted:function(){this.getuserlist()},methods:{changeBox:function(e,o){var t=this;if(t.username="",t.password="",t.id=null,"1"==e)t.power={datastatistics1:!1,daydata1:!1,oacustomer1:!1,order1:!1,achievement1:!1,profits1:!1,moneylog1:!1,devices1:!1,datastatistics2:!1,daydata2:!1,oacustomer2:!1,order2:!1,achievement2:!1,profits2:!1,money:!1,devices2:!1,manage:!1,operationlog:!1,check_order:!1,groupdata:!1,groupmanagement:!1,devicestate:!1},t.username="",t.password="",t.t1=!0,t.title="新增用户";else if(2==e){t.id=o,t.t1=!1,t.title="修改用户";for(var a=void 0,r=0,s=t.userlist.length;r<s;r++)if(t.userlist[r].id==o){a=r;break}t.power=t.userlist[a].auth,t.password=t.userlist[a].password,t.username=t.userlist[a].username,t.real_name=t.userlist[a].real_name,t.userType=t.userlist[a].group}this.dialogVisible=!0},setUser:function(){var e=this;console.log(e.userType);var o=window.$g_Api+"/oa/manage/edituser",t={token:e.token,uid:e.uid,username:e.username,password:e.password,power:e.power,real_name:e.real_name,group:e.userType};e.userApi(o,t,"新增用户成功")},reviseUser:function(){var e=this,o=window.$g_Api+"/oa/manage/update_user_info",t={token:e.token,uid:e.uid,username:e.username,password:e.password,power:e.power,id:e.id,real_name:e.real_name,group:e.userType};e.userApi(o,t,"修改用户成功!")},userApi:function(e,o,t){var a=this;if(!a.username||!a.password)return a.$message.warning("用户名和密码不能为空"),!1;a.loading=!0,a.$axios({method:"post",url:e,data:o}).then(function(e){a.loading=!1,0==e.data.code?(a.$message.success(t),a.getuserlist(),a.dialogVisible=!1,a.power={}):a.$message.error(e.data.message)}).catch(function(e){a.$message.error(e)})},del:function(e){var o=this;o.$axios({method:"post",url:window.$g_Api+"/oa/manage/remove_user",data:{token:o.token,uid:o.uid,id:e}}).then(function(e){0==e.data.code&&o.getuserlist()}).catch(function(e){o.$message.error(e)})},open2:function(e){var o=this;this.$confirm("此操作将删除该用户, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){o.del(e),o.$message({type:"success",message:"删除成功!"})}).catch(function(){o.$message({type:"info",message:"已取消删除"})})},getuserlist:function(){var e=this;e.$axios({method:"post",url:window.$g_Api+"/oa/manage",data:{token:e.token,uid:e.uid}}).then(function(o){0==o.data.code?e.userlist=o.data.data:console.error(o.data.message)}).catch(function(e){console.error(e)})}}},r={render:function(){var e=this,o=e.$createElement,t=e._self._c||o;return t("div",{staticClass:"my_wap",attrs:{id:"manage"}},[t("div",{staticClass:"crumbs"},[t("el-breadcrumb",{attrs:{separator:"/"}},[t("el-breadcrumb-item",[t("i",{staticClass:"el-icon-warning"}),e._v("权限管理")])],1)],1),e._v(" "),t("div",{staticClass:"container wap"},[t("el-button",{attrs:{type:"primary"},on:{click:function(o){e.changeBox("1")}}},[e._v("+新增用户")]),e._v(" "),t("div",{staticClass:"userlist_box"},[t("table",[e._m(0),e._v(" "),t("tbody",e._l(e.userlist,function(o){return t("tr",{key:o.id},[t("td",[e._v(e._s(o.real_name))]),e._v(" "),t("td",[e._v(e._s(o.username))]),e._v(" "),t("td",[e._v(e._s(o.password))]),e._v(" "),t("td",[e._v(e._s(o.group))]),e._v(" "),t("td",[t("el-button",{attrs:{type:"primary"},on:{click:function(t){e.changeBox("2",o.id)}}},[e._v("查看修改")])],1),e._v(" "),t("td",[t("el-button",{attrs:{type:"danger"},on:{click:function(t){e.open2(o.id)}}},[e._v("删除用户")])],1)])}),0)])])],1),e._v(" "),t("el-dialog",{attrs:{title:e.title,visible:e.dialogVisible,width:"40%"},on:{"update:visible":function(o){e.dialogVisible=o}}},[t("div",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],staticClass:"addUserBox"},[[t("el-radio-group",{staticStyle:{"margin-top":"-40px"},model:{value:e.userType,callback:function(o){e.userType=o},expression:"userType"}},[t("el-radio",{attrs:{label:"客服"}},[e._v("客服")]),e._v(" "),t("el-radio",{attrs:{label:"主管"}},[e._v("主管")]),e._v(" "),t("el-radio",{attrs:{label:"股东"}},[e._v("股东")]),e._v(" "),t("el-radio",{attrs:{label:"合伙人"}},[e._v("合伙人")]),e._v(" "),t("el-radio",{attrs:{label:"管理员"}},[e._v("管理员")])],1)],e._v(" "),t("p",[t("span",{staticStyle:{display:"inline-block",width:"80px"}},[e._v("真实姓名:")]),e._v(" "),t("input",{directives:[{name:"model",rawName:"v-model",value:e.real_name,expression:"real_name"}],attrs:{type:"text"},domProps:{value:e.real_name},on:{input:function(o){o.target.composing||(e.real_name=o.target.value)}}}),e._v(" "),t("br"),e._v(" "),t("span",{staticStyle:{display:"inline-block","margin-top":"8px",width:"80px"}},[e._v("设置用户名:")]),e._v(" "),t("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],attrs:{type:"text"},domProps:{value:e.username},on:{input:function(o){o.target.composing||(e.username=o.target.value)}}}),e._v(" "),t("br"),e._v(" "),t("span",{staticStyle:{display:"inline-block","margin-top":"8px",width:"80px"}},[e._v("设置密码:")]),e._v(" "),t("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],attrs:{type:"text"},domProps:{value:e.password},on:{input:function(o){o.target.composing||(e.password=o.target.value)}}})]),e._v(" "),t("p",[e._v("\n                权限设置:\n            ")]),e._v(" "),t("p",{staticClass:"cheackBox"},[[t("el-checkbox",{model:{value:e.power.datastatistics1,callback:function(o){e.$set(e.power,"datastatistics1",o)},expression:"power.datastatistics1"}},[e._v("实时数据(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.daydata1,callback:function(o){e.$set(e.power,"daydata1",o)},expression:"power.daydata1"}},[e._v("每日数据(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.oacustomer1,callback:function(o){e.$set(e.power,"oacustomer1",o)},expression:"power.oacustomer1"}},[e._v("客户人数(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.order1,callback:function(o){e.$set(e.power,"order1",o)},expression:"power.order1"}},[e._v("订单比(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.achievement1,callback:function(o){e.$set(e.power,"achievement1",o)},expression:"power.achievement1"}},[e._v("员工绩效(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.profits1,callback:function(o){e.$set(e.power,"profits1",o)},expression:"power.profits1"}},[e._v("股东收益(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.moneylog1,callback:function(o){e.$set(e.power,"moneylog1",o)},expression:"power.moneylog1"}},[e._v("转账记录(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.devices1,callback:function(o){e.$set(e.power,"devices1",o)},expression:"power.devices1"}},[e._v("设备管理(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.groupdata,callback:function(o){e.$set(e.power,"groupdata",o)},expression:"power.groupdata"}},[e._v("分组数据(可视)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.oacustomer2,callback:function(o){e.$set(e.power,"oacustomer2",o)},expression:"power.oacustomer2"}},[e._v("客户人数(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.achievement2,callback:function(o){e.$set(e.power,"achievement2",o)},expression:"power.achievement2"}},[e._v("员工绩效(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.profits2,callback:function(o){e.$set(e.power,"profits2",o)},expression:"power.profits2"}},[e._v("股东收益(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.money,callback:function(o){e.$set(e.power,"money",o)},expression:"power.money"}},[e._v("新建转账(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.devices2,callback:function(o){e.$set(e.power,"devices2",o)},expression:"power.devices2"}},[e._v("设备管理(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.manage,callback:function(o){e.$set(e.power,"manage",o)},expression:"power.manage"}},[e._v("用户管理(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.operationlog,callback:function(o){e.$set(e.power,"operationlog",o)},expression:"power.operationlog"}},[e._v("操作日志(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.groupmanagement,callback:function(o){e.$set(e.power,"groupmanagement",o)},expression:"power.groupmanagement"}},[e._v("分组管理(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.check_order,callback:function(o){e.$set(e.power,"check_order",o)},expression:"power.check_order"}},[e._v("订单查询(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.devicestate,callback:function(o){e.$set(e.power,"devicestate",o)},expression:"power.devicestate"}},[e._v("设备推广(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.accountoutput,callback:function(o){e.$set(e.power,"accountoutput",o)},expression:"power.accountoutput"}},[e._v("账号产出(操作)")]),e._v(" "),t("el-checkbox",{model:{value:e.power.order2,callback:function(o){e.$set(e.power,"order2",o)},expression:"power.order2"}},[e._v("订单比(操作)")])]],2)],2),e._v(" "),t("div",{staticClass:"bnt_box"},[e.t1?t("el-button",{attrs:{type:"primary"},on:{click:function(o){e.setUser()}}},[e._v("新增用户")]):t("el-button",{attrs:{type:"primary"},on:{click:function(o){e.reviseUser()}}},[e._v("修改用户")])],1)])],1)},staticRenderFns:[function(){var e=this,o=e.$createElement,t=e._self._c||o;return t("thead",[t("tr",[t("th",[e._v("真实姓名")]),e._v(" "),t("th",[e._v("用户名")]),e._v(" "),t("th",[e._v("密码")]),e._v(" "),t("th",[e._v("类型")]),e._v(" "),t("th",[e._v("操作")]),e._v(" "),t("th",[e._v("操作")])])])}]};var s=t("VU/8")(a,r,!1,function(e){t("1ILn")},null,null);o.default=s.exports}});