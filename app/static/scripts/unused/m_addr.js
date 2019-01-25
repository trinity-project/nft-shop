require(['jquery','jquery-cityselect'],function($){
	// actionsheet
	var actionsheet = {
	    bind: function () {
	        $('.bottom-option').on('click', '.bottom-btn', function () {
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
	
	$('.go-back').on('click',function(){
		history.back();
		// history.go(-1); //后退+刷新 
	})
	//初始化城市选择数据
	$('#city').citySelect({
	    url: '/static/dist/scripts/city.min.js',
	    //默认省市区/县
	    // prov:"请选择", //省份 
	    // city:"请选择", //城市 
	    // dist:"请选择", //区县 
	    required: false,
	    nodata: 'none'
	})

	function check_befor_submit(create){
	    if(create){
	        if($('.address').find('tbody').find('.addr-row').length >= 5){
	            return false;
	        }
	    }
	    var $form = $('form'), is_correct=false;
	    $form.find('#province').val($form.find('.prov').val());
	    $form.find('#city_input').val($form.find('.city').val());
	    $form.find('#dist').val($form.find('.dist').val());
	    var name = $form.find('#name').val(),
	        detail = $form.find('#detail').val(),
	        tel = $form.find('#tel').val(),
	        province = $form.find('#province').val(),
	        city = $form.find('#city_input').val(),
	        dist = $form.find('#dist').val();
	    if($.trim(name).length > 0 && $.trim(detail).length > 0 && $.trim(tel).length >0){
	        if($.trim(province).length > 0 && $.trim(city).length > 0){
	            is_correct = true;
	        }else if($.trim(province).length ==0 ){
	            $form.find('.prov').focus();
	        }else if($.trim(city).length ==0 ){
	            $form.find('.city').focus();
	        }
	    }else if($.trim(name).length ==0 ){
	        $form.find('#name').focus();
	    }else if($.trim(detail).length ==0 ){
	        $form.find('#detail').focus();
	    }else if($.trim(tel).length ==0 ){
	        $form.find('#tel').focus();
	    }
	    return is_correct;
	}

	var uid = $('.list').data("uid"),
	    data={},
	    url= '/api/v1.0/address';
	//提交表单
	$('#submitbtn').on('click',function(){
	    var that = $(this),check_para = true;
	    if(that.closest('form').attr('action').indexOf('?edit=true') != -1){
	        check_para = false;
	    }
	    if(!check_befor_submit(check_para)){
	        return false;
	    }else{
	        $('#actionsheet_cancel').click();
	    }
	})
	//地址操作
	$('.options').find('a').on('click',function(){
		console.log("click");
	    var that = $(this),data={},method,
	        addr_id = that.closest('.item').data("id");
	    console.log(uid,addr_id);
	    if((that.hasClass('delete-addr')) || (that.hasClass('default-addr'))){
	        if(that.hasClass('delete-addr')){
	            method = 'DELETE';
	        }else if(that.hasClass('default-addr')){
	            method = 'PUT';
	        }
	        if(Number(addr_id).toString()!= 'NaN' && Number(addr_id) > 0){
	            if(Number(uid).toString()!='NaN' && Number(uid) > 0){
	                data.addr_id = addr_id;
	                data.uid = uid;
	                $.ajax({
	                    url: url,
	                    type: method,
	                    data: data,
	                    success: function(res,status){
	                        if(status=='success' && res.message=='ok'){
	                            if(method == 'DELETE'){
	                                that.closest('.item').fadeOut();
	                            }else{
	                                $('.list').find('.text-left').find('a').text('设为默认');
	                                $('.list').find('.text-left').find('a').addClass('default-addr');
	                                $('.list').find('.text-left').find('a').addClass('link-color');
	                                that.removeClass('default-addr');
	                                that.removeClass('link-color');
	                                // that.removeClass('lin');
	                                that.text('默认');
	                            }
	                        }
	                    }
	                });
	            }
	        }
	    }else if(that.hasClass('edit-addr')){
	        console.log('kkkkkk');
	        var $form = $('form'),$item=that.closest('.item');
	        $form.attr('action',url + '?edit=true&addr_id=' + addr_id);
	        $form.find('#name').val($item.data("name"));
	        $form.find('#detail').val($item.data("detail"));
	        $form.find('#tel').val($item.data("tel"));
	        $form.find('#province').val($item.data("prov"));
	        $form.find('#city_input').val($item.data("city"));
	        $form.find('#dist').val($item.data("dist"));
	            // var dist = 
	        $('#city').citySelect({
	            url: '/static/dist/scripts/city.min.js',
	            prov: $item.data("prov"),
	            city: $item.data("city"),
	            dist: $item.data("dist"),
	            required: false,
	            nodata: 'none'
	        });
	      
	        $('.bottom-btn').click();
	    }
	   
	})

})