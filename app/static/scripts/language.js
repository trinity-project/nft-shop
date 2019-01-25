
require(['jquery','language-text','bootstrap'], function ($, getLanguageText) {
    
    function sleep(begin, n){
        console.log(begin, n);
        while(Date.now() < begin + n){}
    }
    function hideDomText() {
        var $textTags = $("[data-language]");
        $textTags.each(function(index, element) {
            $(this).css("display","none");
        });
    }
    // hideDomText();
    function changeDomText(name, language) {
        var $textTags = $("[data-language]"),
            lgText = getLanguageText(name, language);
        console.log(name, language, lgText);
        $textTags.each(function(index, element) {
            var $el = $(this),
                textKey = $el.data().language;
            // $el.text($.i18n.prop(textKey));
            $el.text(lgText[textKey]);
            // $el.text(lgText[textKey]).fadeIn(100 + 100*(index+1));
        });
        // sleep(Date.now(), 100);
        console.log(Date.now());
    }
    function loadProperties(language) {
        var pathname = window.location.pathname;
        changeDomText(pathname, language);
        // $.i18n.properties({
        //     // name: ['strings_en_US','strings_zh_CN'], // 资源文件名称
        //     name: 'strings', // 资源文件名称
        //     path: '/static/language/', // 资源文件所在目录路径
        //     mode: 'map', // 模式：变量或 Map 
        //     language: type, // 对应的语言
        //     cache: true,
        //     async: true,
        //     encoding: 'UTF-8',
        //     callback: function () { // 回调方法
        //         var path = location.pathname;
        //         changeDomText();
        //     }
        // });
    }

    function switchLang() {
        var currentLanguage = window.localStorage.getItem("language") || "en";
            language = currentLanguage == "cn" ? "en" : "cn";
        window.localStorage.language = language;
        window.location.reload(true);
    }
    $(document).ready(function(){
        console.log(Date.now());
        $(".switch-lg-btn").on("click", switchLang);
        var language = window.localStorage.getItem("language") || "en";
        loadProperties(language);
    });
    // $('.scroll-top').on('click',function(){
	// 	var scrollTop = $(window).scrollTop();
	// 	if (scrollTop >= 150){
	// 		$('html,body').animate({scrollTop:0},'slow');
	// 	}
	// });
});