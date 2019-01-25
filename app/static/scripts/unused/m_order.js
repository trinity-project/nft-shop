require(["jquery",'pingpp-js'],function($,pingpp){
	var dialog = {
		show: function(title,body) {
			var $tips_dialog = $('#tips_dialog');
			$tips_dialog.find('.weui_dialog_hd').text(title);
			$tips_dialog.find('.weui_dialog_bd').text(body);
			$('#tips_dialog').show()
		},
	    bind: function () {
            $('#tips_dialog').on('click', '.weui_btn_dialog', function () {
                $('#tips_dialog').hide();
            });
	    }
	};
	dialog.bind();
	var data = {charge_type: '购买'};
	data.pay_method = $('#pay_method').val();
	data.channel = $('#channel').val();
	var code = $('#coupon').val();
	var coupon_amount = Number($('#coupon').data('amount'));
	function check_before_submit(){
		var is_correct = false;
		console.log(code,coupon_amount,data.amount);
		// console.log(data);
		if (data.charge_type != '购买'){
			data.charge_type = '购买';
		}
		if(data.amount.toString() != 'NaN' && data.pid.toString() != 'NaN' && data.amount > 0 && data.pid > 0){
			if (data.pay_method == '微信' && data.channel == 'wx_pub'){
				is_correct = true;
			}else if(data.pay_method == '余额'){
				fill_form_fileds(data);
				is_correct = true;
			}else if(data.pay_method == '优惠券' && code.length > 0 && coupon_amount >= data.amount){
				fill_form_fileds(data);
				is_correct = true;
			}else{
				dialog.show('表单错误','请检查后重新提交');
			}
		}
		return is_correct;
	}

	$('#submit-btn').on('click', function(){
		var that = $(this);
		if(!check_before_submit() || that.attr('disabled') != undefined || that.attr('disabled_submit') == 'yes'){
			return false;
		}
		
		if(data.pay_method == '微信'){
			that.attr('disabled',true);
			that.addClass('weui_btn_disabled');
			$.post('/charge',data,function(res,status){
				if(status=='success' && res){
					if (res == '创建订单失败' || res == '订单数据不合法'){
						$(this).attr('disabled',false);
						$(this).removeClass('weui_btn_disabled');
					}else{
						// console.log(res);
						//调用支付控件
						pingpp.createPayment(res,function(result,err){
							// console.log(result);
							// console.log(err.msg);
							// console.log(err.extra);
							if (result == "success") {
							    //查询服务端支付结果
							    var json_obj = JSON.parse(res),
							    	check_url = '/charge/result/' + json_obj.order_no;
							    $.get(check_url,function(check_res){
							    	// console.log(check_res);
							    	// dialog.show('支付结果','支付成功');
							    	if(check_res.status){
							    		location.replace('/pay/result?para=' + json_obj.order_no);
							    		//支付成功处理
							    	}
							    })
							} else if (result == "fail") {
								dialog.show('支付结果','支付失败,请尝试重新提交订单');
							    // charge 不正确或者微信公众账号支付失败时会在此处返回
							} else if (result == "cancel") {
								console.log('取消付款');
						        // 微信公众账号支付取消支付
							}
						})
					}
				}
			})
			return false;
		}
		else{
			that.addClass('weui_btn_disabled');
			that.attr('disabled_submit','yes');
		}
	}) 
	function fill_form_fileds(data){
		// console.log(data);
		var $form = $('form');
		$form.find('#amount').val(data.amount);
		$form.find('#pay_method').val(data.pay_method);
		$form.find('#channel').val(data.channel);
		if ($form.find('#charge_type').val() != '购买'){
			$form.find('#charge_type').val('购买');
		}
	}
	//支付方式选择
	$('input[name="methods"]').on('change',function(){
		data.pay_method = $(this).val();
		data.channel = $(this).data("channel"); 
	})
	//优惠券选择
	$('.coupon-list').on('click','.coupon',function(){
		var that = $(this);
		that.closest('.coupon-list').find('.coupon-checked').removeClass('coupon-checked');
		that.find('.check-flag').addClass('coupon-checked');
		$('#coupon').val(that.data('code'));
		code = that.data('code');
		coupon_amount = Number(that.data('amount'));
	})
	//订单数量
	data.pid = Number($('.order-count').data("pid"));
	data.amount = Number($('.order-count').data('count'));
})