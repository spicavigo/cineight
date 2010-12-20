$(function() {
    $('.user_action span').live('click', function(){
        var that = this;
        $.get(AJAX_URL, {'data_id': $(this).attr('data-id')}, function(html){
            $(that).html(html);
        });
    })
        
    $('#follower_detail').live('click', function(){
        $.fancybox({
            width:150,
            height:100,
            autoDimensions: true,
            titleShow: false,
            href: $(this).attr('href')
        });
        return false;
    });
    
    $('#following_detail').live('click', function(){
        $.fancybox({
            width:150,
            height:100,
            autoDimensions: true,
            titleShow: false,
            href: $(this).attr('href')
        });
        return false;
    });
    
    $('#edit_user_profile').live('click', function(){
        $.fancybox({
            titleShow: false,
            href: $(this).attr('href')
        });
        return false;
    });

    $('#user_info').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(response){
            $.fancybox.close();
       });
       
    });
});
