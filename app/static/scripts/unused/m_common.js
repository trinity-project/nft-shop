require(['jquery','vendor/scroll_load','jquery-downcount'],function($,Load){
	$('.toggle-cate').on('click',function(){
		var target = $('.cate-list'),that = $(this);
		if(target.css('display')=='none'){
			target.show();
		}else{
			target.hide();
		}
	})

	//到计时
	var $count_doms = $('.count-down');
    $.each($count_doms,function(index){
        var that = $(this);
        that.downCount({
            finish: new Date(that.data('finish')).getTime(),
            now: parseInt(that.data('now'))*1000
        },function(){
            that.find('span').text('0');
            location.reload();
        })
    })

	$('.go-back').on('click',function(){
		history.back();
		// history.go(-1); //后退+刷新 
	})
	$('.scroll-top').on('click',function(){
		var scrollTop = $(window).scrollTop();
		if (scrollTop >= 50){
			$('html,body').animate({scrollTop:0},'slow');
		}
	})

	var url_path_name = location.pathname,target,api,tpl_name;
	if (url_path_name == '/announced'){
		//揭晓页面
		target = $('.announced-body');
		tpl_name = 'announced_item_tpl';
		api = '/api/v1.0/announc_list';
		Load.scroll_load(api,target,tpl_name);
	}else if (url_path_name.indexOf('/product/history/') == 0){
		target = $('.history-body');
		tpl_name = 'history_item_tpl';
		api = '/api/v1.0/history_list';
		var proid = Number(url_path_name[url_path_name.length -1]);
		if (proid.toString() != 'NaN' && proid > 0){
			api = api + '?proid=' + proid;
			Load.scroll_load(api,target,tpl_name);
		}
		//历史开奖页面
	}else if(url_path_name.indexOf('/list') == 0){
		//m端首页
		target = $('.index-list');
		tpl_name = 'list_item_tpl';
		api = '/api/v1.0/index_list';
		var cid = Number(url_path_name[url_path_name.length -1]);
		if (cid.toString() == 'NaN'){
			if (location.search.length > 0){
				api += location.search;
			}
		}else{
			if (location.search.length > 0){
				api = api + location.search + '&cid=' + cid;
			}else{
				api = api + '?cid=' + cid;
			}
		}
		Load.scroll_load(api,target,tpl_name);
	}
	
})