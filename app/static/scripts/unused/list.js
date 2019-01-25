require(['jquery'], function ($) {
	 //判断用户登陆
    function check_login(){
        if($('body').hasClass('login')){
            return true;
        }else{
            return false;
        }
    }
    $('.db-btn').on('click',function(eve){
    	if(!check_login()){
            location.href = '/login?next=' + location.href;
            return false;
        }
        else if(!check_before_submit(eve.target)){
            return false;
        }    
    })
    //检查表单字段
    $('input[name="amount"]').on('keyup',function(){
        var that = $(this);
        if(that.val().length == 1){
            that.val(that.val().replace(/[^1-9]/g,'1'))
        }else{
            that.val(that.val().replace(/\D/g,'1'))
        }
    })

    $('input[name="amount"]').on('afterpaste',function(){
        var that = $(this);
        if(that.val().length == 1){
            that.val(that.val().replace(/[^1-9]/g,'1'))
        }else{
            that.val(that.val().replace(/\D/g,'1'))
        }
    })
    $('.join-select').find('a').on('click',function(){
        var that = $(this),cur_amount = 1;

        if(that.hasClass('minus')){
            cur_amount = Number(that.next('input[name="amount"]').val());
            if(cur_amount != NaN && cur_amount >1 ){
                that.next('input[name="amount"]').val(cur_amount-1);
            }
        }else{
            cur_amount =  Number(that.prev('input[name="amount"]').val());
            var max = Number(that.data("max"));
            if(cur_amount != NaN && (cur_amount < max)){
                that.prev('input[name="amount"]').val(cur_amount + 1);
            }
        }
    })

    function check_before_submit(target){
        console.log(target);
        var parent = $(target).prev('.join-select'),
            amount = Number(parent.find('input[name="amount"]').val()), 
            pid = Number(parent.find('input[name="pid"]').val()),
            max = Number(parent.find('.plus').data('max'));
        console.log(amount,pid,max);
        if(amount != NaN && pid != NaN && pid != 0 && max!= NaN){
            if(amount >= 1 && amount <= max){
                return true
            }else{
                parent.find('input[name="amount"]').focus();
            }
        }
    }
})