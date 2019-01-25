require(['jquery', 'pingpp-js'],function($, pingpp){
	$('.go-back').on('click',function(){
		history.back();
		// history.go(-1); //后退+刷新 
	})
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

	var data = {amount: 10, pay_method: '微信', channel: 'wx_pub', charge_type: '充值'};
	//充值金额选择
	// $('input[name="count"]').on('click',function(){
	// 	var that = $(this);
	// 	console.log(that.val());
	// })
	$('input[name="count"]').on('change',function(){
		var that = $(this);
		console.log(that.val());
		if(Number(that.val()).toString() != 'NaN'){
			data.amount = Number(that.val());
		}
	})
	$('.other-input').on('keyup',function(){
		var that = $(this);
		if(that.val().length == 1){
		    that.val(that.val().replace(/[^1-9]/g,'1'))
		}else{
		    that.val(that.val().replace(/\D/g,'1'))
		}
		if(Number(that.val()).toString() != 'NaN'){
			data.amount = Number(that.val());
		}
	})
	//支付方式选择
	$('input[name="methods"]').on('change',function(){
		data.pay_method = $(this).val();
		data.channel = $(this).data("channel"); 
	})

	function check_before_submit(){
		var is_correct = false;
		if(data.amount > 0 && (data.pay_method=='微信') && (data.channel == "wx_pub")){
			is_correct = true
		}else{
			dialog.show('表单错误','请选择充值数量或支付方式');
		}
		// fill_form_fileds(data);
		return is_correct;
	}

	function fill_form_fileds(data){
		// console.log(data);
		var $form = $('form');
		$form.find('#amount').val(data.amount);
		$form.find('#pay_method').val(data.pay_method);
		$form.find('#channel').val(data.channel);
		if ($form.find('#charge_type').val() != '充值'){
			$form.find('#charge_type').val('充值');
		}
	}
	$('#submit-btn').on('click',function(){
		// console.log('click');
		// console.log(data);
		
		if(check_before_submit() && $(this).attr('disabled') == undefined){
			$(this).attr('disabled',true);
			$(this).addClass('weui_btn_disabled');
			$.post('/charge',data,function(res,status){
				if(status=='success' && res){
					if (res == '创建订单失败' || res == '订单数据不合法'){
						$(this).attr('disabled',false);
						$(this).removeClass('weui_btn_disabled');
					}else{
						console.log(res);
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
		}
	})
})