    //function for the navigation button
$(function(){
    var clicked = false;
    $('.tabNav').live("click", function(e) {
        if (clicked) {
            return false;
        }
        clicked = true;
        var that = this;
        var data_id = $(this).attr("data-id");
        $(this).html("Loading...");
        $.get(AJAX_URL, {
            'data_id': data_id
        }, function(html) {
            $(html).find("span.spoiler").hide();
            $(that).parents('.lzTab').find('.elements').append($(html).find('.elements').html());
            $(that).parents('.lzTab').find('.tabBtns').replaceWith($(html).find('.tabBtns'));
            $('.rating:not("#ui-rating-null")').rating({'showCancel':false});
            $('textarea').autoResize();
            init_textarea();
            clicked = false;
        });
    });
});
