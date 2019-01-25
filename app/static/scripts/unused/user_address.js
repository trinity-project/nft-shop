require(['jquery', 'modal-box', 'jquery-cityselect'], function ($) {

    $('.add-addr').on('click',function(){
        $('#addr_modal').modal('show');
        // $('#city').citySelect({
        //     url: '/static/dist/scripts/city.min.js',
        //     prov:"江西", //省份 
        //     city:"上饶", //城市
        //     dist: '万年县' 
        // })
    })

    $('#city').citySelect({
        url: '/static/dist/scripts/city.min.js',
        //默认省市区/县
        // prov:"请选择", //省份 
        // city:"请选择", //城市 
        // dist:"请选择", //区县 
        required: false,
        nodata: 'none'
    })

    var uid = $('.info-list').data("id"),
        data={},
        url= '/api/v1.0/address';

    $('#submitbtn').on('click',function(){
        var that = $(this),check_para = true;
        if(that.closest('form').attr('action').indexOf('?edit=true') != -1){
            check_para = false;
        }
        if(!check_befor_submit(check_para)){
            return false;
        }else{
            $('#addr_modal').modal('hide');
        }
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
    
    //编辑地址

    //地址操作
    $('.options-addr').find('a').on('click',function(){
        var that = $(this),data={},method,
            addr_id = that.closest('tr').data("id");
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
                                    that.closest('tr').fadeOut();
                                }else{
                                    that.closest('tbody').find('.default-flag').text('');
                                    that.fadeOut();
                                    that.closest('tr').find('.default-flag').text('是');
                                }
                            }
                        }
                    });
                }
            }
        }else{
            console.log('kkkkkk');
            var $form = $('form'),$tr=that.closest('tr');
            $form.attr('action',url + '?edit=true&addr_id=' + addr_id);
            $form.find('#name').val($tr.data("name"));
            $form.find('#detail').val($tr.data("detail"));
            $form.find('#tel').val($tr.data("tel"));
            $form.find('#province').val($tr.data("prov"));
            $form.find('#city_input').val($tr.data("city"));
            $form.find('#dist').val($tr.data("dist"));
                // var dist = 
            $('#city').citySelect({
                url: '/static/dist/scripts/city.min.js',
                prov: $tr.data("prov"),
                city: $tr.data("city"),
                dist: $tr.data("dist"),
                required: false,
                nodata: 'none'
            });
          
            $('#addr_modal').modal('show');
        }
       
    })
    //设为默认地址
   
});
