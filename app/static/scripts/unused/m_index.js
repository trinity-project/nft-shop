require(['jquery'],function($){
	$('.toggle-cate').on('click',function(){
		var target = $('.cate-list'),that = $(this);
		if(target.css('display')=='none'){
			target.show();
		}else{
			target.hide();
		}
	})
	
})