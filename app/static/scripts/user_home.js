require(['jquery', 'modal-box', 'bootstrap'], function ($) {
    var usd_price = 0;
    //自定义handlebars help
    // Handlebars.registerHelper("compare",function(v1,v2,options){
    //     if(v1 > v2){return options.fn(this);}
    //     else{return options.inverse(this);}
    // });

    // function get_uid(){
    //     var uid = $('.info-list').data("id");
    //     return uid;
    // }

    // function get_type(){
    //     var path = location.pathname;
    //     if(path.indexOf('zj') > 0){
    //         return 'win';
    //     }else if(path.indexOf('show') > 0){
    //         return 'show';
    //     }else if(path.indexOf('cz') > 0){
    //         return 'cz';
    //     }else if(path.indexOf('address') > 0){
    //         return 'address';
    //     }else{
    //         return 'join';
    //     }
    // }
    //滚动加载数据
    // (function(){
    //     var $window = $(window),
    //         $document = $(document),
    //         page = 2,
    //         init_top = 0,
    //         page_type = get_type();

    //     function load_list(url,target_container,tpl_name){
    //         $.get(url,function(res,status){
    //             if(status == 'success' && res.message == 'ok'){
    //                 if(res.data && res.data.length > 0){
    //                     var html = Handlebars.templates[tpl_name](res);
    //                     target_container.append(html);
    //                     //可能还有下一页
    //                     if(res.data.length == 20){
    //                         page+=1;
    //                         //绑定滚动事件
    //                         $window.bind('scroll',onScroll);
    //                     }else{
    //                         $('.tips').fadeIn();
    //                     }
    //                 }else{
    //                     $('.tips').fadeIn();
    //                 }
    //             }
    //         })
    //     }

    //     function onScroll(e){
    //         var win_height = window.innerHeight ? window.innerHeight : $window.height(); // iphone fix
    //         var close_to_bottome = ($window.scrollTop() + win_height > $document.height() - 100);
    //         var scroll_direction = $window.scrollTop() > init_top;
    //         if(close_to_bottome && scroll_direction){
    //             //进入事件处理后解绑事件
    //             $window.unbind('scroll', onScroll);
    //             //更新init_top
    //             init_top = $window.scrollTop();
    //             var url,target,tpl_name;
    //             if(page_type == 'join'){
    //                 url = '/api/v1.0/user_join?uid=' + get_uid() + '&page=' + page;
    //                 target = $('table .join-body');
    //                 tpl_name = 'join_tpl';
    //             }else if(page_type == 'win'){
    //                 url = '/api/v1.0/user_win?uid=' + get_uid() + '&page=' + page;
    //                 target = $('.lucky-body');
    //                 tpl_name = 'lucky_tpl';
    //             }else if(page_type == 'cz'){
    //                 url = '/api/v1.0/user_cz?uid=' + get_uid() + '&page=' + page;
    //                 target = $('.cz-body');
    //                 tpl_name = 'charge_tpl';
    //             }else if(page_type == 'show'){
    //                 url = '/api/v1.0/user_show?uid=' + get_uid() + '&page=' + page;
    //                 // target = $('.cz-body');
    //                 tpl_name = 'show_tpl';
    //                 return;
    //             }else{
    //                 return;
    //             }
    //             if(url && target && tpl_name){
    //                 load_list(url,target,tpl_name);
    //             }
    //         }
    //     };
    //     // $window.bind('scroll',onScroll);
    // })();
   
    //时间对象的格式化; 
    Date.prototype.format = function(format) {  
        /* 
         * eg:format="yyyy-MM-dd hh:mm:ss"; 
         */  
        var o = {  
            "M+" : this.getMonth() + 1, // month  
            "d+" : this.getDate(), // day  
            "h+" : this.getHours(), // hour  
            "m+" : this.getMinutes(), // minute  
            "s+" : this.getSeconds(), // second  
            "q+" : Math.floor((this.getMonth() + 3) / 3), // quarter  
            "S" : this.getMilliseconds()  
            // millisecond  
        }  
        if (/(y+)/.test(format)) {  
            format = format.replace(RegExp.$1, (this.getFullYear() + "").substr(4  
                            - RegExp.$1.length));  
        } 
        for (var k in o) {  
            if (new RegExp("(" + k + ")").test(format)) {  
                format = format.replace(RegExp.$1, RegExp.$1.length == 1  
                                ? o[k]  
                                : ("00" + o[k]).substr(("" + o[k]).length));  
            }  
        }  
        return format;  
    }
   
    // var require_min_count = 1,
    //     require_max_count = 5,
    //     cur_url_path = location.pathname,
    //     pic_list = [],
    //     max_file_size = '1MB',
    //     img_domain = 'http://img.aixunbang.com/',
    //     get_token_url = '/get/qiniu/uptoken';

    // var uploader = Qiniu.uploader({
    //     runtimes: 'html5,flash,html4',      // 上传模式,依次退化
    //     browse_button: 'edit-avatar',         // 上传选择的点选按钮，**必需**
    //     uptoken_url: get_token_url,
    //     get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的 uptoken
    //     // unique_names: true,
    //     multi_selection: false,              //是否开启多选文件
    //     domain: img_domain,
    //     //container: 'container',             // 上传区域 DOM ID，默认是 browser_button 的父元素，
    //     //flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入 flash,相对路径
    //     max_retries: 1,                     // 上传失败最大重试次数
    //     dragdrop: false,                     // 开启可拖曳上传
    //     drop_element: 'imgbox',          // 拖曳上传区域元素的 ID，拖曳文件或文件夹后可触发上传
    //     chunk_size: '4mb',                  // 分块上传时，每块的体积
    //     auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传,
    //     filters: {
    //         mime_types: [
    //             {title : "Image files", extensions : "jpg,jpeg,png"}
    //         ],
    //         max_file_size: max_file_size            // 最大文件体积限制
    //     },
    //     init: {
    //         'QueueChanged': function(up){
    //             //更新当前要上传的文件数量
    //         },
    //         'FileUploaded': function(up, file, info) {
    //             console.log(info);
    //             var res = $.parseJSON(info);
    //             console.log(res.key);
    //             var source_link = img_domain + res.key;  //获取上传成功后的文件的Url
    //             update_avatar_src(source_link);
    //             request_update_avatar(source_link)
    //         },
    //         'Error': function(up, err, errTip) {
    //             if(err && err.code == plupload.FILE_SIZE_ERROR){
    //                 alert('图片大小超过' + max_file_size + '了');
    //             }
    //             else if(err && err.code == plupload.FILE_EXTENSION_ERROR){
    //                 alert('当前选择的文件不符合要求,请检查要上传的文件是否为jpg/png/jpeg');
    //             }
    //                //上传出错时,处理相关的事情
    //         },
    //         'UploadComplete': function() {
    //                //队列文件处理完毕后,处理相关的事情
    //         },
    //         'Key': function(up, file) {
    //             // console.log(file,up);
    //             var date = new Date().format('yyyy-MM-dd')
    //             var milliscond = Date.now().toString();
    //             var file_sufix = '.' + file.name. split('.')[1]
    //             var key = 'avatar/' + date + '/' + milliscond + file_sufix
    //             return key;
    //             // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
    //             // 该配置必须要在 unique_names: false , save_key: false 时才生效
    //         }
    //     }
    // }); 
    // function update_avatar_src(url){
    //     $('#edit-avatar').prev('img').attr('src',url);
    // }

    // function request_update_avatar(url){
    //     $.ajax({
    //         url: '/update/avatar/' + get_uid(),
    //         type: 'PUT',
    //         data: {avatar: url},
    //         success: function(res,status){
    //             console.log(res);
    //         }
    //     })
    // }
    function load_eth_price(){
        $.get("https://api.coinmarketcap.com/v2/ticker/1027/",function(res,status){
            console.log(status, res);
            if(status == 'success' && typeof(res) == 'object'){
                usd_price = res.data.quotes.USD.price;
                console.log(usd_price);
            }
        });
    }
    load_eth_price()
    // dom 事件
    $(function() {
        $('.distribute-option').on("click", function(evt){
            $('#option-modal').modal();
            // var visibleWindow = $(window).height(),
            //     $modal =  $('#option-modal');
            //     setTimeout(function(){
            //         var dialogHeight = $modal.find('.modal-dialog').height();
            //         var offset = (visibleWindow - dialogHeight) / 2;
            //         console.log(visibleWindow, dialogHeight, offset);
            //         $modal.find('.modal-dialog').css('margin-top' ,offset);
            //     },0)
            $tr = $(evt.target).closest('.item');
            var assetType = $($tr.find('.data')[0]).text().trim(),
                assetAvailable = $($tr.find('.data')[2]).text().trim(),
                assetID =  $($tr.find('.data')[4]).text().trim(),
                coinID =  $($tr.find('.data')[5]).text().trim(),
                pageNum =  $($tr.find('.data')[6]).text().trim();
            $('.modal-body .asset-type').text(assetType);
            $('.modal-body .asset-no').text(assetID);
            $('.modal-body .available-count').val(assetAvailable);
            $('.modal-body .coin-no').text(coinID);

            if(assetType.toLowerCase().indexOf("wba") != -1) {
                $('.modal-body .available-count').attr("readonly", true);
            }else {
                $('.modal-body .available-count').attr("readonly", false);
            }
            $('.modal-body .asset-id').val(assetID);
            $('.modal-body .asset-name').val(assetType);
            $('.modal-body .coin-id').val(coinID);
            $('.modal-body .page').val(pageNum);
        });
        $('.recharge-option .recharge').on("click", function(evt){
            $target = $(evt.target);
            $assetType = $('#recharge-asset-type');
            $amount = $("#recharge-amount");
            $('#recharge-option-modal').modal();
            // var visibleWindow = $(window).height(),
            //     $modal =  $('#recharge-option-modal'),
            //     $select = $modal.find("select");
            //     dialogHeight = $modal.find('.modal-dialog').height();
            // var offset = (visibleWindow - dialogHeight) / 2;
            // console.log(visibleWindow, dialogHeight, offset);
            // $modal.find('.modal-dialog').css('margin-top' ,offset);
            $amount.focus();
            if ($select.val().toLowerCase().indexOf("wba") != -1) {
                $amount.val(1);
                $amount.attr("readonly", true);
            }else {
                $amount.attr("readonly", false);
            }
        });

        $('#recharge-option-modal select').on("change", function(evt){
            var selValue = $(evt.target).val();
            if (selValue.toLowerCase().indexOf("wba") != -1){
                $("#recharge-amount").val(1);
                $("#recharge-amount").attr("readonly", true);
            } else {
                $("#recharge-num").attr("hidden", true);
            }
        });
        // 兑换资产
        var exchange_ratio = 0;
        $('.recharge-option .exchange').on("click", function(evt){
            $("#exchange-option-modal").modal();
            if (usd_price) {
                exchange_ratio = 0.1/usd_price;
            }
            $("#exchange-price").val("E" + exchange_ratio.toFixed(8));

        });
        // $("#exchange-quantity").on("input",function(){
        //     var num = $("#exchange-quantity").val();
        //     if(0 > num){
        //         num = 0;
        //         $("#exchange-quantity").val(0)
        //     }
        //     $("#exchange-amount").val(num * usd_price);
        // })
        var $exchange_amount = $("#exchange-amount");
            $exchange_quantity = $("#exchange-quantity"),
            $exchange_price = $("#exchange-price"),
            $exchange_type = $("#exchange-type"),
            $exchange_pair = $("#exchange-pair"),
            $select_type = $("#exchange-type-select"),
            $select_pair = $("#exchange-pair-select");
        $exchange_pair.val($select_pair.val());
        $exchange_type.val($select_type.val());
        
        $("#exchange-quantity").on("input", function(evt) {
            var num = $("#exchange-quantity").val();
            if(0 > num){
                num = 0;
                $("#exchange-quantity").val(0)
            }
            var price = parseFloat($exchange_price.val().replace("E", "")),
                total = parseFloat($(this).val()) * price;
            if (total.toString() == "NaN") {
                total = 0;
            }
            $exchange_amount.val("E" + total.toFixed(8));
        });
        $select_type.on("change", function() {
            $exchange_type.val($(this).val());
        });
        $select_pair.on("change", function() {
            $exchange_pair.val($(this).val());
        });

        // 提币操作的模态框script函数
        $('.distribute-option-1').on("click", function(evt){
            $('#option-modal-1').modal();
            // var visibleWindow = $(window).height(),
            //     $modal =  $('#option-modal-1'),
            //     dialogHeight = $modal.find('.modal-dialog').height();
            // var offset = (visibleWindow - dialogHeight) / 3;
            // console.log(visibleWindow, dialogHeight, offset);
            // $modal.find('.modal-dialog').css('margin-top' ,offset);
            $tr = $(evt.target).closest('.item');
            var assetType = $($tr.find('.data')[0]).text().trim() || 'WBA',
                assetAvailable = $($tr.find('.data')[2]).text().trim(),
                assetID =  $($tr.find('.data')[4]).text().trim(),
                coinID = $($tr.find('.data')[5]).text().trim();
                pageNum = $($tr.find('.data')[6]).text();
            // console.log(assetType.length, assetType);
            if (assetType.length > 10){
                assetType = 'WBA';
            }
            $('.modal-body .asset-type').text(assetType);
            $('.modal-body .asset-no').text(assetID);
            $('.modal-body .available-count').val(assetAvailable);
            $('.modal-body .coin-type').val(assetType);
            $('.modal-body .coin-id').val(coinID);
            $('.modal-body .asset-no').val(assetID);
            $('.modal-body .page-num').attr('value',pageNum);
            if(assetType.toLowerCase().indexOf("wba") != -1) {
                $('.modal-body .available-count').attr("readonly", true);
            }else {
                $('.modal-body .available-count').attr("readonly", false);
            }
        });
        // 挂售操作的模态框script函数
        $('.distribute-option-2').on("click", function(evt){
            $('#option-modal-2').modal();
            // var visibleWindow = $(window).height(),
            //     $modal = $('#option-modal-2'),
            //     dialogHeight = $modal.find('.modal-dialog').height();
            // var offset = (visibleWindow - dialogHeight) / 2;
            // console.log(visibleWindow, dialogHeight, offset);
            // $modal.find('.modal-dialog').css('margin-top', offset);
            $tr = $(evt.target).closest('.item');
            var assetType = $($tr.find('.data')[0]).text(),
                assetAvailable = $($tr.find('.data')[2]).text(),
                assetID = $($tr.find('.data')[4]).text(),
                coinID = $($tr.find('.data')[5]).text(),
                pageNum = $($tr.find('.data')[6]).text();
            $('.modal-body .asset-type').text(assetType);
            $('.modal-body .asset-no').text(assetID);
            $('.modal-body .available-count').val(assetAvailable);
            $('.modal-body .asset-no').val(assetID);
            $('.modal-body .coin-id').val(coinID);
            $('.modal-body .available-count').attr("readonly", true);
            $('.modal-body .coin-name').attr('value',assetType);
            $('.modal-body .page-num').attr('value',pageNum);
        });
        // 停止挂售操作的模态框script函数
        $('.distribute-option-3').on("click", function(evt){
            $('#option-modal-3').modal();
            // var visibleWindow = $(window).height(),
            //     $modal = $('#option-modal-3'),
            //     dialogHeight = $modal.find('.modal-dialog').height();
            // var offset = (visibleWindow - dialogHeight) / 2;
            // console.log(visibleWindow, dialogHeight, offset);
            // $modal.find('.modal-dialog').css('margin-top', offset);
            $tr = $(evt.target).closest('.item');
            var assteID = $($tr.find('.data')[0]).text(),
                assteTime = $($tr.find('.data')[1]).text(),
                assteType = $($tr.find('.data')[2]).text(),
                asstePrice = $($tr.find('.data')[3]).text(),
                pageNum = $($tr.find('.data')[6]).text();
            $('.modal-body .asste-id').attr('value',assteID);
            $('.modal-body .asste-time').attr('value',assteTime);
            $('.modal-body .asste-type').attr('value',assteType);
            $('.modal-body .asste-price').attr('value',asstePrice);
            $('.modal-body .asste-time').text(assteTime);
            $('.modal-body .asset-type').text(assteType);
            $('.modal-body .asste-price').text(asstePrice);
            $('.modal-body .page-num').attr('value',pageNum);
        });
        // 订单详情的模态框script函数
        $('.modalBox').on("click", function(evt){
            $('#orderinfos-modal').modal();
            // var visibleWindow = $(window).height(),
            //     $modal = $('#orderinfos-modal'),e
            //     dialogHeight = $modal.find('.modal-dialog').height();
            // var offset = (visibleWindow - dialogHeight) / 3;
            // console.log(visibleWindow, dialogHeight, offset);
            // $modal.find('.modal-dialog').css('margin-top', offset);
            $div = $(evt.target).closest('.modalBox');
            var create_time = $($div.find('.data')[0]).text(),
                order_id = $($div.find('.data')[1]).text(),
                sell = $($div.find('.data')[2]).text(),
                t_price = $($div.find('.data')[3]).text(),
                price = $($div.find('.data')[4]).text(),
                quantity = $($div.find('.data')[5]).text(),
                com_name = $($div.find('.data')[6]).text(),
                com_type = $($div.find('.data')[7]).text();

            $('.modal-body .order_id').text(order_id);
            $('.modal-body .com_name').text(com_name);
            $('.modal-body .price').text(price);
            $('.modal-body .quantity').text(quantity);
            $('.modal-body .com_type').text(com_type);
            $('.modal-body .t_price').text(t_price);
            $('.modal-body .sell').text(sell);
            $('.modal-body .create_time').text(create_time);
        });
    });


});
