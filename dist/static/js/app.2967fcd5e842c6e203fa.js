webpackJsonp([14],{"6CwT":function(e,n){},NHnr:function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var a=t("fZjL"),r=t.n(a),o=t("//Fk"),p=t.n(o),i=t("7+uW"),u={render:function(){var e=this.$createElement,n=this._self._c||e;return n("div",{attrs:{id:"app"}},[n("router-view")],1)},staticRenderFns:[]};var s=t("VU/8")(null,u,!1,function(e){t("6CwT")},null,null).exports,c=t("/ocq");i.default.use(c.a);var l=new c.a({routes:[{path:"/",redirect:"/login"},{path:"/home",component:function(e){return Promise.all([t.e(0),t.e(3)]).then(function(){var n=[t("MpTN")];e.apply(null,n)}.bind(this)).catch(t.oe)},meta:{title:"自述文件"},children:[{path:"/home",name:"home",component:function(e){return t.e(7).then(function(){var n=[t("Jjwz")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/today",name:"today",component:function(e){return t.e(5).then(function(){var n=[t("vQug")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/untreated",name:"untreated",component:function(e){return t.e(8).then(function(){var n=[t("OjCw")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/transactionRecord",name:"transactionRecord",component:function(e){return t.e(2).then(function(){var n=[t("6AtE")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/deviceInfo",name:"deviceInfo",component:function(e){return t.e(10).then(function(){var n=[t("i2eM")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/paymentSettings",name:"paymentSettings",component:function(e){return t.e(1).then(function(){var n=[t("Cf0F")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/privilegeManagement",name:"privilegeManagement",component:function(e){return t.e(4).then(function(){var n=[t("9wlK")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/userInfo",name:"userInfo",component:function(e){return Promise.all([t.e(0),t.e(12)]).then(function(){var n=[t("w64o")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/operationLog",name:"operationLog",component:function(e){return t.e(6).then(function(){var n=[t("wH8w")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"/data",name:"data",component:function(e){return t.e(9).then(function(){var n=[t("SjB2")];e.apply(null,n)}.bind(this)).catch(t.oe)}}]},{path:"/login",component:function(e){return Promise.all([t.e(0),t.e(11)]).then(function(){var n=[t("GF4k")];e.apply(null,n)}.bind(this)).catch(t.oe)}}]}),f=t("mtWM"),h=t.n(f),I=t("zL8q"),d=t.n(I),m=(t("tvR6"),t("XLwt"),t("mw3O")),v=t.n(m),g=(t("j1ja"),{setSub:function(e){return e[1]?((e[0]-e[1])/e[1]*100).toFixed(2)+"%":""},formatDate:function(e){if(e&&0!=e){var n=new Date(1e3*e);return n.getFullYear()+"-"+(n.getMonth()+1)+"-"+n.getDate()+"   "+n.getHours()+":"+n.getMinutes()+":"+n.getSeconds()}return""},getIntDate:function(e){return e&&e>0?(parseInt(e/1e4)>9?"20"+parseInt(e/1e4):"200"+parseInt(e/1e4))+"-"+(parseInt(e%1e4/100)>9?parseInt(e%1e4/100):"0"+parseInt(e%1e4/100))+"-"+(parseInt(e%100/1)>9?parseInt(e%100/1):"0"+parseInt(e%100/1)):""},getIntDate2:function(e){return e&&e>0?parseInt(e/1e4)+"-"+(parseInt(e%1e4/100)>9?parseInt(e%1e4/100):"0"+parseInt(e%1e4/100))+"-"+(parseInt(e%100/1)>9?parseInt(e%100/1):"0"+parseInt(e%100/1)):""},getIntTime2:function(e){return e?(parseInt(e%1e6/1e4)>9?parseInt(e%1e6/1e4):"0"+parseInt(e%1e6/1e4))+":"+(parseInt(e%1e4/100)>9?parseInt(e%1e4/100):"0"+parseInt(e%1e4/100))+":"+(parseInt(e%100)>9?parseInt(e%100):"0"+parseInt(e%100)):""},getIntTime:function(e){return e?(parseInt(e/1e10)>9?"20"+parseInt(e/1e10):"200"+parseInt(e/1e10))+"-"+(parseInt(e%1e10/1e8)>9?parseInt(e%1e10/1e8):"0"+parseInt(e%1e10/1e8))+"-"+(parseInt(e%1e8/1e6)>9?parseInt(e%1e8/1e6):"0"+parseInt(e%1e8/1e6))+" "+(parseInt(e%1e6/1e4)>9?parseInt(e%1e6/1e4):"0"+parseInt(e%1e6/1e4))+":"+(parseInt(e%1e4/100)>9?parseInt(e%1e4/100):"0"+parseInt(e%1e4/100))+":"+(parseInt(e%100)>9?parseInt(e%100):"0"+parseInt(e%100)):""},getspeed:function(e){return e?e.toFixed(0):e},getvol:function(e){return e>3.4?parseInt((e-3.4)/.8*100)+"%":"0%"},getnewvol:function(e){return e?Math.floor(10*e)/10:e},secondToDate:function(e){var n=parseInt(e)+"秒";if(parseInt(e)>60){var t=parseInt(e)%60,a=parseInt(e/60);if(n=a+"分"+t+"秒",a>60)a=parseInt(e/60)%60,n=parseInt(parseInt(e/60)/60)+"小时"+a+"分"+t+"秒"}return n}});i.default.use(d.a,{size:"small"}),h.a.interceptors.request.use(function(e){return e},function(e){return p.a.reject(e)}),h.a.interceptors.response.use(function(e){if(1006!=e.data.code)return e;l.replace({path:"/login"})},function(e){return p.a.reject(e)});for(var y in i.default.prototype.$ajax=function(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},t=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"post",a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"application/json;charset=UTF-8";return h.a.defaults.withCredentials=!1,h.a.defaults.headers={"Content-Type":a},e=window.$g_Api+e,new p.a(function(o,p){var i=void 0;if("get"===t&&r()(n).length>0){var u="";r()(n).forEach(function(e){u+=e+"="+n[e]+"&"}),e=e+"?"+u,i=h.a.get(e)}else i="text/plain"==a||"application/json;charset=UTF-8"==a?h.a.post(e,v.a.parse(n)):h.a.post(e,v.a.stringify(n));i.then(function(e){o(e.data)}).catch(function(e){p(e)})})},i.default.prototype.$axios=h.a,i.default.prototype.$qs=v.a,g)i.default.filter(y,g[y]);new i.default({router:l,render:function(e){return e(s)}}).$mount("#app")},tvR6:function(e,n){}},["NHnr"]);