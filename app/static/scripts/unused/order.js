require([],function(){
	function check_before_submit(){
		var is_correct = false,
			pid = document.getElementById('pid').getAttribute('value'),
			// title = document.getElementById('title').getAttribute('value'),
			amount = document.getElementById('amount').getAttribute('value'),
			pay_method = document.getElementById('pay_method').getAttribute('value'),
			channel = document.getElementById('channel').getAttribute('value'),
			action = document.getElementById('post-form').getAttribute('action'),
			coupon_dom = document.getElementById('coupon'),
			charge_type = document.getElementById('charge_type').getAttribute('value');
		if(charge_type != '购买'){
			document.getElementById('charge_type').setAttribute('value','购买');
		}
		if((Number(pid).toString() != 'NaN' && Number(pid) > 0) && (Number(amount).toString() != 'NaN' && Number(amount) > 0)){
			// console.log(pid,title,amount,pay_method,channel);
			if(pay_method == '微信' || pay_method == '余额' || pay_method == '优惠券'){
				if(pay_method == '微信' && (channel == 'wx_pub' || channel == 'wx_wap') && action == '/charge'){
					is_correct = true;
				}else if(pay_method == '余额' && action == '/pay/handler') {
					is_correct = true;
				}else if(pay_method == '优惠券' && action == '/pay/handler' && coupon_dom) {
					is_correct = true;
				}else{
					alert('订单数据不合法，请重新提交');
				}
			}else{
				alert('请选择一种支付方式');
			}
		}else{
			alert('订单数据不合法，请重新提交');
		}
		return is_correct;
	}

	document.getElementById('submit-btn').onclick = function(eve){
		if(!check_before_submit()){
			return false;
		}
	}
})