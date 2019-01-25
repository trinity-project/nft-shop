require(['jquery'],function($){
    $(document).ready(function(){
        $('.get_address').on('click',function(){
            // $(this).attr('disabled',true);
            var win_id = $(this).data('id');
            $.get('/get_zj_user_address/' + win_id , function(res,status){
                console.log(res,status);
                if(res.message == 'ok'){
                    $('#name').val(res.name);
                    $('#tel').val(res.tel);
                    $('#address').val(res.whole);
                }else{
                    alert(res.message);
                }
            })
        })
    })
})