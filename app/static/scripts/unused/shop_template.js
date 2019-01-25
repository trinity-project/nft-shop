(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['history_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "		<div class=\"user-avatar\">\n			<img src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.zj_user : stack1)) != null ? stack1.avatar : stack1), depth0))
    + "\">\n		</div>\n		<div class=\"user-name\">\n			恭喜 <a href=\"/user/"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.zj_user : stack1)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.zj_user : stack1)) != null ? stack1.name : stack1), depth0))
    + "</a>获得了<span class=\"red-color\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "</span>\n		</div>\n		<hr>\n		<ul>\n			<li>用户ID："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.display_id : stack1), depth0))
    + "(用户唯一不变标识)</li>\n			<li>幸运号码：<strong>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</strong></li>\n			<li>揭晓时间：<span class=\"describe-info\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.kj_time : stack1), depth0))
    + "</span></li>\n		</ul>\n";
},"3":function(container,depth0,helpers,partials,data) {
    return "		<div style=\"margin:10px 0 20px 0\">该期即将揭晓....</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<h3>开奖信息</h3>\n<div class=\"history-period\">\n	<div class=\"numbers-select\">\n		<a href=\"javascript:void(0)\" class=\"left\"><span class=\"glyphicon glyphicon-chevron-left\"></span></a>\n		<span class=\"number-show\">期号："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.number : stack1), depth0))
    + "</span>\n		<a href=\"javascript:void(0)\" class=\"right\"><span class=\"glyphicon glyphicon-chevron-right\"></span></a>\n	</div>\n	<div class=\"kj-result\">\n"
    + ((stack1 = (helpers.compare || (depth0 && depth0.compare) || helpers.helperMissing).call(depth0 != null ? depth0 : {},((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.status : stack1),1,{"name":"compare","hash":{},"fn":container.program(1, data, 0),"inverse":container.program(3, data, 0),"data":data})) != null ? stack1 : "")
    + "		<div class=\"text-center\">\n			<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.data : depth0)) != null ? stack1.id : stack1), depth0))
    + "\" class=\"btn btn-primary\">查看详情</a>\n		</div>\n	</div>\n</div>";
},"useData":true});
templates['join_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<ul class=\"item\">\n	<li class=\"time\">"
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "<span></span></li>\n	<li class=\"avatar\"><img src=\""
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.avatar : stack1), depth0))
    + "\"></li>\n	<li class=\"name\"><a href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.name : stack1), depth0))
    + "</span></a></li>\n	<li class=\"join-count\"><span>参与了<strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</span><a data-num=\""
    + alias2(alias1((depth0 != null ? depth0.num : depth0), depth0))
    + "\" class=\"view-num\" href=\"javascript:void(0)\">查看号码</a></li>\n</ul>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['show_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<div class=\"col-md-3 col-sm-4 col-xs-6 fix-padding\">\n	<div class=\"announced-item\">\n		<div class=\"img-link\">\n			<a href=\"/show/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\"><img src=\""
    + alias2(alias1((depth0 != null ? depth0.thumbnail : depth0), depth0))
    + "!list\"></a>\n		</div>\n		<div class=\"item-title\">\n            <a href=\"/show/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "</a>\n        </div>\n        <div><span>幸运号码：</span><strong>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</strong>\n        	<span class=\"describe-info\">第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期</span>\n        </div>\n		<div class=\"content\">\n			<ul class=\"post-info\">\n				<li class=\"user-name\"><a href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.name : stack1), depth0))
    + "</a></li>\n				<li class=\"time\">"
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "</li>\n			</ul>\n            <div class=\"post\">"
    + alias2(alias1((depth0 != null ? depth0.title : depth0), depth0))
    + "</div>\n		</div>\n	</div>\n</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
})();