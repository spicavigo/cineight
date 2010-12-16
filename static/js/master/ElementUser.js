$(function() {
    $('.user_action span').live('click', function(){
        var that = this;
        $.get(AJAX_URL, {'data_id': $(this).attr('data-id')}, function(html){
            $(that).html(html);
        });
    })
        
     $('#follower_detail').fancybox({
        width:150,
        height:100,
        autoDimensions: false,
        titleShow: false
    });
    $('#following_detail').fancybox({
        width:150,
        height:100,
        autoDimensions: true,
        titleShow: false
    });      
    $('#edit_user_profile').fancybox({
        titleShow: false
    });
    $('#user_info').live('submit', function(e){
       e.preventDefault();
       var data = $(this).serialize();
       $.get(AJAX_URL, data, function(response){
            $.fancybox.close();
       });
       
    });
});
