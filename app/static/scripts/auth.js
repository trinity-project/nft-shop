require(['jquery','bootstrap'], function ($) {
    $('.site-navbar').hide();
    function requestVerifyCode(){
        var email = $("#email").val().trim(),
            imageCode = $("#image_code").val().trim(),
            left_countdown = 90,
            sms_left_el = document.getElementById('get-sms-left'),
            sms_btn_el = document.getElementById('get_code');
            console.log(email,imageCode)
        // var lang = document.getElementById('skr').innerHTML;
        //     console.log(lang)
        var lang = $(".form-group label")[0].textContent;
        if (email.length > 0 && imageCode.length == 4){
            var url = "/get/verify/code?email=" + email + "&image_code=" + imageCode;
            sms_btn_el.setAttribute('class','disabled');
            $.get(url,function(res,status){
                console.log('status:' + status, 'res:' + res.result);
                if(status == 'success' && res.result == "success"){
                    if(lang == "Email"){
                        alert("The verification code has been sent to " + email + ". You'll receive the verification code within 5 minutes.")
                    }else{
                        alert("验证码已发送至" + email + "邮箱，5分钟内有效 请尽快验证");
                    };
                    sms_left_el.setAttribute('class','text-desc');
                    sms_btn_el.setAttribute('class','disabled hidden');
                    var timer_id = setInterval(time_handler,1000);
                    function time_handler(){
                        sms_left_el.textContent = left_countdown + 's后可重新获取';
                        if(left_countdown == 0) {
                            sms_left_el.setAttribute('class','text-desc hidden');
                            sms_btn_el.setAttribute('class','');
                            clearInterval(timer_id);
                        }
                        left_countdown -= 1;
                    }
                }else{
                    sms_btn_el.setAttribute('class','');
                    if(lang == "Email"){
                        alert("Please enter correct e-mail address and verification code.");
                    }else{
                        alert("请求正确填写邮件地址和图片验证码!");
                    }
                }
            });
        }else{
            if(lang == "Email"){
                alert("Please enter correct e-mail address and verification code.");
            }else{
                alert("请求正确填写邮件地址和图片验证码!");
            }
        }
    }
    $("#get_code").on("click", function(evt){
        if($(this).attr("class").indexOf('disabled') != -1){
            return false;
        }
        console.log("kkkk");
        requestVerifyCode();
    }),
    $("#code_img").on("click",function (evt) {
        $.get("/refresh/verify/code",function (res) {
            $("#code_img").attr('src','data:image/png;base64,' + res)
        })
    })
});