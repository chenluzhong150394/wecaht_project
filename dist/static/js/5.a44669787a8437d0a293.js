webpackJsonp([5],{QwFy:function(t,e){},fRGa:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o={name:"operationLog",data:function(){return{token:sessionStorage.getItem("token"),uid:sessionStorage.getItem("uid"),log:null}},mounted:function(){this.getData()},methods:{getData:function(){var t=this;t.$axios({method:"post",url:window.$g_Api+"/oa/operationlog",data:{token:t.token,uid:t.uid}}).then(function(e){0==e.data.code?t.log=e.data.data:console.error(e.data.message)}).catch(function(t){})}}},a={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"my_wap",attrs:{id:"operationlog"}},[t._m(0),t._v(" "),n("div",{staticClass:"log_box"},[n("table",[t._m(1),t._v(" "),n("tbody",t._l(t.log,function(e,o){return n("tr",[n("td",[t._v(t._s(e.record))]),t._v(" "),n("td",[t._v(t._s(e.time))]),t._v(" "),n("td",[t._v(t._s(e.username))])])}),0)])])])},staticRenderFns:[function(){var t=this.$createElement,e=this._self._c||t;return e("p",{staticClass:"position"},[e("i",{staticClass:"el-icon-location-outline"}),this._v("您现在的位置：操作日志")])},function(){var t=this.$createElement,e=this._self._c||t;return e("thead",[e("tr",[e("th",[this._v("操作记录")]),this._v(" "),e("th",[this._v("时间")]),this._v(" "),e("th",[this._v("用户名")])])])}]};var i=n("VU/8")(o,a,!1,function(t){n("QwFy")},"data-v-e6b689be",null);e.default=i.exports}});