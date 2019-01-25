require(['jquery','vendor/scroll_load'],function($,Load){
	var target = $('.list-container'),
		uid = target.data('uid'),
		api = '/api/v1.0/user_join',
		tpl_name;
	if(location.pathname.indexOf('join') > 0){
		api = '/api/v1.0/user_join';
		tpl_name = 'join_item_tpl';
	}else if(location.pathname.indexOf('cz') > 0){
		api = '/api/v1.0/user_cz';
		tpl_name = 'charge_item_tpl';
	}else if(location.pathname.indexOf('zj') > 0){
		api = '/api/v1.0/user_win';
		tpl_name = 'lucky_item_tpl';
	}else{
		api = '/api/v1.0/user_show';
		tpl_name = 'show_item_tpl';
	}
	api = api + '?uid=' + uid;
	if(target && uid && tpl_name){
		Load.scroll_load(api,target,tpl_name);
	}
	$('.go-back').on('click',function(){
		history.back();
		// history.go(-1); //后退+刷新 
	})
})