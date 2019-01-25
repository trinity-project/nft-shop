define(['jquery'],function($){
	var scroll_page = 2,
        load_page = 1,
        scroll_fun,
        list_per_page = 20;
	 //自定义handlebars help
	Handlebars.registerHelper("compare",function(v1,v2,options){
	    if(v1 > v2){return options.fn(this);}
	    else{return options.inverse(this);}
	});

	var load_list = function (url,target_container,tpl_name){
		$('.loading-tips').show();
	    $.get(url,function(res,status){
	        if(status == 'success' && res.message == 'ok'){
	        	$('.loading-tips').hide();
	            if(res.data && res.data.length > 0){
	                var html = Handlebars.templates[tpl_name](res);
	                target_container.append(html);
	                //可能还有下一页
	                if(res.data.length == list_per_page){
	                	//直接滚动加载
	                	if(url.indexOf('page=') >= 0 ){
	                		scroll_page += 1;
                            //绑定事件
                            $(window).bind('scroll',scroll_fun);
	                	}
                		//首次通过ajax加载第一页后滚动加载
                        else{
                            $(window).unbind('scroll');
                            scroll_load(url,target_container,tpl_name);
                        }
	                }else{
	                    $('.load-tips').fadeIn();
	                }
	            }else{
	                $('.load-tips').fadeIn();
	            }
	        }
	    })
	};

	var scroll_load = function (api,target_container,tpl_name){
        var $window = $(window),
            $document = $(document),
            init_top = 0;
        scroll_fun =  function(e){
            var win_height = window.innerHeight ? window.innerHeight : $window.height(); // iphone fix
            var close_to_bottome = ($window.scrollTop() + win_height > $document.height() - 100);
            var scroll_direction = $window.scrollTop() > init_top;
            if(close_to_bottome && scroll_direction){
                //进入事件处理后解绑事件
                $window.unbind('scroll', scroll_fun);
                //更新init_top
                init_top = $window.scrollTop();
                if(api && target_container && tpl_name){
                	var url;
                	if (api.indexOf('?') >= 0){
                		url =  api + '&page=' + scroll_page; 
                	}else{
                		url =  api + '?page=' + scroll_page; 
                	}
					
                    load_list(url,target_container,tpl_name);
                }
            }
        };
        $window.bind('scroll', scroll_fun);
    };

    return {
    	scroll_load: scroll_load,
    	load_list: load_list
    }
})