require(['jquery','jquery-downcount'], function ($) {

    var $count_doms = $('.count-down').find('.count-num');
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
});
