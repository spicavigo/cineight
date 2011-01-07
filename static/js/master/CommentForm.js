function init_textarea(){
        $('.comment_area').each(function(){
            $(this).css('width','352px');
            if ($(this)[0].value == ''){
                $(this)[0].value = 'Write a Comment ...';
                $(this).css('color', '#a7a7a8');
            }
        });
        $('.reco_element .comment_area').each(function(){
            $(this).css('width','302px');
        });
        $('.reco_element .comment_submit').each(function(){
                $(this).css('margin-left','254px');
        });
        $('.comment_area').focus(function(){
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
        $.get(AJAX_URL, data, function(html){
            if (html == 'ok'){
                var a = '<div class="comment"><div class="large"><a href="/user/' + USER + '">' + NAME + '</a> says:</div><div style="padding-left: 10px">' + msg + '</div></div>';
                $(that).parents('.comments').prepend(a);
            }
        }); 
    });
});