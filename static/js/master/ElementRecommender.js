$(function() {
    $('.uaction span').live('click', function(){
        var that = this;
        $.get(AJAX_URL, {'data_id': $(this).attr('data-id')}, function(html){
            $(that).html(html);
        });
    })
});
