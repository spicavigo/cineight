function init_textarea(ele){
        if(ele == undefined) {ele=$('body'); } else {ele = $(ele);}
        ele.find('.comment_area').each(function(){
            $(this).css('width','352px');
            if ($(this)[0].value == ''){
                $(this)[0].value = 'Write a Comment ...';
                $(this).css('color', '#a7a7a8');
            }
        });
        ele.find('.reco_element .comment_area').each(function(){
            $(this).css('width','302px');
        });
        ele.find('.reco_element .comment_submit').each(function(){
                $(this).css('margin-left','254px');
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
            if (html.success){
                var a = '<div class="comment"><div class="large"><a href="/user/' + USER + '">' + NAME + '</a> says:</div><div style="padding-left: 10px">' + msg + '</div></div>';
                $(that).parents('.comments').prepend(a);
            }
        }); 
    });
    $('.action_comment>span').live('click', function(){
        var data = $(this).parent('.action_comment').siblings('.comments');
        if ($(data).is(':hidden')){
            $(data).fadeIn('slow');
        } else {
            $(data).fadeOut('slow');
        }
    });
});