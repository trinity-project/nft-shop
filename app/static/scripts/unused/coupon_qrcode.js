require(['jquery','modal-box'],function($){
    $(document).ready(function(){
        var product_title = $('.qrcode-list').data('product');
        var coupon_name = $('.qrcode-list').data('coupon');
        $('.get-qrcode').on('click',function(){
            var that = $(this);
            // $(this).attr('disabled',true);
            var coupon_id = that.data('id');
            that.addClass('disabled');
            that.attr('disabled',true);
            $.get('/seller/create_qr/' + coupon_id , function(res,status){
                console.log(res,status);
                if(status == 'success'){
                    modal_box.find('.coupon-code').text('优惠码: ' + coupon_name + '--' + res.code);
                    modal_box.find('.coupon-product').text('扫码领取优惠券参与 ' + product_title);
                    modal_box.find('img').attr('src',res.qr_picture);
                    modal_box.modal('show');
                    var html = '<li><a data-pic="'+ res.qr_picture +'" class="link-color" href="javascript:void(0);">' +
                    '<span>'+ coupon_name +'--'+ res.code +'</span></a></li>';
                    $('.qrcode-list').append(html);
                    that.attr('disabled',false);
                    that.removeClass('disabled');
                }
                //show qr_code;
            })
        })
        var modal_box = $('#qrcode-modal');
        $('.qrcode-list').on('click','a',function(){
            modal_box.find('.coupon-code').text('优惠码: ' + $(this).find('span').text());
            modal_box.find('.coupon-product').text('扫码领取优惠券参与 ' + product_title);
            modal_box.find('img').attr('src',$(this).data('pic'));
            modal_box.modal('show');
        })
    })
})