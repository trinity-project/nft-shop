require(['jquery'],function($){
	var data = {pay_count: 10};
	

	function check_before_submit(){
		var is_correct = false;
		if(data.pay_count > 0 && (data.pay_method=='微信') && (data.channel == "wx_pub" || data.channel == 'wx_pub_qr' )){
			is_correct = true
		}else{
			alert('请选择充值数量或支付方式');
		}
		fill_form_fileds(data);
		return is_correct;
	}

	function fill_form_fileds(data){
		var $form = $('form');
		$form.find('#amount').val(data.pay_count);
		$form.find('#pay_method').val(data.pay_method);
		$form.find('#channel').val(data.channel);
		if ($form.find('#charge_type').val() != '充值'){
			$form.find('#charge_type').val('充值');
		}
	}

	document.getElementById('submit-btn').onclick = function(eve){
		if(!check_before_submit()){
			return false;
		}
	}
	//充值数量选择
	$('.count-select').find('li').on('click',function(){
		var that = $(this);
		that.closest('.count-select').find('li').removeClass('hover');
		that.addClass('hover');
		if(Number(that.data("value")).toString() != 'NaN'){
			data.pay_count = Number(that.data('value'));
		}
		// console.log(data);
	})
	$('.count-select').find('.other-count').on('keyup',function(){
		var that = $(this);
		if(that.val().length == 1){
		    that.val(that.val().replace(/[^1-9]/g,'1'))
		}else{
		    that.val(that.val().replace(/\D/g,'1'))
		}
		if(Number(that.val()).toString() != 'NaN'){
			data.pay_count = Number(that.val());
		}
		// console.log(data);
	})
	//支付方式选择
	$('.third-content').find('li').on('click',function(){
		var that = $(this);
		that.closest('.third-content').find('li').removeClass('hover');
		that.addClass('hover');
		data.pay_method = that.data("name");
		data.channel = that.data("channel");
		// console.log(data);
	})
})