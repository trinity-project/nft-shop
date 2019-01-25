(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['charge_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<tr>\n	<td style=\"color:#888;\">"
    + alias2(alias1((depth0 != null ? depth0.created_datetime : depth0), depth0))
    + "</td>\n	<td>"
    + alias2(alias1((depth0 != null ? depth0.pay_method : depth0), depth0))
    + "</td>\n	<td><strong>"
    + alias2(alias1((depth0 != null ? depth0.pay_count : depth0), depth0))
    + "</strong></td>\n	<td><strong>"
    + alias2(alias1((depth0 != null ? depth0.db_count : depth0), depth0))
    + "</strong></td>\n"
    + ((stack1 = helpers["if"].call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.status : depth0),{"name":"if","hash":{},"fn":container.program(2, data, 0),"inverse":container.program(4, data, 0),"data":data})) != null ? stack1 : "")
    + "</tr>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "	<td style=\"color:green\">成功</td>\n";
},"4":function(container,depth0,helpers,partials,data) {
    return "	<td style=\"color:green\">失败</td>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
templates['join_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression, alias3=depth0 != null ? depth0 : {};

  return "<tr>\n	<td class=\"col-img\"><a target=\"_blank\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\"></a></td>\n	<td class=\"product-info\">\n		<a class=\"link-color\" target=\"_blank\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "</a>\n		<div class=\"describe-info\">总需：<span>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.total_count : stack1), depth0))
    + "</span>人次</div>\n"
    + ((stack1 = helpers.unless.call(alias3,((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),{"name":"unless","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "	</td>\n	<td>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "</td>\n\n	<td>\n"
    + ((stack1 = helpers["if"].call(alias3,((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),{"name":"if","hash":{},"fn":container.program(4, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "		"
    + ((stack1 = helpers.unless.call(alias3,((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),{"name":"unless","hash":{},"fn":container.program(9, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "\n	</td>\n	<td>\n		<div>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "人次</div>\n"
    + ((stack1 = helpers.unless.call(alias3,((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),{"name":"unless","hash":{},"fn":container.program(11, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "	</td>\n	<td><a class=\"link-color\" target=\"_blank\" href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">详情</a></td>\n</tr>\n";
},"2":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "		<div class=\"sell-progress\">\n			<span class=\"orange\" style=\"width:"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.percent : stack1), depth0))
    + "%\"></span>\n		</div>\n		<div class=\"describe-info clearfix\">\n			<span>参与："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.join_count : stack1), depth0))
    + "人次</span>\n			<span class=\"pull-right\">剩余："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.left : stack1), depth0))
    + "人次</span>\n		</div>\n";
},"4":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = (helpers.compare || (depth0 && depth0.compare) || helpers.helperMissing).call(depth0 != null ? depth0 : {},((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.status : stack1),1,{"name":"compare","hash":{},"fn":container.program(5, data, 0),"inverse":container.program(7, data, 0),"data":data})) != null ? stack1 : "");
},"5":function(container,depth0,helpers,partials,data) {
    return "			已经揭晓\n			";
},"7":function(container,depth0,helpers,partials,data) {
    return "正在揭晓\n";
},"9":function(container,depth0,helpers,partials,data) {
    return "正在进行";
},"11":function(container,depth0,helpers,partials,data) {
    return "		<div class=\"buy-more\">\n			<a class=\"link-color\" href=\"javascript:;\">追加</a>\n		</div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "\n";
},"useData":true});
templates['lucky_tpl'] = template({"1":function(container,depth0,helpers,partials,data) {
    var stack1, alias1=container.lambda, alias2=container.escapeExpression;

  return "<div class=\"col-md-3 col-sm-4 col-xs-6 fix-padding\">\n	<div class=\"announced-item\">\n		<div class=\"img-link\">\n			<a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\"><img src=\""
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.thumbnail : stack1), depth0))
    + "\"></a>\n		</div>\n		<div class=\"item-title\"><a href=\"/shop/"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.id : stack1), depth0))
    + "\">"
    + alias2(alias1(((stack1 = ((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.product : stack1)) != null ? stack1.title : stack1), depth0))
    + "</a></div>\n		<div class=\"sell-info\">总需："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.total_count : stack1), depth0))
    + "人次</div>\n		<div class=\"period-info\">期号："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.number : stack1), depth0))
    + "</div>\n		<div class=\"result\">\n			<ul class=\"result-info\">\n				<li>幸运号码： <strong>"
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_num : stack1), depth0))
    + "</strong></li>\n				<li>本期参与：<strong>"
    + alias2(alias1((depth0 != null ? depth0.count : depth0), depth0))
    + "</strong>人次</li>\n				<li>揭晓时间："
    + alias2(alias1(((stack1 = (depth0 != null ? depth0.period : depth0)) != null ? stack1.kj_time : stack1), depth0))
    + "</li>\n			</ul>\n		</div>\n"
    + ((stack1 = helpers.unless.call(depth0 != null ? depth0 : {},((stack1 = ((stack1 = (depth0 != null ? depth0.item : depth0)) != null ? stack1.period : stack1)) != null ? stack1.has_show : stack1),{"name":"unless","hash":{},"fn":container.program(2, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "")
    + "	</div>\n</div>\n";
},"2":function(container,depth0,helpers,partials,data) {
    return "		<div class=\"show-back\"><a href=\"/show/post\"><span class=\"glyphicon glyphicon-camera\"></span><span>晒单</span></a></div>\n";
},"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return ((stack1 = helpers.each.call(depth0 != null ? depth0 : {},(depth0 != null ? depth0.data : depth0),{"name":"each","hash":{},"fn":container.program(1, data, 0),"inverse":container.noop,"data":data})) != null ? stack1 : "");
},"useData":true});
})();