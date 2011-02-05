function init_textarea(ele){
        if(ele == undefined) {ele=$('body'); } else {ele = $(ele);}
        ele.find('.comment_area').each(function(){
            //$(this).css('width','100%');
            if ($(this)[0].value == ''){
                $(this)[0].value = 'Write a Comment ...';
                $(this).css('color', '#a7a7a8');
            }
        });
        ele.find('.reco_element .comment_area').each(function(){
            //$(this).css('width','100%');
        });
        ele.find('.reco_element .comment_submit').each(function(){
                $(this).css('margin-left','50%');
        });
        ele.find('.comment_area').focus(function(){
                                if ($(this)[0].value == 'Write a Comment ...'){
                                    $(this)[0].value = '';
                                    $(this).css('color', '#363637');
                                    $(this).css('height','24px');
                                }
                            }).blur(function(){
                                if ($(this)[0].value == ''){
                                    $(this)[0].value = 'Write a Comment ...';
                                    $(this).css('color', '#a7a7a8');
                                    $(this).css('height','12px');
                                }
                            });
    }
$(function(){
    
    init_textarea();
    $('.comment_form').live('submit', function(e){
        e.preventDefault();
        var msg = $(this).find('.comment_area').val();
        var data = $(this).serialize();
        var that = this;
        $(that).find('textarea').val('');
        $.get(AJAX_URL, data, function(html){
                var a = '<div class="comment"><div class="large"><a href="/user/' + USER_ID + '">' + USER_NAME + '</a> says:</div><div style="padding-left: 10px">' + msg + '</div></div>';
                //$(that).parents('.comment').prepend(a);
                $(a).insertBefore($(that).parents('.comment'));
        }); 
    });
    $('.action_comment>span').live('click', function(){
        var data = $(this).parent('.action_comment').siblings('.comments');
        if ($(data).is(':hidden')){
            $(data).fadeIn('slow');
            $(this).html('Hide');
        } else {
            $(data).fadeOut('slow');
            $(this).html('Show');
        }
    });
    $('.comments').each(function(){
        var comments = $(this).children('.comment');
        if (comments.length > 3){
            $(this).prepend('<div class="show_all link">Show All</div>');
            for(var i=comments.length-3; i<comments.length; i++){
                comments.eq(i).show();
            }            
        } else {
            comments.show();
        }
    });
    $('.show_all').live('click', function(){
        $(this).siblings().show();
        $(this).remove();
    })
});