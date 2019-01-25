require(['jquery','affix','bootstrap'],function(){
	// $('.scroll-top').on('click',function(){
	// 	var scrollTop = $(window).scrollTop();
	// 	if (scrollTop >= 150){
	// 		$('html,body').animate({scrollTop:0},'slow');
	// 	}
	// })
	$("#closeHint").on("click",function(){
		$("#hint").hide();
	})
})