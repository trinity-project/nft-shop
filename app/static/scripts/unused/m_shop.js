require(['jquery','vendor/scroll_load','jquery-downcount'],function($,Load){
	// actionsheet
	var actionsheet = {
	    bind: function () {
	        $('#container').on('click', '#showActionSheet', function () {
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
	    bind: function () {
	        $('.m-shop').on('click','.view-num',function () {
	        	var that = $(this),num_text = that.data('num').toString();
	        	if(that.data('zj')){
	        	    var flag_num = '<strong>' + that.data('zj') + '</strong>';
	        	    num_text = num_text.replace(that.data('zj'),flag_num);
	        	}
	        	$('#num_dialog').find('.weui_dialog_title').html('所有号码');
	        	$('#num_dialog').find('.weui_dialog_bd').html(num_text);
	            $('#num_dialog').show().on('click', '.weui_btn_dialog', function () {
	                $('#num_dialog').off('click').hide();
	            });
	        });
	        $('.m-shop').on('click','.get-coupon',function(){
	        	$('#num_dialog').on('click', '.weui_btn_dialog', function () {
	        	    $('#num_dialog').off('click').hide();
	        	});
	        })
	    },
	    show:function(title,msg){
	    	$('#num_dialog').find('.weui_dialog_title').html(title);
	    	$('#num_dialog').find('.weui_dialog_bd').html(msg);
	    	$('#num_dialog').show();
	    },
	};
	dialog.bind();
	//到计时
	var $count_dom = $('.count-down');
	var $diff_now = $('.diff-now');
    if( $count_dom.length > 0){
    	$count_dom.downCount({
    		finish: new Date($diff_now.data('finish')).getTime(),
    		now: parseFloat($diff_now.data('now'))*1000
    	},function(){
    		$count_dom.find('span').text('0');
    		location.reload();
    	})
    }
    
	//检查表单字段
	$('input[name="amount"]').on('keyup',function(){
	    var that = $(this);
	    if(that.val().length == 1){
	        that.val(that.val().replace(/[^1-9]/g,'1'))
	    }else{
	        that.val(that.val().replace(/\D/g,'1'))
	    }
	    update_count_list(that.val());
	})

	$('input[name="amount"]').on('afterpaste',function(){
	    var that = $(this);
	    if(that.val().length == 1){
	        that.val(that.val().replace(/[^1-9]/g,'1'))
	    }else{
	        that.val(that.val().replace(/\D/g,'1'))
	    }
	    update_count_list(that.val());
	})

	$('.join-select').find('a').on('click',function(){
	    var that = $(this),cur_amount = 1;

	    if(that.hasClass('minus')){
	        cur_amount = Number(that.next('input[name="amount"]').val());
	        if(cur_amount.toString() != 'NaN' && cur_amount >1 ){
	            that.next('input[name="amount"]').val(cur_amount-1);
	        }
	    }else{
	        cur_amount =  Number(that.prev('input[name="amount"]').val());
	        var max = Number(that.data("max"));
	        if(cur_amount.toString() != 'NaN' && (cur_amount < max)){
	            that.prev('input[name="amount"]').val(cur_amount + 1);
	        }
	    }
	    update_count_list($('input[name="amount"]').val());
	})

	$('.count-list').find('span').on('click',function(){
		var that = $(this),target=$('input[name="amount"]');
		that.closest('.count-list').find('span').removeClass('active');
		that.addClass('active');
		target.val(that.data('value'));
	})

	function update_count_list(amount){
		var all_count = $('.count-list').find('span');
		all_count.removeClass('active');
		$.each(all_count,function(){
			if($(this).data('value') == amount){
				$(this).addClass('active');
			}
		})
	}

	function check_before_submit(){
	    var amount = Number($('input[name="amount"]').val()), 
	        pid = Number($('input[name="pid"]').val()),
	        max = Number($('.join-select').find('.plus').data('max'));
	    if(amount.toString() != 'NaN' && pid.toString() != 'NaN' && pid != 0 && max.toString() != 'NaN'){
	        if(amount >= 1 && amount <= max){
	            return true
	        }else{
	            $('input[name="amount"]').focus();
	        }
	    }
	}

	  //判断用户登陆
    function check_login(){
        if($('body').hasClass('login')){
            return true;
        }else{
            return false;
        }
    }

	//submit 
	$('.submit-btn').on('click',function(){
		if(!check_login()){
		    location.href = '/login?next=' + location.href;
		    return false;
		}            
	    if(!check_before_submit()){
	        return false;
	    }
	})

	// 领取优惠券请求
	$('.get-coupon').on('click',function(){
		var that = $(this),coupon_id = that.data("id");
		if(!check_login()){
			dialog.show('领取优惠券','抱歉,您需要先登陆!');
			return;
		}else if(that.attr('disabled-submit') == 'yes'){
			return;
		}else{
			that.css('color','#999');
			that.attr('disabled-submit','yes');
			$.get('/get_coupon_without_qrcode/' + coupon_id,function(res,status){
				if(status=='success'){
					dialog.show('领取优惠券',res);
				}else{
					dialog.show('网络错误','请稍后重试');
				}
			})
			// get coupon
			//callback
			
		}
	})

	$(document).ready(function(){
		var target = $('.join-body'),
			pid = target.data('pid'),
			api = '/api/v1.0/period_join_record?pid=' + pid;
		Load.load_list(api,target,'period_join_item_tpl');
	})

	$('.scroll-top').on('click',function(){
		var scrollTop = $(window).scrollTop();
		if (scrollTop >= 50){
			$('html,body').animate({scrollTop:0},'slow');
		}
	})
})