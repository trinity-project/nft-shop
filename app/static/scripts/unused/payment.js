require(['jquery','jquery-qrcode'],function($){
    (function(){
        // console.log($('#qrcode').data("json"));
        var target = $('#qrcode'),
            json_obj = target.data("json");
        if(typeof(json_obj) != 'object'){
            json_obj = JSON.parse(json_obj);
        }
        target.qrcode({
            render: "canvas",
            width: 200,
            height: 200,
            text: json_obj.credential.wx_pub_qr
        });
    })()

    var charge_order = $('#charge_order').data("order"),
        timer_id = false,
        check_times = 0,
        check_max_times = 15,
        check_interval = 4000,
        check_url = '/charge/result/' + charge_order;
    // console.log(charge_order);

    //轮询服务端支付结果
    function check_pay_result(){
        $.get(check_url,function(res,status){
            check_times ++;
            if(status == 'success'){
                // console.log(res.status);
                if(res.status){
                    //支付成功 处理
                    location.replace('/pay/result?para=' + charge_order);
                    
                }else{
                    if(timer_id){
                        clearTimeout(timer_id);
                    }
                    if(check_times < check_max_times){
                        timer_id = setTimeout(check_pay_result,check_interval);
                    }
                }
            }
        })
    }
    $(document).ready(function(){
        check_pay_result();
    })
})