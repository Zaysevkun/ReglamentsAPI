(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-779a4409"],{"3a1c":function(t,e,s){},"45fc":function(t,e,s){"use strict";var a=s("23e7"),r=s("b727").some,i=s("a640"),n=s("ae40"),o=i("some"),c=n("some");a({target:"Array",proto:!0,forced:!o||!c},{some:function(t){return r(this,t,arguments.length>1?arguments[1]:void 0)}})},"562d":function(t,e,s){"use strict";var a=s("3a1c"),r=s.n(a);r.a},fe16:function(t,e,s){"use strict";s.r(e);var a=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("b-container",{staticClass:"pt-4"},[s("div",{staticClass:"large-title mt-5"},[t._v("Комментарии от "+t._s(t.revisions.length?t.revisions[0].created_by.department.name:""))])]),s("div",{staticClass:"md-text mt-5 pt-5"},[s("b-container",t._l(t.revisions,(function(e){return s("b-row",{key:e.id,staticClass:"w-100 task-item",attrs:{"align-v":"center"}},[s("b-col",{staticClass:"justify-content-between d-flex align-items-center",attrs:{cols:"5"}},[s("div",{directives:[{name:"b-toggle",rawName:"v-b-toggle",value:"collapse-"+e.id,expression:"`collapse-${revision.id}`"}],staticClass:"clearitem d-flex align-items-center"},[s("div",{staticClass:"dot-wrapper mr-3 pl-1 pt-1"},[s("div",{staticClass:"large-dot",class:{"bg-grey":e.is_marked_solved}})]),s("div",{staticClass:"text-blue ml-3",class:{"text-grey":e.is_marked_solved}},[t._v("Комментарий от "+t._s(e.created_by.department.name))])]),s("b-icon",{staticClass:"float-right text-blue",attrs:{icon:"chevron-down"}})],1),s("b-col",{staticClass:"text-right small_grey-text",attrs:{cols:"2"}},[e.is_marked_solved?s("div",[t._v("Решенный")]):s("router-link",{attrs:{to:"/reglament/"+t.taskId+"/"+t.revisorId+"/"+e.id}},[t._v("Перейти")])],1),s("b-col",{staticClass:"text-right small_grey-text",attrs:{cols:"3"}},[t._v(" "+t._s(e.created_by.last_name?e.created_by.last_name:"")+" "+t._s(e.created_by.first_name?e.created_by.first_name[0]+". ":"")+" "+t._s(e.created_by.patronymic_name?e.created_by.patronymic_name[0]+".":"")+" ")]),s("b-col",{staticClass:"text-right small_grey-text",attrs:{cols:"2"}},[t._v(" "+t._s(t.moment(e.created_at).format("DD.MM.YYYY HH:mm"))+" ")]),s("b-col",{attrs:{cols:"8"}},[s("b-collapse",{attrs:{id:"collapse-"+e.id}},[s("b-card",{staticClass:"mt-4 mb-2"},[t._v(t._s(e.report))])],1)],1)],1)})),1)],1)],1)},r=[],i=(s("45fc"),s("5530")),n=s("bc34"),o=s("2f62"),c=s("c1df"),l=s.n(c),d={name:"Revisions",components:{},props:{taskId:{required:!0,type:String},revisorId:{required:!0,type:String}},data:function(){return{reglament:{},revisions:[],moment:l.a}},created:function(){this.getReglament(),this.getRevisionsByUser()},computed:Object(i["a"])({},Object(o["mapGetters"])(["currentUser"])),methods:{hasIssue:function(t){return console.log(t),this.revisions.some((function(e){return!e.is_marked_solved&&e.created_by.username===t.username}))},gotoIssue:function(t){console.log(t)},getReglament:function(){var t=this;n["a"].getReglament(this.taskId).then((function(e){var s=e.data;t.reglament=s[0]}))},getRevisionsByUser:function(){var t=this;n["a"].getRevisionsByUser(this.taskId,this.revisorId).then((function(e){var s=e.data;t.revisions=s.results}))}}},m=d,v=(s("562d"),s("2877")),u=Object(v["a"])(m,a,r,!1,null,"78d1a9c1",null);e["default"]=u.exports}}]);
//# sourceMappingURL=chunk-779a4409.03e7568a.js.map