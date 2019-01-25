require(['jquery'],function($){
    $(document).ready(function(){
        $('.get_code_img').on('click',function(){
            $(this).attr('disabled',true);
            if(check_before_post()){
                var data = {};
                data.code_param = $('#code_param').val();
                $.post('/get_qrcode_param', data, function(res,status){
                    console.log(res,status);
                    if(res){
                        res = JSON.parse(res);
                        $('#code_img').val(res.url);
                        $('#code_link').val(res.code_link);
                        $('#ticket').val(res.ticket);
                    }
                })
            }
        })
        
    })
    function check_before_post(){
        is_correct = false
        if($('#name').val().length > 0 && $('#code_param').val().length > 0){
            if($('#code_param').val().indexOf('seller_') >= 0){
                is_correct = true;
            }else{
                alert('二维码参数不合法');
            }
        }else{
            alert('商家名称或二维码参数不能为空');
        }
        return is_correct;
    }
})