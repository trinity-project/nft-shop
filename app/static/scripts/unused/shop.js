require(['jquery','jquery-downcount','modal-box'], function ($) {
	var $count_dom = $('.down-count');
	var $diff_now = $('.diff-now');
    if( $count_dom.length > 0){
    	$count_dom.downCount({
    		finish: new Date($diff_now.data('finish')).getTime(),
    		now: parseFloat($diff_now.data('now'))*1000
    	},function(){
    		$count_dom.find('span').text('0');
            timer_id = setTimeout(reflush,4000);
            function reflush(){
                location.reload();
                clearTimeout(timer_id);
            }
    		
    	})
    }

     //自定义handlebars help
    Handlebars.registerHelper("compare",function(v1,v2,options){
        if(v1 > v2){return options.fn(this);}
        else{return options.inverse(this);}
    });

    function get_pid(){
        return $('.product-content').data("pid");
    }

    function get_proid(){
        return $('.product-content').data("proid");
    }

    function checkr_scroll_or_load(target,page){
        if(target.children().length == 0 && page == 1){
            return 'load';
        }
        else if((target.children().length >= list_per_page) && (target.children().length%list_per_page == 0)){
            return 'scroll';
        }
    }

    var join_page = 1,
        show_page = 1,
        proid = get_proid(),
        pid = get_pid(),
        join_api = '/api/v1.0/period_join_record?pid=' + pid,
        show_api = '/api/v1.0/product_show?proid=' + proid,
        list_per_page = 20,
        scroll_handle;

    //tab 切换
    $('.tabs li').on('click',function(){
        var that = $(this);
        var $tabs = that.closest('.tabs');
        var $cur_tab = $tabs.find('.current');
        function switch_tab(class_name){
            $tabs.find('li').removeClass('current');
            that.addClass('current');
            var $target_container = $('.product-content');
            $target_container.children().hide();
            $target_container.find(class_name).show();
            // console.log(class_name);
            if(scroll_handle){
                $(window).unbind('scroll',scroll_handle);
            }
        }
        if(that.attr('class') == $cur_tab.attr('class')){
            //click 当前的tab do nothing
            return;
        }
        else if(that.attr('class') == 'tab-detail'){
            //详情tab
            switch_tab('.product-detail');
        }
        else if(that.attr('class') == 'tab-join'){
            //参与tab
            switch_tab('.join-record');
            var tpl_nmae = 'join_tpl',
                target = $('.join-record'),
                check_scroll_load = checkr_scroll_or_load(target,join_page);
            if(check_scroll_load == 'load'){
                load_list(join_api,target,tpl_nmae);
            }else if(check_scroll_load == 'scroll'){
                scroll_load(join_api,target,tpl_nmae);
            }
        }
        else if(that.attr('class') == 'tab-show'){
            //晒单tab
            switch_tab('.product-show');
            var tpl_nmae = 'show_tpl',
                target = $('.product-show'),
                check_scroll_load = checkr_scroll_or_load(target,show_page);
            if(check_scroll_load == 'load'){
                load_list(show_api,target,tpl_nmae);
            }else if(check_scroll_load == 'scroll'){
                scroll_load(show_api,target,tpl_nmae);
            }
        }else{
            //计算结果tab
            switch_tab('.count-result');
        }
      
    })

    function load_list(url,target_container,tpl_name){
        $.get(url,function(res,status){
            if(status == 'success' && res.message == 'ok'){
                if(res.data && res.data.length > 0){
                    var html = Handlebars.templates[tpl_name](res);
                    target_container.append(html);
                    //可能还有下一页
                    if(res.data.length == list_per_page){
                        var api;
                        if (tpl_name == 'join_tpl'){
                            join_page+=1;
                            api = join_api;
                        }else if(tpl_name == 'show_tpl'){
                            api = show_api;
                            show_page+=1;
                        }
                        scroll_load(api,target_container,tpl_name);
                    }else{
                        $('.load-tips').fadeIn();
                    }
                }else{
                    $('.load-tips').fadeIn();
                }
            }
        })
    };
    //滚动加载数据
    function scroll_load(api,target,tp_name){
        var $window = $(window),
            $document = $(document),
            init_top = 0;
            // page_type = get_type();
        scroll_handle = function(){
            console.log(tp_name);
            var win_height = window.innerHeight ? window.innerHeight : $window.height(); // iphone fix
            var close_to_bottome = ($window.scrollTop() + win_height > $document.height() - 100);
            var scroll_direction = $window.scrollTop() > init_top;
            if(close_to_bottome && scroll_direction){
                //进入事件处理后解绑事件
                $window.unbind('scroll', scroll_handle);
                //更新init_top
                init_top = $window.scrollTop();
                if(api && target && tp_name){
                    var url;
                    if (tp_name == 'join_tpl'){
                        url = api + '&page=' + join_page;
                    }else if(tp_name == 'show_tpl'){
                        url = api + '&page=' + show_page;
                    }
                    load_list(url,target,tp_name);
                }
            }
        };
        $window.bind('scroll', scroll_handle);
    }

    //获取历史开奖数据
    $(document).ready(function(){
        var $period_nh = $('.history-container'),
            closest_no = Number($period_nh.attr("no")),
            current_no = closest_no,
            status = Number($period_nh.data("status")),
            min_no = Number($period_nh.attr("minno"));

        if(!status){
            if(closest_no){
                get_history_data(proid,closest_no,$period_nh);
            }else{
                $period_nh.html('<h3>开奖信息</h3><div>该商品暂无开奖信息</div>');
            }
        }
        $('.period-nh').delegate('.history-period .left','click',function(){
            var that = $(this);
            if(that.hasClass('disabled') || current_no==closest_no){
                return;
            }else{
                get_history_data(proid,current_no+1,$period_nh);
            }
        })
        $('.period-nh').delegate('.history-period .right','click',function(){
            var that = $(this);
            if(that.hasClass('disabled') || current_no==min_no){
                return;
            }else{
                // console.log(current_no,closest_no);
                get_history_data(proid,current_no-1,$period_nh);
            }
        })

        function get_history_data(proid,number,target){
            var url = '/api/v1.0/period_history?proid=' + proid + '&number=' + number;
            target.prev('.loading-tips').show();
            $.get(url,function(res,status){
                var html = Handlebars.templates['history_tpl'](res);
                target.html(html);
                current_no = res.data.number;
                update_select_status(res.data.number);
                target.prev('.loading-tips').hide();
            })
        };
        function update_select_status(number){
            console.log(number,min_no);
            var $left_sel = $('.numbers-select').find('.left'),
                $right_sel = $('.numbers-select').find('.right');
            if(number==closest_no){
                $left_sel.addClass('disabled');
            }else{
                $left_sel.removeClass('disabled');
            }
            if(number==min_no){
                $right_sel.addClass('disabled');
            }else{
                $right_sel.removeClass('disabled');
            }
        };
    })

    //查看参与号码
    $('body').delegate('.view-num','click',function(){
        var target = $('#num-modal'),that = $(this) ,num_text = that.data('num').toString();
        // console.log(num_text);
        if(that.data('zj')){
            // console.log('zjl');
            // console.log(typeof(num_text));
            var flag_num = '<strong>' + that.data('zj') + '</strong>';
            num_text = num_text.replace(that.data('zj'),flag_num);
        }
        target.find('.num-content').html(num_text);
        target.modal('show');
    })

    //判断用户登陆
    function check_login(){
        if($('body').hasClass('login')){
            return true;
        }else{
            return false;
        }
    }
    $('form').find('button').on('click',function(){
        if(!check_login()){
            location.href = '/login?next=' + location.href;
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
            if(cur_amount.toString() != 'NaN' && cur_amount >1 ){
                that.next('input[name="amount"]').val(cur_amount-1);
            }
        }else{
            cur_amount =  Number(that.prev('input[name="amount"]').val());
            var max = Number(that.data("max"));
            if(cur_amount.toString() != 'NaN' && (cur_amount < max)){
                that.prev('input[name="amount"]').val(cur_amount + 1);
            }
        }
    })

    function check_before_submit(){
        var amount = Number($('input[name="amount"]').val()), 
            pid = Number($('input[name="pid"]').val()),
            max = Number($('.join-select').find('.plus').data('max'));
        if(amount.toString() != 'NaN' && pid.toString() != 'NaN' && pid != 0 && max.toString()!= 'NaN'){
            if(amount >= 1 && amount <= max){
                return true
            }else{
                $('input[name="amount"]').focus();
            }
        }
    }
    //submit 
    $('button[type=submit]').on('click',function(){
        if(!check_before_submit()){
            return false;
        }
    })

    var SimpleShare = function (options) {
        // get share content
        options = options || {};
        var url = options.url || window.location.href;
        var title = options.title || document.title;
        var content = options.content || '';
        var pic = options.pic || '';

        // fix content format
        url = encodeURIComponent(url);
        title = encodeURIComponent(title);
        content = encodeURIComponent(content);
        pic = encodeURIComponent(pic);

        // share target url
        var qzone = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url={url}&title={title}&pics={pic}&summary={content}';
        var weibo = 'http://service.weibo.com/share/share.php?url={url}&title={title}&pic={pic}&searchPic=false';
        var tqq = 'http://share.v.t.qq.com/index.php?c=share&a=index&url={url}&title={title}&appkey=801cf76d3cfc44ada52ec13114e84a96';
        var renren = 'http://widget.renren.com/dialog/share?resourceUrl={url}&srcUrl={url}&title={title}&description={content}';
        var douban = 'http://www.douban.com/share/service?href={url}&name={title}&text={content}&image={pic}';
        var facebook = 'https://www.facebook.com/sharer/sharer.php?u={url}&t={title}&pic={pic}';
        var twitter = 'https://twitter.com/intent/tweet?text={title}&url={url}';
        var linkedin = 'https://www.linkedin.com/shareArticle?title={title}&summary={content}&mini=true&url={url}&ro=true';
        var weixin = 'http://qr.liantu.com/api.php?text={url}';
        var qq = 'http://connect.qq.com/widget/shareqq/index.html?url={url}&desc={title}&pics={pic}';

        // replace content functions
        function replaceAPI (api) {
            api = api.replace('{url}', url);
            api = api.replace('{title}', title);
            api = api.replace('{content}', content);
            api = api.replace('{pic}', pic);

            return api;
        }

        // share target
        this.qzone = function() {
            window.open(replaceAPI(qzone));
        };
        this.weibo = function() {
            window.open(replaceAPI(weibo));
        };
        this.tqq = function() {
            window.open(replaceAPI(tqq));
        };
        this.renren = function() {
            window.open(replaceAPI(renren));
        };
        this.douban = function() {
            window.open(replaceAPI(douban));
        };
        this.facebook = function() {
            window.open(replaceAPI(facebook));
        };
        this.twitter = function() {
            window.open(replaceAPI(twitter));
        };
        this.linkedin = function() {
            window.open(replaceAPI(linkedin));
        };
        this.qq = function() {
            window.open(replaceAPI(qq));
        };
        this.weixin = function(callback) {
            if (!callback) {
                window.open(replaceAPI(weixin));
            }else{
                callback(replaceAPI(weixin));
            }
        };
    };

    $('.shareto').find('a').on('click',function(){
        var that = $(this),
            options = {
                title: $('title').text(),
                content: '1元就有机会购得'  + $('.title').text(),
                pic: $('.product-img').find('img').attr('src')
            },
            share_instance = new SimpleShare(options);
             // console.log(options);
        if (that.hasClass('share-to-weibo')){
            //分享到微博
            share_instance.weibo();
        }else if(that.hasClass('share-to-qq')){
            share_instance.qzone();
        }
    })
});
