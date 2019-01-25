(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['announced_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = (helpers.compare || (depth0 && depth0.compare) || helpers.helperMissing).call(depth0 != null ? depth0 : {},((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),1,{"name":"compare","hash":{},"fn":container.program(2, data, 0),"inverse":container.program(4, data, 0),"data":data})) != null ? stack1 : "");
},"2":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr class=\"head\">\n	<td class=\"head-col\" colspan=\"3\">\n		<div>\n			<span>第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期</span>\n			<span class=\"pull-right red-color\">揭晓时间: "
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_time : stack1), depth0))
    + "</span>\n		</div>\n	</td>\n</tr>\n<tr class=\"m-history-item\">\n	<td class=\"col-img\"><a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img style=\"border-radius:0\" src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\"></a></td>\n	<td class=\"join-detail\">\n		<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">\n			<div class=\"zj-user\">\n				<span class=\"describe-info\">幸运用户: </span><span>"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.zj_user : stack1)) != null ? stack1.name : stack1), depth0))
    + "</span>\n			</div>\n			<div class=\"user-id\">\n				<span><span class=\"describe-info\">用户ID: </span>"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.zj_user : stack1)) != null ? stack1.display_id : stack1), depth0))
    + "(唯一不变的标识)</span>\n			</div>\n			<div class=\"lucky-num describe-info\"><span>幸运号码: <strong>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</strong></span></div>\n			<div class=\"join-info describe-info\">\n				<span>参与人次: <strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</span>\n			</div>\n		</a>\n	</td>\n	<td style=\"font-size:14px;\">\n		<a style=\"color:#ccc;\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><span class=\"glyphicon glyphicon-chevron-right\"></span></a>\n	</td>\n</tr>\n<tr><td colspan=\"3\"></td></tr>\n";
},"4":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr class=\"head\">\n	<td class=\"head-col\" colspan=\"3\">\n		<div>\n			<span>第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期揭晓在即</span>\n		</div>\n	</td>\n</tr>\n<tr class=\"m-history-item\">\n	<td class=\"col-img\"><a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img style=\"border-radius:0\" src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\"></a></td>\n	<td class=\"join-detail\">\n		<div class=\"count-down kj-number text-center\" data-finish=\"\" data-now=\"\">\n		</div>\n	</td>\n	<td style=\"font-size:14px;\">\n		<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\" style=\"color:#ccc;\" href=\"\"><span class=\"glyphicon glyphicon-chevron-right\"></span></a>\n	</td>\n</tr>\n<tr><td colspan=\"3\"></td></tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['charge_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<li class=\"item\">\n	<div class=\"charge-count clearfix\">\n		<span style=\"margin-right:15px;\">充值金额: <strong>"
    + alias2(alias1((depth0 != null ? depth0.pay_count : depth0), depth0))
    + "</strong>元</span>\n		<span>获得夺宝币: <strong>"
    + alias2(alias1((depth0 != null ? depth0.db_count : depth0), depth0))
    + "</strong>个</span>\n		<span class=\"pull-right\">"
    + alias2(alias1((depth0 != null ? depth0.pay_method : depth0), depth0))
    + "支付</span>\n	</div>\n	<div class=\"charge-info describe-info clearfix\">\n		<span >时间: "
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "</span>\n		<span class=\"pull-right\">\n			<span>状态: </span>\n			<span style=\"color:green\">"
    + ((stack1 = helpers["if"].call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.status : depth0),{"name":"if","hash":{},"fn":container.program(2, data, 0),"inverse":container.program(4, data, 0),"data":data})) != null ? stack1 : "")
    + "</span>\n		</span>\n	</div>\n</li>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "成功";
},"4":function(container,depth0,helpers,partials,data) {
    return "失败";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['history_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr class=\"head\">\n	<td class=\"head-col\" colspan=\"3\">\n		<div>\n			<span>第"
    + alias2(alias1((depth0 != null ? depth0.number : depth0), depth0))
    + "期</span>\n			<span class=\"pull-right red-color\">揭晓时间: "
    + alias2(alias1((depth0 != null ? depth0.kj_time : depth0), depth0))
    + "</span>\n		</div>\n	</td>\n</tr>\n<tr class=\"m-history-item\">\n	<td class=\"col-img\"><a href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.zj_user : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img src=\""
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.zj_user : depth0)) != null ? stack1.avatar : stack1), depth0))
    + "\"></a></td>\n	<td class=\"join-detail\">\n		<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">\n			<div class=\"zj-user\">\n				<span class=\"describe-info\">幸运用户: </span><span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.zj_user : depth0)) != null ? stack1.name : stack1), depth0))
    + "</span>\n			</div>\n			<div class=\"user-id\">\n				<span><span class=\"describe-info\">用户ID: </span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.zj_user : depth0)) != null ? stack1.display_id : stack1), depth0))
    + "(唯一不变的标识)</span>\n			</div>\n			<div class=\"lucky-num describe-info\"><span>幸运号码: <strong>"
    + alias2(alias1((depth0 != null ? depth0.kj_num : depth0), depth0))
    + "</strong></span></div>\n		</a>\n	</td>\n	<td style=\"font-size:14px;\">\n		<a style=\"color:#ccc;\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><span class=\"glyphicon glyphicon-chevron-right\"></span></a>\n	</td>\n</tr>\n<tr><td colspan=\"3\"></td></tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['join_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr>\n	<td class=\"col-img\">\n		<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">\n			<img src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\">\n		</a>\n	</td>\n	<td class=\"product-info\">\n		<a class=\"link-color\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "</a>\n		<div class=\"describe-info\">总需<span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.total_count : stack1), depth0))
    + "</span>人次</div>\n"
    + ((stack1 = (helpers.compare || (depth0 && depth0.compare) || helpers.helperMissing).call(depth0 != null ? depth0 : {},((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),0,{"name":"compare","hash":{},"fn":container.program(2, data, 0),"inverse":container.program(7, data, 0),"data":data})) != null ? stack1 : "")
    + "		<div class=\"period-number\">第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期</div>\n	</td>\n</tr>\n";
},"2":function(container,depth0,helpers,partials,data) {
    var stack1;

  return "		<div class=\"describe-info clearfix\">\n			<span>参与<strong>"
    + container.escapeExpression(container.lambda(((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.count : stack1), depth0))
    + "</strong>人次</span>\n			<span class=\"pull-right\">"
    + ((stack1 = (helpers.compare || (depth0 && depth0.compare) || helpers.helperMissing).call(depth0 != null ? depth0 : {},((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),1,{"name":"compare","hash":{},"fn":container.program(3, data, 0),"inverse":container.program(5, data, 0),"data":data})) != null ? stack1 : "")
    + "</span>\n		</div>\n";
},"3":function(container,depth0,helpers,partials,data) {
    return "已揭晓";
},"5":function(container,depth0,helpers,partials,data) {
    return "揭晓中";
},"7":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "		<div class=\"sell-progress\">\n			<span class=\"orange\" style=\"width:"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.pecent : stack1), depth0))
    + "%\"></span>\n		</div>\n		<div class=\"describe-info clearfix\">\n			<span>参与<strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</span>\n			<span class=\"pull-right\">剩余"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.left : stack1), depth0))
    + "人次</span>\n		</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['list_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<div class=\"col-md-3 col-sm-4 col-xs-6 fix-padding\">\n	<div class=\"product-item\">\n		<div class=\"img-link\">\n			<a target=\"_blank\" href=\"/shop/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\"><img src=\""
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.product : depth0)) != null ? stack1.thumbnail : stack1), depth0))
    + "\"></a>\n		</div>\n		<div class=\"item-title\"><a target=\"_blank\" href=\"/shop/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.product : depth0)) != null ? stack1.title : stack1), depth0))
    + "</a></div>\n		<div class=\"text-right describe-info\">\n			<span class=\"\">剩余"
    + alias2(alias1((depth0 != null ? depth0.left : depth0), depth0))
    + "人次</span>\n		</div>\n		<div class=\"sell-progress\">\n			<span class=\"orange\" style=\"width:"
    + alias2(alias1((depth0 != null ? depth0.pecent : depth0), depth0))
    + "%\"></span>\n		</div>\n		<div class=\"join-info text-center \">\n			<a class=\"db-btn\" href=\"/shop/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\">立即参加</a>\n		</div>\n	</div>\n</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['lucky_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr>\n	<td class=\"col-img\">\n		<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">\n			<img src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\">\n		</a>\n	</td>\n	<td class=\"product-info\">\n		<a class=\"link-color\" target=\"_blank\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "\n		</a>\n		<div class=\"describe-info clearfix\">\n			<span>总需<span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.total_count : stack1), depth0))
    + "</span>人次</span>\n			<span class=\"pull-right\">总共参与<strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</span>\n		</div>\n		<div class=\"describe-info jx-time\">\n			<span>揭晓时间: "
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_time : stack1), depth0))
    + "</span>\n		</div>\n		<div class=\"period-number clearfix\">\n			<span>第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期</span>\n			<span class=\"pull-right\">幸运号码: <strong>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</strong></span>\n		</div>\n	</td>\n</tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['period_join_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr class=\"m-join-item\">\n	<td class=\"col-img\"><a href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img src=\""
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.avatar : stack1), depth0))
    + "\"></a></td>\n	<td class=\"join-detail\">\n		<a href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.id : stack1), depth0))
    + "\" class=\"link-color\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.name : stack1), depth0))
    + "</a>\n		<a class=\"view-num link-color\" href=\"javascript:void(0);\" data-num=\""
    + alias2(alias1((depth0 != null ? depth0.num : depth0), depth0))
    + "\">查看号码</a>\n		<div class=\"user-id\">\n			<span><span class=\"describe-info\">用户ID: </span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.display_id : stack1), depth0))
    + "(唯一不变的标识)</span>\n		</div>\n		<div class=\"join-info clearfix\">\n			<span>参与了<strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</span>\n			<span class=\"describe-info pull-right\">"
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "</span>\n		</div>\n	</td>\n</tr>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['show_item_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<div class=\"col-md-3 col-sm-4 col-xs-6 fix-padding\">\n	<div class=\"product-item\">\n		<div class=\"img-link\">\n			<a href=\"/show/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\"><img src=\""
    + alias2(alias1((depth0 != null ? depth0.thumbnail : depth0), depth0))
    + "!list\"></a>\n		</div>\n		<div class=\"product-title\"><a class=\"link-color\" href=\"/show/"
    + alias2(alias1((depth0 != null ? depth0.id : depth0), depth0))
    + "\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.product : depth0)) != null ? stack1.title : stack1), depth0))
    + "</a></div>\n		<div><span class=\"describe-info\">第"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "期</span></div>\n		<div class=\"lucky-number\">\n			<span class=\"describe-info\">幸运号码： <span class=\"red-color\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</span></span>\n		</div>\n		<div class=\"user-info describe-info\">\n			<a class=\"link-color\" href=\"/user/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.owner : depth0)) != null ? stack1.name : stack1), depth0))
    + "</a>\n			<span class=\"pull-right time\">"
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "</span>\n		</div>\n	</div>\n</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
})();