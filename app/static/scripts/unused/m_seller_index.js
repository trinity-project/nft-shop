require(['jquery'],function($){
	var data = {},seller_id;
	// actionsheet
	var actionsheet = {
	    bind: function () {
	        $('#container').on('click', '#showActionSheet', function () {
	        	if(!seller_id){
	        		seller_id = $(this).data("id");
	        	}
	            var mask = $('#mask');
	            var weuiActionsheet = $('#weui_actionsheet');
	            weuiActionsheet.addClass('weui_actionsheet_toggle');
	            mask.show()
	                .focus()//加focus是为了触发一次页面的重排(reflow or layout thrashing),使mask的transition动画得以正常触发
	                .addClass('weui_fade_toggle').one('click', function () {
	                hideActionSheet(weuiActionsheet, mask);
	            });
	            $('#actionsheet_cancel').one('click', function () {
	                hideActionSheet(weuiActionsheet, mask);
	            });
	            mask.unbind('transitionend').unbind('webkitTransitionEnd');

	            function hideActionSheet(weuiActionsheet, mask) {
	                weuiActionsheet.removeClass('weui_actionsheet_toggle');
	                mask.removeClass('weui_fade_toggle');
	                mask.on('transitionend', function () {
	                    mask.hide();
	                }).on('webkitTransitionEnd', function () {
	                    mask.hide();
	                })
	            }
	        });
	    }
	};
	actionsheet.bind();

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
	//check befor submit
	function check_before_submit(){
		is_correct = false;
		data.code = $('#ex_code').val();
		data.password = $('#ex_password').val();
		if(data.code.length == 5 && data.password.length == 5){
			if(Number(data.code).toString() != 'NaN' && Number(data.password).toString() != 'NaN'){
				is_correct = true;
			}else{
				$('#ex_code').focus();
			}
		}else{
			$('#ex_code').focus();
		}
		return is_correct;
	}
	//限制输入长度
	$('#ex_code').on('keypress',function(){
		// console.log('keyup');
		// console.log($(this).val().length);
		if($(this).val().length ==5 ){
			return false;
		}
	})
	$('#ex_password').on('keypress',function(){
		// console.log('keyup');
		// console.log($(this).val().length);
		if($(this).val().length ==5 ){
			return false;
		}
	})

	//提交
	$('.submit-btn').on('click',function(){
		var that = $(this);
		if(!check_before_submit() || that.attr('disabled') == 'disabled'){
			return false;
		}
		that.attr('disabled',true);
		that.addClass('weui_btn_disabled');
		var api = '/seller/' + seller_id + '/exchange';
		$.post(api,data,function(res,status){
			that.attr('disabled',false);
			that.removeClass('weui_btn_disabled');
			$('#actionsheet_cancel').click();
			if(status == 'success'){
				//show result

				dialog.show('兑换结果',res)
				console.log(res);
			}else{
				dialog.show('网络错误','请稍后重试!');
				//发送错误 请稍重试
			}
		})
	})
})