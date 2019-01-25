require(['jquery','bootstrap'], function ($) {
      // 订单的模态框script函数
      $('.order-infos').on("click", function(evt){
        $('#order-modal').modal();
        $(".quantity .inputNum").val(1);
        // var visibleWindow = $(window).height(),
        //     $modal = $('#order-modal'),e
        //     dialogHeight = $modal.find('.modal-dialog').height();
        // var offset = (visibleWindow - dialogHeight) / 3;
        // console.log(visibleWindow, dialogHeight, offset);
        // $modal.find('.modal-dialog').css('margin-top', offset);
        $div = $(evt.target).closest('.product-item');
        var commodity_id = $($div.find('input')[0]).val(),
            commodity_name = $($div.find('input')[1]).val(),
            commodity_seller = $($div.find('input')[2]).val(),
            commodity_price = $($div.find('input')[4]).val(),
            commodity_uint = $($div.find('input')[5]).val(),
            commodity_type = $($div.find('input')[3]).val(),
            commodity_desc = $($div.find('input')[7]).val(),
            prop_num = $($div.find('input')[8]).val(),
            page = $($div.find('input')[6]).val();
        $('.modal-body .commodity_id').text(commodity_id);
        $('.modal-body .commodity_name').text(commodity_name);
        $('.modal-body .commodity_seller').text(commodity_seller);
        $('.modal-body .commodity_type').text(commodity_type);
        $('.modal-body .commodity_price').text(commodity_price);
        $('.modal-body .commodity_uint').text(commodity_uint);
        $('.modal-body .commodity_desc').text(commodity_desc);
        $('.modal-body .prop_num').text(prop_num);
        $('.modal-body #id').attr('value',commodity_id);
        $('.modal-body #name').attr('value',commodity_name);
        $('.modal-body #sell').attr('value',commodity_seller);
        $('.modal-body #price').attr('value',commodity_price);
        $('.modal-body #type').attr('value',commodity_type);
        $('.modal-body #uint').attr('value',commodity_uint);
        $('.modal-body #page').attr('value',page);
    });
    $(".quantity .subBtn").click(function(){
        var num = $(".quantity .inputNum").val();
        var price = $(".commodity_price").eq(1).text();
        if (1 >= num ){
            $(".quantity .inputNum").val(1);
            return;
        }
        num = num - 1;
        $(".quantity .inputNum").val(num);
        $(".commodity_price").eq(0).text(num * price);
    })
    $(".quantity .addBtn").click(function(){
        var price = $(".commodity_price").eq(1).text();
        var num = $(".quantity .inputNum").val();
        if (99 <= num ){
            $(".quantity .inputNum").val(99);
            return;
        }
        num = num*1 + 1;
        $(".quantity .inputNum").val(num);
        $(".commodity_price").eq(0).text(num * price);
    })
    $(".quantity .inputNum").on("input",function(){
        var num = $(".quantity .inputNum").val();
        var price = $(".commodity_price").eq(1).text();
        // if (0 >= num || "" === num ){
        //     $(".quantity .inputNum").val(1);
        //     num =0
        // }
        $(".commodity_price").eq(0).text( num * price);
    })
})