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
        var len = $(that).parents('.lzTab').find('.elements > div').length - 1;
        $(this).html("Loading...");
        $.get(AJAX_URL, {
            'data_id': data_id
        }, function(html) {
            var parent = $(that).parents('.lzTab');
            //FB.XFBML.Host.parseDomElement(html);
            $(html).find("span.spoiler").hide();
            
            //$(html).find('textarea').autoResize();
            //init_textarea(html);
            parent.find('.elements').append($(html).find('.elements').html());
            parent.find('.tabBtns').replaceWith($(html).find('.tabBtns'));
            $('.rating:not("#ui-rating-null")').rating({'showCancel':false});            
            clicked = false;
            var new_parent = parent.find('.elements > div:gt(' + len + ')');
            init_textarea(new_parent);
            new_parent.find('textarea').autoResize(); 
            new_parent.find('.mimage').appear(function(){
                var that = $(this);
                $(this).attr('src', that.attr('data-src'));
              }, {
                one: true
            });
            FB.XFBML.parse();            
        });
    });
});
